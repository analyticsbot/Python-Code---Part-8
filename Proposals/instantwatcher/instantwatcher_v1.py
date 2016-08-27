import requests
from BeautifulSoup import BeautifulSoup
from selenium immport webdriver
import pandas as pd
from text_unidecode import unidecode
import random, time
print 'All modules import successfully!'

## movies
page = 1
df =pd.DataFrame(columns = ['Title','Rating','Genres','Year'])
i = 0
while True:
    url = 'http://instantwatcher.com/search?content_type=1&sort=available_from%20desc&layout=none&page=' + str(page)
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
                driver.get(url)
                if rr2:
                    break
        except:
            pass
        #soup1 = BeautifulSoup(rr1.content)
        soup = BeautifulSoup(driver.page_source)
        title = soup1.find(attrs = {'class':'title'}).getText()
        year = soup1.find(attrs = {'class':'year'}).getText()
        rating = soup1.find(attrs = {'class':'average_rating'}).getText()
        genres_list= soup1.findAll(attrs = {'class':'genres-list'})
        for genre in genres_list:
                genres = unidecode(genre.getText())
        i+=1
        if df.shape[0]%51==0:
            print df.shape
        df.loc[i] = [title, rating, genres, year]
        time.sleep(random.randint(0,1))

df.to_csv('movies.csv', index = False, encoding = 'utf-8')
print 'Movies done!'
'''
## season
page = 1
i = 0
df = pd.DataFrame(columns = ['Title','Year','Genre'])

while True:
    url = 'http://instantwatcher.com/search?content_type=2&sort=available_from%20desc&layout=none&page=' + str(page)
    page+=1
    rr = requests.get(url)
    soup = BeautifulSoup(rr.content)
    links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})
    if len(links)==0:
        break
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

df.to_csv('season.csv', index = False, encoding = 'utf-8')
print 'Seasons done!'	

## series

df = pd.DataFrame(columns = ['Title','Year','Genre'])
page=1
i=0
while True:
    url = 'http://instantwatcher.com/search?content_type=3&sort=available_from%20desc&layout=none&page=' + str(page)
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
