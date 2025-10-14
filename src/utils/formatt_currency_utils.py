def format_currency(value: float) -> str:
    """
    Format a float value into a human-readable currency string.

    Examples:
    1234.56 -> "$1,234.56"
    1000000 -> "$1,000,000,.00"
    -52.9   -> "-52.90"

    Args:
        value(float): Numeric value to format
    
    Returns:
        str: Formatted string with currency symbol and two decimal places
    
    """

    if not isinstance (value, (int, float)):
        return "Invalid value"
    
    #Format the number with commas and two decimal places
    
    formatted = f"${value:,.2f}"

    #Handle negative values with leading "-"
    if value < 0:
        formatted = f"-${abs(value):,.2f}"

    return formatted