import yfinance as yf
from .base_data_manager import BaseDataManager

class StockDataManager(BaseDataManager):
    """
    Retrieves historical stock price data.
    Inherits the fetch_data() interface from BaseDataManager.
    """

    def fetch_data(self, ticker: str, start: str, end: str):
        """
        Fetch stock price data using the yfinance API.

        Args:
            ticker (str): Stock ticker symbol.
            start (str): Start date (YYYY-MM-DD).
            end (str): End date (YYYY-MM-DD).

        Returns:
            pandas.DataFrame: Historical OHLCV data.
        """
        super().fetch_data()  # Required per project instructions
        ticker_obj = yf.Ticker(ticker)
        return ticker_obj.history(start=start, end=end)
