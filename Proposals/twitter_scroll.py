from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.implicitly_wait(30)
url = "https://twitter.com"

driver.get(url + "/search?q=narendra+modi")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    html_source = driver.page_source
    data = html_source.encode('utf-8')

