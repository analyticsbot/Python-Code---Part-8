import requests
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import pandas as pd
from text_unidecode import unidecode
import random, time
print 'All modules import successfully!'

driver = webdriver.Firefox()
'''
## movies
page = 1
df =pd.DataFrame(columns = ['Title','Rating','Genres','Year'])
i = 0
while True:
    url = 'http://instantwatcher.com/search?content_type=1&sort=available_from%20desc&page=' + str(page)
    page+=1
    #rr = requests.get(url)
    driver.get(url)
    #soup = BeautifulSoup(rr.content)
    soup = BeautifulSoup(driver.page_source)
    links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})
    if len(links)==0:
        break
    
    for link in links:
        link = link.find('a')['href']
        new_link = 'http://instantwatcher.com'+ link
        try:
            while True:
                #rr1 = requests.get(new_link)
                driver.get(new_link)
                if driver:
                    break
        except:
            pass
        #soup1 = BeautifulSoup(rr1.content)
        soup1 = BeautifulSoup(driver.page_source)
        try:
            title = soup1.find(attrs = {'class':'title'}).getText()
        except:
            title = ''
        try:
            year = soup1.find(attrs = {'class':'year'}).getText()
        except:
            year = ''
        try:
            rating = soup1.find(attrs = {'class':'average_rating'}).getText()
        except:
            rating = ''
        genres = ''
        try:
            genres_list= soup1.findAll(attrs = {'class':'genres-list'})
        
            for genre in genres_list:
                    genres = unidecode(genre.getText())
        
        except:
            pass
        i+=1
        if df.shape[0]%51==0:
            print df.shape
        df.loc[i] = [title, rating, genres, year]
        time.sleep(random.randint(0,0))

df.to_csv('movies.csv', index = False, encoding = 'utf-8')
print 'Movies done!'
'''
## season
page = 1
i = 0
df = pd.DataFrame(columns = ['Title','Year','Genre'])

while True:
    url = 'http://instantwatcher.com/search?content_type=2&sort=available_from%20desc&page=' + str(page)
    page+=1
    driver.get(url)
    #soup = BeautifulSoup(rr.content)
    soup = BeautifulSoup(driver.page_source)
    links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})
    if len(links)==0:
        break
    
    for link in links:
        link = link.find('a')['href']
        new_link = 'http://instantwatcher.com'+ link
        try:
            while True:
                #rr1 = requests.get(new_link)
                driver.get(new_link)
                if driver:
                    break
        except:
            pass
        #soup1 = BeautifulSoup(rr1.content)
        soup2 = BeautifulSoup(driver.page_source)
        try:
            title = soup2.find(attrs = {'class':'title'}).getText()
        except:
            title = ''
        try:
            year = soup2.find(attrs = {'class':'year'}).getText()
        except:
            year = ''
        genres = ''
        try:
            genres_list= soup2.findAll(attrs = {'class':'genres-list'})
            for genre in genres_list:
                    genres = unidecode(genre.getText())
        except:
            pass
        i+=1
        if df.shape[0]%51==0:
            print df.shape
        df.loc[i] = [title, year, genres]
        time.sleep(random.randint(0,0))

df.to_csv('Seasons.csv', index = False, encoding = 'utf-8')
print 'Seasons done!'	
'''
## series

df = pd.DataFrame(columns = ['Title','Year','Genre'])
page=1
i=0
while True:
    url = 'http://instantwatcher.com/search?content_type=3&sort=available_from%20desc&page=' + str(page)
    page+=1
    rr = requests.get(url)
    soup = BeautifulSoup(rr.content)
    links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})
    if len(links)==0:
        break
    i=0
    for link in links:
        link = link.find('a')['href']
        new_link = 'http://instantwatcher.com'+ link
        try:
            while True:
                rr2 = requests.get(new_link)
                if rr2:
                    break
        except:
            pass
        soup2 = BeautifulSoup(rr2.content)
        title = soup2.find(attrs = {'class':'title'}).getText()
        year = soup2.find(attrs = {'class':'year'}).getText()
        genres_list= soup2.findAll(attrs = {'class':'genres-list'})
        for genre in genres_list:
                genres = unidecode(genre.getText())
        i+=1
        if df.shape[0]%51==0:
            print df.shape
        df.loc[i] = [title, year, genres]
        time.sleep(random.randint(0,1))

df.to_csv('series.csv', index = False, encoding = 'utf-8')
print 'Series done!'
'''
