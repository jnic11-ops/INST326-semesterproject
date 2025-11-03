"""
NewsAnalyzer class for fetching and analyzing news sentiment and keywords.

Integrates functions from:
- data_collection/fetch_news.py
- analysis/wordcloud_data.py
- analysis/sentiment_analysis.py
"""

from src.data_collection.fetch_news import fetch_news
from src.analysis.wordcloud_data import generate_wordcloud_data
from src.analysis.sentiment_analysis import sentiment_analysis


class NewsAnalyzer:
    """Handles retrieval, sentiment analysis, and keyword extraction from stock-related news."""

    def __init__(self, api_key: str):
        """
        Initialize a NewsAnalyzer instance.

        Args:
            api_key (str): API key for news retrieval.
        """
        self._api_key = api_key
        self._articles = []
        self._sentiments = []
        self._keywords = {}

    @property
    def articles(self):
        """list[dict]: Get stored articles."""
        return self._articles

    @property
    def keywords(self):
        """dict: Get extracted keyword frequencies."""
        return self._keywords

    def fetch(self, ticker: str):
        """Fetch recent news articles related to a given stock ticker."""
        print(f"Fetching news for {ticker}...")
        self._articles = fetch_news(ticker, self._api_key)
        if not self._articles:
            raise RuntimeError(f"No news found for {ticker}")

    def analyze_sentiment(self):
        """Perform sentiment analysis on the fetched news."""
        if not self._articles:
            raise RuntimeError("No news articles loaded. Run fetch() first.")
        self._sentiments = sentiment_analysis(self._articles)
        return self._sentiments

    def extract_keywords(self):
        """Generate a word frequency dictionary for visualization."""
        if not self._articles:
            raise RuntimeError("No news articles loaded. Run fetch() first.")
        self._keywords = generate_wordcloud_data(self._articles)
        return self._keywords

    def __str__(self):
        return f"NewsAnalyzer with {len(self._articles)} articles"

    def __repr__(self):
        return f"NewsAnalyzer(api_key='***hidden***')"
