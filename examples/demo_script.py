"""
Demo Script for Stock Analysis System
-------------------------------------

This script demonstrates how the main classes in the project work together:
- DataProcessor
- StockDataManager
- StockAnalyzer
- PortfolioManager

It shows how to load a portfolio, fetch stock data, clean text, and run basic analysis.
"""

from data_processor import DataProcessor
from stock_data_manager import StockDataManager
from stock_analyzer import StockAnalyzer
from portfolio_manager import PortfolioManager


def main():

    print("\n=== DEMO: Portfolio Loading ===")
    portfolio = PortfolioManager("my_portfolio.csv")
    print(portfolio)
    print("Holdings:", portfolio.portfolio)

    print("\n=== DEMO: Fetching Stock Data ===")
    manager = StockDataManager(api="yahoo")
    df = manager.fetch_stock_data("AAPL", "2024-01-01", "2024-02-01")
    print(df.head())

    print("\n=== DEMO: Running Indicators ===")
    analyzer = StockAnalyzer("AAPL", df)
    sma = analyzer.calculate_sma(10)
    rsi = analyzer.calculate_rsi(14)
    anomalies = analyzer.detect_anomalies()

    print("First 5 SMA values:", sma[:5])
    print("First 5 RSI values:", rsi[:5])
    print("Anomaly indices:", anomalies)

    print("\n=== DEMO: Data Processing ===")
    dp = DataProcessor()
    cleaned = dp.clean_text("The STOCK market is UP today!!")
    formatted = dp.format_currency(12345.678)

    print("Cleaned text:", cleaned)
    print("Formatted currency:", formatted)
    print("Processed count:", dp.processed_count)


if __name__ == "__main__":
    main()
