
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import datetime
import csv
import pandas as pd
import os
import pickle
import yfinance as yf
import requests

class DailyData:
    def __init__(self, date, close, volume):
        self.date = date
        self.close = close
        self.volume = volume

class Stock:
    def __init__(self, symbol, shares):
        self.symbol = symbol
        self.shares = shares
        self.history = []

    def add_data(self, daily_data):
        self.history.append(daily_data)

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "shares": self.shares,
            "history": [(d.date, d.close, d.volume) for d in self.history]
        }

    def from_dict(data):
        stock = Stock(data["symbol"], data["shares"])
        for date, close, volume in data["history"]:
            stock.add_data(DailyData(date, close, volume))
        return stock

def retrieve_stock_web(date_start, date_end, stock_list):
    period1 = int(time.mktime(time.strptime(date_start, "%m/%d/%y")))
    period2 = int(time.mktime(time.strptime(date_end, "%m/%d/%y")))

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

    for stock in stock_list:
        symbol = stock.symbol
        url = f"https://finance.yahoo.com/quote/{symbol}/history?period1={period1}&period2={period2}&interval=1d&filter=history&frequency=1d"

        try:
            service = Service("./chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except Exception as e:
            raise RuntimeWarning("Chrome Driver Not Found or Error Opening Browser")

        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 7:
                try:
                    date = cols[0].text.strip()
                    close = float(cols[5].text.strip().replace(",", ""))
                    volume = int(cols[6].text.strip().replace(",", ""))
                    daily_data = DailyData(date, close, volume)
                    stock.add_data(daily_data)
                except Exception:
                    continue

def download_retrived_csv(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            data = [{
                "symbol": stock.symbol,
                'Date': d.date,
                'Close': d.close,
                'Volume': d.volume
            } for d in stock.history]
            df = pd.DataFrame(data)
            df.to_csv(f"{symbol}_retrieved.csv", index=False)
            return True
    return False

def import_stock_web_csv(stock_list, symbol, filename):
    target_stock = None
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            target_stock = stock
            break

    if not target_stock:
        raise ValueError(f"Stock symbol '{symbol}' not found in stock list.")

    with open(filename, "r") as file:
        datareader = csv.reader(file, delimiter=",")
        next(datareader)
        for row in datareader:
            try:
                date = row[0].strip()
                close = float(row[1].strip().replace(",", ""))
                volume = int(row[2].strip().replace(",", ""))
                daily_data = DailyData(date, close, volume)
                target_stock.add_data(daily_data)
            except Exception:
                continue

def save_data_to_database(stock_list, filename="stocks_db.pkl"):
    data = [stock.to_dict() for stock in stock_list]
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data_from_database(filename="stocks_db.pkl"):
    if not os.path.exists(filename):
        return []
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return [Stock.from_dict(stock_data) for stock_data in data]

def get_current_price(symbol): 
    API_KEY = "N9LNZ3Q3I1QALQOV"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        print(f"[DEBUG] Full Alpha Vantage response: {data}")

        if "Global Quote" not in data or "05. price" not in data["Global Quote"]:
            print(f"[ERROR] API price fetch failed or empty for symbol: {symbol}")
            return 0.0

        price = float(data["Global Quote"]["05. price"])
        return round(price, 2)

    except Exception as e:
        print(f"[ERROR] API price fetch failed: {e}")
        return 0.0
