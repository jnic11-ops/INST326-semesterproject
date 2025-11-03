import re
import string
from datetime import datetime


class DataProcessor:
    """
    Process and clean raw text, date, and numeric data for consistency.
    """

    def __init__(self):
        self._processed_count = 0

    @property
    def processed_count(self):
        """Number of processed items."""
        return self._processed_count

    def normalize_date(self, date_str: str) -> datetime:
        """Normalize a date string into a datetime object."""
        formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
        for fmt in formats:
            try:
                result = datetime.strptime(date_str, fmt)
                self._processed_count += 1
                return result
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {date_str}")

    def clean_text(self, text: str) -> str:
        """Remove punctuation, lowercase, and remove common stopwords."""
        stopwords = {"the", "is", "in", "on", "and", "a", "of", "to"}
        text = re.sub(r"<.*?>", " ", text).lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = [t for t in text.split() if t not in stopwords]
        self._processed_count += 1
        return " ".join(tokens)

    def format_currency(self, value: float) -> str:
        """Format a float value as a readable USD string."""
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric.")
        self._processed_count += 1
        return f"${value:,.2f}"

    def __str__(self):
        return f"DataProcessor(processed={self._processed_count})"
