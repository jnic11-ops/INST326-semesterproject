from unittest.mock import MagicMock, patch
import pandas as pd
import pytest

from system.system_controller import SystemController


def test_stock_timeseries_happy_path_builds_payload():
    sc = SystemController()
    sc.data_manager = MagicMock()
    sc.data_manager.validate_ticker.return_value = True
    sc.data_manager.fetch_stock_data.return_value = pd.DataFrame({
        "Date": ["2025-01-01", "2025-01-02"],
        "Close": [10.0, 11.0]
    })

    with patch("system.system_controller.StockAnalyzer") as Analyzer, \
         patch("system.system_controller.UserQueryBuilder.prepare_chart_payload") as prep:

        analyzer = MagicMock()
        analyzer.indicators = {"SMA_20": [10, 11], "RSI_14": [40, 50]}
        analyzer.detect_anomalies.return_value = []
        Analyzer.return_value = analyzer

        prep.return_value = {
            "datasets": [{"data": [10.0, 11.0]}],
            "labels": ["2025-01-01", "2025-01-02"],
            "title": "Test"
        }

        result = sc.get_stock_timeseries("AAPL", "2025-01-01", "2025-02-01")

        analyzer.calculate_sma.assert_called_once()
        analyzer.calculate_rsi.assert_called_once()
        assert "datasets" in result


def test_news_sentiment_pipeline():
    sc = SystemController()
    sc.news_analyzer = MagicMock()
    sc.news_analyzer.articles = [{}]
    sc.news_analyzer.analyze_sentiment.return_value = [{"sentiment_label": "positive"}]
    sc.news_analyzer.extract_keywords.return_value = {"apple": 3}

    result = sc.get_news_with_sentiment("AAPL", ["feed1"])

    sc.news_analyzer.fetch.assert_called_once()
    assert result["keywords"]["apple"] == 3


def test_set_portfolio_csv_initializes_manager():
    sc = SystemController()
    with patch("system.system_controller.PortfolioManager") as PM:
        sc.set_portfolio_csv("portfolio.csv")
        PM.assert_called_once()
        assert sc.portfolio_manager is not None


def test_build_portfolio_dashboard_without_manager_raises():
    sc = SystemController()
    with pytest.raises(RuntimeError):
        sc.build_portfolio_dashboard()


def test_export_analysis_creates_file(tmp_path):
    sc = SystemController(data_dir=str(tmp_path))
    out = sc.export_analysis({"x": 1}, "test.json")

    assert "analysis_reports" in out
    assert (tmp_path / "analysis_reports" / "test.json").exists()
