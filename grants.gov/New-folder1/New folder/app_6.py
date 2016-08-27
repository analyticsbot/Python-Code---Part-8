# import the Flask class from the flask module and other required modules
from bs4 import BeautifulSoup
import requests, threading, re, os, Queue, logging, gc, json,time
from random import choice 
from threading import Thread
from text_unidecode import unidecode      
from logging import FileHandler
from amazon.api import AmazonAPI
from selenium import webdriver
import pandas as pd
from amazon_api_data import *

def getAmazonProducts(searchterm, driver, pg_max =2):
    url = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + '+'.join(searchterm.split())
    pg_num = 1
    #driver = webdriver.Firefox()
    prod = {}
    
    count = 0
    continue_ = True
    while continue_:
             
        if pg_num == 1:
            url = url
            pg_num += 1
        else:
            if pg_num == pg_max + 1:
                break
            url = 'http://www.amazon.com/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(searchterm.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(searchterm.split())
            pg_num += 1

        # retreived the response and pass to beautifulsoup
        driver.get(url)
        
        # get all the products on the search page
        elements = driver.find_elements_by_css_selector('.s-result-item.celwidget')        

        # loop through the elements and get title, url, price_old, price_new, image url, asin and add to a dict object
        for elem in elements:
            print count   
            count +=1
            if count==16:
                continue_ = False
                break
            
            try:
                title = elem.find_element_by_css_selector('.a-size-medium.a-color-null.s-inline.s-access-title.a-text-normal').text
            except Exception,e:
                try:
                    title = elem.find_element_by_css_selector('.a-link-normal.s-access-detail-page.a-text-normal').text
                except:
                    title = 'NA'
            try:
                url = elem.find_element_by_css_selector('.a-link-normal.s-access-detail-page.a-text-normal').get_attribute('href')
            except Exception,e:
                url = 'NA'
            try:
                price_old = re.findall(r'\d+.\d+', elem.find_element_by_css_selector('.a-size-small.a-color-secondary.a-text-strike').text)[0]
            except Exception,e:
                price_old = 'NA'
            
            try:
                image = elem.find_element_by_css_selector('.s-access-image.cfMarker').get_attribute('src')
            except Exception,e:
                image = 'NA'
                
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                asin =  'NA'
            try:
                price_new = re.findall(r'\d+.\d+', elem.find_element_by_css_selector('.a-size-base.a-color-price.s-price.a-text-bold').text)[0]
            except Exception,e:
                try:
                    product = amazon.lookup(ItemId=unidecode(asin))
                    price_new = str(product.price_and_currency[0])
                    if price_new is not None:
                        price_new = price_new
                    else:
                        price_new = 'NA'
                except:
                    try:
                        product = amazon1.lookup(ItemId=unidecode(asin))
                        price_new = str(product.price_and_currency[0])
                        if price_new is not None:
                            price_new = price_new
                        else:
                            price_new = 'NA'
                    except:
                        try:
                            price_new = re.findall(r'\d+.\d+', elem.find_element_by_css_selector('.a-color-price').text)[0]
                        except:
                            price_new = 'NA'

            try:
                y = elem.find_elements_by_tag_name('a')
                num_reviews = y[-1].text
            except:
                num_reviews = 'NA'

            prod['product' + str(count)] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                       'asin': asin, 'num_reviews':num_reviews}
            
            
    #driver.close()        
    return prod

def getElement(product_details, element):    
    for product_detail in product_details:
        name = product_detail.find_element_by_tag_name('th').text.strip()
        if name == element:
            return product_detail.find_element_by_tag_name('td').text.strip()
        
def getSKUData(amazon, driver, prod, queue):
    data = []
    asin = (prod['asin'])
    image = prod['image']
    title = prod['title']
    price = prod['price_new'].replace(',','.')
    num_reviews = prod['num_reviews']
    url = 'http://www.amazon.com/dp/' + unidecode(asin)    
    
    #driver = webdriver.Firefox()
    driver.get(url)
    try:
        product = amazon.lookup(ItemId=unidecode(asin))
    except:
        pass
    
    try:
        product_details = driver.find_element_by_id('productDetails_techSpec_section_1').find_elements_by_tag_name('tr')
    except:
        product_details = []
    try:
        product_details += driver.find_element_by_id('productDetails_detailBullets_sections1').find_elements_by_tag_name('tr')
    except:
        pass
    try:
        product_details += driver.find_element_by_id('productDetails_techSpec_section_2').find_elements_by_tag_name('tr')
    except:
        pass
    try:
        product_details += driver.find_element_by_id('productDetails_feature_div').find_elements_by_tag_name('tr')
    except:
        pass
        
    # try to get the sales rank else return True. Does not work sometimes. Need to be more robust.
    try:        
        salesRankElem = getElement(product_details, 'Best Sellers Rank').strip()
    except Exception,e:
        salesRank = 'NA'
        try:
            salesRank = product.sales_rank
        except:
            salesRank = 'NA'
    try:
        Main_Image = driver.find_element_by_id('imgTagWrapperId').find_element_by_tag_name('img').get_attribute('src')
    except:
        Main_Image = 'NA'
    try:
        Num_Images =  len(driver.find_element_by_id('altImages').find_elements_by_css_selector('.a-spacing-small.item'))
    except:
        Num_Images = 'NA'
    Title = title
    Price = price
    try:
        Average_Customer_Review = driver.find_element_by_css_selector('.reviewCountTextLinkedHistogram.noUnderline').get_attribute('title')
    except:
        Average_Customer_Review = getElement(product_details, 'Customer Reviews')
    try:
        Average_Customer_Review = Average_Customer_Review.replace('Be the first to review this item','')
    except:
        Average_Customer_Review = Average_Customer_Review 
    Stars_and_numbers = {}
    try:
        Ratings = driver.find_elements_by_css_selector('.a-histogram-row')        
        for rating in Ratings:
            try:
                key = rating.find_elements_by_css_selector('.a-text-right.aok-nowrap')[0].text
                value = rating.find_elements_by_css_selector('.a-text-right.aok-nowrap')[1].text
                Stars_and_numbers[key] = value
            except:
                key = rating.find_elements_by_css_selector('.a-nowrap')[0].text
                value = rating.find_elements_by_css_selector('.a-nowrap')[1].text
                Stars_and_numbers[key] = value
    except:
        pass
                    
    #Stars_and_numbers = data.find(attrs = {'class':'a-icon-alt'}).getText()
    Product_Link = url
    try:
        Description = product.editorial_review
        soup = BeautifulSoup(Description)
        Description = unidecode(soup.getText())
    except:
        Description = 'NA'
    try:
        features = driver.find_element_by_id('feature-bullets').find_elements_by_tag_name('li')
        try:
            Feature1 = features[0].text
        except:
            Feature1 = 'NA'
        try:
            Feature2 = features[1].text
        except:
            Feature2 = 'NA'
        try:
            Feature3 = features[2].text
        except:
            Feature3 = 'NA'
        try:
            Feature4 = features[3].text
        except:
            Feature4 = 'NA'
        try:
            Feature5 = features[4].text
        except:
            Feature5 = 'NA'
    except:
        Feature1 = 'NA'
        Feature2 = 'NA'
        Feature3 = 'NA'
        Feature4 = 'NA'
        Feature5 = 'NA'
    try:
        Dimensions = getElement(product_details, 'Product Dimensions')
    except:
        Dimensions = product.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height', 'ItemDimensions.Length', 'ItemDimensions.Weight'])
        Dimensions = ' x '.join([str(value) for key, value in Dimensions.items()])
    
    try:
        breadcrums = driver.find_element_by_css_selector('.a-subheader.a-breadcrumb.feature').find_elements_by_tag_name('li')
        b = ''
        i = 0
        for bread in breadcrums:
            if i%2==0:
                b = b + '|' + bread.text.strip()
                if i==0:
                    Main_Cat = b[1:]
            i+=1
        Category_Tree = b.replace('|||','|')[1:]
    except:
        Category_Tree = 'NA'
        Main_Cat = 'NA'
    
    try:
        brand = product.brand
    except:
        brand = getElement(product_details, 'Brand Name')
        if brand == '':
            brand = Title.split()[0]
    
    
    try:
        Shipping_Weight = getElement(product_details, 'Shipping Weight')
    except:
        Shipping_Weight = product.get_attribute('PackageDimensions.Weight')
    Shipping_Weight = re.findall(r'\d+\.\d+', str(Shipping_Weight)).replace('[','').replace(']','')
        
    ASIN = asin
       
    try:
        Sold_and_shipped_by = driver.find_element_by_id('merchant-info').text.replace('\n','').strip()
    except:
        Sold_and_shipped_by = 'NA'
    try:
        Item_Model_Number = getElement(product_details, 'Item model number')        
    except:
        Item_Model_Number = product.mpn
    Amazon_Best_Seller_Rank = salesRank
    try:
        Num_of_reviews = int(num_reviews)
    except:
        try:
            Num_of_reviews = re.findall(r'(\d+)', driver.find_element_by_id('acrCustomerReviewText'))[0]
        except:
            Num_of_reviews = 'NA'
    driver.close()
    data = [Main_Image, Num_Images, Title, Price, Average_Customer_Review, Stars_and_numbers, Product_Link, \
            Description, Feature1, Feature2, Feature3, Feature4, Feature5, Category_Tree, Main_Cat, brand, \
            Dimensions, Shipping_Weight, Item_Model_Number, Sold_and_shipped_by, Amazon_Best_Seller_Rank, Num_of_reviews]
    queue.put(data)

def main(products, amazon_api_list):
    queue_list = []
    numProducts = len(products.keys())
    for i in range(numProducts):
        queue_list.append(Queue.Queue())

    threads= []
    c =0
    
    for i in products.keys():
        driver = webdriver.Firefox()
        amazon=amazon_api_list[c]
        c+=1
        threads.append(Thread(target = getSKUData, args=(amazon, driver, products[i], queue_list[products.keys().index(i)])))
        
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    queue_data = []
    for q in queue_list:
        queue_data.append(q.get())
        
    return queue_data

f=open('100_keywords.csv', 'rb')
data = f.read().split('\n')[:1]
data = [d.strip() for d in data]
driver1 = webdriver.Firefox()

drivers = []

for d in data:
    searchterm = d.strip().replace('"','').replace("'",'').replace("/",' ')
    
    products = getAmazonProducts(searchterm, driver1)
    #print len(products.keys())
    data = main(products, amazon_api_list)
    #print len(data), data[0]

    df = pd.DataFrame(columns = ['Main_Image' , 'Num_Images' , 'Title' , 'Price' , 'Average_Customer_Review' , 'Stars_and_numbers' , 'Product_Link' , 'Description' , 'Feature1' , 'Feature2' , 'Feature3' , 'Feature4' , 'Feature5' , 'Category_Tree' , 'Main_Cat' , 'brand' , 'Dimensions' , 'Shipping_Weight' , 'Item_Model_Number' , 'Sold_and_shipped_by' , 'Amazon_Best_Seller_Rank' , 'Num_of_reviews'])

    count = 1
    for d in data:
        df.loc[count] = d
        count +=1  

    df.to_csv(searchterm[1:50] + '.csv', index = False, encoding = 'utf-8')
