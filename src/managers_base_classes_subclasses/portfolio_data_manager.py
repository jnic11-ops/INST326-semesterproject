import csv
from .base_data_manager import BaseDataManager

class PortfolioDataManager(BaseDataManager):
    """
    Loads and normalizes user portfolio data from a CSV file.
    """

    def fetch_data(self, file_path: str) -> dict:
        """
        Load and parse portfolio CSV data.

        Args:
            file_path (str): Path to CSV file.

        Returns:
            dict: {ticker: {"shares": float, "buy_price": float}}
        """
        super().fetch_data()  # Polymorphic structure requirement

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
