import re

def validate_ticker(ticker: str) -> bool:
    """
    Validate a stock ticker symbol.

    A valid ticker:
    - Must be between 1 and 7 characters long
    - Can contain uppercase letters, numbers, dots ('.'), or dashes ('-')
    - Must not include spaces or other special characters

    Examples of valid tickers:
        'AAPL', 'TSLA', 'BRK.A', 'RDS-B', 'GOOG', 'MSFT'
    Examples of invalid tickers:
        'goog' (lowercase)
        'BRK/A' (slash not allowed)
        'APPLE!' (special character)
        'TOOLONGNAME' (too long)

    Args:
        ticker (str): Stock ticker symbol

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(ticker, str):
        return False

    # Regex: uppercase letters, numbers, dots, or dashes, 1–7 chars
    pattern = r'^[A-Z0-9.-]{1,7}$'
    return bool(re.match(pattern, ticker))



if __name__ == "__main__":
    test_cases = [
        "AAPL", "TSLA", "BRK.A", "RDS-B", "GOOG", "goog", "BRK/A", "APPLE!", "TOOLONGNAME"
    ]

    for t in test_cases:
        print(f"{t:12} -> {validate_ticker(t)}")

