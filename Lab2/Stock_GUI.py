import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog , StringVar, OptionMenu
from stock_data import *
#Stock, DailyData,get_current_price, retrieve_stock_web, import_stock_web_csv, save_data_to_database, load_data_from_database, download_retrived_csv
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil import parser 

class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("STOCK MANAGEMENT AND ANALYSER SYSTEM")
        self.geometry("1000x600")
        self.stocks = []
        self.current_frame = None
        self.transactions = []
        self.show_welcome_screen()

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack()

    def show_welcome_screen(self):
        self.show_frame(WelcomeFrame)

    def show_main_menu(self):
        self.show_frame(MainMenuFrame)

    def show_manage_stocks_menu(self):
        self.show_frame(ManageStocksMenuFrame)

    def show_add_stock_screen(self):
        self.show_frame(AddStockFrame)

    def show_update_stock_screen(self):
        self.show_frame(UpdateStockFrame)

    def show_delete_stock_screen(self):
        self.show_frame(DeleteStockFrame)

    def show_list_stock_screen(self):
        self.show_frame(ListStockFrame)

    def show_add_daily_data(self):
        self.show_frame(AddDailyDataFrame)

    def show_manage_data_menu(self):
        self.show_frame(ManageDataFrame)

    def show_retrive_data_menu(self):
        self.show_frame(RetrieveWebFrame)
    
    def show_transaction_report(self):
        self.show_frame(TransactionReportFrame)
    
    def show_chart(self):
        self.show_frame(ChartFrame)

    def add_stock(self, symbol, shares):
        if any(s.symbol == symbol for s in self.stocks):
            messagebox.showerror("Error", "Stock already exists.")
            return
        try:
            shares = int(shares)
            self.stocks.append(Stock(symbol, shares))
            messagebox.showinfo("Success", "Stock added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Shares must be an integer.")

    def update_stock(self, symbol, shares, operation):
        for stock in self.stocks:
            if stock.symbol == symbol:
                try:
                    shares = int(shares)
                    price = get_current_price(symbol) 
                    date = datetime.now().strftime("%m/%d/%y")
                    
                    if operation == "BUY":
                        stock.shares += shares
                    elif operation == "SELL":
                        if stock.shares >= shares:
                            stock.shares -= shares
                        else:
                            messagebox.showerror("Error", "Insufficient shares to sell.")
                            return
                    # Log transaction
                    self.transactions.append(Transaction(date, symbol, operation, shares, price))
                    messagebox.showinfo("Success", f"{operation} {shares} shares of {symbol} at ${price} per share, total cost: ${shares * price}.")
                    return
                except ValueError:
                    messagebox.showerror("Error", "Invalid number of shares.")
                    return
        messagebox.showerror("Error", "Stock not found.")


    def list_stocks(self):
        if not self.stocks:
            return "No stocks available."
        return "\n".join(f"{s.symbol}: {s.shares} shares" for s in self.stocks)

class WelcomeFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Welcome to Stock Management System", font=("Arial", 16)).pack(pady=50)
        tk.Button(self, text="Start", command=master.show_main_menu).pack(pady=20)

class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Main Menu", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="1. Manage Stocks", command=master.show_manage_stocks_menu).pack(pady=10)
        tk.Button(self, text="2. Add Daily Data", command=master.show_add_daily_data).pack(pady=10)
        tk.Button(self, text="3. Manage Data", command=master.show_manage_data_menu).pack(pady=10)
        tk.Button(self, text="4. Show Report", command=master.show_transaction_report).pack(pady=10)
        tk.Button(self, text="5. Show Chart", command=master.show_chart).pack(pady=10)
        tk.Button(self, text="Exit", command=master.destroy).pack(pady=10)

class ManageStocksMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Manage Stocks", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Add Stock", command=master.show_add_stock_screen).pack(pady=10)
        tk.Button(self, text="Update Stock", command=master.show_update_stock_screen).pack(pady=10)
        tk.Button(self, text="Delete Stock", command=master.show_delete_stock_screen).pack(pady=10)
        tk.Button(self, text="List Stocks", command=master.show_list_stock_screen).pack(pady=10)
        tk.Button(self, text="Back", command=master.show_main_menu).pack(pady=10)

class AddStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Add Stock", font=("Arial", 14)).pack(pady=10)
        tk.Label(self, text="SYMBOL", font=("Arial", 12)).pack(pady=10)
        self.symbol = tk.Entry(self)
        self.symbol.pack()
        tk.Label(self, text="SHARE", font=("Arial", 12)).pack(pady=10)
        self.shares = tk.Entry(self)
        self.shares.pack()
        tk.Button(self, text="Add", command=self.add).pack(pady=10)
        tk.Button(self, text="Back", command=master.show_manage_stocks_menu).pack()

    def add(self):
        self.master.add_stock(self.symbol.get().upper(), self.shares.get())

class UpdateStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Update Stock", font=("Arial", 14)).pack(pady=10)
        tk.Label(self, text="SYMBOL", font=("Arial", 12)).pack(pady=10)
        self.symbol = tk.Entry(self)
        self.symbol.pack()
        tk.Label(self, text="SHARE", font=("Arial", 12)).pack(pady=10)
        self.shares = tk.Entry(self)
        self.shares.pack()
        tk.Button(self, text="Buy", command=lambda: self.update("BUY")).pack(pady=5)
        tk.Button(self, text="Sell", command=lambda: self.update("SELL")).pack(pady=5)
        tk.Button(self, text="Back", command=master.show_manage_stocks_menu).pack()

    def update(self, operation):
        self.master.update_stock(self.symbol.get().upper(), self.shares.get(), operation)

class DeleteStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Delete Stock", font=("Arial", 14)).pack(pady=10)
        self.symbol = tk.Entry(self)
        self.symbol.pack()
        tk.Button(self, text="Delete", command=self.delete).pack(pady=10)
        tk.Button(self, text="Back", command=master.show_manage_stocks_menu).pack()

    def delete(self):
        self.master.delete_stock(self.symbol.get().upper())

class ListStockFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Stock List", font=("Arial", 14)).pack(pady=10)
        self.text = tk.Text(self, height=15, width=50)
        self.text.pack()
        self.text.insert("1.0", master.list_stocks())
        tk.Button(self, text="Back", command=master.show_manage_stocks_menu).pack(pady=10)

class AddDailyDataFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Add Daily Data", font=("Arial", 14)).pack(pady=10)
        self.symbol = tk.Entry(self)
        self.symbol.pack()
        self.data = tk.Entry(self)
        self.data.pack()
        tk.Button(self, text="Add", command=self.add_data).pack(pady=10)
        tk.Button(self, text="Back", command=master.show_main_menu).pack()

    def add_data(self):
        symbol = self.symbol.get().upper()
        for stock in self.master.stocks:
            if stock.symbol == symbol:
                try:
                    date, close, volume = self.data.get().split(",")
                    stock.add_data(DailyData(date.strip(), float(close.strip()), int(volume.strip())))
                    messagebox.showinfo("Success", "Daily data added.")
                    return
                except Exception:
                    messagebox.showerror("Error", "Invalid format. Use: mm/dd/yy,price,volume")
                    return
        messagebox.showerror("Error", "Stock not found.")

class ManageDataFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Manage Data", font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Save Data", command=lambda: save_data_to_database(master.stocks)).pack(pady=5)
        tk.Button(self, text="Load Data", command=self.load_data).pack(pady=5)
        tk.Button(self, text="Import CSV", command=self.import_csv).pack(pady=5)
        tk.Button(self, text="Retrieve from Web", command=master.show_retrive_data_menu).pack(pady=5)
        tk.Button(self, text="Back", command=master.show_main_menu).pack(pady=10)

    
    def load_data(self):
        self.master.stocks = load_data_from_database()
        messagebox.showinfo("Loaded", "Data loaded successfully.")

    def import_csv(self):
        filename = filedialog.askopenfilename()
        symbol = simpledialog.askstring("Symbol", "Enter stock symbol:")
        import_stock_web_csv(self.master.stocks, symbol.upper(), filename)
        messagebox.showinfo("Imported", "Data imported successfully.")

class RetrieveWebFrame(tk.Frame): 
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Retrieve Data from Web", font=("Arial", 14)).pack(pady=10)
        tk.Label(self, text="Symbol (e.g., MSFT):").pack()
        self.symbol_entry = tk.Entry(self)
        self.symbol_entry.pack()

        tk.Label(self, text="Start Date (mm/dd/yy):").pack()
        self.start_entry = tk.Entry(self)
        self.start_entry.pack()

        tk.Label(self, text="End Date (mm/dd/yy):").pack()
        self.end_entry = tk.Entry(self)
        self.end_entry.pack()

        self.result_label = tk.Label(self, text="Count : ", font=("Arial", 12))
        self.result_label.pack(pady=5)

        tk.Button(self, text="Retrieve", command=self.retrieve_data).pack(pady=10)
        tk.Button(self, text="Download CSV", command=self.download_csv).pack(pady=5)
        tk.Button(self, text="Back", command=master.show_manage_data_menu).pack()

    def retrieve_data(self):
        symbol = self.symbol_entry.get().upper()
        start = self.start_entry.get()
        end = self.end_entry.get()
        target_stock = next((s for s in self.master.stocks if s.symbol == symbol), None)

        if not target_stock:
            target_stock = Stock(symbol, 0)  
            self.master.stocks.append(target_stock)

        try:
            old_len = len(target_stock.history)
            retrieve_stock_web(start, end, [target_stock])
            new_len = len(target_stock.history)
            count = new_len - old_len
            
             # Show sample retrieved data in console
            print(f"[INFO] Retrieved {count} new records for {symbol}")
            for d in target_stock.history[-5:]:  # Show last 5 for quick check
                 print(f"Date: {d.date}, Close: {d.close}, Volume: {d.volume}")

            
            self.result_label.config(text=f"Records Retrieved: {count}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}")

    def download_csv(self):
        symbol = self.symbol_entry.get().upper()
        if download_retrived_csv(self.master.stocks, symbol):
            messagebox.showinfo("Downloaded", f"{symbol}_retrieved.csv saved.")
        else:
            messagebox.showerror("Error", "Stock not found.")

class Transaction:
    def __init__(self, date, symbol, action, shares, price):
        self.date = date
        self.symbol = symbol
        self.action = action  # "BUY" or "SELL"
        self.shares = shares
        self.price = price

class TransactionReportFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Transaction Report", font=("Arial", 16)).pack(pady=10)

        self.text = tk.Text(self, height=20, width=70)
        self.text.pack()

        tk.Button(self, text="Show Report", command=self.show_report).pack(pady=5)
        tk.Button(self, text="Back", command=master.show_main_menu).pack(pady=10)

    def show_report(self):
        self.text.delete("1.0", tk.END)
        if not self.master.transactions:
            self.text.insert(tk.END, "No transactions yet.")
            return
        self.text.insert(tk.END, f"Date\tSymbol\tAction\tShares\tPrice\n")
        self.text.insert(tk.END, "-"*60 + "\n")
        for t in self.master.transactions:
            self.text.insert(tk.END, f"{t.date}\t{t.symbol}\t{t.action}\t{t.shares}\t${t.price}\n")

class ChartFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Chart", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self, text="Select Symbol:").pack()
        self.symbol_var = StringVar()
        self.symbol_var.set("Select...")  # Default value

        # Populate dropdown
        symbols = [s.symbol for s in master.stocks]
        if not symbols:
            symbols = ["No data"]
        self.dropdown = OptionMenu(self, self.symbol_var, *symbols)
        self.dropdown.pack(pady=5)

        tk.Button(self, text="Generate Chart", command=self.create_chart).pack(pady=5)
        
        tk.Button(self, text="Back", command=master.show_main_menu).pack(pady=10)

    def create_chart(self):
        symbol = simpledialog.askstring("Stock Symbol", "Enter stock symbol to chart:")
        #symbol = symbols
        if not symbol:
            return
        print("i am running till here ")
        matched = next((s for s in self.master.stocks if s.symbol.upper() == symbol.upper()), None)
        if not matched or not matched.history:
            messagebox.showerror("Chart Error", f"No data found for symbol '{symbol}'")
            return

        try:
            print("i am here ")
            sorted_data = sorted(matched.history, key=lambda x: parser.parse(x.date))
            print("i am also here ")
            dates = [parser.parse(d.date) for d in sorted_data]
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
    app = StockApp()
    app.mainloop()
