import csv
import os

class PortfolioManager:
    """
    Manage user portfolio files and provide access to holdings data.
    """

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self._file_path = file_path
        self._portfolio = self._load_portfolio()  # main loading method

    @property
    def portfolio(self):
        """Return the loaded portfolio dictionary."""
        return self._portfolio

    # ------------------------------------------------
    # Private methods
    # ------------------------------------------------
    def _load_portfolio(self) -> dict:
        """
        Load portfolio data from CSV file by calling parsing function.
        Keeps loading logic separate from parsing logic.
        """
        return self._parse_portfolio_csv()

    def _parse_portfolio_csv(self) -> dict:
        """
        Parse a CSV file of user holdings into a normalized dictionary.

        Returns:
            dict: {ticker: {"shares": float, "buy_price": float}}
        """
        portfolio = {}
        with open(self._file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    portfolio[row["ticker"].upper()] = {
                        "shares": float(row["shares"]),
                        "buy_price": float(row["buy_price"]),
                    }
                except (KeyError, ValueError):
                    continue
        return portfolio

    # ------------------------------------------------
    # String representations
    # ------------------------------------------------
    def __str__(self):
        return f"PortfolioManager(file='{self._file_path}', stocks={len(self._portfolio)})"

    def __repr__(self):
        return f"PortfolioManager(file_path='{self._file_path}')"


