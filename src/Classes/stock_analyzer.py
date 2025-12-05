import pandas as pd
import math

class StockAnalyzer:
    """Performs analytical operations on stock data such as SMA, RSI, and anomaly detection."""

    def __init__(self, ticker: str, data: pd.DataFrame):
        if data.empty or "Close" not in data.columns:
            raise ValueError("Data must be a non-empty DataFrame containing a 'Close' column.")

        self._ticker = ticker.upper()
        self._data = data.copy()
        self._indicators = {}

    @property
    def ticker(self):
        return self._ticker

    @property
    def data(self):
        return self._data

    @property
    def indicators(self):
        return self._indicators

    # ============================================================
    # SAFE PRICE EXTRACTOR
    # ============================================================
    def _get_close_prices(self):
        """
        Safely return closing prices as a float list.
        Handles cases where: 
        - Yahoo returns duplicate columns
        - Close is a DataFrame instead of Series
        - Values are dtype=object instead of float
        """
        prices = self._data["Close"]

        # Fix: Close returned as DataFrame with 1 column
        if isinstance(prices, pd.DataFrame):
            prices = prices.iloc[:, 0]

        # Convert to Python list
        prices = prices.tolist()

        # Convert to float and filter out None/NaN
        clean_prices = []
        for p in prices:
            try:
                clean_prices.append(float(p))
            except Exception:
                clean_prices.append(None)

        return clean_prices

    # ============================================================
    # SMA
    # ============================================================
    def _simple_moving_average(self, values, window=20):
        if not isinstance(values, list):
            raise TypeError("values must be a list")
        if window < 1:
            raise ValueError("window must be >= 1")

        n = len(values)
        out = [None] * n
        running_sum = 0.0

        for i, v in enumerate(values):
            if v is None:
                continue  # Skip invalid entries
            
            running_sum += float(v)
            if i >= window:
                if values[i - window] is not None:
                    running_sum -= float(values[i - window])

            if i >= window - 1:
                out[i] = running_sum / window

        return out

    # ============================================================
    # RSI
    # ============================================================
    def _calculate_rsi(self, prices, window=14):
        gains, losses = [0.0], [0.0]
        rsi = []

        # Compute gains and losses
        for i in range(1, len(prices)):
            if prices[i] is None or prices[i - 1] is None:
                gains.append(0.0)
                losses.append(0.0)
                continue

            change = prices[i] - prices[i - 1]
            gains.append(max(change, 0))
            losses.append(max(-change, 0))

        for i in range(len(prices)):
            if i + 1 < window:
                rsi.append(None)
                continue

            avg_gain = sum(gains[i + 1 - window:i + 1]) / window
            avg_loss = sum(losses[i + 1 - window:i + 1]) / window

            if avg_loss == 0:
                rsi.append(100.0)
                continue

            rs = avg_gain / avg_loss
            rsi_val = 100 - (100 / (1 + rs))
            rsi.append(rsi_val)

        return rsi

    # ============================================================
    # Anomalies
    # ============================================================
    def _detect_price_anomalies(self, prices, threshold=0.05):
        anomalies = []

        for i in range(1, len(prices)):
            if prices[i] is None or prices[i - 1] is None:
                continue

            if prices[i - 1] == 0:
                continue

            change_pct = abs(prices[i] - prices[i - 1]) / prices[i - 1]

            if change_pct > threshold:
                anomalies.append(i)

        return anomalies

    # ============================================================
    # PUBLIC METHODS
    # ============================================================
    def calculate_sma(self, window=20):
        prices = self._get_close_prices()
        sma_values = self._simple_moving_average(prices, window)
        self._indicators[f"SMA_{window}"] = sma_values
        self._data[f"SMA_{window}"] = sma_values
        return sma_values

    def calculate_rsi(self, window=14):
        prices = self._get_close_prices()
        rsi_values = self._calculate_rsi(prices, window)
        self._indicators[f"RSI_{window}"] = rsi_values
        self._data[f"RSI_{window}"] = rsi_values
        return rsi_values

    def detect_anomalies(self, threshold=0.05):
        prices = self._get_close_prices()
        return self._detect_price_anomalies(prices, threshold)

    def __str__(self):
        return f"StockAnalyzer({self._ticker}) with {len(self._data)} records"

    def __repr__(self):
        return f"StockAnalyzer(ticker='{self._ticker}')"
