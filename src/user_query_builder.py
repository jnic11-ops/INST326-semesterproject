class UserQueryBuilder:
    """
    Convert user interface parameters into structured query filters.
    """

    def __init__(self):
        self._last_query = None

    def build_user_query(self, params: dict) -> dict:
        """
        Build a normalized query from UI parameters.
        Example:
            {"ticker": "AAPL", "sector": "Tech", "sentiment": "positive"}
        """
        query = {}
        if "ticker" in params:
            query["ticker"] = params["ticker"].upper()
        if "sector" in params:
            query["sector"] = params["sector"].title()
        if "sentiment" in params:
            query["sentiment"] = params["sentiment"].lower()

        self._last_query = query
        return query

    def __str__(self):
        return f"UserQueryBuilder(last_query={self._last_query})"
