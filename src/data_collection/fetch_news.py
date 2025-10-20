def fetch_news(ticker, providers, cleaner=None, limit=None):
    """Fetch and normalize news items for a ticker from one or more providers (no imports).

    This function does not import any modules. It expects:
      - `providers`: a list (or tuple) of callables. Each provider must accept `(ticker,)`
        and return an iterable of dicts with keys:
          {
            "id": <str>,
            "ticker": <str or None>,
            "published_at": <ISO8601 string or sortable timestamp>,
            "source": <str>,        # e.g., feed URL or domain
            "title": <str>,
            "url": <str>,
            "summary": <str or None>  # optional
          }
      - `cleaner`: optional callable(text) -> str to create `cleaned_text`

    The function will:
      - collect from all providers,
      - attach/override 'ticker' with the input ticker if missing,
      - build 'cleaned_text' using `cleaner(title + " " + summary)` when available,
      - sort by 'published_at' ascending, and
      - optionally apply a tail `limit`.

    Args:
        ticker (str): Stock symbol these articles relate to.
        providers (list | tuple): Provider callables returning iterable news dicts.
        cleaner (callable | None): Optional function to clean headline/summary text.
        limit (int | None): Optional max number of news items after sorting.

    Returns:
        list: List of normalized news item dicts sorted by ascending 'published_at'.

    Raises:
        TypeError: If inputs have incorrect types.
        ValueError: If providers yield no news.
        KeyError: If a required key is missing in a returned item.

    Examples:
        >>> def p1(t):
        ...     return [{
        ...         "id": "n1", "ticker": t, "published_at": "2025-10-19T12:00:00Z",
        ...         "source": "example.com", "title": "Apple rises", "url": "https://example.com/a1", "summary": "Shares up on strong demand."
        ...     }]
        >>> def p2(t):
        ...     return [{
        ...         "id": "n2", "ticker": None, "published_at": "2025-10-19T13:00:00Z",
        ...         "source": "rss.example.org", "title": "AAPL headlines", "url": "https://rss.example.org/a2", "summary": ""
        ...     }]
        >>> def cleaner(txt): return " ".join([w for w in (txt or "").lower().split() if w not in {"the","a","an","and","of","to","is","in"}])
        >>> items = fetch_news("AAPL", [p1, p2], cleaner=cleaner)
        >>> [i["id"] for i in items]
        ['n1', 'n2']
        >>> items[-1]["cleaned_text"]
        'aapl headlines'
    """
    if not isinstance(ticker, str):
        raise TypeError("ticker must be a string")
    if not isinstance(providers, (list, tuple)) or not all(callable(p) for p in providers):
        raise TypeError("providers must be a list/tuple of callables")
    if limit is not None and not isinstance(limit, int):
        raise TypeError("limit must be an int or None")
    if cleaner is not None and not callable(cleaner):
        raise TypeError("cleaner must be callable or None")

    collected = []
    for prov in providers:
        batch = prov(ticker)
        if batch:
            for item in batch:
                # Validate required keys
                if "id" not in item:
                    raise KeyError("Missing required key in news item: id")
                if "published_at" not in item:
                    raise KeyError("Missing required key in news item: published_at")
                if "source" not in item:
                    raise KeyError("Missing required key in news item: source")
                if "title" not in item:
                    raise KeyError("Missing required key in news item: title")
                if "url" not in item:
                    raise KeyError("Missing required key in news item: url")

                # Normalize ticker
                if "ticker" not in item or item["ticker"] is None:
                    item["ticker"] = ticker

                # Build cleaned_text
                if cleaner is not None:
                    title = item.get("title", "") or ""
                    summary = item.get("summary", "") or ""
                    item["cleaned_text"] = cleaner((title + " " + summary).strip())

                collected.append(item)

    if not collected:
        raise ValueError("No news data returned by providers")

    # Sort by time in ascending order
    collected.sort(key=lambda r: r["published_at"])

    if isinstance(limit, int) and limit > 0:
        collected = collected[-limit:]

    return collected
