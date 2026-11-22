# Power BI & Tableau Integration & Data Modeling Guide

## 1. Star Schema Relationship Architecture
Connect the tables in Power BI Model View or Tableau Data Source Canvas with the following cardinalities:

| From Table (Dimension) | From Column | To Table (Fact) | To Column | Cardinality | Cross Filter |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Dim_Date` | `date_key` | `Fact_StockAnalytics` | `date_key` | 1 to Many (1:*) | Single (`Dim_Date` filters Fact) |
| `Dim_Company` | `symbol` | `Fact_StockAnalytics` | `symbol` | 1 to Many (1:*) | Single (`Dim_Company` filters Fact) |
| `Dim_Sector` | `sector_key` | `Dim_Company` | `sector_key` | 1 to Many (1:*) | Single |
| `Dim_Date` | `date_key` | `Fact_SectorPerformance`| `date_key` | 1 to Many (1:*) | Single |
| `Dim_Sector` | `sector_key` | `Fact_SectorPerformance`| `sector_key` | 1 to Many (1:*) | Single |
| `Dim_Date` | `date_key` | `Fact_MarketSummary` | `date_key` | 1 to Many (1:*) | Single |

---

## 2. Essential Power BI DAX Measures

### A. Closing Price & Latest Trading Session
```dax
Latest Close Price = 
CALCULATE(
    MAX(Fact_StockAnalytics[close]),
    LASTNONBLANK(Dim_Date[full_date], CALCULATE(COUNTROWS(Fact_StockAnalytics)))
)
```

### B. Cumulative Return (Base 100 Index)
```dax
Cumulative Return Index = 
VAR InitialClose = 
    CALCULATE(
        FIRSTNONBLANKVALUE(Dim_Date[full_date], MAX(Fact_StockAnalytics[close])),
        ALLSELECTED(Dim_Date)
    )
VAR CurrentClose = [Latest Close Price]
RETURN
    DIVIDE(CurrentClose - InitialClose, InitialClose, 0) * 100
```

### C. 30-Day Realized Volatility
```dax
Avg Realized Volatility 30D = 
AVERAGE(Fact_StockAnalytics[annualized_volatility_30d])
```

### D. Golden Cross Indicator (Bullish Signal)
```dax
Golden Cross Signal = 
VAR Sma50 = AVERAGE(Fact_StockAnalytics[sma_50])
VAR Sma200 = AVERAGE(Fact_StockAnalytics[sma_200])
RETURN
    IF(
        ISBLANK(Sma50) || ISBLANK(Sma200),
        "Insufficient History",
        IF(Sma50 > Sma200, "Bullish (Golden Cross)", "Bearish (Death Cross)")
    )
```

### E. RSI Status (Overbought / Oversold)
```dax
RSI Status = 
VAR CurrentRSI = AVERAGE(Fact_StockAnalytics[rsi_14])
RETURN
    SWITCH(
        TRUE(),
        CurrentRSI >= 70, "Overbought (>= 70)",
        CurrentRSI <= 30, "Oversold (<= 30)",
        "Neutral"
    )
```

### F. Advance / Decline Line (Market Breadth)
```dax
Net Advances = 
SUM(Fact_MarketSummary[advancers_count]) - SUM(Fact_MarketSummary[decliners_count])
```

---

## 3. Tableau Calculated Fields Reference

- **Daily Return %:** `([Close] - LOOKUP(ATTR([Close]), -1)) / LOOKUP(ATTR([Close]), -1) * 100`
- **Bollinger Band Width:** `([Bollinger Upper] - [Bollinger Lower]) / [Sma 20]`
- **Trading Volume (Millions):** `[Volume] / 1000000`
- **Market Cap (INR Lakh Crores):** `[Market Cap] / 1000000000000`
