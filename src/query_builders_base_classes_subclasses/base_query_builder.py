from abc import ABC, abstractmethod

class BaseQueryBuilder(ABC):
    """Abstract base class for all query builders."""

    @abstractmethod
    def build_query(self, params: dict):
        pass

