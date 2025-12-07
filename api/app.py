# api/app.py
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from system.system_controller import SystemController

# ======================================================
# Common tickers for autocomplete
# ======================================================
COMMON_TICKERS = [
    "AAPL", "TSLA", "MSFT", "AMZN", "NVDA", "META", "GOOG",
    "NFLX", "AMD", "INTC", "BA", "DIS", "WMT", "JPM", "V", "MA"
]

# ======================================================
# AutoComplete Entry (Google Style)
# ======================================================
class AutoCompleteEntry(ttk.Entry):
    """A ttk.Entry with Google-style autocomplete dropdown below the entry box."""

    def __init__(self, parent, suggestions, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.suggestions = suggestions
        self.listbox = None
        self.parent = parent

        self.bind("<KeyRelease>", self.show_suggestions)
        self.bind("<FocusOut>", lambda e: self.hide_suggestions())

    def show_suggestions(self, event=None):
        text = self.get().upper()

        if not text:
            self.hide_suggestions()
            return

        matches = [s for s in self.suggestions if s.startswith(text)]

        if not matches:
            self.hide_suggestions()
            return

        if self.listbox is None:
            self.listbox = tk.Listbox(self.parent, height=5)
            self.listbox.bind("<<ListboxSelect>>", self.select_item)

        # Position listbox right below the entry box
        x = self.winfo_x()
        y = self.winfo_y() + self.winfo_height()
        self.listbox.place(x=x, y=y, width=self.winfo_width())

        self.listbox.delete(0, tk.END)
        for item in matches:
            self.listbox.insert(tk.END, item)

    def hide_suggestions(self):
        if self.listbox:
            self.listbox.place_forget()

    def select_item(self, event):
        selection = self.listbox.get(self.listbox.curselection())
        self.delete(0, tk.END)
        self.insert(0, selection)
        self.hide_suggestions()


# ======================================================
# Utility for sparkline
# ======================================================
def generate_sparkline(values):
    if not values:
        return ""
    charset = "▁▂▃▄▅▆▇█"
    mn, mx = min(values), max(values)
    span = mx - mn if mx != mn else 1
    return "".join(charset[int((v - mn) / span * (len(charset) - 1))] for v in values)


# ======================================================
# Main App
# ======================================================
class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Information Retrieval & Analysis Tool")
        self.geometry("740x600")

        self.sc = SystemController(portfolio_csv_path="ex_portfolio.csv")
        self.last_payload = None

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, Page1_Stock, Page2_News, Page3_Portfolio, Page4_Plot):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ======================================================
# HOME PAGE
# ======================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Stock Analysis Tool", font=("Arial", 22, "bold")).pack(pady=20)

        ttk.Button(self, text="1) Stock Timeseries + Indicators",
                   command=lambda: controller.show_frame(Page1_Stock)).pack(fill="x", padx=40, pady=8)

        ttk.Button(self, text="2) News Sentiment + Keywords",
                   command=lambda: controller.show_frame(Page2_News)).pack(fill="x", padx=40, pady=8)

        ttk.Button(self, text="3) Portfolio Dashboard",
                   command=lambda: controller.show_frame(Page3_Portfolio)).pack(fill="x", padx=40, pady=8)

        ttk.Button(self, text="4) Plot Stock Chart",
                   command=lambda: controller.show_frame(Page4_Plot)).pack(fill="x", padx=40, pady=8)

        ttk.Button(self, text="Quit Program",
                   command=self.controller.destroy).pack(side="left", padx=10, pady=20)


# ======================================================
# PAGE 1 — Stock Timeseries + Indicators
# ======================================================
class Page1_Stock(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Stock Timeseries + Indicators", font=("Arial", 16, "bold")).pack(pady=10)

        # Autocomplete ticker entry
        ttk.Label(self, text="Ticker (AAPL, TSLA, MSFT...):").pack()
        self.ticker_entry = AutoCompleteEntry(self, COMMON_TICKERS, width=20)
        self.ticker_entry.pack(pady=3)

        # Dates
        self.start_entry = ttk.Entry(self, width=20)
        self.end_entry = ttk.Entry(self, width=20)

        self._add_labeled_entry("Start Date (YYYY-MM-DD):", self.start_entry)
        self._add_labeled_entry("End Date (YYYY-MM-DD):", self.end_entry)

        ttk.Button(self, text="Run Analysis", command=self.run_analysis).pack(pady=10)

        self.output = tk.Text(self, width=80, height=20, wrap="word")
        self.output.pack(pady=10)

    def _add_labeled_entry(self, text, entry):
        ttk.Label(self, text=text).pack()
        entry.pack(pady=3)

    def run_analysis(self):
        ticker = self.ticker_entry.get().upper().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        payload = self.controller.sc.get_stock_timeseries(ticker, start, end)

        if "error" in payload:
            messagebox.showerror("Error", payload["error"])
            return

        self.controller.last_payload = payload

        prices = payload["datasets"][0]["data"]
        spark = generate_sparkline(prices)

        last_price = prices[-1]
        sma20 = payload["indicators"]["SMA_20"][-1]
        rsi14 = payload["indicators"]["RSI_14"][-1]
        anomalies = payload["anomalies"]

        text = (
            f"\n Ticker: {ticker}\n"
            f"Range: {start} → {end}\n\n"
            f"Latest Closing Price: ${last_price:.2f}\n"
            f"SMA-20: {sma20:.2f}\n"
            f"RSI-14: {rsi14:.2f}\n"
            f"Sparkline Trend: {spark}\n"
            f"Anomalies (>7%): {len(anomalies)}\n"
        )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)


# ======================================================
# PAGE 2 — News Sentiment
# ======================================================
class Page2_News(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="News Sentiment Analysis", font=("Arial", 16, "bold")).pack(pady=10)

        # -------------------------------
        # Beginner-friendly instructions
        # -------------------------------
        instructions = (
            "This tool checks the most recent financial news articles related\n"
            "to your selected stock and analyzes whether the overall tone is\n"
            "positive, negative, or neutral.\n\n"
            "How to use:\n"
            " • Enter a stock ticker symbol (e.g., AAPL, TSLA, MSFT).\n"
            " • Click 'Analyze News' to fetch articles and extract sentiment.\n"
            " • You will also see the most common keywords mentioned\n"
            "   across news sources.\n\n"
            "Tip: Use autocomplete to quickly select popular tickers."
        )

        ttk.Label(self, text=instructions, justify="left", font=("Arial", 10), foreground="gray20").pack(pady=5)

        # -------------------------------
        # Ticker entry (with autocomplete)
        # -------------------------------
        ttk.Label(self, text="Ticker Symbol:").pack()
        self.ticker_entry = AutoCompleteEntry(self, COMMON_TICKERS, width=25)
        self.ticker_entry.pack(pady=3)

        ttk.Button(self, text="Analyze News", command=self.run_news).pack(pady=10)

        self.output = tk.Text(self, width=80, height=20)
        self.output.pack(pady=10)

    def run_news(self):
        ticker = self.ticker_entry.get().upper().strip()

        feed_urls = [
            "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        ]

        result = self.controller.sc.get_news_with_sentiment(ticker, feed_urls)

        sentiments = result["sentiment"]
        keywords = result["keywords"]

        pos = sum(1 for s in sentiments if s["sentiment_label"] == "positive")
        neg = sum(1 for s in sentiments if s["sentiment_label"] == "negative")
        neu = len(sentiments) - pos - neg

        # Output display
        text = (
            f"\nArticles Retrieved: {len(result['articles'])}\n\n"
            f"Positive: {pos}\n"
            f"Neutral:  {neu}\n"
            f"Negative: {neg}\n\n"
            "Top Keywords:\n"
        )

        for word, freq in list(keywords.items())[:10]:
            text += f"  {word:<12} {freq}\n"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)



# ======================================================
# PAGE 3 — Portfolio Dashboard
# ======================================================
class Page3_Portfolio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Portfolio Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        self.output = tk.Text(self, width=80, height=22)
        self.output.pack(pady=10)

        ttk.Button(self, text="Load Portfolio", command=self.load_portfolio).pack()

    def load_portfolio(self):
        try:
            dashboard = self.controller.sc.build_portfolio_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        text = (
            f"Total Portfolio Value: ${dashboard['total_value']:.2f}\n\n"
            "Positions:\n"
        )

        for pos in dashboard["positions"]:
            text += (
                f"• {pos['ticker']}: {pos['shares']} shares → "
                f"${pos['position_value']:.2f} "
                f"({pos['pct_of_portfolio']}%)\n"
            )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)


# ======================================================
# PAGE 4 — Plot Stock Chart
# ======================================================
class Page4_Plot(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back", command=lambda: controller.show_frame(HomePage)
                  ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Plot Stock Chart", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Button(self, text="Show Chart", command=self.plot_chart).pack(pady=20)

    def plot_chart(self):
        payload = self.controller.last_payload
        if not payload:
            messagebox.showerror("Error", "Run Option 1 first.")
            return

        prices = payload["datasets"][0]["data"]
        dates = payload["labels"]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, prices, label="Price", color="blue")

        for name, series in payload["indicators"].items():
            plt.plot(dates, series, label=name)

        plt.title(payload["title"])
        plt.xlabel("Date")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()


# ======================================================
# RUN APP
# ======================================================
if __name__ == "__main__":
    app = StockApp()
    app.mainloop()







