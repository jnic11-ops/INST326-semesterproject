# base_analyzer.py
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """ Abstract base for all analyzers."""

    def __init__(self, data_manager):
        self.data_manager = data_manager

    @abstractmethod
    def analyze(self):
        """Perform analysis and return results."""
        pass
