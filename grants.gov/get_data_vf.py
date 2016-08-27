## import all required modules
import json, requests
from text_unidecode import unidecode
import pandas as pd
from pyPdf import PdfFileReader
import pyPdf, os
from threading import Thread

## base url for each of grants. Add the application id
base_url= 'http://www.grants.gov/grantsws/OppDetails?oppId='
## base url for each document type. Add document id to access the document
document_url = 'http://www.grants.gov/grantsws/rest/oppdetails/att/download/'

## read all the application ids into a file
open_df = pd.read_csv('open_applications.csv')
open_id = list(open_df['id'])[:6]
## num of threads. Depends on CPU/RAM
num_threads = 5
json_folder = 'open1'

if not os.path.exists(json_folder):
    os.makedirs(json_folder)

def readPDF(filename):
    """Function to read the attachment and return the contents"""
    input = PdfFileReader(file(filename, "rb"))
    content = ''
    for page in input.pages:
        content += ' ' + page.extractText()
    return content

def download_file(url):
    """ function to download the files to local"""
    local_filename = url.split('/')[-1] + '.pdf'
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

for id in open_id:
    url = base_url + str(id)
    response = requests.get(url)
    data = json.loads(unidecode(response.content))
    f = open(str(id) + '.json', 'wb')
    try:
        document_id = data['synopsisAttachmentFolders'][0]['synopsisAttachments'][0]['id']
        doc_url = document_url + str(document_id)
        pdfFileName = download_file(doc_url)
        pdfData = readPDF(pdfFileName)
        data['synopsisAttachmentFolders'][0]['synopsisAttachments'][0]['documentContent'] = pdfData
    except:
        pass
    
    try:
        contactInfo = data['opportunityPkgs'][0]['contactInfo'].split('\r\n')
        name = contactInfo[0]
        for val in contactInfo:
            if 'E-mail' in val:
                email = val.replace('E-mail','').replace(':','').strip()            
            elif 'Phone' in val:
                phone = val.replace('Phone','').replace(':','').strip() 
            else:
                title = val.replace(':','').strip()
        
    
        data['opportunityPkgs'][0]['contactInfo'] = { "name": name, "title": title, "email": email, "phone": phone }
    except:
        pass
    try:
        agencyContactDesc = data['synopsis']['agencyContactDesc'].split('\r\n')
        name = agencyContactDesc[0]
        for val in agencyContactDesc:
            if 'E-mail' in val:
                email = val.replace('E-mail','').replace(':','').strip()            
            elif 'Phone' in val:
                phone = val.replace('Phone','').replace(':','').strip() 
            else:
                title = val.replace(':','').strip() 
        data['synopsis']['agencyContactDesc'] = { "name": name, "title": title, "phone": phone }
    except:
        pass
    data = json.dumps(data)
    f.write((data))
    #f.write(str(data))
    f.close()

def downloadJSON(ids):
    """ function to download the json for each application"""
    for id in ids:
        url = base_url + str(id)
        ## request the json from the url
        response = requests.get(url)
        data = json.loads(unidecode(response.content))
        f = open(json_folder + '/' + str(id) + '.json', 'wb')
        ## save the document. read it and add the contents
        try:
            document_id = data['synopsisAttachmentFolders'][0]['synopsisAttachments'][0]['id']
            doc_url = document_url + str(document_id)
            pdfFileName = download_file(doc_url)
            pdfData = readPDF(pdfFileName)
            data['synopsisAttachmentFolders'][0]['synopsisAttachments'][0]['documentContent'] = pdfData
        except:
            pass

        ## change the contactInfo key to an object with name, email, and title
        try:
            contactInfo = data['opportunityPkgs'][0]['contactInfo'].split('\r\n')
            name = contactInfo[0]
            for val in contactInfo:
                if 'E-mail' in val:
                    email = val.replace('E-mail','').replace(':','').strip()            
                elif 'Phone' in val:
                    phone = val.replace('Phone','').replace(':','').strip() 
                else:
                    title = val.replace(':','').strip()
            
        
            data['opportunityPkgs'][0]['contactInfo'] = { "name": name, "title": title, "email": email, "phone": phone }
        except:
            pass
        ## change the agencyContactDesc into name, email,phone, and title
        try:
            agencyContactDesc = data['synopsis']['agencyContactDesc'].split('\r\n')
            name = agencyContactDesc[0]
            for val in agencyContactDesc:
                if 'E-mail' in val:
                    email = val.replace('E-mail','').replace(':','').strip()            
                elif 'Phone' in val:
                    phone = val.replace('Phone','').replace(':','').strip() 
                else:
                    title = val.replace(':','').strip() 
            data['synopsis']['agencyContactDesc'] = { "name": name, "title": title, "phone": phone }
        except:
            pass
        ## write the json as output
        data = json.dumps(data)
        f.write((data))
        f.close()

## use threads to reduce the time
threads= []
## divide data b/w threads
data_each_file = len(open_id)/num_threads

## intialize the threads
for i in range(num_threads+1):
    ids = open_id[i*data_each_file:data_each_file*(i+1)]
    threads.append(Thread(target = downloadJSON, args=(ids,)))

## start the threads
for t in threads:
    t.start()
