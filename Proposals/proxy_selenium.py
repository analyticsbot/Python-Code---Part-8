from selenium import webdriver
import time
from selenium.webdriver.common.proxy import *

driver = webdriver.Firefox()
driver.get('http://www.whatsmyip.org/')

time.sleep(5)
##
##PROXY= '203.156.126.38:8080'
##webdriver.DesiredCapabilities.FIREFOX['proxy']={
##    "httpProxy":PROXY,
##    "ftpProxy":PROXY,
##    "sslProxy":PROXY,
##    "noProxy":None,
##    "proxyType":"MANUAL",
##    "autodetect":False
##}
##driver = webdriver.Firefox(proxy=PROXY)
##driver.get('http://www.whatsmyip.org/')

myProxy = "203.156.126.38:8080"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': None,
    "autodetect":False
    })

driver = webdriver.Firefox(proxy=proxy)
driver.get('http://www.whatsmyip.org/')
