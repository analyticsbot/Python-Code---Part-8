# import the Flask class from the flask module and other required modules
from bs4 import BeautifulSoup
from threading import Thread
from text_unidecode import unidecode
from amazon.api import AmazonAPI
from selenium import webdriver
import pandas as pd
from amazon_api_data import *
import time, requests

def getAmazonProducts(searchterm, amazon):
    data = []
    products = amazon.search(Keywords=searchterm, SearchIndex='All')
    count = 0
    for product in products:
        try:
            count+=1
            if count ==17:
                break
            time.sleep(1)
            try:
                asin = product.asin
            except:
                asin = 'NA'
            url = 'http://www.amazon.com/dp/' + unidecode(asin)    
            try:
                salesRank = product.sales_rank
            except:
                salesRank = 'NA'
            try:
                Main_Image = product.large_image_url
            except:
                Main_Image = 'NA'
            try:
                Num_Images =  len(product.images)
            except:
                Num_Images ='NA'
            try:
                Title = product.title
            except:
                Title = 'NA'
            try:
                Price = product.price_and_currency[0]
            except:
                Price = 'NA'
            try:
                review = product.reviews[1]
                headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0', 'Content-Type':'application/x-www-form-urlencoded'}

                response = requests.get(review, headers=headers)
                soup1 = BeautifulSoup(response.content)
                try:
                    Average_Customer_Review = soup1.find(attrs={'class':'asinReviewsSummary'}).find('img')['title']
                except:
                    Average_Customer_Review = 'NA'
                try:
                    ratings_ = soup1.find(attrs={'class':'txtsmaller histogramPPD'}).findAll('div')
                    
                    Stars_and_numbers = {}
                    for i in ratings_:
                        try:
                            f = i['title'].replace('of rating','').strip().split('represent')
                            key = f[0]
                            value= f[1]
                            Stars_and_numbers[key] = value
                        except:
                            pass
                except:
                    Stars_and_numbers = {}
                try:
                    Num_of_reviews = soup1.find(attrs={'class':'crIFrameHeaderHistogram'}).find('b').getText()
                except:
                    Num_of_reviews = 'NA'
            except:
                pass
            Stars_and_numbers = str(Stars_and_numbers)
            Product_Link = url
            try:
                Description = product.editorial_review
                soup = BeautifulSoup(Description)
                Description = unidecode(soup.getText())
            except:
                Description = 'NA'
                
            features = product.features
            try:
                Feature1 = features[0]
            except:
                Feature1 = 'NA'
            try:
                Feature2 = features[1]
            except:
                Feature2 = 'NA'
            try:
                Feature3 = features[2]
            except:
                Feature3 = 'NA'
            try:
                Feature4 = features[3]
            except:
                Feature4 = 'NA'
            try:
                Feature5 = features[4]
            except:
                Feature5 = 'NA'
            
            try:
                Dimensions = product.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height', 'ItemDimensions.Length', 'ItemDimensions.Weight'])
            except:
                Dimensions = 'NA'
            Category_Tree = ''    
            Main_Cat = ''
            ancestors = product.browse_nodes[0].ancestors[::-1]
            current_cat = product.browse_nodes[0].name
            cat_count =0
            for i in ancestors:
                if cat_count == 0:
                    Main_Cat= i.name
                Category_Tree += '|' + i.name
                cat_count+=1
            Category_Tree = Category_Tree[1:] + '|' + current_cat
            
            try:
                brand = product.brand
            except:
                brand = 'NA'
            try:
                Shipping_Weight = product.get_attribute('PackageDimensions.Weight')
            except:
                Shipping_Weight = 'NA'
            ASIN = asin
            Sold_and_shipped_by = 'Ships from and sold by ' + product.publisher
            try:
                Item_Model_Number = product.mpn
            except:
                Item_Model_Number = 'NA'
            Amazon_Best_Seller_Rank = salesRank
            

            data.append([Main_Image, Num_Images, Title, Price, Average_Customer_Review, Stars_and_numbers, Product_Link, \
                Description, Feature1, Feature2, Feature3, Feature4, Feature5, Category_Tree, Main_Cat, brand, \
                Dimensions, Shipping_Weight, Item_Model_Number, Sold_and_shipped_by, Amazon_Best_Seller_Rank, Num_of_reviews])
        except:
            break
    return data

f=open('100_keywords.csv', 'rb')
data = f.read().split('\n')[1:]
data = [d.strip() for d in data]

for d in data:
    searchterm = d.strip().replace('"','').replace("'",'').replace("/",' ')
    print 'getting data for ', searchterm

    try:
        data = getAmazonProducts(searchterm, amazon)
    except:
        print 'no data for ', searchterm

    df = pd.DataFrame(columns = ['Main_Image' , 'Num_Images' , 'Title' , 'Price' , 'Average_Customer_Review' , 'Stars_and_numbers' , 'Product_Link' , 'Description' , 'Feature1' , 'Feature2' , 'Feature3' , 'Feature4' , 'Feature5' , 'Category_Tree' , 'Main_Cat' , 'brand' , 'Dimensions' , 'Shipping_Weight' , 'Item_Model_Number' , 'Sold_and_shipped_by' , 'Amazon_Best_Seller_Rank' , 'Num_of_reviews'])

    count = 1
    for d in data:
        df.loc[count] = d
        count +=1  

    df.to_csv(searchterm[:50] + '.csv', index = False, encoding = 'utf-8')
