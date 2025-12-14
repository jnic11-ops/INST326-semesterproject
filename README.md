# Stock Market Data & News Analysis System — Project 4  
**INST326: Object-Oriented Programming for Information Science**  
Capstone Integration, Persistence, and Testing

---

## Team Information
**Team Members & Contributions**
- **Matthew Daniel** — Lead Developer; system integration, GUI development, persistence implementation, documentation, testing coordination
- **Jacob Nicholson** — Testing and validation
- **Matthew Daniel & Jacob Nicholson** — Data analysis and portfolio logic

---

## Project Overview
This project is a complete, functional financial information system that retrieves, analyzes, visualizes, and persists stock market and financial news data. It integrates all major components developed throughout the semester into a cohesive, end-to-end application.

The system answers real-world financial information questions by combining:
- Historical stock price analysis
- Technical indicators and anomaly detection
- Financial news sentiment analysis
- Portfolio tracking from user-provided data
- Interactive visualizations
- Persistent data storage and exportable reports

This Project 4 submission represents a **capstone artifact**, demonstrating system completeness, data persistence, testing strategy, and professional software development practices.

When running app.py may need to run in VSCode or in your computers terminal
---

## Key Features

### 1. Stock Time Series & Indicators
- Historical stock price retrieval
- Simple Moving Average (SMA-20)
- Relative Strength Index (RSI-14)
- Anomaly detection
- Input validation with minimum date range enforcement
- Automatic handling of weekends and future dates

### 2. News Sentiment Analysis
- RSS-based financial news retrieval
- Sentiment classification (positive, neutral, negative)
- Keyword frequency extraction
- Display of article metadata and sources

### 3. Portfolio Dashboard
- Load portfolio data from CSV files
- Dynamic portfolio updates at runtime
- Total portfolio value calculation
- Position-level valuation and portfolio weighting

### 4. Interactive Stock Chart Visualization
- Price and indicator overlays
- Hover tooltips for prices and indicators
- Zoom, pan, and reset controls
- Adaptive x-axis formatting based on date range
- Visual anomaly markers

### 5. Data Import & Export
- Import CSV files for portfolio tracking
- Preview imported CSV data
- Export analysis results to JSON
- Graceful handling of invalid or unreadable files

### 6. Data Persistence
- Application state saved on exit
- Previous analysis restored on restart
- Safe handling of missing or corrupted state files

---

## System Architecture
The system follows a modular, layered architecture to ensure separation of concerns and maintainability.

### User Interface Layer (View)
- Implemented in `api/app.py`
- Built using Tkinter
- Handles user input, navigation, and visualization
- Each major feature is implemented as a dedicated page

### Controller Layer
- Implemented in `system/system_controller.py`
- Coordinates all workflows
- Manages persistence, imports, and exports
- Decouples UI logic from core system logic

### Core Logic & Data Layer
Located in `src/classes/`, including:
- `StockDataManager`
- `StockAnalyzer`
- `NewsAnalyzer`
- `PortfolioManager`
- `DataProcessor`
- `UserQueryBuilder`

This separation of concerns improves extensibility, testability, and long-term maintainability.

---

## Object-Oriented Design
This system builds on object-oriented principles developed in earlier projects, including inheritance, composition, encapsulation, and separation of concerns.

Core components such as data managers, analyzers, and processors are encapsulated into dedicated classes with clearly defined responsibilities. Composition is used to coordinate these components within the `SystemController`, allowing flexible integration without tight coupling.

This design enables the system to evolve without requiring major changes to existing UI or business logic.

---

## Data Persistence & File Locations

The application persists data and outputs files in the following locations:

- **`data/app_state.json`**  
  Stores the most recent analysis payload and restores it on application restart.

- **`data/analysis_reports/`**  
  Contains exported JSON analysis reports generated via Option 6.

- **Portfolio CSV files**  
  The default portfolio file is `ex_portfolio.csv`.  
  Users may import additional CSV files at runtime via Option 5, dynamically updating
  the active portfolio used in Option 3.

---

## Portfolio CSV Format
Portfolio CSV files must contain the following columns:

- `ticker` — stock symbol (e.g., AAPL, MSFT)
- `shares` — number of shares held

Example:
```csv
ticker,shares
AAPL,10
MSFT,5
NVDA,3

```
---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/jnic11-ops/INST326-semesterproject.git

# Enter project directory
cd INST326-semesterproject

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

```
### **Required Python Function Libraries**
* pandas
* yfinance
* feedparser
* requests
* matplotlib
* pytest (Install this specifically to run unit and integration tests)

---

## **Running the Application**
```python
python api/app.py
```
Use the main menu to access:
1. Stock Time Series + Indicators
2. News Sentiment Analysis
3. Portfolio Dashboard
4. Plot Stock Chart
5. Import CSV
6. Export Last Analysis

---

## **Testing**
Testing was conducted through comprehensive and structured manual and functional testing
to verify correct behavior across all workflows, including:
* Input validation and error handling
* Data retrieval and analysis
* Import and export functionality
* Persistence across application restarts
* End-to-end user workflows
Automated unit and integration tests are limited; testing for this project was primarily conducted through manual and functional validation.
Detailed testing strategy, coverage, and results are documented in ```testing.md. ```

---

## **Documentation**
* ```README.md ``` — Project overview, setup, and usage
* ```architecture.md ```— System design and architectural decisions
* ```testing.md``` — Testing strategy and results

---

## **Known Limitations**
* News relevance filtering is keyword-based and may include unrelated articles
* External APIs depend on network availability and data freshness
* Automated unit tests are limited

---

## ** Future Enhancements**
* Automated unit and integration testing
* Advanced sentiment visualization
* Portfolio performance charts
* Improved news relevance filtering

## AI Collaboration & Usage Disclosure

AI-assisted tools were used during development to support system integration,
debugging, and documentation refinement. AI assistance helped with:

- Debugging complex integration issues across GUI, controller, and data layers
- Suggesting patterns for file I/O, persistence, and error handling
- Improving clarity and structure of documentation
- Assisting with test planning and edge-case identification

All AI-generated suggestions were **reviewed, understood, tested, and adapted**
by the development team. No AI-generated code was used without human validation,
and all final implementation decisions were made by the team.

AI was **not** used to bypass learning objectives or submit unverified solutions.
Team members take full responsibility for the correctness, behavior, and design
of the final system.

AI collaboration was documented separately in individual AI journals in
accordance with course guidelines.




