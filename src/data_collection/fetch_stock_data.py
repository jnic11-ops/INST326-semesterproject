def fetch_stock_data(ticker, provider, interval="5min", limit=None, validator=None):
    """Fetch recent OHLCV bars for a ticker using a provider function (no imports).

    This function does not import any modules. Instead, it relies on:
      - a `provider` callable you pass in (e.g., an Alpha Vantage adapter)
      - an optional `validator` callable to validate the ticker

    The `provider` must accept `(ticker, interval)` and return an iterable of dicts,
    each dict having at least:
        {
          "ticker": <str>,
          "ts": <ISO8601 string or sortable timestamp>,
          "open": <float>,
          "high": <float>,
          "low": <float>,
          "close": <float>,
          "volume": <int or float>,
          "source": <str>
        }

    Args:
        ticker (str): Stock symbol (e.g., "AAPL").
        provider (callable): Function that returns raw bar dicts given (ticker, interval).
        interval (str): Provider-specific bar interval (default "5min").
        limit (int | None): Optional max number of bars to return after sorting.
        validator (callable | None): Optional function taking `ticker` -> bool.

    Returns:
        list: List of normalized bar dicts sorted by ascending 'ts'.

    Raises:
        TypeError: If inputs have incorrect types.
        ValueError: If ticker is invalid or provider returns no data.
        KeyError: If a required key is missing in a returned bar.

    Examples:
        >>> def fake_provider(t, i):
        ...     return [
        ...         {"ticker": t, "ts": "2025-10-19T14:00:00Z", "open": 10, "high": 12, "low": 9, "close": 11, "volume": 1000, "source": "fake"},
        ...         {"ticker": t, "ts": "2025-10-19T14:05:00Z", "open": 11, "high": 13, "low": 10, "close": 12, "volume": 900, "source": "fake"},
        ...     ]
        >>> def fake_validator(t): return t.isupper()
        >>> bars = fetch_stock_data("AAPL", fake_provider, interval="5min", validator=fake_validator)
        >>> len(bars), bars[-1]["close"]
        (2, 12)
    """
    if not isinstance(ticker, str):
        raise TypeError("ticker must be a string")
    if not callable(provider):
        raise TypeError("provider must be callable")
    if limit is not None and not isinstance(limit, int):
        raise TypeError("limit must be an int or None")
    if validator is not None and not callable(validator):
        raise TypeError("validator must be callable or None")

    if validator is not None and not validator(ticker):
        raise ValueError("Invalid ticker")

    raw = provider(ticker, interval)
    data = list(raw) if raw is not None else []
    if not data:
        raise ValueError("No price data returned by provider")

    required = ("ticker", "ts", "open", "high", "low", "close", "volume", "source")
    for row in data:
        for key in required:
            if key not in row:
                raise KeyError("Missing required key in price bar: " + key)

    # Sort by timestamp (assumes provider returns comparable 'ts' values, e.g., ISO8601 strings)
    data.sort(key=lambda r: r["ts"])

    if isinstance(limit, int) and limit > 0:
        data = data[-limit:]

    return data

