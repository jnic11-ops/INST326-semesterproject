import pandas as pd
import yfinance as yf
from datetime import datetime
import re


class StockDataManager:
    """
    Manages fetching and validating stock data and related news from external APIs.
    """

    def __init__(self, api: str = "yahoo"):
        if api.lower() not in ["yahoo"]:
            raise ValueError("Currently only 'yahoo' API is supported.")
        self._api = api.lower()
        self._last_ticker = None

    # ------------------------------------------------
    # Ticker validation
    # ------------------------------------------------
    def validate_ticker(self, ticker: str) -> bool:
        """Validate a stock ticker symbol (1-7 chars, uppercase, dot/dash allowed)."""
        pattern = r"^[A-Z0-9.-]{1,7}$"
        valid = bool(re.match(pattern, ticker))
        if valid:
            self._last_ticker = ticker
        return valid

    # ------------------------------------------------
    # Fetch stock data
    # ------------------------------------------------
    def fetch_stock_data(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """Fetch OHLCV data for a given ticker using yfinance."""
        if not self.validate_ticker(ticker):
            raise ValueError(f"Invalid ticker: {ticker}")

        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")

        data = yf.download(ticker, start=start_dt, end=end_dt, progress=False)

        if data.empty:
            print(f"No data found for {ticker}.")
            return pd.DataFrame()

        data.reset_index(inplace=True)
        data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

        return data

    # ------------------------------------------------
    # Fetch news for a ticker (refactored function)
    # ------------------------------------------------
    def fetch_news(self, ticker, providers, cleaner=None, limit=None):
        """
        Fetch and normalize news items for a ticker from one or more providers.

        Args:
            ticker (str): Stock symbol.
            providers (list | tuple): Provider callables returning iterable news dicts.
            cleaner (callable | None): Optional text cleaner.
            limit (int | None): Optional max number of articles.

        Returns:
            list: Sorted list of normalized news items.
        """
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
                    for key in ["id", "published_at", "source", "title", "url"]:
                        if key not in item:
                            raise KeyError(f"Missing required key in news item: {key}")

                    # Normalize ticker
                    if "ticker" not in item or item["ticker"] is None:
                        item["ticker"] = ticker

                    # Clean text
                    if cleaner is not None:
                        title = item.get("title", "") or ""
                        summary = item.get("summary", "") or ""
                        item["cleaned_text"] = cleaner((title + " " + summary).strip())

                    collected.append(item)

        if not collected:
            raise ValueError("No news data returned by providers")

        collected.sort(key=lambda r: r["published_at"])

        if isinstance(limit, int) and limit > 0:
            collected = collected[-limit:]

        return collected

    def __str__(self):
        return f"StockDataManager(api='{self._api}', last_ticker='{self._last_ticker}')"
