# system/system_controller.py

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

import pandas as pd

from src.classes.stock_data_manager import StockDataManager
from src.classes.stock_analyzer import StockAnalyzer
from src.classes.news_analyzer import NewsAnalyzer
from src.classes.data_processor import DataProcessor
from src.classes.portfolio_manager import PortfolioManager
from src.classes.user_query_builder import UserQueryBuilder


class SystemController:
    """
    Coordinates PortfolioManager, StockDataManager,
    analyzers, processors, and query builders.
    """

    def __init__(self, portfolio_csv_path: Optional[str] = None, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "analysis_reports"), exist_ok=True)
        os.makedirs(os.path.join(self.data_dir, "stock_cache"), exist_ok=True)

        # Core components
        self.data_manager = StockDataManager()
        self.data_processor = DataProcessor()
        self.news_analyzer = NewsAnalyzer()
        self.query_builder = UserQueryBuilder()

        # NEW: Save CSV path for dynamic updates later
        self.portfolio_csv_path = portfolio_csv_path

        # Optional portfolio manager
        self.portfolio_manager = (
            PortfolioManager(portfolio_csv_path, data_manager=self.data_manager)
            if portfolio_csv_path else None
        )

    # =============================================================
    # NEW — Allow updating portfolio CSV dynamically
    # =============================================================
    def set_portfolio_csv(self, path: str):
        """Updates portfolio CSV path and reloads the portfolio manager."""
        self.portfolio_csv_path = path
        self.portfolio_manager = PortfolioManager(path, data_manager=self.data_manager)

    # =============================================================
    # STOCK TIME SERIES + INDICATORS
    # =============================================================
    def get_stock_timeseries(self, ticker: str, start: str, end: str) -> Dict[str, Any]:

        if not self.data_manager.validate_ticker(ticker):
            return {"error": f"Invalid ticker: {ticker}"}

        try:
            df = self.data_manager.fetch_stock_data(ticker, start, end)
        except Exception as e:
            return {"error": f"Failed to fetch data: {e}"}

        if df is None or df.empty:
            return {"error": f"No data found for {ticker} between {start} and {end}."}

        df = df.loc[:, ~df.columns.duplicated()]

        if "Date" not in df.columns:
            df = df.reset_index()

        if "Date" not in df.columns:
            return {"error": "Data source returned no Date column."}

        if "Close" not in df.columns:
            return {"error": "Data source returned no Close column."}

        # Ensure numeric Close values
        try:
            df["Close"] = df["Close"].astype(float)
        except Exception:
            return {"error": "Close column contains invalid numerical values."}

        # Analyze indicators
        analyzer = StockAnalyzer(ticker, df)
        analyzer.calculate_sma(window=20)
        analyzer.calculate_rsi(window=14)
        anomalies = analyzer.detect_anomalies(threshold=0.07)

        close_data = df["Close"]
        if isinstance(close_data, pd.DataFrame):
            close_data = close_data.iloc[:, 0]
        prices = close_data.tolist()

        date_data = df["Date"]
        if isinstance(date_data, pd.DataFrame):
            date_data = date_data.iloc[:, 0]
        timestamps = date_data.astype(str).tolist()

        payload = UserQueryBuilder.prepare_chart_payload(
            prices=prices,
            timestamps=timestamps,
            indicators=analyzer.indicators,
            title=f"{ticker} Price Chart"
        )

        payload["indicators"] = analyzer.indicators
        payload["anomalies"] = anomalies

        return payload

    # =============================================================
    # NEWS + SENTIMENT
    # =============================================================
    def get_news_with_sentiment(self, ticker: str, feed_urls: List[str]):
        self.news_analyzer.fetch(ticker, feed_urls)
        sentiments = self.news_analyzer.analyze_sentiment()
        keywords = self.news_analyzer.extract_keywords()

        return {
            "articles": self.news_analyzer.articles,
            "sentiment": sentiments,
            "keywords": keywords,
        }

    # =============================================================
    # PORTFOLIO
    # =============================================================
    def compute_portfolio_value(self, start: str, end: str) -> float:
        if not self.portfolio_manager:
            raise RuntimeError("PortfolioManager not initialized.")
        return self.portfolio_manager.compute_total_value(start, end)

    def build_portfolio_dashboard(self) -> Dict[str, Any]:
        if not self.portfolio_manager:
            raise RuntimeError("PortfolioManager not initialized.")

        portfolio = self.portfolio_manager.portfolio
        latest_prices = {}

        for ticker in portfolio.keys():
            df = self.data_manager.fetch_stock_data(
                ticker,
                start="2024-01-01",
                end=datetime.now().strftime("%Y-%m-%d")
            )
            price = df["Close"].iloc[-1] if not df.empty else None
            latest_prices[ticker] = price

        return UserQueryBuilder.build_dashboard_summary(
            portfolio, latest_prices, news_items=None, alerts=None
        )

    # =============================================================
    # UTILITIES
    # =============================================================
    def clean_text(self, text: str) -> str:
        return self.data_processor.clean_text(text)

    def normalize_date(self, date_str: str):
        return self.data_processor.normalize_date(date_str)

    def format_currency(self, value: float) -> str:
        return self.data_processor.format_currency(value)

    # =============================================================
    # PERSISTENCE (Save/Load GUI State)
    # =============================================================
    def save_state(self, state: dict, filename: str = "data/app_state.json") -> None:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except OSError as e:
            print(f"[WARNING] Failed to save state: {e}")

    def load_state(self, filename: str = "data/app_state.json") -> dict:
        path = Path(filename)
        if not path.exists():
            return {}

        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[WARNING] Failed to load state: {e}")
            return {}

    # =============================================================
    # CSV IMPORT
    # =============================================================
    def import_csv(self, path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(path)
        except Exception as e:
            raise ValueError(f"Unable to read CSV file: {e}")

        if not isinstance(df, pd.DataFrame):
            raise ValueError("CSV did not load as a DataFrame.")

        return df

    # =============================================================
    # EXPORT ANALYSIS JSON
    # =============================================================
    def export_analysis(self, payload: Dict[str, Any], filename: Optional[str] = None) -> str:
        filename = filename or f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        out_path = os.path.join(self.data_dir, "analysis_reports", filename)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)

        return out_path

    def __str__(self):
        return "<SystemController: integrated app layer>"



