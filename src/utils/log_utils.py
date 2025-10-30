from datetime import datetime

def log_metadata(source: str, params: dict) -> dict:
    """
    Create a standardized metadata entry for API calls or data retrieval.

    Args:
        source (str): Name of the data source or API (e.g., "AlphaVantage", "TheNewsAPI").
        params (dict): Dictionary of parameters used in the request.

    Returns:
        dict: A dictionary containing metadata including timestamp, source, and parameters.
    """
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "parameters": params
    }

    return metadata

#test
meta = log_metadata("AlphaVantage", {"ticker": "AAPL", "interval": "1d"})
print(meta)
# {'timestamp': '2025-10-20T11:55:12.345678', 'source': 'AlphaVantage', 'parameters': {'ticker': 'AAPL', 'interval': '1d'}}
