# system/data_pipeline.py
from typing import Any, Dict, List, Optional
from analyzers_base_classes_subclasses.base_analyzer import BaseAnalyzer

class DataPipeline:
    """
    Composition-based pipeline that coordinates data managers and analyzers.
    Expects:
      - stock_manager: object with fetch_stock_data(ticker, start, end) -> DataFrame/dict
      - news_manager: object with fetch(ticker, feed_urls)/fetch_news method
      - analyzers: list of BaseAnalyzer instances
    """

    def __init__(self, stock_manager: Any, news_manager: Any, analyzers: Optional[List[BaseAnalyzer]] = None):
        self.stock_manager = stock_manager
        self.news_manager = news_manager
        self.analyzers = analyzers or []

    def run_for_ticker(self, ticker: str, start: str, end: str, feed_urls: Optional[List[str]] = None) -> Dict:
        result = {"ticker": ticker}
        # fetch stock data (attempt multiple possible method names)
        stock_data = None
        try:
            stock_data = self.stock_manager.fetch_stock_data(ticker, start, end)
        except Exception as e:
            try:
                stock_data = self.stock_manager.fetch_stock(ticker, start, end)
            except Exception as e2:
                result["stock_error"] = str(e)

        result["stock_data"] = stock_data

        # fetch news
        news = []
        try:
            if hasattr(self.news_manager, "fetch"):
                if feed_urls:
                    self.news_manager.fetch(ticker, feed_urls)
                    news = getattr(self.news_manager, "articles", [])
                else:
                    # fallback if manager exposes fetch_news
                    news = getattr(self.news_manager, "fetch_news", lambda t: [])(ticker)
        except Exception as e:
            result["news_error"] = str(e)

        result["news"] = news

        # run analyzers polymorphically
        analysis = {}
        for analyzer in self.analyzers:
            try:
                # decide which data type to pass: prefer stock_data if Analyzer name suggests stock
                name = analyzer.__class__.__name__.lower()
                if "stock" in name or "trend" in name:
                    analysis[analyzer.__class__.__name__] = analyzer.analyze(stock_data)
                else:
                    analysis[analyzer.__class__.__name__] = analyzer.analyze(news)
            except Exception as e:
                analysis[analyzer.__class__.__name__] = {"error": str(e)}
        result["analysis"] = analysis
        return result
