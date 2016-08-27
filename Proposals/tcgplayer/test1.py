from selenium import webdriver
import time
from selenium.webdriver.common.proxy import *

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", "http://manutd0707:vbym5o5r80uvaer@us-fl.proxymesh.com")
profile.set_preference("network.proxy.http_port", "31280")
profile.update_preferences()
##import requests
##auth = requests.auth.HTTPProxyAuth('manutd0707', 'vbym5o5r80uvaer')
##proxies = {'http': 'http://us-fl.proxymesh.com:31280'}
###response = requests.get('http://icanhazip.com', proxies=proxies, auth=auth)
##print response.text


driver = webdriver.Firefox(firefox_profile=profile)

#driver = webdriver.Firefox()
driver.get('http://www.whatismyipaddress.org/')

##time.sleep(5)
##
##myProxy = "http://manutd0707:vbym5o5r80uvaer@us-fl.proxymesh.com:31280"
##
##proxy = Proxy({
##    'proxyType': ProxyType.MANUAL,
##    'httpProxy': myProxy,
##    'ftpProxy': myProxy,
##    'sslProxy': myProxy,
##    'noProxy': None,
##    "autodetect":False
##    })
##
##driver = webdriver.Firefox(proxy=proxy)
##driver.get('http://www.whatismyipaddress.org/')
