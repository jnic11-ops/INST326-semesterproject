# main.py
from system.system_controller import SystemController
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from datetime import datetime


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def generate_sparkline(values):
    """Convert numeric list into a mini ASCII sparkline."""
    if not values:
        return ""

    charset = "▁▂▃▄▅▆▇█"
    mn = min(values)
    mx = max(values)
    span = mx - mn if mx != mn else 1

    return "".join(
        charset[int((v - mn) / span * (len(charset) - 1))]
        for v in values
    )


def run_cli():
    # Load your portfolio (optional)
    sc = SystemController(portfolio_csv_path="ex_portfolio.csv")

    print_header("Stock Information Retrieval & Analysis Tool")

    # Store last stock payload for Option 4
    global last_stock_payload
    last_stock_payload = None

    while True:
        print("\nOptions:")
        print("1) Get stock timeseries + indicators")
        print("2) Get news sentiment + keywords")
        print("3) Build portfolio dashboard (requires CSV)")
        print("4) Plot stock chart (matplotlib)")
        print("0) Quit")

        choice = input("Choose: ").strip()

        # ==========================================================
        # OPTION 1 — STOCK ANALYSIS
        # ==========================================================
        if choice == "1":
            print_header("Stock Timeseries + Indicator Analysis")

            ticker = input("Enter ticker (e.g., AAPL, MSFT, TSLA): ").upper()
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")

            payload = sc.get_stock_timeseries(ticker, start, end)

            if "error" in payload:
                print(f"\nERROR: {payload['error']}")
                continue

            # Extract values
            prices = payload["datasets"][0]["data"]
            sma20 = payload["indicators"]["SMA_20"][-1]
            rsi14 = payload["indicators"]["RSI_14"][-1]
            anomalies = payload["anomalies"]

            last_price = prices[-1]
            spark = generate_sparkline(prices)

            print("\n------------------------------------------------------------")
            print(f"📌 Ticker: {ticker}")
            print(f"📅 Dates: {start} → {end}")
            print(f"• Latest Closing Price: ${last_price:.2f}")
            print(f"• SMA-20: {sma20:.2f}")
            print(f"• RSI-14: {rsi14:.2f}")
            print(f"• Anomalies Detected (>7% moves): {len(anomalies)}")
            print(f"• Price Sparkline: {spark}")
            print("------------------------------------------------------------")

            last_stock_payload = payload

        # ==========================================================
        # OPTION 2 — NEWS SENTIMENT
        # ==========================================================
        elif choice == "2":
            print_header("News Sentiment & Keyword Extraction")

            ticker = input("Enter ticker (e.g., AAPL, TSLA): ").upper()
            feed_input = input(
                "Enter RSS feed URLs (comma-separated), or press Enter for defaults: "
            )

            feed_urls = (
                [u.strip() for u in feed_input.split(",")]
                if feed_input.strip()
                else [
                    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
                    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
                ]
            )

            result = sc.get_news_with_sentiment(ticker, feed_urls)

            print(f"\nArticles Retrieved: {len(result['articles'])}")

            sentiments = result["sentiment"]
            pos = sum(1 for a in sentiments if a.get("sentiment_label") == "positive")
            neg = sum(1 for a in sentiments if a.get("sentiment_label") == "negative")
            neu = len(sentiments) - pos - neg

            print("\n SENTIMENT BREAKDOWN")
            print(f"• Positive: {pos}")
            print(f"• Neutral:  {neu}")
            print(f"• Negative: {neg}")

            print("\n TOP KEYWORDS:")
            for word, freq in list(result["keywords"].items())[:10]:
                print(f"  {word:<12} {freq}")

        # ==========================================================
        # OPTION 3 — PORTFOLIO DASHBOARD
        # ==========================================================
        elif choice == "3":
            print_header("Portfolio Dashboard")

            if not sc.portfolio_manager:
                print(" Portfolio CSV not provided.")
                continue

            dashboard = sc.build_portfolio_dashboard()

            print(f"\nTotal Portfolio Value: ${dashboard['total_value']:.2f}\n")

            for pos in dashboard["positions"]:
                print(
                    f"• {pos['ticker']}: {pos['shares']} shares → "
                    f"${pos['position_value']:.2f} ({pos['pct_of_portfolio']}%)"
                )

        # ==========================================================
        # OPTION 4 — MATPLOTLIB CHART (IMPROVED)
        # ==========================================================
        elif choice == "4":
            print_header("Interactive Stock Chart")

            if last_stock_payload is None:
                print(" Run Option 1 first to load stock data.")
                continue

            p = last_stock_payload
            dates_raw = p["labels"]
            prices = p["datasets"][0]["data"]
            sma_20 = p["indicators"]["SMA_20"]
            anomalies = p["anomalies"]

            # Convert to datetime objects
            dates = [
                datetime.fromisoformat(d) if isinstance(d, str) else d
                for d in dates_raw
            ]

            # Create plot
            plt.figure(figsize=(14, 7))

            # Price line
            plt.plot(dates, prices, label="Price", color="blue", linewidth=1.6)

            # SMA-20
            plt.plot(dates, sma_20, label="SMA 20", color="orange", linewidth=2)

            # Anomalies
            anomaly_dates = [dates[i] for i in anomalies]
            anomaly_prices = [prices[i] for i in anomalies]
            plt.scatter(anomaly_dates, anomaly_prices, color="red", label="Anomalies", s=50)

            # Title and labels
            plt.title(p["title"], fontsize=18, weight="bold")
            plt.xlabel("Date", fontsize=12)
            plt.ylabel("Price ($)", fontsize=12)

            # Better date formatting
            plt.gca().xaxis.set_major_locator(MonthLocator(interval=1))
            plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m"))

            plt.xticks(rotation=45, fontsize=10)
            plt.grid(True, linestyle="--", alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()

        # ==========================================================
        # EXIT
        # ==========================================================
        elif choice == "0":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option. Choose 0–4.")


if __name__ == "__main__":
    run_cli()










