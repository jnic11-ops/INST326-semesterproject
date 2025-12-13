# System Architecture & Design

## Overview
This project follows a modular, layered architecture that separates the
graphical user interface (GUI), system coordination logic, and core data
processing components. This design improves maintainability, readability,
and extensibility.

The application is structured around a central controller that coordinates
all system components while keeping UI code independent from data logic.

---

## High-Level Architecture

The system consists of three main layers:

### 1. User Interface Layer (View)
- Implemented in `api/app.py`
- Built using Tkinter
- Responsible for:
  - Collecting user input
  - Displaying results
  - Rendering charts and visualizations
  - Navigating between application pages

Each major feature is implemented as a separate page class:
- `Page1_Stock` – Stock time series and indicators
- `Page2_News` – News sentiment and keyword analysis
- `Page3_Portfolio` – Portfolio dashboard
- `Page4_Plot` – Interactive stock chart
- `PageCSV_Import` – CSV import and preview
- `PageExport` – Export analysis to JSON

---

### 2. Controller Layer
- Implemented in `system/system_controller.py`
- Acts as the central coordinator for the application
- Responsibilities:
  - Orchestrating data retrieval and analysis
  - Managing application state persistence
  - Handling file imports and exports
  - Connecting UI requests to backend logic

The `SystemController` prevents tight coupling between the UI and core logic.

---

### 3. Core Logic & Data Layer
Located in `src/classes/`, including:

- `StockDataManager` – Fetches historical stock data
- `StockAnalyzer` – Computes indicators (SMA, RSI) and detects anomalies
- `NewsAnalyzer` – Fetches RSS feeds, analyzes sentiment, extracts keywords
- `PortfolioManager` – Calculates portfolio value and weights
- `DataProcessor` – Cleans text, formats currency, normalizes dates
- `UserQueryBuilder` – Formats data payloads for charts and dashboards

---

## Data Flow
1. User enters input in the GUI
2. UI sends request to `SystemController`
3. Controller calls appropriate manager/analyzer
4. Results are processed and returned to the UI
5. UI displays results or visualizations

---

## Design Decisions & Rationale

- **Separation of concerns**: Keeps UI logic separate from data processing
- **Central controller**: Simplifies integration and coordination
- **Modular page design**: Makes features easier to test and extend
- **Dynamic CSV handling**: Allows portfolio file updates at runtime
- **Defensive error handling**: Prevents crashes and improves UX

---

## Known Limitations
- News relevance filtering is keyword-based and may include unrelated articles
- No automated unit tests (manual testing used)
- External APIs depend on network availability and data freshness

---

## Future Enhancements
- Automated unit testing
- More advanced sentiment visualization
- Portfolio performance charts
- Improved news relevance filtering
