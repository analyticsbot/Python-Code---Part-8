

from selenium import webdriver
import time

fp = webdriver.FirefoxProfile("C:/Users/Luka Stevanov/Application Data/Mozilla/Firefox/Profiles/qumo42ba.default")

browser = webdriver.Firefox(fp, proxy=None)
browser.get("https://sfbay.craigslist.org/eby/boa/5198833412.html")
time.sleep(1)
browser.get("http://google.com")

