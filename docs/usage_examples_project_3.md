This document demonstrates how to use the Stock Market Data & News Analysis System with examples highlighting inheritance, polymorphism, and composition.

#### **1. Data Processors (Polymorphism)**

All processors inherit from BaseProcessor and implement process() differently.
```python
from processors_base_classes_subclasses.text_processor import TextProcessor
from processors_base_classes_subclasses.date_processor import DateProcessor
from processors_base_classes_subclasses.currency_processor import CurrencyProcessor

# Create processor instances
processors = [
    TextProcessor(),
    DateProcessor(),
    CurrencyProcessor()
]

# Sample inputs
samples = [
    "<p>Hello World!</p>",  # For TextProcessor
    "2025-11-23",           # For DateProcessor
    1234.56                  # For CurrencyProcessor
]

# Polymorphic processing
for p, sample in zip(processors, samples):
    result = p.process(sample)
    print(f"{p.__class__.__name__} -> {result}")

```
Output Example:
```python
TextProcessor -> hello world
DateProcessor -> 2025-11-23 00:00:00
CurrencyProcessor -> $1,234.56
```
Polymorphism: same process() call, different behavior depending on subclass.

#### **2. Analyzers (Polymorphism)**

Both NewsAnalyzer and StockAnalyzer inherit from BaseAnalyzer. They implement analyze() differently.
```python
from analyzers_base_classes_subclasses.news_analyzer import NewsAnalyzer
from analyzers_base_classes_subclasses.stock_analyzer import StockAnalyzer

class DummyDataManager:
    def fetch_data(self, query): return {}
    def process_data(self, data): return {}

data_manager = DummyDataManager()

analyzers = [
    NewsAnalyzer(data_manager),
    StockAnalyzer("AAPL", data_manager)
]

# Polymorphic analysis
for analyzer in analyzers:
    result = analyzer.analyze()
    print(f"{analyzer.__class__.__name__} -> {result}")
```

Output Example:
```python
NewsAnalyzer -> {'sentiment': 'positive', 'keywords': ['stock', 'market']}
StockAnalyzer -> {'trend': 'up', 'volatility': 0.02}
```
Polymorphism: same analyze() interface, different implementations.

#### **3. Query Builders (Polymorphism)**

All query builders inherit from BaseQueryBuilder and implement build_query().
```python
from query_builders_base_classes_subclasses.dashboard_query_builder import DashboardQueryBuilder
from query_builders_base_classes_subclasses.user_query_builder import UserQueryBuilder

builders = [
    DashboardQueryBuilder(),
    UserQueryBuilder()
]

ticker = "AAPL"
for builder in builders:
    query = builder.build_query({"ticker": ticker})
    print(f"{builder.__class__.__name__} -> {query}")
```

Output Example:
```python
DashboardQueryBuilder -> {'ticker': 'AAPL', 'start_date': '2024-01-01', 'end_date': '2024-12-31', 'summary': True}
UserQueryBuilder -> {'ticker': 'AAPL', 'filters': None, 'include_history': False}
```
Polymorphism: same build_query() method, different subclass behaviors.

#### **4. PortfolioManager (Composition)**

PortfolioManager contains instances of StockDataManager and optionally other processors or analyzers.
```python
from portfolio_manager import PortfolioManager
from data_managers_base_classes_subclasses.stock_data_manager import StockDataManager

# Initialize manager with a portfolio file and composed data manager
pm = PortfolioManager("portfolio.csv", stock_manager=StockDataManager())

# Compute total value using the composed StockDataManager
total_value = pm.compute_total_value("2025-01-01", "2025-11-01")
print(f"Total Portfolio Value: ${total_value:,.2f}")
```
Composition: PortfolioManager "has-a" StockDataManager instead of inheriting.

#### **5. Combined Example (Polymorphic Workflow)**
```python
# Demonstrate polymorphic analysis on a portfolio
portfolio_analyzers = [
    NewsAnalyzer(data_manager),
    StockAnalyzer("GOOG", data_manager)
]

for a in portfolio_analyzers:
    summary = a.analyze()
    print(f"{a.__class__.__name__} Summary -> {summary}")
```

This shows uniform handling of multiple object types, demonstrating polymorphism in a real workflow.