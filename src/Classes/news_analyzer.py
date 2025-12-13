"""
NewsAnalyzer class for fetching and analyzing news sentiment and keywords.

Integrates:
- RSS/Atom feed fetching (via feedparser)
- Functions: generate_wordcloud_data, sentiment_analysis
"""

import feedparser
from datetime import datetime
from src.Functions.analysis.wordcloud_data import generate_wordcloud_data
from src.Functions.analysis.sentiment_analysis import sentiment_analysis


def fetch_feed(url: str):
    """Utility function to fetch and parse an RSS/Atom feed."""
    return feedparser.parse(url)


class NewsAnalyzer:
    """Handles retrieval, sentiment analysis, and keyword extraction for stock-related news."""

    def __init__(self, api_key: str = None):
        self._api_key = api_key
        self._articles = []
        self._sentiments = []
        self._keywords = {}

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------
    @property
    def articles(self):
        return self._articles

    @property
    def keywords(self):
        return self._keywords

    # ---------------------------------------------------------
    # INTERNAL: Normalize dates
    # ---------------------------------------------------------
    def _parse_date(self, raw_date: str):
        """Attempt to convert feed 'published' timestamps into real datetime objects."""
        try:
            return datetime(*feedparser.parse(raw_date).updated_parsed[:6])
        except Exception:
            return raw_date  # fallback: return string

    # ---------------------------------------------------------
    # INTERNAL: Fetch from RSS feed
    # ---------------------------------------------------------
    def _fetch_from_feed(self, feed_url: str):
        parsed = fetch_feed(feed_url)
        articles = []

        for entry in parsed.entries:
            articles.append({
                "title": entry.get("title", "").strip(),
                "description": entry.get("description", "").strip(),
                "published_at": self._parse_date(entry.get("published", "")),
                "source": feed_url,
                "link": entry.get("link", "")
            })

        return articles

    # ---------------------------------------------------------
    # PUBLIC FETCH (with ticker filtering + deduplication)
    # ---------------------------------------------------------
    def fetch(self, ticker: str, feed_urls: list[str]):
        """
        Fetch recent news articles from multiple RSS feeds.
        Filters articles to only those relevant to the given ticker symbol.
        """
        all_articles = []
        ticker_upper = ticker.upper()

        for url in feed_urls:
            all_articles.extend(self._fetch_from_feed(url))

        if not all_articles:
            raise RuntimeError(f"No news found from given feeds.")

        # ---------------------------------------------------------
        # FILTER ARTICLES THAT MENTION THE TICKER
        # ---------------------------------------------------------
        filtered = []
        for a in all_articles:
            text = f"{a['title']} {a['description']}".upper()
            if ticker_upper in text:      # basic relevance filter
                filtered.append(a)

        # If nothing passes filter, fall back to ALL articles
        self._articles = filtered if filtered else all_articles

        # ---------------------------------------------------------
        # REMOVE DUPLICATE TITLES
        # ---------------------------------------------------------
        unique = {}
        for a in self._articles:
            unique[a["title"]] = a
        self._articles = list(unique.values())

        # ---------------------------------------------------------
        # SORT MOST RECENT FIRST
        # ---------------------------------------------------------
        self._articles.sort(
            key=lambda x: x.get("published_at", ""),
            reverse=True
        )

    # ---------------------------------------------------------
    # Sentiment Analysis
    # ---------------------------------------------------------
    def analyze_sentiment(self):
        if not self._articles:
            raise RuntimeError("No news articles loaded. Run fetch() first.")
        self._sentiments = sentiment_analysis(self._articles)
        return self._sentiments

    # ---------------------------------------------------------
    # Sentiment Summary (NEW)
    # ---------------------------------------------------------
    def sentiment_summary(self):
        """
        Summarize positive, neutral, and negative percentages.
        Must be called AFTER analyze_sentiment().
        """
        if not self._sentiments:
            raise RuntimeError("Sentiment not calculated. Run analyze_sentiment() first.")

        counts = {"positive": 0, "neutral": 0, "negative": 0}

        for s in self._sentiments:
            label = s.get("sentiment_label", "").lower()
            if label in counts:
                counts[label] += 1

        total = sum(counts.values())
        if total == 0:
            return counts

        return {
            "positive": round(counts["positive"] / total * 100, 2),
            "neutral": round(counts["neutral"] / total * 100, 2),
            "negative": round(counts["negative"] / total * 100, 2),
        }

    # ---------------------------------------------------------
    # Keyword Extraction
    # ---------------------------------------------------------
    def extract_keywords(self):
        if not self._articles:
            raise RuntimeError("No news articles loaded. Run fetch() first.")

        self._keywords = generate_wordcloud_data(self._articles)
        return self._keywords

    # ---------------------------------------------------------
    # Representations
    # ---------------------------------------------------------
    def __str__(self):
        return f"NewsAnalyzer with {len(self._articles)} articles"

    def __repr__(self):
        return f"NewsAnalyzer(api_key='***hidden***')"


