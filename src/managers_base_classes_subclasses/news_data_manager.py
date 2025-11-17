import requests
from .base_data_manager import BaseDataManager

class NewsDataManager(BaseDataManager):
    """
    Retrieves financial news articles for a given stock.
    """

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def fetch_data(self, ticker: str):
        """
        Fetch current news articles related to a stock.

        Args:
            ticker (str): Stock symbol.

        Returns:
            list[dict]: Parsed article data.
        """
        super().fetch_data()  # Required for assignment consistency

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": ticker,
            "apiKey": self.api_key,
            "sortBy": "publishedAt",
            "language": "en",
        }
        response = requests.get(url, params=params)
        data = response.json()

        return data.get("articles", [])

