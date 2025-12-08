s Page4_Plot(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Button(
            self, text="← Back",
            command=lambda: controller.show_frame(HomePage)
        ).pack(anchor="w", padx=10, pady=10)

        ttk.Label(
            self, text="Plot Stock Chart",
            font=("Arial", 18, "bold")
        ).pack()

        ttk.Button(self, text="Show Chart", command=self.plot_chart).pack(pady=12)

    def plot_chart(self):
        payload = self.controller.last_payload
        if not payload:
            messagebox.showerror("Error", "Run Option 1 first.")
            return

        # Retrieve chart data
        prices = payload["datasets"][0]["data"]
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in payload["labels"]]
        anomalies = payload.get("anomalies", [])

        fig, ax = plt.subplots(figsize=(10, 5))

        # Price line
        ax.plot(dates, prices, label="Price", color="blue", linewidth=1.5)

        # Plot indicators
        for name, series in payload["indicators"].items():
            ax.plot(dates, series, label=name)

        # -----------------------------------------
        # Plot anomaly dots (anomalies = list of int)
        # -----------------------------------------
        anomaly_x = []
        anomaly_y = []

        for idx in anomalies:
            if isinstance(idx, int) and 0 <= idx < len(dates):
                anomaly_x.append(dates[idx])
                anomaly_y.append(prices[idx])

        if anomaly_x:
            ax.scatter(
                anomaly_x,
                anomaly_y,
                color="red",
                s=50,
                label="Anomaly",
                zorder=5
            )

        # Format x-axis dates
        locator = mdates.AutoDateLocator()
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

        plt.title(payload["title"])
        plt.xlabel("Date")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()