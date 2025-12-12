# query_builders_base_classes_subclasses/base_query_builder.py
from abc import ABC, abstractmethod
from typing import Dict

class BaseQueryBuilder(ABC):
    """Abstract query builder that normalizes UI input into API/db queries."""

    @abstractmethod
    def build_query(self, params: Dict) -> Dict:
        """
        Build and return a normalized query dict from user-provided params.
        """
        raise NotImplementedError



