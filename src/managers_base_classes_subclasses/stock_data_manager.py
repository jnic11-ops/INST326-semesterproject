import yfinance as yf
from .base_data_manager import BaseDataManager

class StockDataManager(BaseDataManager):
    """
    Retrieves historical stock price data.
    """

    def __init__(self):
        super().__init__()
        self.source = "Yahoo Finance"

    def fetch_data(self, ticker: str, start: str, end: str):
        ticker_obj = yf.Ticker(ticker)
        return ticker_obj.history(start=start, end=end)
