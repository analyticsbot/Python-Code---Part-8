import time, pyPdf, requests, json
import pandas as pd
from text_unidecode import unidecode

## urls to access all the open,closed, archived ids
archived_url = 'http://www.grants.gov/grantsws/OppsSearch?jp=%7B%22startRecordNum%22:0,%22sortBy%22:%22openDate%7Cdesc%22,%22oppStatuses%22:%22archived%22,%22rows%22:99999%7D'
open_url = 'http://www.grants.gov/grantsws/OppsSearch?jp=%7B%22startRecordNum%22:0,%22sortBy%22:%22openDate%7Cdesc%22,%22oppStatuses%22:%22open%22,%22rows%22:99999%7D'
closed_url = 'http://www.grants.gov/grantsws/OppsSearch?jp=%7B%22startRecordNum%22:0,%22sortBy%22:%22openDate%7Cdesc%22,%22oppStatuses%22:%22closed%22,%22rows%22:99999%7D'

## parse open applications
print 'getting the application ids'
resp = requests.get(open_url)
j = json.loads(resp.content)
## read the oppHits objects
k = j['oppHits']
open_id = []

## create an empty dataframe with the following columns
df = pd.DataFrame(columns = ["id","number","title","agency","openDate","closeDate","cfdaList"])
count = 0
for value in k:
    try:
        id = value["id"]
    except:
        id = 'NA'
    try:
        number = value["number"]
    except:
        number = 'NA'
    try:
        title = value["title"]
    except:
        title = 'NA'
    try:
        agency = value["agency"]
    except:
        agency = 'NA'
    try:
        openDate = value["openDate"]
    except:
        openDate = 'NA'
    try:
        openDate = value["openDate"]
    except:
        openDate = 'NA'
    try:
        closeDate = value["closeDate"]
    except:
        closeDate = 'NA'
    try:
        cfdaList = value["cfdaList"]
    except:
        cfdaList = 'NA'
    df.loc[count+1] = [id,number,title,agency,openDate,closeDate,cfdaList]
    open_id.append(value["id"])
    count +=1

## write out the dataframe to a csv file
df.to_csv('open_applications.csv', index = False)
print 'got open application ids. Wrote to file-- open_applications.csv'

## parse closed applications
print 'parsing closed application ids'
resp = requests.get(closed_url)
j = json.loads(unidecode(resp.content))
k = j['oppHits']
closed_id = []
df = pd.DataFrame(columns = ["id","number","title","agency","openDate","closeDate","cfdaList"])
count = 0
for value in k:
    try:
        id = value["id"]
    except:
        id = 'NA'
    try:
        number = value["number"]
    except:
        number = 'NA'
    try:
        title = value["title"]
    except:
        title = 'NA'
    try:
        agency = value["agency"]
    except:
        agency = 'NA'
    try:
        openDate = value["openDate"]
    except:
        openDate = 'NA'
    try:
        openDate = value["openDate"]
    except:
        openDate = 'NA'
    try:
        closeDate = value["closeDate"]
    except:
        closeDate = 'NA'
    try:
        cfdaList = value["cfdaList"]
    except:
        cfdaList = 'NA'
    df.loc[count+1] = [id,number,title,agency,openDate,closeDate,cfdaList]
    closed_id.append(value["id"])
    count +=1
df.to_csv('closed_applications.csv', index = False)
print 'got closed application ids. Wrote to file-- closed_applications.csv'

## parse archived applications
print 'parsing archived application ids'
resp = requests.get(archived_url)
j = json.loads(unidecode(resp.content))
k = j['oppHits']
archived_id = []
df = pd.DataFrame(columns = ["id","number","title","agency","openDate","closeDate","cfdaList"])
count = 0
for value in k:
    try:
        id = value["id"]
    except:
        id = 'NA'
    try:
        number = value["number"]
    except:
        number = 'NA'
    try:
        title = value["title"]
    except:
        title = 'NA'
    try:
        agency = value["agency"]
    except:
        agency = 'NA'
    try:
        openDate = value["openDate"]
    except:
        openDate = 'NA'
    try:
        openDate = value["openDate"]
    except:
        openDate = 'NA'
    try:
        closeDate = value["closeDate"]
    except:
        closeDate = 'NA'
    try:
        cfdaList = value["cfdaList"]
    except:
        cfdaList = 'NA'
    df.loc[count+1] = [id,number,title,agency,openDate,closeDate,cfdaList]
    archived_id.append(value["id"])
    count +=1
df.to_csv('archived_applications.csv', index = False)
print 'got archived application ids. Wrote to file-- archived_applications.csv'

