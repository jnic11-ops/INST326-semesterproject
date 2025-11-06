Class Design Documentation
Information Retrieval and Analysis System for Stock Data

This document outlines the object-oriented design of the system, describing the purpose, integrated functions, and design principles of each class.
All classes follow strong encapsulation, validation, and modularity principles and integrate functions from the Project 1 function library where applicable.

1. StockDataManager

Purpose:
Manages the retrieval and validation of stock market data and related news from APIs (e.g., Yahoo Finance, NewsAPI).
Handles input validation, API normalization, and unified error handling.

Integrated Functions:

fetch_stock_data

fetch_news

validate_ticker

Design Decisions:
Centralizes all market data access in one interface to ensure consistent validation and structure before analysis.
Allows flexible integration of new APIs with minimal modification to other components.

Future Inheritance Potential:

CryptoDataManager – support for cryptocurrency tickers.

ExtendedMarketDataManager – includes ETF, index, or macroeconomic data.

MockDataManager – for testing and simulation.

2. DataProcessor

Purpose:
Cleans and formats text, dates, and numerical data for analysis consistency.
Provides standardized preprocessing to prepare raw market and sentiment data.

Integrated Functions:

normalize_date

clean_text

format_currency

Design Decisions:
Centralizes normalization logic to ensure reproducibility and reduce redundancy.
Encapsulation of preprocessing logic simplifies updates and guarantees consistent outputs across modules.

Future Inheritance Potential:

FinancialDataProcessor – adds financial metric transformations.

TextDataProcessor – integrates advanced NLP pipelines for sentiment extraction.

3. PortfolioManager

Purpose:
Handles portfolio file ingestion, validation, and normalization.
Parses holdings from CSV files into structured dictionaries for analysis or reporting.

Integrated Functions:

_parse_portfolio_csv

_load_portfolio

Design Decisions:
Separates file parsing and validation for clarity and reusability.
Provides a consistent interface for downstream analytics, such as performance evaluation or visualization.

Future Inheritance Potential:

AdvancedPortfolioManager – integrates brokerage APIs for live updates.

SimulatedPortfolioManager – supports backtesting and virtual trading.

4. StockAnalyzer

Purpose:
Performs analytical computations on stock data, including technical indicators and anomaly detection.
Supports operations like Simple Moving Average (SMA), Relative Strength Index (RSI), and volatility-based anomaly detection.

Integrated Functions:

_simple_moving_average

_calculate_rsi

_detect_price_anomalies

calculate_sma

calculate_rsi

detect_anomalies

Design Decisions:
Encapsulates all analytical logic to keep mathematical computations separate from data retrieval and presentation.
Maintains extensibility for adding future analytics like MACD, Bollinger Bands, or custom indicators.

Future Inheritance Potential:

AdvancedStockAnalyzer – integrates multi-factor analysis and ML-driven forecasting.

SentimentStockAnalyzer – merges technical and news sentiment signals.

5. Utility Modules

Although not core entity classes, these modules support reusable, system-wide functionality for clean code structure.

a. log_utils (log_metadata)

Purpose:
Standardizes metadata creation for API calls or data retrieval.
Each call records source, parameters, and timestamp for traceability.

Function:

log_metadata(source, params)

Usage Example:

meta = log_metadata("AlphaVantage", {"ticker": "AAPL", "interval": "1d"})


Design Role:
Supports consistent logging across all modules — improves transparency and debugging of data sources.

b. url_utils (extract_domain)

Purpose:
Extracts the clean domain name from a URL for standardization and reporting.

Function:

extract_domain(url)

Usage Example:

extract_domain("https://www.bloomberg.com/news/article")
# returns: "bloomberg.com"


Design Role:
Useful for summarizing news sources or verifying valid API URLs within the NewsAnalyzer and related modules.

6. (Optional) NewsAnalyzer (if included)

Purpose:
Analyzes financial news articles for sentiment and relevance to a given ticker or portfolio.
Integrates text processing with DataProcessor.

Integrated Functions:

analyze_sentiment

summarize_articles

Design Decisions:
Bridges unstructured text data with structured financial signals, enabling correlation between sentiment and market performance.


