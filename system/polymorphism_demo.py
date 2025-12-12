# system/polymorphism_demo.py
"""
Polymorphism demo: run multiple analyzers via BaseAnalyzer interface.
Run from project root:
    python -m system.polymorphism_demo
"""

from analyzers_base_classes_subclasses.base_analyzer import BaseAnalyzer
# import existing concrete analyzers (adjust import paths if needed)
try:
    from analyzers_base_classes_subclasses.news_analyzer import NewsAnalyzer
except Exception:
    from news_analyzer import NewsAnalyzer  # fallback local import

try:
    from analyzers_base_classes_subclasses.stock_analyzer import StockAnalyzer
except Exception:
    from stock_analyzer import StockAnalyzer  # fallback

# Create minimal inputs for demo
sample_articles = [
    {"title": "Company X reports strong profit and growth"},
    {"title": "Company Y faces regulatory concern, stock down"}
]
# For stock analyzer, provide a simple object with 'Close' series (list)
sample_stock_data = {"Close": [100, 102, 101, 105, 110]}

# instantiate analyzers
analyzers: list[BaseAnalyzer] = []

# Try to instantiate NewsAnalyzer if signature matches; otherwise keep simple
try:
    na = NewsAnalyzer()  # many NewsAnalyzer implementations accept api_key optional
except TypeError:
    # fallback: wrap a minimal stub that conforms to BaseAnalyzer
    class _SimpleNews(BaseAnalyzer):
        def analyze(self, data):
            return {"count": len(data)}
    na = _SimpleNews()

try:
    sa = StockAnalyzer("DEMO", pd.DataFrame(sample_stock_data))  # some implementations accept (ticker, df)
except Exception:
    # fallback simple adapter that uses underlying analyze method if present
    class _SimpleStock(BaseAnalyzer):
        def analyze(self, data):
            return {"min": min(data.get("Close", [])), "max": max(data.get("Close", []))}
    sa = _SimpleStock()

analyzers = [na, sa]

print("Running polymorphism demo:\n")
for a in analyzers:
    try:
        out = a.analyze(sample_articles if a is na else sample_stock_data)
    except Exception as e:
        out = {"error": str(e)}
    print(f"{a.__class__.__name__}: {out}")
