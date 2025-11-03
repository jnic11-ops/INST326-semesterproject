"""
sentiment_analysis.py

Performs a simple, rule-based sentiment analysis without external libraries.
"""

def sentiment_analysis(news_articles: list[dict]) -> list[dict]:
    """
    Perform simple sentiment analysis using word matching.

    Args:
        news_articles (list[dict]): List of dicts with at least 'title' or 'description'.

    Returns:
        list[dict]: Same list, each article with 'sentiment_score' and 'sentiment_label'.
    """
    positive_words = {"gain", "rise", "growth", "profit", "strong", "optimistic", "success", "increase", "up"}
    negative_words = {"loss", "drop", "fall", "decline", "weak", "fear", "down", "crash", "negative"}

    analyzed = []

    for article in news_articles:
        text = (article.get("title") or article.get("description") or "").lower()
        score = 0

        for word in positive_words:
            if word in text:
                score += 1
        for word in negative_words:
            if word in text:
                score -= 1

        # Label sentiment
        if score > 0:
            label = "positive"
        elif score < 0:
            label = "negative"
        else:
            label = "neutral"

        enriched = article.copy()
        enriched["sentiment_score"] = score
        enriched["sentiment_label"] = label
        analyzed.append(enriched)

    return analyzed
