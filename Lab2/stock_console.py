import stock_data
from stock_data import Stock
import matplotlib.pyplot as plt

stock_list = []

def main_menu():
    while True:
        print("\n===== Stock Analysis Console =====")
        print("1 - Manage Stocks")
        print("2 - Add Daily Stock Data (Manual)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit")
        choice = input("Enter option: ")

        if choice == '1':
            manage_stocks()
        elif choice == '2':
            add_daily_data()
        elif choice == '3':
            show_report()
        elif choice == '4':
            show_chart()
        elif choice == '5':
            manage_data()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Try again.")

def manage_stocks():
    while True:
        print("\n--- Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Back")
        choice = input("Enter option: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            stock_list.append(Stock(symbol, shares))
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            for stock in stock_list:
                if stock.symbol == symbol:
                    shares = int(input("Enter new number of shares: "))
                    stock.shares = shares
                    break
            else:
                print("Stock not found.")
        elif choice == '3':
            symbol = input("Enter stock symbol to delete: ").upper()
            stock_list[:] = [s for s in stock_list if s.symbol != symbol]
        elif choice == '4':
            for stock in stock_list:
                print(f"{stock.symbol} - {stock.shares} shares")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

def add_daily_data():
    symbol = input("Enter stock symbol: ").upper()
    date = input("Enter date (m/d/yy): ")
    price = float(input("Enter closing price: "))
    volume = int(input("Enter volume: "))
    for stock in stock_list:
        if stock.symbol == symbol:
            stock.add_price(date, price, volume)
            print("Data added.")
            return
    print("Stock not found.")

def show_report():
    for stock in stock_list:
        print(f"\n--- {stock.symbol} Report ---")
        for record in stock.history:
            print(f"{record.date} | Close: {record.close} | Volume: {record.volume}")

def show_chart():
    symbol = input("Enter stock symbol to chart: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            dates = [data.date for data in stock.history]
            prices = [data.close for data in stock.history]
            plt.plot(dates, prices)
            plt.title(f"{symbol} Price History")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            return
    print("Stock not found.")

def manage_data():
    while True:
        print("\n--- Manage Data ---")
        print("1 - Load from DB")
        print("2 - Save to DB")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV")
        print("0 - Back")
        choice = input("Enter option: ")

        if choice == '3':
            symbol = input("Enter stock symbol: ").upper()
            date_start = input("Enter start date (m/d/yy): ")
            date_end = input("Enter end date (m/d/yy): ")
            stock_obj = next((s for s in stock_list if s.symbol == symbol), None)
            if stock_obj:
                stock_data.retrieve_stock_web(date_start, date_end, [stock_obj])
                print("Data retrieved from web.")
            else:
                print("Stock not found in portfolio. Please add it first.")
        elif choice == '4':
            symbol = input("Enter stock symbol: ").upper()
            filename = input("Enter full path to CSV file: ")
            stock_data.import_stock_web_csv(stock_list, symbol, filename)
            print("CSV data imported.")
        elif choice == '1':
            print("TODO: Load from database.")
        elif choice == '2':
            print("TODO: Save to database.")
        elif choice == '0':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
