import csv
from .base_data_manager import BaseDataManager

class PortfolioDataManager(BaseDataManager):
    """
    Loads and normalizes portfolio data from a CSV file.
    """

    def __init__(self):
        super().__init__()
        self.source = "CSV File"

    def fetch_data(self, file_path: str) -> dict:
        portfolio = {}
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ticker = row["ticker"].upper()
                    portfolio[ticker] = {
                        "shares": float(row["shares"]),
                        "buy_price": float(row["buy_price"]),
                    }
                except (KeyError, ValueError):
                    continue

        return portfolio

