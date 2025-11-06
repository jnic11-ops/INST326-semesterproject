import pandas as pd
import yfinance as yf
from datetime import datetime
import re


class StockDataManager:
    """
    Manages fetching and validating stock data and related news from external APIs.

    Example:
        >>> manager = StockDataManager(api="yahoo")
        >>> df = manager.fetch_stock_data("AAPL", "2024-01-01", "2024-05-01")
        >>> print(df.head())
    """

    def __init__(self, api: str = "yahoo"):
        """
        Initialize StockDataManager with an API source.

        Args:
            api (str): The API to use for data retrieval (currently only 'yahoo' supported).

        Raises:
            ValueError: If the API is not supported.
        """
        if api.lower() not in ["yahoo"]:
            raise ValueError("Currently only 'yahoo' API is supported.")
        self._api = api.lower()
        self._last_ticker = None

    # ------------------------------------------------
    # Encapsulated Properties
    # ------------------------------------------------
    @property
    def api(self):
        """Return the active API source."""
        return self._api

    @property
    def last_ticker(self):
        """Return the most recently validated ticker."""
        return self._last_ticker

    # ------------------------------------------------
    # Ticker validation
    # ------------------------------------------------
    def validate_ticker(self, ticker: str) -> bool:
        """
        Validate a stock ticker symbol (1–7 uppercase characters, dot/dash allowed).

        Example:
            >>> manager = StockDataManager()
            >>> manager.validate_ticker("AAPL")
            True
        """
        pattern = r"^[A-Z0-9.-]{1,7}$"
        valid = bool(re.match(pattern, ticker))
        if valid:
            self._last_ticker = ticker
        return valid

    # ------------------------------------------------
    # Fetch stock data
    # ------------------------------------------------
    def fetch_stock_data(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Fetch OHLCV data for a given ticker using yfinance.

        Args:
            ticker (str): Stock symbol.
            start (str): Start date in 'YYYY-MM-DD'.
            end (str): End date in 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: DataFrame with ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'].

        Example:
            >>> manager = StockDataManager()
            >>> df = manager.fetch_stock_data("AAPL", "2024-01-01", "2024-05-01")
            >>> print(df.head())
        """
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
    # Fetch news for a ticker
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

        Example:
            >>> def provider(t):
            ...     return [{"id": "1", "published_at": "2025-11-03T12:00:00Z",
            ...              "source": "example.com", "title": "Market update", "url": "https://example.com"}]
            >>> manager = StockDataManager()
            >>> news = manager.fetch_news("AAPL", [provider])
            >>> print(news[0]["title"])
            Market update
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
                    for key in ["id", "published_at", "source", "title", "url"]:
                        if key not in item:
                            raise KeyError(f"Missing required key in news item: {key}")

                    if "ticker" not in item or item["ticker"] is None:
                        item["ticker"] = ticker

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

    # ------------------------------------------------
    # String Representations
    # ------------------------------------------------
    def __str__(self):
        return f"StockDataManager(api='{self._api}', last_ticker='{self._last_ticker}')"

    def __repr__(self):
        return f"StockDataManager(api={self._api!r}, last_ticker={self._last_ticker!r})"

