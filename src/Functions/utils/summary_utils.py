from typing import Iterable, Dict, Any

def build_system_summaries(components: Iterable[object]) -> list[Dict[str, Any]]:
    """
    Demonstrate polymorphism: works with any object that implements summarize().

    Args:
        components: Objects such as PortfolioManager, StockAnalyzer, NewsAnalyzer, etc.

    Returns:
        list[dict]: Summary dictionaries from each component.
    """
    summaries = []
    for component in components:
        # Same method name, different concrete implementations.
        summaries.append(component.summarize())
    return summaries
