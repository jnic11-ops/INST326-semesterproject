# main.py
from system.system_controller import SystemController
import matplotlib.pyplot as plt


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
    sc = SystemController(portfolio_csv_path=None)

    print_header("Stock Information Retrieval & Analysis Tool")

    while True:
        print("\nOptions:")
        print("1) Get stock timeseries + indicators")
        print("2) Get news sentiment + keywords")
        print("3) Build portfolio dashboard (requires CSV)")
        print("4) Plot stock chart (matplotlib)")
        print("0) Quit")

        choice = input("Choose: ").strip()

        # ==========================================================
        # OPTION 1 — STOCK TIMESERIES + INDICATORS
        # ==========================================================
        if choice == "1":
            print_header("Stock Timeseries + Indicator Analysis")

            ticker = input("Enter ticker (e.g., AAPL, MSFT, TSLA): ").upper()
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")

            payload = sc.get_stock_timeseries(ticker, start, end)

            if "error" in payload:
                print(f"\n ERROR: {payload['error']}")
                continue

            last_price = payload["datasets"][0]["data"][-1]
            sma20 = payload["indicators"]["SMA_20"][-1]
            rsi14 = payload["indicators"]["RSI_14"][-1]
            anomalies = payload["anomalies"]

            prices = payload["datasets"][0]["data"]
            spark = generate_sparkline(prices)

            print("\n------------------------------------------------------------")
            print(f" Ticker: {ticker}")
            print(f" Latest Closing Price: ${last_price:.2f}")
            print(f" SMA-20: {sma20:.2f}")
            print(f" RSI-14: {rsi14:.2f}")
            print(f" Anomalies Detected (>7% moves): {len(anomalies)}")
            print(f" Price Trend Sparkline: {spark}")
            print("------------------------------------------------------------")

            # Save payload for Option 4 plotting
            global last_stock_payload
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

            if feed_input.strip():
                feed_urls = [u.strip() for u in feed_input.split(",")]
            else:
                feed_urls = [
                    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
                    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
                ]

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

            print(f"\nTotal Portfolio Value: ${dashboard['total_value']:.2f}")
            print("\nPositions:")
            for pos in dashboard["positions"]:
                print(
                    f" • {pos['ticker']}: {pos['shares']} shares → "
                    f"${pos['position_value']:.2f} ({pos['pct_of_portfolio']}%)"
                )

        # ==========================================================
        # OPTION 4 — PLOT MATPLOTLIB CHART
        # ==========================================================
        elif choice == "4":
            print_header("Interactive Stock Chart")

            if "last_stock_payload" not in globals():
                print(" Run Option 1 first to load stock data.")
                continue

            p = last_stock_payload
            prices = p["datasets"][0]["data"]
            dates = p["labels"]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, prices, label="Price", color="blue")
            plt.title(p["title"])
            plt.xlabel("Date")
            plt.ylabel("Price ($)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.legend()
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








