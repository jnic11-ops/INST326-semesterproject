# analyzers_base_classes_subclasses/base_analyzer.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAnalyzer(ABC):
    """
    Abstract base for analyzers that take some input data and return a dict of results.

    Subclasses must implement analyze(data) which returns a serializable dict.
    """

    @abstractmethod
    def analyze(self, data: Any) -> Dict:
        """
        Perform analysis on the provided data and return a dictionary of results.

        Args:
            data: Input data (e.g., DataFrame, list of articles, etc.)

        Returns:
            dict: Analysis results (serializable)
        """
        raise NotImplementedError("Subclasses must implement analyze()")



