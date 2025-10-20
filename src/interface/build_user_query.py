def build_user_query(params: dict) -> dict:
    """
    Interpret a user's UI input parameters and convert them into a structured query
    for use with data retrieval or analysis functions.

    Args:
        params (dict): User-specified filters or query parameters.
            Example:
                {
                    "ticker": "AAPL",
                    "sector": "Technology",
                    "sentiment": "positive",
                    "limit": 25
                }

    Returns:
        dict: Structured query dictionary suitable for downstream API or database functions.
    """

    if not isinstance(params, dict):
        raise ValueError("Input parameters must be provided as a dictionary.")

    query = {"filter": {}, "query_type": "custom", "limit": 50}

    # Map common parameters to filters
    if "ticker" in params and params["ticker"]:
        query["filter"]["ticker"] = [params["ticker"].upper()]

    if "sector" in params and params["sector"]:
        query["filter"]["sector"] = [params["sector"].title()]

    if "sentiment" in params and params["sentiment"]:
        query["filter"]["sentiment"] = [params["sentiment"].lower()]

    # Allow custom result limits
    if "limit" in params:
        try:
            query["limit"] = int(params["limit"])
        except ValueError:
            query["limit"] = 50

    # Define query type automatically based on available fields
    if "ticker" in query["filter"] and "sentiment" in query["filter"]:
        query["query_type"] = "stock_sentiment"
    elif "sector" in query["filter"]:
        query["query_type"] = "sector_summary"
    else:
        query["query_type"] = "general_query"

    return query

def build_user_query(params: dict) -> dict:
    """
    Interpret a user's UI input parameters and convert them into a structured query
    for use with data retrieval or analysis functions.

    Args:
        params (dict): User-specified filters or query parameters.
            Example:
                {
                    "ticker": "AAPL",
                    "sector": "Technology",
                    "sentiment": "positive",
                    "limit": 25
                }

    Returns:
        dict: Structured query dictionary suitable for downstream API or database functions.
    """

    if not isinstance(params, dict):
        raise ValueError("Input parameters must be provided as a dictionary.")

    query = {"filter": {}, "query_type": "custom", "limit": 50}

    # Map common parameters to filters
    if "ticker" in params and params["ticker"]:
        query["filter"]["ticker"] = [params["ticker"].upper()]

    if "sector" in params and params["sector"]:
        query["filter"]["sector"] = [params["sector"].title()]

    if "sentiment" in params and params["sentiment"]:
        query["filter"]["sentiment"] = [params["sentiment"].lower()]

    # Allow custom result limits
    if "limit" in params:
        try:
            query["limit"] = int(params["limit"])
        except ValueError:
            query["limit"] = 50

    # Define query type automatically based on available fields
    if "ticker" in query["filter"] and "sentiment" in query["filter"]:
        query["query_type"] = "stock_sentiment"
    elif "sector" in query["filter"]:
        query["query_type"] = "sector_summary"
    else:
        query["query_type"] = "general_query"

    return query


#Example Input: if __name__ == "__main__":
 #   example = {
  #      "ticker": "AAPL",
   #     "sector": "Technology",
    #    "sentiment": "positive",
     #   "limit": 25
   # }
    # result = build_user_query(example)
   # print(result) 

