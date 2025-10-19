from typing import List, Dict
import math

def calculate_technical_indicators(prices: List[float], window: int = 14) -> Dict[str, List[float]]:
    """
    Calculate moving averages (SMA) and Relative Strength Index (RSI) for a stock.

    Parameters
    ----------
    prices : List[float]
        Chronological list of stock prices (oldest first)
    window : int
        Lookback period for calculations (default=14)

    Returns
    -------
    Dict[str, List[float]]
        {
            "SMA": [...],
            "RSI": [...]
        }

    Raises
    ------
    ValueError
        If prices list is too short or window is invalid
    """
    if len(prices) < window or window < 2:
        raise ValueError("Prices list too short or window < 2")

    sma: List[float] = []
    rsi: List[float] = []

    # Calculate SMA
    for i in range(len(prices)):
        if i + 1 < window:
            sma.append(None)
        else:
            sma.append(sum(prices[i+1-window:i+1])/window)

    # Calculate RSI
    gains: List[float] = [0.0]
    losses: List[float] = [0.0]
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    for i in range(len(prices)):
        if i + 1 < window:
            rsi.append(None)
        else:
            avg_gain = sum(gains[i+1-window:i+1])/window
            avg_loss = sum(losses[i+1-window:i+1])/window
            rs = avg_gain / avg_loss if avg_loss != 0 else math.inf
            rsi_val = 100 - (100 / (1 + rs))
            rsi.append(rsi_val)

    return {"SMA": sma, "RSI": rsi}
