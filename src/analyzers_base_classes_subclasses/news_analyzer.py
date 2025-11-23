# news_analyzer.py
from base_analyzer import BaseAnalyzer

class NewsAnalyzer(BaseAnalyzer):
    def __init__(self, data_manager):
        super().__init__(data_manager)

    def analyze(self):
        articles = self.data_manager.fetch_data(["http://feed1.com"])
        processed = self.data_manager.process_data(articles)
        return {"sentiment": "positive", "keywords": ["stock", "market"]}
