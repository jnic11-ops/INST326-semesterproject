# polymorphism_demo.py

from analyzers_base_classes_subclasses.news_analyzer import NewsAnalyzer
from analyzers_base_classes_subclasses.stock_analyzer import StockAnalyzer

from query_builders_base_classes_subclasses.dashboard_query_builder import DashboardQueryBuilder
from query_builders_base_classes_subclasses.user_query_builder import UserQueryBuilder

from processors_base_classes_subclasses.currency_processor import CurrencyProcessor
from processors_base_classes_subclasses.date_processor import DateProcessor
from processors_base_classes_subclasses.text_processor import TextProcessor


# -------------------------------
# 1. Polymorphism – Analyzer Hierarchy
# -------------------------------

def run_analysis(analyzer):
    """
    Demonstrates polymorphism: this function only knows about the base type.
    It calls analyze(), but each subclass behaves differently.
    """
    return analyzer.analyze()


def demo_analyzers(data_manager):
    analyzers = [
        NewsAnalyzer(data_manager),
        StockAnalyzer("AAPL", data_manager),
    ]

    for a in analyzers:
        result = run_analysis(a)
        print(f"{a.__class__.__name__} -> {result}")


# -------------------------------
# 2. Polymorphism – Query Builder Hierarchy
# -------------------------------

def build_query(builder, ticker):
    """Calls the same method on different subclasses."""
    params = {"ticker": ticker}
    return builder.build_query(params)


def demo_query_builders():
    builders = [
        DashboardQueryBuilder(),
        UserQueryBuilder(),
    ]

    for b in builders:
        q = build_query(b, "AAPL")
        print(f"{b.__class__.__name__} -> {q}")


# -------------------------------
# 3. Polymorphism – Processor Hierarchy
# -------------------------------

def demo_processors():
    processors = [
        CurrencyProcessor(),
        DateProcessor(),
        TextProcessor(),
    ]

    samples = [
        1234.56,              # For CurrencyProcessor
        "2024-05-11",         # For DateProcessor
        "<p>Hello World!</p>" # For TextProcessor
    ]

    for p, value in zip(processors, samples):
        result = p.process(value)
        print(f"{p.__class__.__name__} -> {result}")


# -------------------------------
# Run all demos
# -------------------------------

if __name__ == "__main__":
    class DummyDataManager:
        """
        A minimal stand-in so analyzers can run their polymorphic behavior
        without requiring the real data managers.
        """
        def fetch_data(self, q):
            return {}
        def process_data(self, q):
            return {}

    data_manager = DummyDataManager()

    print("\n--- Analyzer Polymorphism ---")
    demo_analyzers(data_manager)

    print("\n--- Query Builder Polymorphism ---")
    demo_query_builders()

    print("\n--- Processor Polymorphism ---")
    demo_processors()
