from managers_base_classes_subclasses.stock_data_manager import StockDataManager
from managers_base_classes_subclasses.news_data_manager import NewsDataManager
from managers_base_classes_subclasses.portfolio_data_manager import PortfolioDataManager


def demo():
    # List of subclasses sharing the same interface (polymorphism)
    managers = [
        StockDataManager(),
        NewsDataManager(api_key="YOUR_API_KEY"),
        PortfolioDataManager()
    ]

    print("\nDemonstrating polymorphism:\n")

    # Each object responds to fetch_data() in its own way
    for manager in managers:
        try:
            result = manager.fetch_data("AAPL")  # Polymorphic call
            print(f"{manager.__class__.__name__} returned type: {type(result)}")
        except Exception as e:
            print(f"{manager.__class__.__name__} raised error: {e}")


if __name__ == "__main__":
    demo()


