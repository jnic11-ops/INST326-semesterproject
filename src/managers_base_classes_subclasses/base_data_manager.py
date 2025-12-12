# managers_base_classes_subclasses/base_data_manager.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseDataManager(ABC):
    """
    Abstract base class for data managers (stock, news, portfolio).

    Concrete managers must implement fetch_data(query) and optionally process_data(data).
    """

    @abstractmethod
    def fetch_data(self, query: Dict) -> Any:
        """Fetch raw data for the given query (e.g., ticker, date range)."""
        raise NotImplementedError

    def process_data(self, data: Any) -> Any:
        """
        Optional hook to normalize or postprocess raw data.
        Default implementation returns data unchanged; subclasses can override.
        """
        return data





