# base_analyzer.py
from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    def __init__(self):
        super().__init__()  # optional, harmless

    @abstractmethod
    def analyze(self):
        pass

