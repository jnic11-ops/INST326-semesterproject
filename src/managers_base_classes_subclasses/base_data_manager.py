from abc import ABC, abstractmethod


class BaseDataManager(ABC):
    """
    Abstract base class for all data managers.
    """


    def __init__(self):
        self.source = "Base Manager"


    @abstractmethod
    def fetch_data(self, query):
        """
        Abstract method all subclasses must implement.
        """
        pass


