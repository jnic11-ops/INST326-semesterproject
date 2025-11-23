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

    def summarize(self) -> dict:
        """
        Polymorphic summary for PortfolioManager.

        Returns:
            dict: Basic metrics about the portfolio loaded from file.
        """
        num_positions = len(self._portfolio)
        total_shares = 0.0
        total_cost_basis = 0.0

        for ticker, position in self._portfolio.items():
            shares = float(position.get("shares", 0.0))
            buy_price = float(position.get("buy_price", 0.0))
            total_shares += shares
            total_cost_basis += shares * buy_price

        avg_buy_price = None
        if total_shares > 0:
            avg_buy_price = total_cost_basis / total_shares

        return {
            "type": "portfolio",
            "file_path": self._file_path,
            "positions": num_positions,
            "total_shares": total_shares,
            "total_cost_basis": total_cost_basis,
            "average_buy_price": avg_buy_price,
        }


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


