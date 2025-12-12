# processors_base_classes_subclasses/base_processor.py
from abc import ABC, abstractmethod
from typing import Any

class BaseProcessor(ABC):
    """
    Abstract processor interface for transforming data (text, date, currency, etc.)
    """

    @abstractmethod
    def process(self, value: Any) -> Any:
        """Process and return the transformed value."""
        raise NotImplementedError


