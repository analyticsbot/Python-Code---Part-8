from selenium import webdriver
from text_unidecode import unidecode
import re
import multiprocessing
from datetime import datetime
from threading import Thread

productIds = ['92800', '92795', '92794', '92793', '92790', '92789', '92788', '92784', '92783', '92782', '92779', '92778', '92777', '92774', '92773', '92772', '92771', '92770', '92769', '92764', '92763', '92762', '92761', '92760', '92759', '92758', '92757', '92756', '92755', '92754', '92753', '92752', '92751', '92744', '92743', '92742', '92741', '92740']

url = '''http://shop.tcgplayer.com/productcatalog/product/getpricetable?pageSize=50\
            &productId={productId}&ConditionId=25&gameName=yugioh&page={page}'''
num_threads = 5

def getJson(pids, url):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", 'http://manutd0707:vbym5o5r80uvaer@s-fl.proxymesh.com')
    profile.set_preference("network.proxy.http_port", "31280")
    profile.update_preferences()
    driver =webdriver.Firefox(firefox_profile=profile)
    for pid in pids:
        page = 1
        while True:
            url1 = url.replace('{productId}', pid).replace('{page}', page)
            driver.get(url1)
            ss = unidecode(driver.page_source)
            dd = re.findall(r'priceTableData\"\>\[({.*?})\]\</td\>\</tr\>', ss)
            if len(dd)==0:
                break
            f = open(pid+'_'+str(page)+'.txt', 'wb')
            f.write(dd[0])
            f.close()
            page+=1
    driver.close()

def split(a, n):
    k, m = len(a) / n, len(a) % n
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))


distributed_data = list(split(productIds, num_threads))
threads = []
for i in range(num_threads):
    data_thread = distributed_data[i]
    threads.append(Thread(target = getJson, args=(data_thread, url, )))

j=1
for thread in threads:
    print 'starting scraper ##', j
    j+=1
    thread.start()
    time.sleep(2)

for thread in threads:
    thread.join()
