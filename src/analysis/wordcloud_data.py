from collections import Counter
import re

def generate_wordcloud_data(news_list: list[dict]) -> dict:
    """
    Extract top keywords and their frequencies from a list of news articles.

    Args:
        news_list (list[dict]): List of news articles where each item has a 'title' or 'description' key.

    Returns:
        dict: A dictionary mapping keywords to their frequency counts.
    """
    all_text = ""

    # Combine titles and descriptions
    for article in news_list:
        text = (article.get("title", "") + " " + article.get("description", "")).lower()
        all_text += " " + text

    # Remove non-alphabetic characters
    words = re.findall(r'\b[a-z]{3,}\b', all_text)  # only alphabetic words length >= 3

    # Count word frequency
    word_counts = Counter(words)

    # Return top 30 keywords
    return dict(word_counts.most_common(30))

#test
# Simulated multiple news articles
news_list = [
    {"title": "Apple stock rises as new iPhone impresses investors"},
    {"title": "Tech stocks fall slightly after strong gains"},
    {"title": "Apple launches new product lineup amid market optimism"},
    {"title": "Investors optimistic as Apple stock reaches record high"}
]

# Run the function
result = generate_wordcloud_data(news_list)

# Display results
print(result)