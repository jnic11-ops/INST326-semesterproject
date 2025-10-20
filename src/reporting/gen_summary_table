def generate_summary_table(portfolio_data):
    """Generate a summary table of portfolio performance statistics.

    Args:
        portfolio_data (list[dict]): A list of stock data entries. Each entry should contain:
            - 'ticker' (str): Stock symbol.
            - 'avg_sentiment' (float): Average sentiment score.
            - 'price_change' (float): Percentage price change.
            - 'volume' (int): Trading volume.

    Returns:
        list[dict]: A summarized list of stocks sorted by performance, 
                    each with 'ticker', 'score', and 'category'.

    Raises:
        TypeError: If portfolio_data is not a list of dictionaries.
        KeyError: If required keys are missing in any record.

    Examples:
        >>> portfolio = [
        ...     {"ticker": "AAPL", "avg_sentiment": 0.8, "price_change": 2.3, "volume": 1200000},
        ...     {"ticker": "MSFT", "avg_sentiment": 0.5, "price_change": -0.4, "volume": 950000},
        ... ]
        >>> generate_summary_table(portfolio)
        [{'ticker': 'AAPL', 'score': 2.6, 'category': 'Strong Positive'},
         {'ticker': 'MSFT', 'score': 0.1, 'category': 'Neutral'}]
    """
    if not isinstance(portfolio_data, list) or not all(isinstance(d, dict) for d in portfolio_data):
        raise TypeError("portfolio_data must be a list of dictionaries")

    summary = []
    for stock in portfolio_data:
        try:
            score = round(stock["avg_sentiment"] + (stock["price_change"] / 100), 2)
            category = (
                "Strong Positive" if score > 0.5 else
                "Neutral" if -0.5 <= score <= 0.5 else
                "Negative"
            )
            summary.append({
                "ticker": stock["ticker"],
                "score": score,
                "category": category
            })
        except KeyError as e:
            raise KeyError(f"Missing required key in portfolio data: {e.args[0]}")

    return sorted(summary, key=lambda x: x["score"], reverse=True)
