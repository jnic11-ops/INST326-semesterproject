import tkinter as tk
from unittest.mock import MagicMock, patch
import matplotlib

matplotlib.use("Agg")

from api.app import Page1_Stock, Page2_News, Page4_Plot, PageExport


def test_stock_analysis_then_plot_workflow():
    root = tk.Tk()
    root.withdraw()

    controller = MagicMock()
    controller.sc = MagicMock()
    controller.last_payload = None

    payload = {
        "datasets": [{"data": [10, 11, 12]}],
        "labels": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "indicators": {"SMA_20": [10, 11, 12], "RSI_14": [40, 50, 60]},
        "anomalies": [],
        "title": "Test"
    }

    controller.sc.get_stock_timeseries.return_value = payload

    p1 = Page1_Stock(root, controller)
    p1.ticker_entry.insert(0, "AAPL")
    p1.start_entry.delete(0, "end")
    p1.start_entry.insert(0, "2025-01-01")
    p1.end_entry.delete(0, "end")
    p1.end_entry.insert(0, "2025-02-15")
    p1.run_analysis()

    assert controller.last_payload == payload

    p4 = Page4_Plot(root, controller)
    p4.plot_chart()
    assert len(p4.chart_frame.winfo_children()) > 0

    root.destroy()


def test_news_sentiment_workflow_updates_output():
    root = tk.Tk()
    root.withdraw()

    controller = MagicMock()
    controller.sc = MagicMock()
    controller.sc.get_news_with_sentiment.return_value = {
        "articles": [{}, {}],
        "sentiment": [
            {"sentiment_label": "positive"},
            {"sentiment_label": "negative"}
        ],
        "keywords": {"apple": 3}
    }

    page = Page2_News(root, controller)
    page.ticker_entry.insert(0, "AAPL")
    page.run_news()

    text = page.output.get("1.0", "end")
    assert "Articles Retrieved: 2" in text
    assert "Positive: 1" in text
    assert "Negative: 1" in text

    root.destroy()


def test_export_analysis_workflow_calls_controller():
    root = tk.Tk()
    root.withdraw()

    controller = MagicMock()
    controller.sc = MagicMock()
    controller.last_payload = {"x": 1}

    page = PageExport(root, controller)

    with patch("api.app.filedialog.asksaveasfilename") as saveas:
        saveas.return_value = "out.json"
        page.export_json()

    controller.sc.export_analysis.assert_called_once()

    root.destroy()
