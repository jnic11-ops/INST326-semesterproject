def build_query(params: dict) -> dict:
    """
    Interpret user interface input into a structured API query dictionary.

    Args:
        params (dict): User input parameters such as:
            {
                "ticker": "AAPL",
                "start_date": "2025-01-01",
                "end_date": "2025-10-01",
                "sentiment": "positive",
                "source": "AlphaVantage"
            }

    Returns:
        dict: Structured query ready to be passed to fetch functions or APIs.
    """
    query = {
        "ticker": params.get("ticker", "").upper(),
        "date_range": {
            "start": params.get("start_date"),
            "end": params.get("end_date")
        },
        "filters": {
            "sentiment": params.get("sentiment"),
            "source": params.get("source")
        }
    }

    # Clean up empty fields
    query = {k: v for k, v in query.items() if v}
    return query

#test
user_input = {
    "ticker": "tsla",
    "start_date": "2025-01-01",
    "end_date": "2025-10-01",
    "sentiment": "neutral"
}

print(build_query(user_input))
# {'ticker': 'TSLA', 'date_range': {'start': '2025-01-01', 'end': '2025-10-01'}, 'filters': {'sentiment': 'neutral'}}
