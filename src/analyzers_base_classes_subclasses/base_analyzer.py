# base_analyzer.py
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    def __init__(self, data_manager):
        self.data_manager = data_manager

    @abstractmethod
    def analyze(self):
        pass

