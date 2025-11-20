import re
import string

def clean_text(text: str) -> str:
    """
    Clean and normalize text for NLP preprocessing.

    Steps:
        1. Remove HTML tags
        2. Convert to lowercase
        3. Remove punctuation
        4. Remove extra spaces
        5. Remove basic stopwords

    Args:
        text (str): Input text (e.g., news article, summary)

    Returns:
        str: Cleaned and normalized text
    """
    if not isinstance(text, str):
        return ""

    # 1 Remove HTML tags (e.g., <p>, <br>)
    text = re.sub(r"<.*?>", " ", text)

    # 2 Convert to lowercase
    text = text.lower()

    # 3 Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 4 Tokenize and remove simple stopwords
    stopwords = {
        "the", "is", "in", "on", "and", "or", "an", "a", "of", "to", "for",
        "with", "this", "that", "by", "it", "as", "from", "at", "be"
    }
    tokens = [word for word in text.split() if word not in stopwords]

    # 5 Rejoin cleaned tokens
    return " ".join(tokens)



