# Class Design Documentation

This document outlines the **object-oriented design** of the *Information Retrieval and Analysis System for Stock Data*.  
Each class integrates core functions, follows encapsulation and validation principles, and is structured for scalability through inheritance.

---

## **1. StockDataManager**

**Purpose:**  
Manages the retrieval and validation of stock market data and related financial news from supported APIs (e.g., Yahoo Finance, NewsAPI).  
Ensures ticker validation, normalized outputs, and unified error handling for external data sources.

**Integrated Functions:**  
- `fetch_stock_data`  
- `fetch_news`  
- `validate_ticker`

**Design Decisions:**  
All market-related retrieval logic is centralized within this class to maintain a single, cohesive data interface.  
This structure promotes modularity and allows consistent validation and preprocessing before data is passed to analysis or visualization components.  
Encapsulation ensures each data source can be extended or swapped without breaking dependencies.

**Future Inheritance Potential:**  
- `CryptoDataManager` – to handle cryptocurrency and blockchain market data.  
- `MockStockDataManager` – to simulate market responses for testing.  
- `ExtendedMarketDataManager` – to integrate ETF or macroeconomic indicators.

---

## **2. DataProcessor**

**Purpose:**  
Processes and normalizes data for consistency across modules, enabling reliable analytics and reporting.  
Handles all text, date, and numerical transformations.

**Integrated Functions:**  
- `normalize_date`  
- `clean_text`  
- `format_currency`

**Design Decisions:**  
Encapsulating all preprocessing functions within this class ensures clean separation between raw data retrieval and analytical computation.  
It streamlines data cleaning operations for reproducibility and prevents redundancy across modules.

**Future Inheritance Potential:**  
- `FinancialDataProcessor` – to calculate ratios, moving averages, and derived metrics.  
- `TextDataProcessor` – to extend text cleaning into NLP-based sentiment extraction.

---

## **3. PortfolioManager**

**Purpose:**  
Handles user portfolio data by parsing, validating, and structuring holdings information from CSV files.  
Provides easy access to normalized data for tracking, analytics, or visualization.

**Integrated Functions:**  
- `parse_portfolio_csv`

**Design Decisions:**  
This class isolates portfolio management responsibilities, ensuring proper schema handling and consistent error reporting.  
By decoupling this logic, portfolio data can be reused across analytical, reporting, or UI modules without code duplication.

**Future Inheritance Potential:**  
- `AdvancedPortfolioManager` – adds brokerage integration and real-time updates.  
- `SimulatedPortfolioManager` – enables educational or backtesting portfolio simulations.

---

## **4. UserQueryBuilder**

**Purpose:**  
Interprets user input from the interface (e.g., ticker, date range, sentiment filter) and converts it into structured, machine-readable queries for APIs or databases.

**Integrated Functions:**  
- `build_user_query`

**Design Decisions:**  
Centralizes user interaction and parameter translation logic.  
This abstraction ensures flexibility — the same query system can serve multiple frontends or APIs without rewriting logic.

**Future Inheritance Potential:**  
- `AdvancedQueryBuilder` – integrates natural language interpretation for human-friendly input.  
- `DatabaseQueryBuilder` – generates structured SQL/NoSQL queries for backend systems.

---

### Summary

| **Class**            | **Purpose**                                  | **Integrated Functions**                                | **Inheritance Potential**                     |
|----------------------|----------------------------------------------|--------------------------------------------------------|-----------------------------------------------|
| `StockDataManager`   | Retrieve and validate market data/news       | `fetch_stock_data`, `fetch_news`, `validate_ticker`    | `CryptoDataManager`, `MockStockDataManager`   |
| `DataProcessor`      | Clean and normalize textual/numerical data   | `normalize_date`, `clean_text`, `format_currency`      | `FinancialDataProcessor`, `TextDataProcessor` |
| `PortfolioManager`   | Manage and parse portfolio files             | `parse_portfolio_csv`                                  | `AdvancedPortfolioManager`                    |
| `UserQueryBuilder`   | Translate UI filters into structured queries | `build_user_query`                                     | `AdvancedQueryBuilder`, `DatabaseQueryBuilder` |

---

### Design Principles Summary

- **Encapsulation:** Each class manages a single responsibility.  
- **Validation:** Input and data type checks prevent runtime errors.  
- **Extensibility:** Clear inheritance paths for future expansion.  
- **Modularity:** Promotes reusability across the project’s analytical pipeline.  
- **Documentation:** Comprehensive docstrings ensure readability and maintainability.

---


