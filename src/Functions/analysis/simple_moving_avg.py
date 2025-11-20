def simple_moving_average(values, window=20):
    """Compute a simple moving average (SMA) over a list of prices.

    Args:
        values (list[float]): Sequence of numeric prices (e.g., closing prices).
        window (int): Window size for the SMA (default 20).

    Returns:
        list[float | None]: SMA values aligned with input length.
            Positions with insufficient history return None.

    Raises:
        TypeError: If values is not a list or window is not an int.
        ValueError: If window < 1.

    Examples:
        >>> simple_moving_average([1, 2, 3, 4, 5], window=3)
        [None, None, 2.0, 3.0, 4.0]
        >>> simple_moving_average([10, 10, 10, 10], window=2)
        [None, 10.0, 10.0, 10.0]
    """
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    if not isinstance(window, int):
        raise TypeError("window must be an int")
    if window < 1:
        raise ValueError("window must be >= 1")

    n = len(values)
    if n == 0:
        return []

    out = [None] * n
    running_sum = 0.0

    for i, v in enumerate(values):
        running_sum += float(v)
        if i >= window:
            running_sum -= float(values[i - window])
        if i >= window - 1:
            out[i] = running_sum / window

    return out
