from selenium import webdriver
from threading import Thread
from text_unidecode import unidecode

f = open('2k.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]
num_threads = 16

def split(a, n):
    """Function to split data evenly among threads"""
    k, m = len(a) / n, len(a) % n
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
            for i in xrange(n))

def downloadHTML(data_thread):
    for url in data_thread:
        driver.get(url)
        f = open(url+'.txt', 'wb')
        f.write(unidecode(driver.page_source))
        f.close()

distributed_ids = list(split(data, num_threads))

threads = []
drivers = []
for i in range(num_threads):
    data_thread = distributed_ids[i]
    driver = webdriver.Firefox()
    drivers.append(driver)
    threads.append(
        Thread(
            target=downloadHTML,
            args=(
                i + 1,
                data_thread,
                driver,
            )))

for thread1 in threads:
    thread1.start()
