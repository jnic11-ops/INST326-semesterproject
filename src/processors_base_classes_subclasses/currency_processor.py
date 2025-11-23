# currency_processor.py
from processors_base_classes_subclasses.base_processor import BaseProcessor


class CurrencyProcessor(BaseProcessor):
    def __init__(self):
        super().__init__() 

    def process(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be numeric.")
        return f"${value:,.2f}"






