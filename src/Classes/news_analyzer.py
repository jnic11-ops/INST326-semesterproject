"""
NewsAnalyzer class for fetching and analyzing news sentiment and keywords.

Integrates:
- RSS/Atom feed fetching (via fetch_feed)
- analysis/wordcloud_data.py
- analysis/sentiment_analysis.py
"""

import feedparser
from src.analysis.wordcloud_data import generate_wordcloud_data
from src.analysis.sentiment_analysis import sentiment_analysis


def fetch_feed(url: str):
    """Utility function to fetch and parse an RSS/Atom feed."""
    return feedparser.parse(url)


class NewsAnalyzer:
    """Handles retrieval, sentiment analysis, and keyword extraction from stock-related news."""

    def __init__(self, api_key: str = None):
        """
        Initialize a NewsAnalyzer instance.

        Args:
            api_key (str, optional): API key for news retrieval. Default None if using feeds.
        """
        self._api_key = api_key
        self._articles = []
        self._sentiments = []
        self._keywords = {}
        
    def summarize(self) -> dict:
        """
        Polymorphic summary for NewsAnalyzer.

        Returns:
            dict: Summary of news coverage, sentiment, and keywords.
        """
        article_count = len(self._articles)

        avg_sentiment = None
        if self._sentiments:
            avg_sentiment = sum(self._sentiments) / len(self._sentiments)

        top_keywords = []
        if self._keywords:
            # take top 5 keywords by frequency
            sorted_items = sorted(
                self._keywords.items(),
                key=lambda kv: kv[1],
                reverse=True
            )
            top_keywords = [word for word, _ in sorted_items[:5]]

        return {
            "type": "news",
            "article_count": article_count,
            "avg_sentiment": avg_sentiment,
            "top_keywords": top_keywords,
        }


    # -----------------------------
    # Properties
    # -----------------------------
    @property
    def articles(self):
        """list[dict]: Get stored articles."""
        return self._articles

    @property
    def keywords(self):
        """dict: Get extracted keyword frequencies."""
        return self._keywords

    # -----------------------------
    # Private feed fetcher
    # -----------------------------
    def _fetch_from_feed(self, feed_url: str):
        """Fetch articles from an RSS/Atom feed URL."""
        parsed = fetch_feed(feed_url)
        articles = []
        for entry in parsed.entries:
            articles.append({
                "title": entry.get("title"),
                "description": entry.get("description", ""),
                "published_at": entry.get("published", ""),
                "source": feed_url,
                "url": entry.get("link", "")
            })
        return articles

    # -----------------------------
    # Public fetch
    # -----------------------------
    def fetch(self, ticker: str, feed_urls: list[str]):
        """
        Fetch recent news articles from multiple feeds for a given stock ticker.

        Args:
            ticker (str): Stock ticker symbol.
            feed_urls (list[str]): List of RSS/Atom feed URLs to fetch from.
        """
        all_articles = []
        for url in feed_urls:
            all_articles.extend(self._fetch_from_feed(url))
        if not all_articles:
            raise RuntimeError(f"No news found for {ticker}")
        self._articles = all_articles

    # -----------------------------
    # Sentiment Analysis
    # -----------------------------
    def analyze_sentiment(self):
        """
        Perform sentiment analysis on the fetched news articles.

        Returns:
            list[dict]: Articles enriched with sentiment_score and sentiment_label.
        """
        if not self._articles:
            raise RuntimeError("No news articles loaded. Run fetch() first.")
        self._sentiments = sentiment_analysis(self._articles)
        return self._sentiments

    # -----------------------------
    # Keyword Extraction
    # -----------------------------
    def extract_keywords(self):
        """
        Generate a word frequency dictionary for visualization.

        Returns:
            dict: Mapping of top keywords to their frequency counts.
        """
        if not self._articles:
            raise RuntimeError("No news articles loaded. Run fetch() first.")
        self._keywords = generate_wordcloud_data(self._articles)
        return self._keywords

    # -----------------------------
    # Representations
    # -----------------------------
    def __str__(self):
        return f"NewsAnalyzer with {len(self._articles)} articles"

    def __repr__(self):
        return f"NewsAnalyzer(api_key='***hidden***')"

