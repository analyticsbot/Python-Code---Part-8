import requests
from BeautifulSoup import BeautifulSoup
import pandas as pd
from text_unidecode import unidecode

## movies
url = 'http://instantwatcher.com/search?content_type=1&sort=available_from%20desc'

df =pd.DataFrame(columns = ['Title','Rating','Genres','Year'])
rr = requests.get(url)
soup = BeautifulSoup(rr.content)
links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})

i = 0
for link in links:
    link = link.find('a')['href']
    new_link = 'http://instantwatcher.com'+ link
    rr1 = requests.get(new_link)
    soup1 = BeautifulSoup(rr1.content)
    title = soup1.find(attrs = {'class':'title'}).getText()
    year = soup1.find(attrs = {'class':'year'}).getText()
    rating = soup1.find(attrs = {'class':'average_rating'}).getText()
    genres_list= soup1.findAll(attrs = {'class':'genres-list'})
    for genre in genres_list:
            genres = unidecode(genre.getText())
    i+=1
    df.loc[i] = [title, rating, genres, year]
df.to_csv('movies.csv', index = False, encoding = 'utf-8')
print 'Movies done'

## season
url = 'http://instantwatcher.com/search?content_type=2&sort=available_from%20desc'
df = pd.DataFrame(columns = ['Title','Year','Genre'])
rr = requests.get(url)
soup = BeautifulSoup(rr.content)
links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})
i=0
for link in links:
    link = link.find('a')['href']
    new_link = 'http://instantwatcher.com'+ link
    rr2 = requests.get(new_link)
    soup2 = BeautifulSoup(rr2.content)
    title = soup2.find(attrs = {'class':'title'}).getText()
    year = soup2.find(attrs = {'class':'year'}).getText()
    genres_list= soup2.findAll(attrs = {'class':'genres-list'})
    for genre in genres_list:
            genres = unidecode(genre.getText())
    i+=1
    df.loc[i] = [title, year, genres]
df.to_csv('season.csv', index = False, encoding = 'utf-8')
print 'Seasons done'	

## series
url = 'http://instantwatcher.com/search?content_type=3&sort=available_from%20desc'
df = pd.DataFrame(columns = ['Title','Year','Genre'])
rr = requests.get(url)
soup = BeautifulSoup(rr.content)
links = soup.findAll(attrs = {'class':'iw-title netflix-title list-title box-synopsis-mode'})
i=0
for link in links:
    link = link.find('a')['href']
    new_link = 'http://instantwatcher.com'+ link
    rr2 = requests.get(new_link)
    soup2 = BeautifulSoup(rr2.content)
    title = soup2.find(attrs = {'class':'title'}).getText()
    year = soup2.find(attrs = {'class':'year'}).getText()
    genres_list= soup2.findAll(attrs = {'class':'genres-list'})
    for genre in genres_list:
            genres = unidecode(genre.getText())
    i+=1
    df.loc[i] = [title, year, genres]
df.to_csv('series.csv', index = False, encoding = 'utf-8')
print 'Series done'
