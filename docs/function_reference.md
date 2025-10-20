# Function Reference
This document provides an overview of all the simple utility, data collection, interface, analysis, and reporting functions in our project. Each record inputted into this document contains the function name, description, parameters, ValueErrors and return values.


---
## validate_ticker(ticker: str) -> bool:

**Description:**
Validates a stock ticker symbol to ensure it follows the proper format for financial markets.

**Rules for a valid ticker:**
- Must be between **1 and 7 characters long**
- Can contain **uppercase letters, numbers, dots (.)**, or **dashes (-)**
- Must **not include spaces or other special characters**

**Examples of valid tickers:**
- `AAPL`, `TSLA`, `BRK.A`, `RDS-B`, `GOOG`, `MSFT`

**Examples of invalid tickers:**
- `goog` → lowercase not allowed  
- `BRK/A` → slashes not allowed  
- `APPLE!` → special character not allowed  
- `TOOLONGNAME` → too long (over 7 chars)

**Parameters:**
- `ticker` (*str*): The stock ticker symbol (e.g., `"AAPL"`, `"TSLA"`).

**Returns:**
- `bool`: `True` if valid, otherwise `False`.

**Example Usage:**
```python
>>> validate_ticker("AAPL")
True

>>> validate_ticker("goog")
False



---

## normalize_date(date_str: str) -> datetime

**Description:**
Converts a date string in various formats (ISO, US, or EU) into a standardized Python `datetime` object.  
Supports flexible formats and optional timestamps.

**Supported Formats:**
- ISO: `'2025-10-09'`
- US: `'10/09/2025'` or `'10-09-2025'`
- EU: `'09/10/2025'` or `'09-10-2025'`
- With time: `'2025-10-09 14:30:00'`

**Parameters:**
- `date_str` (*str*): Input date string to convert.

**Returns:**
- `datetime`: A standardized `datetime` object representing the parsed date.

**Raises:**
- `ValueError`: If the date format is unrecognized or input is not a string.

**Example Usage:**
```python
>>> normalize_date("2025-10-09")
datetime.datetime(2025, 10, 9, 0, 0)

>>> normalize_date("09/10/2025")
datetime.datetime(2025, 10, 9, 0, 0)

>>> normalize_date("2025-10-09 14:30:00")
datetime.datetime(2025, 10, 9, 14, 30)



---

## 🔹 clean_text(text: str) -> str

**Description:**  
Cleans and normalizes text for natural language processing (NLP) preprocessing.  
This function removes HTML tags, punctuation, stopwords, converts text to lowercase,  
and removes extra whitespace to produce clean, tokenized text suitable for analysis.

**Parameters:**
- `text` (*str*): Input text (e.g., news article, summary).

**Returns:**
- `str`: Cleaned and normalized text.

**Processing Steps:**
1. Remove HTML tags (e.g., `<p>`, `<br>`).  
2. Convert all text to lowercase.  
3. Remove punctuation symbols.  
4. Remove common English stopwords.  
5. Remove extra spaces and rejoin tokens.

**Example:**
```python
>>> clean_text("<p>This is a Sample text, with HTML tags!</p>")
'sample text html tags'


---

## format_currency(value: float) -> str

**Description:**  
Formats a numeric value (int or float) into a human-readable U.S. currency string.  
It adds commas for thousands separators, two decimal places, and a `$` sign.  
Handles both positive and negative values gracefully.

**Parameters:**
- `value` (*float*): Numeric value to format as currency.

**Returns:**
- `str`: Formatted currency string with symbol (`$`) and two decimal places.

**Error Handling:**
- Returns `"Invalid value"` if input is not a number.

**Example:**
```python
>>> format_currency(1234.56)
'$1,234.56'

>>> format_currency(1000000)
'$1,000,000.00'

>>> format_currency(-52.9)
'-$52.90'

>>> format_currency("abc")
'Invalid value'







---

## parse_portfolio_csv(file_path: str) -> dict

**Description:**  
Parses a user's portfolio CSV file and normalizes its schema into a standardized dictionary.  
Validates numeric values and ensures required columns exist (`ticker`, `shares`, `buy_price`).

**Expected CSV Format:** 

---
## fetch_stock_data — Retrieve Historical Stock Prices

Example showing how to download Apple (AAPL) stock data from Yahoo Finance between two dates.

```python
from src.data_collection.fetch_stock_data import fetch_stock_data

# Fetch data including adjusted close prices
df1 = fetch_stock_data("yahoo", "AAPL", "2024-01-01", "2024-05-01", use_adjusted=True)
print("With Adjusted Close:")
print(df1.head())

# Fetch data without adjusted close
df2 = fetch_stock_data("yahoo", "AAPL", "2024-01-01", "2024-05-01", use_adjusted=False)
print("\nWithout Adjusted Close:")
print(df2.head())





---

### 🧩 build_user_query(params: dict) -> dict

**Description:**  
Interprets user-provided parameters (from a web UI, CLI, or config file) and converts them into a structured query dictionary that can be used by backend data retrieval or analysis functions.

**Parameters:**
| Name | Type | Description |
|------|------|--------------|
| `params` | `dict` | User input parameters, including optional filters such as `ticker`, `sector`, `sentiment`, and `limit`. |

**Returns:**  
`dict` – A structured query containing filters, query type, and a result limit.

**Example Input:**
```python
{
    "ticker": "AAPL",
    "sector": "Technology",
    "sentiment": "positive",
    "limit": 25
}







