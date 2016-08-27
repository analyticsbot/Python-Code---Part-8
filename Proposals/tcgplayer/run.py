from selenium import webdriver
from text_unidecode import unidecode
import re
import multiprocessing

driver =webdriver.FireFox()

productIds = ['92800', '92795', '92794', '92793', '92790', '92789', '92788', '92784', '92783', '92782', '92779', '92778', '92777', '92774', '92773', '92772', '92771', '92770', '92769', '92764', '92763', '92762', '92761', '92760', '92759', '92758', '92757', '92756', '92755', '92754', '92753', '92752', '92751', '92744', '92743', '92742', '92741', '92740']

url = '''http://shop.tcgplayer.com/productcatalog/product/getpricetable?pageSize=50\
            &productId={productId}&ConditionId=25&gameName=yugioh&page={page}'''


for pid in productIds:
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
        

def mp_worker((inputs, the_time)):
    print " Processs %s\tWaiting %s seconds" % (inputs, the_time)
    time.sleep(int(the_time))
    print " Process %s\tDONE" % inputs

def mp_handler():
    p = multiprocessing.Pool(2)
    p.map(mp_worker, data)

if __name__ == '__main__':
    mp_handler()
