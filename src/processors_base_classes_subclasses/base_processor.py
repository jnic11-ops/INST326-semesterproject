# base_processor.py
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """Abstract base class for any data processor."""

    @abstractmethod
    def process(self, data):
        """Process input data and return normalized result."""
        pass
