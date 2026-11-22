// ==============================================================================
// POWER QUERY (M) ETL SCRIPT — DIRECT CSV IMPORT FOR POWER BI DESKTOP
// ==============================================================================

// 1. Dim_Company
let
    Source = Csv.Document(File.Contents(@"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\data\Dim_Company.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"symbol", type text}, {"company_name", type text}, {"sector", type text}, {"industry", type text}, {"market", type text}, {"currency", type text}, {"market_cap", Int64.Type}, {"sector_key", Int64.Type}})
in
    #"Changed Type"

// 2. Fact_StockAnalytics
let
    Source = Csv.Document(File.Contents(@"D:\BDA Project\financial-market-intelligence\05_powerbi_dashboard\data\Fact_StockAnalytics.csv"), [Delimiter=",", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"symbol", type text}, {"trade_date", type date}, {"date_key", Int64.Type}, {"open", type number}, {"high", type number}, {"low", type number}, {"close", type number}, {"volume", Int64.Type}, {"daily_return_pct", type number}, {"sma_7", type number}, {"sma_20", type number}, {"sma_50", type number}, {"bollinger_upper", type number}, {"bollinger_lower", type number}, {"rsi_14", type number}, {"sector_key", Int64.Type}})
in
    #"Changed Type"
