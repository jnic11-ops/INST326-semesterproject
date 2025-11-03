from typing import Dict, Any, List, Optional
from datetime import datetime

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
