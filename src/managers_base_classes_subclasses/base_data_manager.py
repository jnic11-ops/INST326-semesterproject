from abc import ABC, abstractmethod

class BaseDataManager(ABC):
    """
    Abstract base class for all data managers in the system.
    Defines the required interface for fetching data from any source.
    """

    @abstractmethod
    def fetch_data(self, query):
        """
        Abstract method all subclasses must override.
        Each subclass fetches data from its own source (API, file, news, etc.)
        """
        pass

