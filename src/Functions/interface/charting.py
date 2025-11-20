from typing import List, Dict, Any, Optional
from datetime import datetime
import statistics

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
