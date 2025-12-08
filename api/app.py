# api/app.py

import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import subprocess
import platform

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from system.system_controller import SystemController


# ======================================================
# Common Tickers
# ======================================================
COMMON_TICKERS = [
    "AAPL", "TSLA", "MSFT", "AMZN", "NVDA", "META",
    "GOOG", "NFLX", "AMD", "INTC", "BA", "DIS",
    "WMT", "JPM", "V", "MA"
]


# ======================================================
# Autocomplete Entry
# ======================================================
class AutoCompleteEntry(ttk.Entry):
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
            self.listbox = tk.Listbox(self.parent, height=6)
            self.listbox.bind("<<ListboxSelect>>", self.select_item)

        self.listbox.place(
            x=self.winfo_x(),
            y=self.winfo_y() + self.winfo_height(),
            width=self.winfo_width()
        )
        self.listbox.delete(0, tk.END)

        for item in matches:
            self.listbox.insert(tk.END, item)

    def hide_suggestions(self):
        if self.listbox:
            self.listbox.place_forget()

    def select_item(self, event):
        if not self.listbox.curselection():
            return
        value = self.listbox.get(self.listbox.curselection())
        self.delete(0, tk.END)
        self.insert(0, value)
        self.hide_suggestions()


# ======================================================
# Sparkline Utility
# ======================================================
def generate_sparkline(values):
    if not values:
        return ""
    charset = "▁▂▃▄▅▆▇█"
    mn, mx = min(values), max(values)
    span = mx - mn if mx != mn else 1
    return "".join(charset[int((v - mn) / span * (len(charset)-1))] for v in values)


# ======================================================
# Main Tkinter App
# ======================================================
class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Information Retrieval & Analysis Tool")
        self.geometry("760x620")

        # System controller (with default portfolio CSV)
        self.sc = SystemController(portfolio_csv_path="ex_portfolio.csv")

        saved = self.sc.load_state()
        self.last_payload = saved.get("last_payload")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (
            HomePage, Page1_Stock, Page2_News, Page3_Portfolio,
            Page4_Plot, PageCSV_Import, PageExport
        ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def show_frame(self, page):
        self.frames[page].tkraise()

    def on_exit(self):
        self.sc.save_state({"last_payload": self.last_payload})
        self.destroy()


# ======================================================
# HOME PAGE
# ======================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(
            self, text="Stock Analysis Tool",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        btn = dict(fill="x", padx=40, pady=8)

        ttk.Button(self, text="1) Stock Timeseries + Indicators",
                   command=lambda: controller.show_frame(Page1_Stock)).pack(**btn)

        ttk.Button(self, text="2) News Sentiment + Keywords",
                   command=lambda: controller.show_frame(Page2_News)).pack(**btn)

        ttk.Button(self, text="3) Portfolio Dashboard",
                   command=lambda: controller.show_frame(Page3_Portfolio)).pack(**btn)

        ttk.Button(self, text="4) Plot Stock Chart",
                   command=lambda: controller.show_frame(Page4_Plot)).pack(**btn)

        ttk.Button(self, text="5) Import CSV",
                   command=lambda: controller.show_frame(PageCSV_Import)).pack(**btn)

        ttk.Button(self, text="6) Export Last Analysis",
                   command=lambda: controller.show_frame(PageExport)).pack(**btn)

        ttk.Button(self, text="Quit Program",
                   command=controller.on_exit).pack(side="left", padx=20, pady=20)


# ======================================================
# PAGE 1 — Stock Analysis
# ======================================================
class Page1_Stock(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)
                   ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Stock Timeseries + Indicators",
                  font=("Arial", 18, "bold")).pack()

        ttk.Label(self, text="Ticker Symbol:").pack()
        self.ticker_entry = AutoCompleteEntry(self, COMMON_TICKERS, width=22)
        self.ticker_entry.pack()

        ttk.Label(self, text="Start Date (YYYY-MM-DD)").pack()
        self.start_entry = ttk.Entry(self, width=25)
        self.start_entry.pack()

        ttk.Label(self, text="End Date (YYYY-MM-DD)").pack()
        self.end_entry = ttk.Entry(self, width=25)
        self.end_entry.pack()

        ttk.Button(self, text="Run Analysis",
                   command=self.run_analysis).pack(pady=12)

        self.output = tk.Text(self, width=90, height=20)
        self.output.pack()

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

        output = (
            f"\nTicker: {ticker}\n"
            f"Range: {start} → {end}\n"
            f"Last Price: {prices[-1]:.2f}\n"
            f"SMA-20: {payload['indicators']['SMA_20'][-1]:.2f}\n"
            f"RSI-14: {payload['indicators']['RSI_14'][-1]:.2f}\n"
            f"Anomalies: {len(payload['anomalies'])}\n"
            f"Trend: {spark}\n"
        )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, output)


# ======================================================
# PAGE 2 — News Sentiment
# ======================================================
class Page2_News(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)
                   ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="News Sentiment Analysis",
                  font=("Arial", 18, "bold")).pack()

        # Instructions for this screen
        ttk.Label(
            self,
            text=(
                "This screen retrieves recent financial news for the chosen ticker and "
                "summarizes overall sentiment (positive, neutral, negative) along with "
                "the most frequent keywords found in the articles."
            ),
            wraplength=700,
            foreground="gray30",
            justify="left"
        ).pack(padx=10, pady=(0, 10))

        ttk.Label(self, text="Ticker Symbol:").pack()
        self.ticker_entry = AutoCompleteEntry(self, COMMON_TICKERS, width=22)
        self.ticker_entry.pack()

        ttk.Button(self, text="Analyze News",
                   command=self.run_news).pack(pady=10)

        self.output = tk.Text(self, width=90, height=20)
        self.output.pack()

    def run_news(self):
        ticker = self.ticker_entry.get().upper().strip()

        feeds = [
            "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        ]

        result = self.controller.sc.get_news_with_sentiment(ticker, feeds)

        sentiments = result["sentiment"]
        keywords = result["keywords"]

        pos = sum(1 for x in sentiments if x["sentiment_label"] == "positive")
        neg = sum(1 for x in sentiments if x["sentiment_label"] == "negative")
        neu = len(sentiments) - pos - neg

        output = (
            f"\nArticles Retrieved: {len(result['articles'])}\n"
            f"Positive: {pos}\nNeutral: {neu}\nNegative: {neg}\n\n"
            "Top Keywords:\n"
        )

        for word, freq in list(keywords.items())[:10]:
            output += f"{word:<12} {freq}\n"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, output)


# ======================================================
# PAGE 3 — Portfolio Dashboard
# ======================================================
class Page3_Portfolio(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)
                   ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Portfolio Dashboard",
                  font=("Arial", 18, "bold")).pack()

        # Instructions + dynamic portfolio file name
        self.info_label = ttk.Label(
            self,
            text="",
            wraplength=700,
            foreground="gray30",
            justify="left"
        )
        self.info_label.pack(padx=10, pady=(0, 10))
        self.update_info_text()

        self.output = tk.Text(self, width=90, height=20)
        self.output.pack()

        ttk.Button(self, text="Load Portfolio",
                   command=self.load).pack(pady=10)

    def update_info_text(self):
        path = self.controller.sc.portfolio_csv_path
        if path:
            filename = os.path.basename(path)
        else:
            filename = "None (no CSV selected yet)"

        text = (
            "This screen summarizes your portfolio using the active portfolio CSV file.\n"
            "It calculates the total portfolio value and shows each position's value and weight.\n\n"
            f"Current portfolio file: {filename}"
        )
        self.info_label.config(text=text)

    def load(self):
        # Refresh info in case CSV was changed via Import CSV
        self.update_info_text()

        try:
            dashboard = self.controller.sc.build_portfolio_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        output = f"Total Portfolio Value: ${dashboard['total_value']:.2f}\n\n"

        for pos in dashboard["positions"]:
            output += (
                f"{pos['ticker']}: {pos['shares']} shares → "
                f"${pos['position_value']:.2f} "
                f"({pos['pct_of_portfolio']}%)\n"
            )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, output)


# ======================================================
# PAGE 4 — Plot Stock Chart
# ======================================================
class Page4_Plot(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(self, text="← Back",
                   command=lambda: controller.show_frame(HomePage)
                   ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Plot Stock Chart",
                  font=("Arial", 18, "bold")).pack()

        # Instructions for this screen
        ttk.Label(
            self,
            text=(
                "This screen plots the price history, indicators (SMA/RSI), and detected anomalies "
                "for the most recent stock analysis you ran in Option 1.\n"
                "Use the toolbar below the chart to zoom and pan, and hover over points to see "
                "exact dates and prices."
            ),
            wraplength=700,
            foreground="gray30",
            justify="left"
        ).pack(padx=10, pady=(0, 10))

        ttk.Button(self, text="Show Chart",
                   command=self.plot_chart).pack(pady=12)

        # container for the chart
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True)

    def plot_chart(self):
        # Clear old widgets
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        payload = self.controller.last_payload
        if not payload:
            messagebox.showerror("Error", "Run Option 1 first.")
            return

        prices = payload["datasets"][0]["data"]
        labels = payload["labels"]
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in labels]

        fig, ax = plt.subplots(figsize=(10, 5), dpi=100)

        # MAIN PRICE LINE
        price_line, = ax.plot(dates, prices, label="Price", color="blue")

        # INDICATORS (SMA, RSI, etc.)
        indicators = payload["indicators"]
        indicator_lines = {}
        for name, series in indicators.items():
            line, = ax.plot(dates, series, label=name)
            indicator_lines[name] = line

        # ANOMALIES (red dots)
        anomalies = payload.get("anomalies", [])
        anomaly_dates = []
        anomaly_prices = []

        for idx in anomalies:
            if 0 <= idx < len(dates):
                anomaly_dates.append(dates[idx])
                anomaly_prices.append(prices[idx])

        scatter_points = None
        if anomaly_dates:
            scatter_points = ax.scatter(
                anomaly_dates,
                anomaly_prices,
                color="red",
                s=45,
                label="Anomaly",
                zorder=5
            )

        # HOVER TOOLTIP (custom)
        tooltip = ax.annotate(
            "",
            xy=(0, 0),
            xytext=(15, 15),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="yellow", alpha=0.75),
            arrowprops=dict(arrowstyle="->"),
            visible=False
        )

        def format_price(p):
            return f"${p:,.2f}"

        def on_hover(event):
            if event.inaxes != ax:
                tooltip.set_visible(False)
                fig.canvas.draw_idle()
                return

            # ANOMALY POINT HOVER
            if scatter_points:
                cont, ind = scatter_points.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    x = anomaly_dates[idx]
                    y = anomaly_prices[idx]

                    tooltip.xy = (x, y)
                    tooltip.set_text(f"{x.strftime('%Y-%m-%d')}\nPrice: {format_price(y)}")
                    tooltip.set_visible(True)
                    fig.canvas.draw_idle()
                    return

            # PRICE LINE HOVER
            cont, ind = price_line.contains(event)
            if cont:
                idx = ind["ind"][0]
                x = dates[idx]
                y = prices[idx]
                tooltip.xy = (x, y)
                tooltip.set_text(f"{x.strftime('%Y-%m-%d')}\nPrice: {format_price(y)}")
                tooltip.set_visible(True)
                fig.canvas.draw_idle()
                return

            # INDICATOR LINES HOVER
            for name, line in indicator_lines.items():
                cont, ind = line.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    x = dates[idx]
                    y = indicators[name][idx]
                    tooltip.xy = (x, y)
                    tooltip.set_text(f"{name}\n{x.strftime('%Y-%m-%d')}\n{format_price(y)}")
                    tooltip.set_visible(True)
                    fig.canvas.draw_idle()
                    return

            tooltip.set_visible(False)
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", on_hover)

        # X-AXIS = YEAR ONLY
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

        # Y-AXIS formatting
        ax.set_ylabel("Price ($)")
        ax.get_yaxis().set_major_formatter(
            plt.FuncFormatter(lambda v, _: f"${v:,.0f}")
        )

        # Final Styling
        plt.title(payload["title"])
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Embed figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Toolbar under the chart (zoom, pan, etc.)
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        # Do NOT re-pack the canvas again here (avoids duplicate widgets)


# ======================================================
# PAGE 5 — CSV Import
# ======================================================
class PageCSV_Import(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(
            self, text="← Back",
            command=lambda: controller.show_frame(HomePage)
        ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(self, text="Import CSV",
                  font=("Arial", 18, "bold")).pack()

        # Instructions for this screen
        ttk.Label(
            self,
            text=(
                "Use this screen to open and inspect any CSV file.\n"
                "If the CSV matches your portfolio format (e.g., tickers and share counts), "
                "it will also become the active portfolio file used in Option 3."
            ),
            wraplength=700,
            foreground="gray30",
            justify="left"
        ).pack(padx=10, pady=(0, 10))

        ttk.Button(self, text="Choose CSV File",
                   command=self.choose_csv).pack(pady=12)

        self.output = tk.Text(self, width=90, height=20)
        self.output.pack()

    def choose_csv(self):
        path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return

        try:
            df = self.controller.sc.import_csv(path)

            # Update SystemController so portfolio dashboard uses this new CSV
            self.controller.sc.set_portfolio_csv(path)

            text = (
                f"CSV Loaded Successfully!\n\n"
                f"File: {os.path.basename(path)}\n"
                f"Rows: {len(df)}\n"
                f"Columns: {list(df.columns)}\n\n"
                f"Preview (First 5 Rows):\n{df.head().to_string()}\n\n"
                "This file is now set as the active portfolio CSV for the Portfolio Dashboard (Option 3)."
            )
        except Exception as e:
            text = f"Error importing CSV:\n{e}"

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)


# ======================================================
# PAGE 6 — Export Last Analysis
# ======================================================
class PageExport(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(
            self, text="← Back",
            command=lambda: controller.show_frame(HomePage)
        ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(
            self, text="Export Last Analysis",
            font=("Arial", 18, "bold")
        ).pack()

        # Instructions for this screen
        ttk.Label(
            self,
            text=(
                "This screen lets you export the most recent stock analysis (from Option 1) "
                "as a JSON file.\nChoose a save location and filename, and the app will "
                "save a structured report that you can open later or share."
            ),
            wraplength=700,
            foreground="gray30",
            justify="left"
        ).pack(padx=10, pady=(0, 10))

        ttk.Button(
            self, text="Export to JSON",
            command=self.export_json
        ).pack(pady=12)

        self.status = tk.Label(self, text="", fg="green")
        self.status.pack()

    # Export JSON with Save-As dialog
    def export_json(self):
        if not self.controller.last_payload:
            messagebox.showerror("Error", "No analysis available to export.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Analysis Report"
        )

        if not save_path:
            return

        try:
            self.controller.sc.export_analysis(self.controller.last_payload, save_path)
            self.status.config(text=f"Exported to:\n{save_path}")

            # Auto-open after saving
            if platform.system() == "Windows":
                os.startfile(save_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", save_path])
            else:
                subprocess.call(["xdg-open", save_path])

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ======================================================
# Run App
# ======================================================
if __name__ == "__main__":
    app = StockApp()
    app.mainloop()











