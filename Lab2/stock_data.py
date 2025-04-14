def retrieve_stock_web(dateStart, dateEnd, stock_list):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time
