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
### log_metadata(source: str, params: dict)
Create a standardized metadata entry for API calls or data retrieval.

```python
metadata = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "parameters": params
    }

    return metadata
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

### fetch_news(ticker, providers, cleaner=None, limit=None)
Fetch and normalize news items for a ticker from one or more providers (no imports)

```python
if not isinstance(ticker, str):
        raise TypeError("ticker must be a string")
    if not isinstance(providers, (list, tuple)) or not all(callable(p) for p in providers):
        raise TypeError("providers must be a list/tuple of callables")
    if limit is not None and not isinstance(limit, int):
        raise TypeError("limit must be an int or None")
    if cleaner is not None and not callable(cleaner):
        raise TypeError("cleaner must be callable or None")

    collected = []
    for prov in providers:
        batch = prov(ticker)
        if batch:
            for item in batch:
                # Validate required keys
                if "id" not in item:
                    raise KeyError("Missing required key in news item: id")
                if "published_at" not in item:
                    raise KeyError("Missing required key in news item: published_at")
                if "source" not in item:
                    raise KeyError("Missing required key in news item: source")
                if "title" not in item:
                    raise KeyError("Missing required key in news item: title")
                if "url" not in item:
                    raise KeyError("Missing required key in news item: url")

                # Normalize ticker
                if "ticker" not in item or item["ticker"] is None:
                    item["ticker"] = ticker

                # Build cleaned_text
                if cleaner is not None:
                    title = item.get("title", "") or ""
                    summary = item.get("summary", "") or ""
                    item["cleaned_text"] = cleaner((title + " " + summary).strip())

                collected.append(item)

    if not collected:
        raise ValueError("No news data returned by providers")

    # Sort by time in ascending order
    collected.sort(key=lambda r: r["published_at"])

    if isinstance(limit, int) and limit > 0:
        collected = collected[-limit:]

    return collected
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
### sentiment_analysis(news_articles: list[dict]) -> list[dict]
Perform simple sentiment analysis using word matching.

```python
 positive_words = {"gain", "rise", "growth", "profit", "strong", "optimistic", "success", "increase", "up"}
    negative_words = {"loss", "drop", "fall", "decline", "weak", "fear", "down", "crash", "negative"}

    analyzed = []

    for article in news_articles:
        text = (article.get("title") or article.get("description") or "").lower()
        score = 0

        for word in positive_words:
            if word in text:
                score += 1
        for word in negative_words:
            if word in text:
                score -= 1

        # Label sentiment
        if score > 0:
            label = "positive"
        elif score < 0:
            label = "negative"
        else:
            label = "neutral"

        enriched = article.copy()
        enriched["sentiment_score"] = score
        enriched["sentiment_label"] = label
        analyzed.append(enriched)

    return analyzed
```
### generate_wordcloud_data(news_list: list[dict]) -> dict
Extract top keywords and their frequencies from a list of news articles.

```python
all_text = ""

    # Combine titles and descriptions
    for article in news_list:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        all_text += " " + text

    # Remove non-alphabetic characters
    words = re.findall(r'\b[a-z]{3,}\b', all_text)  # only alphabetic words length >= 3

    # Count word frequency
    word_counts = Counter(words)

    # Return top 30 keywords
    return dict(word_counts.most_common(30))

#test
# Simulated multiple news articles
news_list = [
    {"title": "Apple stock rises as new iPhone impresses investors"},
    {"title": "Tech stocks fall slightly after strong gains"},
    {"title": "Apple launches new product lineup amid market optimism"},
    {"title": "Investors optimistic as Apple stock reaches record high"}
]

# Run the function
result = generate_wordcloud_data(news_list)

# Display results
print(result)
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
### generate_summary_table(portfolio_data)
Generate a summary table of portfolio performance statistics.

```python
if not isinstance(portfolio_data, list) or not all(isinstance(d, dict) for d in portfolio_data):
        raise TypeError("portfolio_data must be a list of dictionaries")

    summary = []
    for stock in portfolio_data:
        try:
            score = round(stock["avg_sentiment"] + (stock["price_change"] / 100), 2)
            category = (
                "Strong Positive" if score > 0.5 else
                "Neutral" if -0.5 <= score <= 0.5 else
                "Negative"
            )
            summary.append({
                "ticker": stock["ticker"],
                "score": score,
                "category": category
            })
        except KeyError as e:
            raise KeyError(f"Missing required key in portfolio data: {e.args[0]}")

    return sorted(summary, key=lambda x: x["score"], reverse=True)
```
