from query_builders.base_query_builder import BaseQueryBuilder

class DashboardQueryBuilder(BaseQueryBuilder):
    """Builds queries automatically for dashboard displays."""

    def build_query(self, params: dict):
        # Example: dashboard gets broader/default queries
        return {
            "ticker": params.get("ticker", "SPY"),
            "start_date": params.get("start_date", "2024-01-01"),
            "end_date": params.get("end_date", "2024-12-31"),
            "summary": True
        }
