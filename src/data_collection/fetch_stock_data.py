import pandas as pd
import datetime as dt

try:
    import yfinance as yf
except ImportError:
    raise ImportError("Please install yfinance: pip install yfinance")


def fetch_stock_data(api: str, ticker: str, start: str, end: str, use_adjusted: bool = True) -> pd.DataFrame:
    """
    Fetch stock price data from Yahoo Finance and return
    a normalized DataFrame with OHLCV (Open, High, Low, Close, Volume)
    — optionally including Adjusted Close prices.

    Args:
        api (str): The API source ('yahoo' supported currently)
        ticker (str): Stock ticker symbol (e.g., 'AAPL')
        start (str): Start date in 'YYYY-MM-DD' format
        end (str): End date in 'YYYY-MM-DD' format
        use_adjusted (bool): Whether to include adjusted close prices (default: True)

    Returns:
        pd.DataFrame: DataFrame with columns:
            ['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume'] (if use_adjusted=True)
            or
            ['Date', 'Open', 'High', 'Low', 'Close', 'Volume'] (if use_adjusted=False)
    """

    if api.lower() != "yahoo":
        raise ValueError("Currently, only 'yahoo' API is supported.")

    # Convert string dates to datetime objects
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in 'YYYY-MM-DD' format.")

    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=not use_adjusted)

    if data.empty:
        print(f"No data found for {ticker} between {start} and {end}.")
        return pd.DataFrame()

    # Reset index for readability
    data.reset_index(inplace=True)

    # Handle Adjusted Close depending on user preference
    if use_adjusted and "Adj Close" in data.columns:
        data.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)
        data = data[["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]]
    else:
        data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

    return data


if __name__ == "__main__":
    # Example: Fetch data including adjusted close
    df1 = fetch_stock_data("yahoo", "AAPL", "2024-01-01", "2024-05-01", use_adjusted=True)
    print("\nWith Adjusted Close:")
    print(df1.head())

    # Example: Fetch data without adjusted close
    df2 = fetch_stock_data("yahoo", "AAPL", "2024-01-01", "2024-05-01", use_adjusted=False)
    print("\nWithout Adjusted Close:")
    print(df2.head())


