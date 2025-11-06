from typing import List, Dict, Any, Optional
from datetime import datetime
import statistics

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

    def prepare_chart_payload(
        prices: List[float],
        timestamps: Optional[List[datetime]] = None,
        indicators: Optional[Dict[str, List[Optional[float]]]] = None,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Prepare a JSON-serializable payload for frontend charting libraries.
    
        Returns labels (ISO datetimes or index), datasets for price and indicators,
        and simple meta stats (min, max, avg).
        """
        if not isinstance(prices, list) or len(prices) == 0:
            raise ValueError("prices must be a non-empty list")
        n = len(prices)
        if timestamps is not None and len(timestamps) != n:
            raise ValueError("timestamps length must match prices")
        labels = ([t.isoformat() if isinstance(t, datetime) else str(t) for t in timestamps]
                  if timestamps else [str(i) for i in range(n)])
        datasets = [{"label": "Price", "data": [None if p is None else round(float(p), 4) for p in prices], "type": "line"}]
        if isinstance(indicators, dict):
            for name, series in indicators.items():
                if isinstance(series, list) and len(series) == n:
                    datasets.append({"label": name, "data": [None if v is None else round(float(v), 4) for v in series], "type": "line"})
        numeric = [float(p) for p in prices if p is not None]
        meta = {"min": min(numeric) if numeric else None, "max": max(numeric) if numeric else None, "avg": round(statistics.mean(numeric), 4) if numeric else None}
        return {"title": title or "Price Chart", "labels": labels, "datasets": datasets, "meta": meta}

    def build_dashboard_summary(
        portfolio: Dict[str, Dict[str, Any]],
        latest_prices: Dict[str, float],
        news_items: Optional[List[Dict[str, Any]]] = None,
        alerts: Optional[List[Dict[str, Any]]] = None,
        max_news: int = 5
    ) -> Dict[str, Any]:
        """
        Build a compact dashboard summary for the frontend.
    
        Returns total portfolio value, per-position breakdown, top alerts,
        and a trimmed list of recent news entries. All outputs are JSON-serializable.
        """
        if not isinstance(portfolio, dict) or not isinstance(latest_prices, dict):
            raise ValueError("portfolio and latest_prices must be dicts")
        if not isinstance(max_news, int) or max_news < 0:
            raise ValueError("max_news must be a non-negative int")
    
        total = 0.0
        positions = []
        for ticker, info in portfolio.items():
            shares = float(info.get("shares", 0))
            buy = info.get("buy_price")
            price = latest_prices.get(ticker)
            position_value = (float(price) * shares) if price is not None else 0.0
            total += position_value
            unrealized = None
            if price is not None and buy is not None:
                unrealized = round((float(price) - float(buy)) * shares, 4)
            positions.append({
                "ticker": ticker,
                "shares": shares,
                "price": round(float(price), 4) if price is not None else None,
                "position_value": round(position_value, 4),
                "purchase_price": round(float(buy), 4) if buy is not None else None,
                "unrealized_pl": unrealized
            })
    
        # compute percent allocation
        for p in positions:
            p["pct_of_portfolio"] = round((p["position_value"] / total) * 100, 2) if total > 0 else 0.0
    
        recent = []
        if isinstance(news_items, list):
            for n in news_items[:max_news]:
                recent.append({
                    "title": n.get("title") or n.get("headline"),
                    "source": n.get("source"),
                    "published_at": (n.get("published_at").isoformat()
                                     if isinstance(n.get("published_at"), datetime) else n.get("published_at")),
                    "sentiment": n.get("sentiment"),
                    "url": n.get("url")
                })
    
        top_alerts = alerts[:10] if isinstance(alerts, list) else []
        return {"total_value": round(total, 4), "positions": positions, "top_alerts": top_alerts, "recent_news": recent}
