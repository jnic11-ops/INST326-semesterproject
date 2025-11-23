# date_processor.py
from processors_base_classes_subclasses.base_processor import BaseProcessor
from datetime import datetime


class DateProcessor(BaseProcessor):
    def __init__(self):
        super().__init__() 

    def process(self, date_str: str):
        formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {date_str}")



