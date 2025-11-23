# base_analyzer.py
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """Abstract base for all analyzers."""

    @abstractmethod
    def analyze(self):
        """Perform analysis and return results."""
        pass
