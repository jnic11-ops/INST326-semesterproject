# Stock Market Data & News Analysis System — Project 3

INST326: Object-Oriented Programming for Information Science
Advanced OOP with Inheritance & Polymorphism


### **Project Overview**
This system is a comprehensive financial data and news analysis platform demonstrating advanced object-oriented programming principles, including:
* Inheritance hierarchies with abstract base classes
* Polymorphic behavior across analyzers, processors, and query builders
* Composition relationships in portfolio management
* Scalable and modular architecture for extensibility

The platform collects and analyzes:
* Real-time & historical stock market data
* Financial news sentiment and topics
* Portfolio tracking from user-uploaded data
* Trend detection and anomaly detection
* Exportable reports (PDF, CSV, JSON)
* Keyword frequency for visualizations (e.g., word clouds)

### **System Architecture**

#### **Inheritance Hierachies**

Data Processors
```python
BaseDataManager (ABC)
├── StockDataManager
├── NewsDataManager
└── PortfolioDataManager
```
* Rationale: Enforces a fetch_data() interface; allows interchangeable data managers.

Query Builders
```python
BaseQueryBuilder (ABC)
├── UserQueryBuilder
└── DashboardQueryBuilder
```
* Rationale: Abstract build_query() method ensures all query builders have consistent behavior.

#### **Composition Relationships**
PortfolioManager
* Has-a StockDataManager
* Has-a NewsAnalyzer
* Has-a BaseProcessor subclasses (optional)

Explanation: PortfolioManager coordinates multiple objects rather than inheriting from them, following the single responsibility principle.

### **Key Features**

#### ** 1. Polymorphic Behavior**

Same method calls produce different results based on object type:

* analyze() → NewsAnalyzer vs. StockAnalyzer
* process() → TextProcessor vs. DateProcessor vs. CurrencyProcessor
* build_query() → DashboardQueryBuilder vs. UserQueryBuilder

Example: Analyzer Polymorphism
```python
from analyzers_base_classes_subclasses import NewsAnalyzer, StockAnalyzer

analyzers = [NewsAnalyzer(data_manager), StockAnalyzer("AAPL", data_manager)]
for a in analyzers:
    print(f"{a.__class__.__name__} -> {a.analyze()}")
```

#### ** 2. Abstract Base Classes**

Enforce consistent interfaces:
* BaseProcessor → process(data)
* BaseAnalyzer → analyze()
* BaseDataManager → fetch_data(query)
* BaseQueryBuilder → build_query(params)

Cannot instantiate abstract classes directly.

#### ** 3. Composition**

PortfolioManager demonstrates composition:
```python
from portfolio_data_manager import PortfolioDataManager
from stock_data_manager import StockDataManager

pm = PortfolioManager("portfolio.csv", stock_manager=StockDataManager())
total_value = pm.compute_total_value("2025-01-01", "2025-11-01")
print(f"Total portfolio value: ${total_value:,.2f}")
```
* Rationale: PortfolioManager contains managers and analyzers instead of inheriting, keeping concerns separated.

### **Installation & Setup**
``` python
# Clone the repository
git clone https://github.com/jnic11-ops/INST326-semesterproject

# Enter project directory
cd INST326-semesterproject

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```
* Python 3.7+ required
* Dependencies: pandas, yfinance, requests

### **Running the system**
```python
# Run full demo
python demo.py
```
* Demonstrates inheritance hierarchies, polymorphic behavior, abstract base class enforcement, and composition relationships.

### **Running Tests**
```python
# Run all tests
python -m unittest test_system -v
```
* Tests cover inheritance, polymorphism, ABC enforcement, composition, and integration workflows.

### **Usage Examples**
#### **1. Data Processors (Polymorphism) **
```python
from processors_base_classes_subclasses.text_processor import TextProcessor
from processors_base_classes_subclasses.date_processor import DateProcessor
from processors_base_classes_subclasses.currency_processor import CurrencyProcessor

# Polymorphic usage: same method call on different subclasses
processors = [
    TextProcessor(),
    DateProcessor(),
    CurrencyProcessor()
]

samples = [
    "<p>Hello World!</p>",  # Text
    "2025-11-23",           # Date
    1234.56                 # Currency
]

for processor, value in zip(processors, samples):
    print(f"{processor.__class__.__name__} -> {processor.process(value)}")
```
#### **Expected Output:**
```python
TextProcessor -> hello world
DateProcessor -> 2025-11-23 00:00:00
CurrencyProcessor -> $1,234.56
```
Explanation: The process() method is polymorphic: same interface, different behavior per subclass.


#### **2. Analyzers (Polymorphism)**
```python
from analyzers_base_classes_subclasses.news_analyzer import NewsAnalyzer
from analyzers_base_classes_subclasses.stock_analyzer import StockAnalyzer

# Dummy data manager for demonstration
class DummyDataManager:
    def fetch_data(self, query): return {}
    def process_data(self, data): return {}

data_manager = DummyDataManager()

analyzers = [
    NewsAnalyzer(data_manager),
    StockAnalyzer("AAPL", data_manager)
]

for analyzer in analyzers:
    print(f"{analyzer.__class__.__name__} -> {analyzer.analyze()}")
```
Explanation: 
analyze() behaves differently depending on whether it's a NewsAnalyzer or StockAnalyzer, demonstrating polymorphism in the analyzer hierarchy.


#### **3. Query Builders (Polymorphism)**
```python
from query_builders_base_classes_subclasses.dashboard_query_builder import DashboardQueryBuilder
from query_builders_base_classes_subclasses.user_query_builder import UserQueryBuilder

builders = [
    DashboardQueryBuilder(),
    UserQueryBuilder()
]

for builder in builders:
    query = builder.build_query({"ticker": "AAPL"})
    print(f"{builder.__class__.__name__} -> {query}")
```
Explanation: 
Both query builders implement build_query() differently but share the same interface, allowing interchangeable use.

#### **4. Portfolio Manager (Composition)**
```python
from portfolio_manager import PortfolioManager
from data_managers_base_classes_subclasses.stock_data_manager import StockDataManager

# PortfolioManager uses composition: contains StockDataManager and coordinates fetching and calculations
pm = PortfolioManager("portfolio.csv", stock_manager=StockDataManager())
total_value = pm.compute_total_value("2025-01-01", "2025-11-01")
print(f"Total portfolio value: ${total_value:,.2f}")
```
Explanation:
PortfolioManager delegates data fetching and computations to its composed objects rather than inheriting from them, demonstrating proper composition.

### **File Structure**
```python
project/
├── base_classes/
│   ├── base_processor.py
│   ├── base_analyzer.py
│   ├── base_data_manager.py
│   └── base_query_builder.py
├── processors_base_classes_subclasses/
├── analyzers_base_classes_subclasses/
├── data_managers_base_classes_subclasses/
├── query_builders_base_classes_subclasses/
├── portfolio_manager.py
├── demo.py
├── test_system.py
└── README.md
```

### **Design Decisions**
#### **Why Inheritance?**
* Clear is-a relationships (e.g., TextProcessor is-a BaseProcessor)
* Code reuse via shared attributes and methods
* Polymorphic method calls across multiple object types

#### **Why Composition?**
* PortfolioManager coordinates multiple objects without inheriting
* Allows flexible relationships, scalable system design
* Maintains single responsibility principle





