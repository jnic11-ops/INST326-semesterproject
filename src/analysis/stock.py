"""
Stock class for managing and analyzing stock price data.

Integrates functions from:
- utils/validation_utils.py
- data_collection/fetch_stock_data.py
- analysis/calc_technical_indicators.py
- analysis/price_anomaly_detect.py
"""

from datetime import datetime
import pandas as pd
from src.utils.validation_utils import validate_ticker
from src.data_collection.fetch_stock_data import fetch_stock_data
from src.analysis.calc_technical_indicators import calculate_technical_indicators
from src.analysis.price_anomaly_detect import detect_price_anomalies


class Stock:
    """Represents a stock and its associated price data and indicators."""

    def __init__(self, ticker: str):
        """
        Initialize a Stock object.

        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL').

        Raises:
            ValueError: If ticker format is invalid.
        """
        if not validate_ticker(ticker):
            raise ValueError(f"Invalid ticker symbol: {ticker}")
        self._ticker = ticker.upper()
        self._data = pd.DataFrame()
        self._indicators = {}

    @property
    def ticker(self) -> str:
        """str: Get the stock ticker symbol."""
        return self._ticker

    @property
    def data(self) -> pd.DataFrame:
        """pd.DataFrame: Return stock price data."""
        return self._data

    def load_data(self, api_key: str, start: str, end: str) -> None:
        """Fetch stock price data and store internally."""
        print(f"Fetching stock data for {self._ticker}...")
        self._data = fetch_stock_data(api_key, self._ticker, start, end)
        if self._data.empty:
            raise RuntimeError(f"No data found for {self._ticker}")

    def analyze_indicators(self) -> None:
        """Calculate technical indicators (SMA, RSI) for stock data."""
        if self._data.empty:
            raise RuntimeError("Stock data must be loaded before analysis.")
        prices = self._data["Close"].tolist()
        self._indicators = calculate_technical_indicators(prices)
        self._data["SMA"] = self._indicators["SMA"]
        self._data["RSI"] = self._indicators["RSI"]

    def detect_anomalies(self):
        """Detect anomalies in stock price trends."""
        if self._data.empty:
            raise RuntimeError("Stock data must be loaded before anomaly detection.")
        prices = self._data["Close"].tolist()
        alerts = detect_price_anomalies(prices)
        return alerts

    def __str__(self):
        return f"Stock({self._ticker}) with {len(self._data)} records"

    def __repr__(self):
        return f"Stock(ticker='{self._ticker}')"
