# Usage Examples for our Information Retrival and Analysis Tool System of Stock Data
This document demonstrates how to use the simple utility functions, data processing functions, interface functions, analysis functions, and reporting functions in practice. 
It includes **example inputs and outputs** and **workflow examples**. 

## 1. Simple Utility Functions

### validate_ticker(ticker: str)


Validate stock ticker symbols.

```python
from src.utils.validate_ticker import validate_ticker

tickers = ["AAPL", "goog", "BRK.A", "RDS-B"]
for t in tickers:
    print(f"{t} valid? -> {validate_ticker(t)}")
```

### extract_domain(url: str)

Extract host/domain from a news URL.
```python
from src.utils.url_utils import extract_domain

urls = [
    "https://www.marketwatch.com/story/tech-stocks-rally-2025-10-30",
    "http://finance.yahoo.com/news/apple-earnings-beat",
    "https://subdomain.reuters.com/article/us-stocks"
]

for u in urls:
    try:
        domain = extract_domain(u)
        print(f"URL: {u}\nDomain: {domain}\n")
    except ValueError as e:
        print(f"Failed to parse URL {u}: {e}\n")
```

### normalize_date(date_str: str)
Convert a date string in various formats to a standardized datetime object.

```python
from src.utils.normalize_date import normalize_date

dates = ["2025-10-14", "10/14/2025", "14-10-2025", "2025-10-14 15:30:00"]

for d in dates:
    normalized = normalize_date(d)
    print(f"Original: {d} -> Normalized: {normalized}")

```

### clean_text(text: str)
Clean and normalize text for NLP preprocessing.

```python
from src.utils.clean_text import clean_text

sample_texts = [
    "<p>The market is <b>rising</b> rapidly!</p>",
    "This, right here, is a great opportunity for investors.",
    "In 2025, AI-driven trading will dominate the markets."
]

for txt in sample_texts:
    cleaned = clean_text(txt)
    print(f"Original: {txt}\nCleaned : {cleaned}\n")

```
### format_currency(value: float)
Format numbers as human-readable currency strings.

```python
from src.utils.format_currency import format_currency

values = [1234.56, 1000000, -52.9, "abc"]

for v in values:
    formatted = format_currency(v)
    print(f"Original: {v} -> Formatted: {formatted}")

```

## 2. Data Collection 

## fetch_stock_data — Retrieve Historical Stock Prices
Example showing how to download Apple (AAPL) stock data from Yahoo Finance between two dates.

```python
from src.data_collection.fetch_stock_data import fetch_stock_data
```
# Fetch data including adjusted close prices
df1 = fetch_stock_data("yahoo", "AAPL", "2024-01-01", "2024-05-01", use_adjusted=True)
print("With Adjusted Close:")
print(df1.head())

# Fetch data without adjusted close
df2 = fetch_stock_data("yahoo", "AAPL", "2024-01-01", "2024-05-01", use_adjusted=False)
print("\nWithout Adjusted Close:")
print(df2.head())

### parse_portfolio_csv(file_path: str)
Parse a user's portfolio CSV file and normalize its schema.

```python
from src.data_collection.parse_portfolio_csv import parse_portfolio_csv

# Example CSV file: portfolio.csv
# ticker,shares,buy_price
# AAPL,10,150.5
# MSFT,5,310
# TSLA,2,700

portfolio = parse_portfolio_csv("portfolio.csv")
print(portfolio)

```
## 3. Interface

### build_user_query Example

This function helps convert user inputs into a structured query format that can be sent to data collection or analysis modules.

```python
from src.interface.build_user_query import build_user_query

# Example user input
params = {
    "ticker": "AAPL",
    "sector": "Technology",
    "sentiment": "positive",
    "limit": 25
}

query = build_user_query(params)
print(query)
```

### build_dashboard_summary(portfolio: dict, latest_prices: dict, news_items: list = None, alerts: list = None, max_news: int = 5) -> dict

Builds a compact, JSON-friendly dashboard data object summarizing the user’s portfolio.

```python
from datetime import datetime
from src.interface.dashboard import build_dashboard_summary

portfolio = {
    "AAPL": {"shares": 10, "buy_price": 150.0},
    "MSFT": {"shares": 3,  "buy_price": 300.0}
}

latest = {"AAPL": 158.2, "MSFT": 317.75}

news = [
    {
        "title": "Apple releases earnings",
        "source": "Reuters",
        "published_at": datetime.utcnow(),
        "sentiment": "positive",
        "url": "https://example.com"
    }
]

summary = build_dashboard_summary(
    portfolio,
    latest_prices=latest,
    news_items=news,
    max_news=3
)

print(summary["total_value"])
print(summary["positions"][0])
```

### prepare_chart_payload(prices: list, timestamps: list = None, indicators: dict = None, title: str = None) -> dict

Creates a chart-friendly payload compatible with most front-end plotting libraries (e.g., Chart.js, Recharts).
Includes ISO-formatted labels, price data, optional technical indicator overlays, and basic statistics.

```python
from datetime import datetime
from src.interface.charts import prepare_chart_payload
from src.analysis.calculate_technical_indicators import calculate_technical_indicators

prices = [100, 101, 102, 101, 103]
stamp = [datetime(2025, 10, 20+i) for i in range(len(prices))]

ind = calculate_technical_indicators(prices, window=3)

payload = prepare_chart_payload(
    prices,
    timestamps=stamp,
    indicators={"SMA": ind["SMA"]},
    title="Portfolio Performance"
)

print(payload["meta"])
print(payload["datasets"][0]["data"])
```

## 4. Analysis

### calculate_technical_indicators(prices: List[float],window: int=14)

Computes small moving averages and relative strength index series for a list of closing prices.

```python
from src.analysis.calculate_technical_indicators import calculate_technical_indicators

# Example chronological closing prices (oldest -> newest)
prices = [100.0, 101.5, 102.0, 101.0, 103.5, 104.0, 105.0, 106.5, 107.0, 108.0]

# Use a short window to keep example outputs compact
indicators = calculate_technical_indicators(prices, window=5)

print("SMA series:")
print(indicators["SMA"])
print("\nRSI series:")
print(indicators["RSI"])
```

### detect_price_anomolies(prices: List[float], timestamps: Optional[List[datetime]] = None, ...)

Detects unusual price movements by using rolling z-scores on log returns. Returns a list of alert dicts.

```python
from datetime import datetime
from src.analysis.anomaly_detection import detect_price_anomalies

prices = [100, 101, 100.5, 101.2, 150.0, 149.0, 151.0, 150.5]
timestamps = [
    datetime(2025, 10, 20),
    datetime(2025, 10, 21),
    datetime(2025, 10, 22),
    datetime(2025, 10, 23),
    datetime(2025, 10, 24),
    datetime(2025, 10, 25),
    datetime(2025, 10, 26),
    datetime(2025, 10, 27),
]

alerts = detect_price_anomalies(prices, timestamps=timestamps, window=3, z_threshold=2.5)

if not alerts:
    print("No anomalies detected.")
else:
    print("Anomalies:")
    for a in alerts:
        print(a)
```


## Reporting

### export_report(data, output_path, file_type="csv")

Export data to CSV or JSON. Example saves anomaly alerts or indicator summaries.

```python
from src.reporting.export_report import export_report
from src.analysis.anomaly_detection import detect_price_anomalies
from datetime import datetime

# Small example dataset (could be anomalies or indicator rows)
alerts = [
    {"ticker": "AAPL", "index": 4, "timestamp": datetime(2025,10,24).isoformat(), "price": 150.0, "z_score": 3.8762, "reason": "High volatility detected"},
    {"ticker": "TSLA", "index": 7, "timestamp": datetime(2025,10,27).isoformat(), "price": 380.5, "z_score": 3.2111, "reason": "High volatility detected"},
]

# Export as CSV
try:
    export_report(alerts, "reports/anomalies_2025-10-27.csv", file_type="csv")
    print("CSV export succeeded.")
except ValueError as e:
    print(f"Export failed: {e}")

# Export as JSON
try:
    export_report(alerts, "reports/anomalies_2025-10-27.json", file_type="json")
    print("JSON export succeeded.")
except ValueError as e:
    print(f"Export failed: {e}")
```

