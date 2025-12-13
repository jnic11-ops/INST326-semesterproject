import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

from system.system_controller import SystemController


# ---------------------------
# get_stock_timeseries (UNIT)
# ---------------------------

def test_invalid_ticker_returns_error():
    sc = SystemController()
    sc.data_manager = MagicMock()
    sc.data_manager.validate_ticker.return_value = False

    result = sc.get_stock_timeseries("BAD", "2025-01-01", "2025-02-01")
    assert "error" in result


def test_fetch_exception_returns_error():
    sc = SystemController()
    sc.data_manager = MagicMock()
    sc.data_manager.validate_ticker.return_value = True
    sc.data_manager.fetch_stock_data.side_effect = RuntimeError("boom")

    result = sc.get_stock_timeseries("AAPL", "2025-01-01", "2025-02-01")
    assert "error" in result


def test_empty_dataframe_returns_error():
    sc = SystemController()
    sc.data_manager = MagicMock()
    sc.data_manager.validate_ticker.return_value = True
    sc.data_manager.fetch_stock_data.return_value = pd.DataFrame()

    result = sc.get_stock_timeseries("AAPL", "2025-01-01", "2025-02-01")
    assert "error" in result


def test_missing_close_column_returns_error():
    sc = SystemController()
    sc.data_manager = MagicMock()
    sc.data_manager.validate_ticker.return_value = True
    sc.data_manager.fetch_stock_data.return_value = pd.DataFrame({
        "Date": ["2025-01-01"]
    })

    result = sc.get_stock_timeseries("AAPL", "2025-01-01", "2025-02-01")
    assert "error" in result


# ---------------------------
# CSV Import (UNIT)
# ---------------------------

def test_import_csv_invalid_path_raises():
    sc = SystemController()
    with pytest.raises(ValueError):
        sc.import_csv("not_real.csv")


# ---------------------------
# Persistence (UNIT)
# ---------------------------

def test_save_and_load_state(tmp_path):
    sc = SystemController()
    file = tmp_path / "state.json"

    sc.save_state({"x": 1}, str(file))
    loaded = sc.load_state(str(file))

    assert loaded["x"] == 1
