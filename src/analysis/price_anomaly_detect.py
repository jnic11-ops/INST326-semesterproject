import math
import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime

def detect_price_anomalies(
    prices: List[float],
    timestamps: Optional[List[datetime]] = None,
    window: int = 20,
    z_threshold: float = 3.0,
    min_window_non_null: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Detect unusual stock price changes using rolling z-scores on log returns.

    Returns beginner-friendly alerts with index, price, timestamp, and reason.

    Parameters
    ----------
    prices : List[float]
        Chronological list of stock prices (oldest first).
    timestamps : Optional[List[datetime]]
        Optional timestamps aligned with prices.
    window : int
        Lookback window size for rolling mean/std.
    z_threshold : float
        Threshold for flagging an anomaly.
    min_window_non_null : Optional[int]
        Minimum non-null returns required to compute z-score.

    Returns
    -------
    List[Dict[str, Any]]
        Each alert contains:
            - index: int
            - timestamp: datetime or None
            - price: float
            - z_score: float
            - reason: str

    Raises
    ------
    ValueError
        If inputs are invalid.
    """
    if not isinstance(prices, list) or len(prices) < 2:
        raise ValueError("prices must be a list with at least 2 entries")
    if timestamps and len(timestamps) != len(prices):
        raise ValueError("timestamps must match prices length")
    if window < 2:
        raise ValueError("window must be >= 2")
    if z_threshold <= 0:
        raise ValueError("z_threshold must be positive")

    if min_window_non_null is None:
        min_window_non_null = math.ceil(window * 0.5)

    # Compute log returns
    n = len(prices)
    returns: List[Optional[float]] = [None] * n
    for i in range(1, n):
        try:
            returns[i] = math.log(prices[i] / prices[i-1])
        except (TypeError, ValueError, ZeroDivisionError):
            returns[i] = None

    alerts: List[Dict[str, Any]] = []
    for i in range(1, n):
        start_idx = max(1, i - window)
        window_vals = [r for r in returns[start_idx:i] if r is not None]
        if len(window_vals) < min_window_non_null or returns[i] is None:
            continue
        mean_w = statistics.mean(window_vals)
        std_w = statistics.pstdev(window_vals)
        z = (returns[i] - mean_w) / std_w if std_w != 0 else float('inf')

        if abs(z) > z_threshold:
            alerts.append({
                "index": i,
                "timestamp": timestamps[i] if timestamps else None,
                "price": prices[i],
                "z_score": round(z, 4),
                "reason": "High volatility detected"
            })
    return alerts
