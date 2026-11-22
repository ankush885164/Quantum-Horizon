"""
Financial Market Intelligence — Market Data Extraction Engine
Author: Data Engineering Team
Description:
    Production-grade extraction script that pulls multi-year historical price data,
    corporate actions (splits/dividends), and company metadata for Indian equities
    listed on NSE/BSE using yfinance and REST APIs.
    
    Data is formatted and persisted into Databricks Unity Catalog Volumes
    (or local staged volume directory for development/testing).
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

import pandas as pd
import requests
import yfinance as yf
from tqdm import tqdm

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MarketDataExtractor")

# Default Indian Stock Universe (Top NSE Large-Cap Stocks across Diverse Sectors)
DEFAULT_SYMBOLS: List[str] = [
    "RELIANCE.NS",   # Energy / Conglomerate
    "TCS.NS",        # Information Technology
    "HDFCBANK.NS",   # Financial Services / Banking
    "INFY.NS",       # Information Technology
    "ICICIBANK.NS",  # Financial Services / Banking
    "NTPC.NS",       # Utilities / Power
    "SBIN.NS",       # Financial Services / Public Sector Banking
    "BHARTIARTL.NS", # Telecommunications
    "ITC.NS",        # FMCG / Consumer Goods
    "LT.NS"          # Construction & Engineering
]

# Sector Mapping Fallback dictionary in case ticker info is sparse
SECTOR_MAP: Dict[str, Dict[str, str]] = {
    "RELIANCE.NS": {"sector": "Energy", "industry": "Oil & Gas Refining & Marketing"},
    "TCS.NS": {"sector": "Information Technology", "industry": "IT Services & Consulting"},
    "HDFCBANK.NS": {"sector": "Financial Services", "industry": "Private Banks"},
    "INFY.NS": {"sector": "Information Technology", "industry": "IT Services & Consulting"},
    "ICICIBANK.NS": {"sector": "Financial Services", "industry": "Private Banks"},
    "NTPC.NS": {"sector": "Utilities", "industry": "Thermal Power Generation"},
    "SBIN.NS": {"sector": "Financial Services", "industry": "Public Sector Banks"},
    "BHARTIARTL.NS": {"sector": "Telecommunications", "industry": "Telecom Services"},
    "ITC.NS": {"sector": "Consumer Defensive", "industry": "Tobacco & FMCG"},
    "LT.NS": {"sector": "Industrials", "industry": "Engineering & Construction"}
}


def sanitize_filename(name: str) -> str:
    """Replaces filesystem-unfriendly characters in symbol strings."""
    return name.replace(".", "_").replace("^", "").strip()


def fetch_historical_prices(
    symbol: str,
    period: str = "5y",
    interval: str = "1d",
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Optional[pd.DataFrame]:
    """
    Fetches historical OHLCV data for a given ticker with automatic retries and exponential backoff.
    
    Args:
        symbol: Ticker symbol (e.g., 'RELIANCE.NS')
        period: Time window (e.g., '1y', '3y', '5y', 'max')
        interval: Data interval (e.g., '1d', '1wk')
        max_retries: Number of retry attempts on failure
        backoff_factor: Multiplier for exponential backoff delay
        
    Returns:
        Cleaned pandas DataFrame containing historical prices, or None on permanent failure.
    """
    logger.info(f"Initiating price download for {symbol} (period={period}, interval={interval})")
    
    for attempt in range(1, max_retries + 1):
        try:
            ticker = yf.Ticker(symbol)
            # Fetch full history including corporate actions
            df: pd.DataFrame = ticker.history(period=period, interval=interval, auto_adjust=False)
            
            if df.empty:
                logger.warning(f"No price data returned for {symbol} on attempt {attempt}")
                if attempt == max_retries:
                    return None
                time.sleep(backoff_factor ** attempt)
                continue
            
            # Reset index to convert DatetimeIndex into explicit column
            df = df.reset_index()
            
            # Standardize column names
            df.columns = [c.replace(" ", "_").lower() for c in df.columns]
            
            # Standardize date column
            if "date" in df.columns:
                df["trade_date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            elif "datetime" in df.columns:
                df["trade_date"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-%m-%d")
            else:
                df["trade_date"] = pd.to_datetime(df.iloc[:, 0]).dt.strftime("%Y-%m-%d")
            
            # Ensure symbol column exists
            df["symbol"] = symbol
            
            # Standardize expected columns
            expected_cols = [
                "symbol", "trade_date", "open", "high", "low", "close",
                "adj_close", "volume", "dividends", "stock_splits"
            ]
            for col in expected_cols:
                if col not in df.columns:
                    if col == "adj_close" and "close" in df.columns:
                        df["adj_close"] = df["close"]
                    elif col in ["dividends", "stock_splits"]:
                        df[col] = 0.0
                    else:
                        df[col] = None

            # Retain only recognized columns
            df = df[expected_cols]
            
            logger.info(f"Successfully extracted {len(df)} records for {symbol}")
            return df
            
        except Exception as exc:
            logger.error(f"Error fetching data for {symbol} (attempt {attempt}/{max_retries}): {exc}")
            if attempt < max_retries:
                sleep_secs = backoff_factor ** attempt
                logger.info(f"Retrying in {sleep_secs:.1f}s...")
                time.sleep(sleep_secs)
            else:
                logger.error(f"Max retries reached for {symbol}. Extraction aborted for this symbol.")
                return None
    return None


def fetch_company_metadata(symbol: str, max_retries: int = 2) -> Dict[str, Any]:
    """
    Extracts fundamental profile, sector classification, and financial metrics.
    
    Args:
        symbol: Ticker symbol (e.g., 'TCS.NS')
        max_retries: Number of retry attempts
        
    Returns:
        Dictionary containing standardized metadata attributes.
    """
    logger.info(f"Fetching company profile and fundamental metadata for {symbol}")
    default_meta = SECTOR_MAP.get(symbol, {"sector": "Unknown", "industry": "Unknown"})
    
    profile: Dict[str, Any] = {
        "symbol": symbol,
        "company_name": symbol.split(".")[0],
        "sector": default_meta.get("sector", "Unknown"),
        "industry": default_meta.get("industry", "Unknown"),
        "currency": "INR",
        "exchange": "NSE",
        "market_cap": None,
        "enterprise_value": None,
        "pe_ratio": None,
        "forward_pe": None,
        "peg_ratio": None,
        "dividend_yield": None,
        "beta": None,
        "fifty_two_week_high": None,
        "fifty_two_week_low": None,
        "extracted_at": datetime.now(timezone.utc).isoformat()
    }
    
    for attempt in range(1, max_retries + 1):
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            if info and isinstance(info, dict):
                profile["company_name"] = info.get("longName") or info.get("shortName") or profile["company_name"]
                profile["sector"] = info.get("sector") or profile["sector"]
                profile["industry"] = info.get("industry") or profile["industry"]
                profile["currency"] = info.get("currency") or "INR"
                profile["exchange"] = info.get("exchange") or "NSE"
                profile["market_cap"] = info.get("marketCap")
                profile["enterprise_value"] = info.get("enterpriseValue")
                profile["pe_ratio"] = info.get("trailingPE")
                profile["forward_pe"] = info.get("forwardPE")
                profile["peg_ratio"] = info.get("pegRatio")
                profile["dividend_yield"] = info.get("dividendYield")
                profile["beta"] = info.get("beta")
                profile["fifty_two_week_high"] = info.get("fiftyTwoWeekHigh")
                profile["fifty_two_week_low"] = info.get("fiftyTwoWeekLow")
                break
        except Exception as e:
            logger.warning(f"Could not retrieve complete info for {symbol} on attempt {attempt}: {e}")
            time.sleep(1.0)
            
    return profile


def run_pipeline(
    symbols: List[str],
    period: str,
    output_base_dir: str
) -> Dict[str, Any]:
    """
    Main extraction orchestrator:
    1. Prepares storage destination directories (Unity Catalog Volume or local landing).
    2. Downloads historical price time series for each symbol.
    3. Fetches company profiles and metadata.
    4. Writes raw CSV and JSON dumps.
    5. Emits an audit manifest for tracking and validation.
    """
    start_time = datetime.now(timezone.utc)
    extraction_date_str = start_time.strftime("%Y-%m-%d")
    
    # Subdirectories for raw staging
    prices_dir = os.path.join(output_base_dir, "raw_market_prices", extraction_date_str)
    meta_dir = os.path.join(output_base_dir, "raw_company_metadata")
    manifest_dir = os.path.join(output_base_dir, "audit_manifests")
    
    os.makedirs(prices_dir, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)
    os.makedirs(manifest_dir, exist_ok=True)
    
    logger.info(f"Target Landing Paths:")
    logger.info(f"  - Prices:   {prices_dir}")
    logger.info(f"  - Metadata: {meta_dir}")
    
    all_prices: List[pd.DataFrame] = []
    all_metadata: List[Dict[str, Any]] = []
    extraction_stats: Dict[str, Any] = {
        "successful_symbols": [],
        "failed_symbols": [],
        "total_rows_extracted": 0
    }
    
    logger.info(f"Starting data extraction for {len(symbols)} symbols...")
    
    for symbol in tqdm(symbols, desc="Processing Tickers"):
        # 1. Fetch Prices
        df_price = fetch_historical_prices(symbol=symbol, period=period)
        if df_price is not None and not df_price.empty:
            # Write individual raw CSV dump for volume partitioning
            sym_clean = sanitize_filename(symbol)
            individual_csv_path = os.path.join(prices_dir, f"{sym_clean}_raw.csv")
            df_price.to_csv(individual_csv_path, index=False)
            
            all_prices.append(df_price)
            extraction_stats["successful_symbols"].append(symbol)
            extraction_stats["total_rows_extracted"] += len(df_price)
        else:
            extraction_stats["failed_symbols"].append(symbol)
            
        # 2. Fetch Metadata
        meta = fetch_company_metadata(symbol=symbol)
        all_metadata.append(meta)
        
        # Brief throttle to be respectful to upstream APIs
        time.sleep(0.5)
        
    # Write aggregated raw prices dump for bulk ingestion
    if all_prices:
        combined_prices_df = pd.concat(all_prices, ignore_axis=True)
        combined_csv_path = os.path.join(prices_dir, "all_symbols_market_prices_raw.csv")
        combined_prices_df.to_csv(combined_csv_path, index=False)
        logger.info(f"Saved combined raw prices to {combined_csv_path} ({len(combined_prices_df)} records)")
        
    # Write aggregated company metadata JSON and CSV
    meta_json_path = os.path.join(meta_dir, f"company_profiles_{extraction_date_str}.json")
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=2)
        
    meta_df = pd.DataFrame(all_metadata)
    meta_csv_path = os.path.join(meta_dir, f"company_profiles_{extraction_date_str}.csv")
    meta_df.to_csv(meta_csv_path, index=False)
    logger.info(f"Saved company metadata to {meta_json_path} and {meta_csv_path}")
    
    # 3. Create Manifest File
    end_time = datetime.now(timezone.utc)
    manifest = {
        "pipeline_name": "Financial Market Intelligence — Extraction",
        "extraction_date": extraction_date_str,
        "start_time_utc": start_time.isoformat(),
        "end_time_utc": end_time.isoformat(),
        "duration_seconds": round((end_time - start_time).total_seconds(), 2),
        "requested_symbols": symbols,
        "successful_symbols": extraction_stats["successful_symbols"],
        "failed_symbols": extraction_stats["failed_symbols"],
        "total_rows_extracted": extraction_stats["total_rows_extracted"],
        "landing_paths": {
            "prices_directory": prices_dir,
            "metadata_directory": meta_dir
        }
    }
    
    manifest_path = os.path.join(manifest_dir, f"extraction_manifest_{extraction_date_str}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    logger.info(f"Extraction audit manifest written to {manifest_path}")
    logger.info(f"Pipeline completed. Total records extracted: {extraction_stats['total_rows_extracted']}")
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Extract Indian Market Equities Data for Databricks Medallion Pipeline"
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        default=DEFAULT_SYMBOLS,
        help="Space-separated list of ticker symbols (e.g., RELIANCE.NS TCS.NS)"
    )
    parser.add_argument(
        "--period",
        type=str,
        default="5y",
        help="Historical lookback period ('1y', '2y', '5y', '10y', 'max')"
    )
    parser.add_argument(
        "--volume-path",
        type=str,
        default="/Volumes/financial_market_intelligence/raw",
        help="Unity Catalog Volume mount path. If path does not exist, falls back to local landing."
    )
    parser.add_argument(
        "--local-fallback-dir",
        type=str,
        default="./landing_volume",
        help="Local staging directory fallback if Unity Catalog Volume path is unreachable"
    )
    
    args = parser.parse_args()
    
    # Check if Unity Catalog volume path is accessible; else use local fallback
    target_dir = args.volume_path
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        logger.warning(
            f"Unable to access Unity Catalog Volume path '{target_dir}' ({e}). "
            f"Switching to local landing directory '{args.local_fallback_dir}'."
        )
        target_dir = os.path.abspath(args.local_fallback_dir)
        os.makedirs(target_dir, exist_ok=True)
        
    logger.info(f"Output directory established at: {target_dir}")
    manifest = run_pipeline(
        symbols=args.symbols,
        period=args.period,
        output_base_dir=target_dir
    )
    print("\n--- Pipeline Summary ---")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
