from datetime import datetime

def normalize_date(date_str: str) -> datetime:
    """ 
    Convert a date string in various formats to a standardized datetime object.

    Supported formats:
        - ISO: '2025-10-09'
        - US: '10/09/2025' or '10-09-2025'
        - EU: '09/10/2025' or '09-10-2025'
        - With time: '2025-10-09 14:30:00'

    Args:
        date_str(str): The date string to convert.

    Returns:
        datetime: The corresponding datetime object.

    Raises:
        ValueError: If the date format is unrecognized. 

    """
    #Validate type early
    if not isinstance(date_str, str):
        raise ValueError("Input must be a string.")
    
    # Trim spaces and standardize separators
    date_str = date_str.strip().replace('.', '-')

    # # List of possible date formats
    DATE_FORMATS = (
        "%Y-%m-%d",         # ISO
        "%Y-%m-%d %H:%M:%S",# ISO + time
        "%m/%d/%Y",         # US
        "%d/%m/%Y",         # EU
        "%m-%d-%Y",         # US with dashes
        "%d-%m-%Y",         # EU with dashes
    )

    # Use next() to stop at first successful parse — faster than looping all
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # If no valid format found
    raise ValueError(f"Unrecognized date format: {date_str}")

