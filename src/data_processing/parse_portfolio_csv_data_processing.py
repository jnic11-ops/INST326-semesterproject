import csv
import os

def parse_portfolio_csv(file_path: str) -> dict:
    """
    Parse a user's portfolio CSV file and normalize its schema.

    Expected CSV format:
        ticker,shares,buy_price
    Example:
        AAPL,10,150.5
        MSFT,5,310
        TSLA,2,700
    
    Args:
        file_path (str): Path to the CSV file containing user holdings.

    Returns:
        dict: Normalized portfolio data, e.g.
            {
                "AAPL": {"shares": 10, "buy_price": 150.5},
                "MSFT": {"shares": 5, "buy_price" : 310.0}
            
            
            }
    
    """

    # Validate file existence
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return {}

    portfolio = {}

    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Ensure required columns exist
        required_columns = {"ticker", "shares", "buy_price"}
        if not required_columns.issubset(reader.fieldnames):
            print(f"Error: Missing columns in CSV. Required: {required_columns}")
            return {}

        for row in reader:
            ticker = row["ticker"].strip().upper()
            try:
                shares = float(row["shares"])
                buy_price = float(row["buy_price"])
            except ValueError:
                print(f"Skipping invalid row: {row}")
                continue  # Skip rows with invalid data

            # Normalize schema
            portfolio[ticker] = {
                "shares": shares,
                "buy_price": buy_price
            }

    return portfolio

