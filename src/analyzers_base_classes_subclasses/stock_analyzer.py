# stock_analyzer.py
from base_analyzer import BaseAnalyzer

class StockAnalyzer(BaseAnalyzer):
    def __init__(self, ticker, data_manager):
        self.ticker = ticker
        self.data_manager = data_manager

    def analyze(self):
        data = self.data_manager.fetch_data(self.ticker)
        processed = self.data_manager.process_data(data)
        return {"SMA": [], "RSI": []}
