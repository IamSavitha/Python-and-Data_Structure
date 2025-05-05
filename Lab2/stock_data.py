from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import datetime
import csv

# DailyData stores individual stock data points
class DailyData:
    def __init__(self, date, close, volume):
        self.date = date
        self.close = close
        self.volume = volume

# Stock holds a list of DailyData entries
class Stock:
    def __init__(self, symbol,shares):
        self.symbol = symbol
        self.shares = shares
        self.history = []

    def add_data(self, daily_data):
        self.history.append(daily_data)

    @staticmethod
    def retrieve_stock_web(date_start, date_end, stock_list):
        period1 = int(time.mktime(time.strptime(date_start, "%m/%d/%y")))
        period2 = int(time.mktime(time.strptime(date_end, "%m/%d/%y")))

        # Setup Chrome options for Selenium
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

            time.sleep(5)  # Allow full page to load
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
                    except Exception as e:
                        continue  # Skip malformed row

# Import historical stock data from a CSV file
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
        next(datareader)  # Skip header row

        for row in datareader:
            try:
                date = row[0].strip()
                close = float(row[4].strip().replace(",", ""))
                volume = int(row[6].strip().replace(",", ""))
                daily_data = DailyData(date, close, volume)
                target_stock.add_data(daily_data)
            except Exception:
                continue  # Skip malformed row
