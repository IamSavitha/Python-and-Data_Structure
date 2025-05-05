import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import stock_data
from datetime import datetime
import matplotlib.pyplot as plt
from stock_data import Stock, import_stock_web_csv
import csv
import os


class StockGUI:
    def __init__(self, master,stock_list):
        self.root = root
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True)
        self.root.title("Stock Data GUI")
        self.root.geometry("600x400")
    

        self.master = master
        self.master.title("Stock Portfolio Manager")
        self.stock_list = []  # Should be assigned externally or populated somehow

        # Create menu bar
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        self.webmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Web", menu=self.webmenu)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV From Yahoo! Finance", command=self.importCSV_web_data)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        # History tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="History")

        # Report tab
        self.report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.report_frame, text="Report")

        # Label placeholders
        self.history_label = tk.Label(self.history_frame, text="History Data Appears Here")
        self.history_label.pack()

        self.report_label = tk.Label(self.report_frame, text="Report Summary Appears Here")
        self.report_label.pack()

        # Listbox for stocks
        self.stockList = tk.Listbox(master)
        self.stockList.pack(side=tk.LEFT, fill=tk.Y)

                # Stock selection list
        self.stockList = tk.Listbox(self.main_frame, height=5)
        for stock in self.stock_list:
            self.stockList.insert(tk.END, stock.symbol)
        self.stockList.pack(pady=10)

        # Main buttons
        tk.Button(self.main_frame, text="Scrape Data", width=20, command=self.scrape_web_data).pack(pady=10)
        tk.Button(self.main_frame, text="Create Chart", width=20, command=self.create_chart).pack(pady=10)
        tk.Button(self.main_frame, text="CSV file", width=20, command=self.importCSV_web_data).pack(pady=10)
        
        tk.Button(self.main_frame, text="Exit", width=20, command=self.root.quit).pack(pady=10)

    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")

        try:
            stock_data.Stock.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
        except Exception:
            messagebox.showerror("Cannot Get Data from Web", "Check Path for Chrome Driver")
            return

        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", "Data Retrieved")

    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(
            title="Select " + symbol + " File to Import",
            filetypes=[('Yahoo Finance! CSV', '*.csv')]
        )

        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")

    def display_stock_data(self):
        # Clear previous content
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        # Display in History tab
        for stock in self.stock_list:
            tk.Label(self.history_frame, text=f"--- {stock.symbol} ---").pack()
            for data in stock.DataList:
                text = f"Date: {data.date}, Close: {data.close}, Volume: {data.volume}"
                tk.Label(self.history_frame, text=text).pack(anchor='w')

        # Display in Report tab (simple summary)
        for stock in self.stock_list:
            if stock.DataList:
                closes = [d.close for d in stock.DataList]
                volumes = [d.volume for d in stock.DataList]
                summary = f"{stock.symbol} → Min: {min(closes):.2f}, Max: {max(closes):.2f}, Avg Volume: {sum(volumes)//len(volumes)}"
                tk.Label(self.report_frame, text=summary).pack(anchor='w')
        
        
    def create_chart(self):
        symbol = simpledialog.askstring("Stock Symbol", "Enter stock symbol to chart:")
        #symbol = symbols
        if not symbol:
            return

        matched = next((s for s in self.stock_list if s.symbol.upper() == symbol.upper()), None)
        if not matched or not matched.DataList:
            messagebox.showerror("Chart Error", f"No data found for symbol '{symbol}'")
            return

        try:
            sorted_data = sorted(matched.DataList, key=lambda x: datetime.strptime(x.date, "%b %d, %Y"))
            dates = [datetime.strptime(d.date, "%b %d, %Y") for d in sorted_data]
            closes = [d.close for d in sorted_data]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, closes, marker='o')
            plt.title(f"{symbol.upper()} Closing Prices")
            plt.xlabel("Date")
            plt.ylabel("Close Price ($)")
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Chart Error", f"Error generating chart: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    #app = StockGUI(root)
    #root.mainloop()

    symbol_input = simpledialog.askstring(
        "Stock Symbols", "Enter stock symbols separated by commas (e.g., AAPL, MSFT, GOOG):"
    )

    if symbol_input:
        symbols = [s.strip().upper() for s in symbol_input.split(",") if s.strip()]
        stock_list = [Stock(symbol) for symbol in symbols]
        root.deiconify()  # Show the main window now
        app = StockGUI(root, stock_list)
        root.mainloop()
    else:
        print("No symbols entered. Exiting.")