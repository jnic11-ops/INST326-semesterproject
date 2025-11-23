from abc import ABC, abstractmethod

class BaseQueryBuilder(ABC):
    """Abstract base class for all query builders."""

    def validate(self, params: dict) -> dict:
        """Shared optional validation/preprocessing for parameters."""
        return params

    @abstractmethod
    def build_query(self, params: dict):
        pass

