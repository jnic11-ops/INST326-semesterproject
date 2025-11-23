from query_builders.base_query_builder import BaseQueryBuilder

class UserQueryBuilder(BaseQueryBuilder):
    """Builds queries based on direct user input."""

    def build_query(self, params: dict):
        return {
            "ticker": params.get("ticker"),
            "start_date": params.get("start_date"),
            "end_date": params.get("end_date")
        }

