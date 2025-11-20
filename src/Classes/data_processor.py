import re
import string
from datetime import datetime

class DataProcessor:
    """
    A utility class for cleaning and formatting text, date, and numeric data.

    This class integrates functions from the project’s preprocessing library and
    provides consistent handling of data normalization tasks.

    Example:
        >>> dp = DataProcessor()
        >>> dp.clean_text("The stock market is UP!")
        'stock market up'
        >>> dp.normalize_date("2025-11-03")
        datetime.datetime(2025, 11, 3, 0, 0)
        >>> dp.format_currency(12345.678)
        '$12,345.68'
    """

    def __init__(self, start_count: int = 0):
        """
        Initialize the DataProcessor with an optional starting count.

        Args:
            start_count (int): Initial processed item count. Must be non-negative.

        Raises:
            ValueError: If start_count is negative.
            TypeError: If start_count is not an integer.
        """
        if not isinstance(start_count, int):
            raise TypeError("start_count must be an integer.")
        if start_count < 0:
            raise ValueError("start_count must be non-negative.")
        self._processed_count = start_count

    # ------------------------------------------------
    # Encapsulation: private attribute + property
    # ------------------------------------------------
    @property
    def processed_count(self):
        """Return the number of processed items."""
        return self._processed_count

    # ------------------------------------------------
    # Instance methods
    # ------------------------------------------------
    def normalize_date(self, date_str: str) -> datetime:
        """
        Normalize a date string into a datetime object.

        Args:
            date_str (str): Date string in common formats ('YYYY-MM-DD', etc.)

        Returns:
            datetime: Parsed date object.

        Raises:
            ValueError: If format is unrecognized.

        Example:
            >>> dp = DataProcessor()
            >>> dp.normalize_date("03/11/2025")
            datetime.datetime(2025, 3, 11, 0, 0)
        """
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
        """
        Clean text by removing punctuation, lowercasing, and removing stopwords.

        Args:
            text (str): Input text.

        Returns:
            str: Cleaned and normalized text.

        Example:
            >>> dp = DataProcessor()
            >>> dp.clean_text("The stock market is UP!")
            'stock market up'
        """
        stopwords = {"the", "is", "in", "on", "and", "a", "of", "to"}
        text = re.sub(r"<.*?>", " ", text).lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = [t for t in text.split() if t not in stopwords]
        self._processed_count += 1
        return " ".join(tokens)

    def format_currency(self, value: float) -> str:
        """
        Format a numeric value as a readable USD currency string.

        Args:
            value (float): Numeric value to format.

        Returns:
            str: Formatted currency string (e.g., '$12,345.67').

        Raises:
            TypeError: If the input is not numeric.

        Example:
            >>> dp = DataProcessor()
            >>> dp.format_currency(12345.678)
            '$12,345.68'
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric.")
        self._processed_count += 1
        return f"${value:,.2f}"

    # ------------------------------------------------
    # String representations
    # ------------------------------------------------
    def __str__(self):
        return f"DataProcessor(processed={self._processed_count})"

    def __repr__(self):
        return f"DataProcessor(processed_count={self._processed_count!r})"

