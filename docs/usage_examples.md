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


### normalize_date(date_str: str)
Convert a date string in various formats to a standardized datetime object.

```python
from src.utils.normalize_date import normalize_date

dates = ["2025-10-14", "10/14/2025", "14-10-2025", "2025-10-14 15:30:00"]

for d in dates:
    normalized = normalize_date(d)
    print(f"Original: {d} -> Normalized: {normalized}")



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


### format_currency(value: float)
Format numbers as human-readable currency strings.

```python
from src.utils.format_currency import format_currency

values = [1234.56, 1000000, -52.9, "abc"]

for v in values:
    formatted = format_currency(v)
    print(f"Original: {v} -> Formatted: {formatted}")



## 2. Data Collection 

## fetch_stock_data — Retrieve Historical Stock Prices
Example showing how to download Apple (AAPL) stock data from Yahoo Finance between two dates.

```python
from src.data_collection.fetch_stock_data import fetch_stock_data

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

