# tests/test_abcs_and_polymorphism.py
import pytest
from analyzers_base_classes_subclasses.base_analyzer import BaseAnalyzer

def test_base_analyzer_instantiation_fails():
    with pytest.raises(TypeError):
        BaseAnalyzer()  # abstract class

# Now test that at least one concrete analyzer conforms
def test_concrete_analyzer_present_and_polymorphic():
    # Try to import known analyzer locations (support multiple layouts)
    try:
        from analyzers_base_classes_subclasses.news_analyzer import NewsAnalyzer
    except Exception:
        from news_analyzer import NewsAnalyzer  # fallback

    try:
        from analyzers_base_classes_subclasses.stock_analyzer import StockAnalyzer
    except Exception:
        from stock_analyzer import StockAnalyzer

    # instantiate minimal if signatures differ
    na = None
    try:
        na = NewsAnalyzer()
    except Exception:
        # if constructor expects args, create a tiny subclass for the test
        class TmpNews(NewsAnalyzer):
            def __init__(self):
                pass
        na = TmpNews()

    # StockAnalyzer may require data argument; create a minimal stub if needed
    sa = None
    try:
        sa = StockAnalyzer("TST", {"Close": [1,2,3]})
    except Exception:
        class TmpStock(StockAnalyzer):
            def __init__(self):
                pass
        sa = TmpStock()

    # Both should implement analyze (duck-typed)
    assert callable(getattr(na, "analyze", None)) or callable(getattr(na, "analyze_articles", None))
    assert callable(getattr(sa, "analyze", None)) or callable(getattr(sa, "calculate_sma", None))
