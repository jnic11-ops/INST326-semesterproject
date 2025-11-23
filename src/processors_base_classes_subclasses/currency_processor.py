# currency_processor.py
from base_processor import BaseProcessor

class CurrencyProcessor(BaseProcessor):
    def process(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric.")
        return f"${value:,.2f}"






