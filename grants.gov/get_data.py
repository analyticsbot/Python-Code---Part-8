import json, requests
from text_unidecode import unidecode
import pandas as pd
from pyPdf import PdfFileReader
import pyPdf

base_url= 'http://www.grants.gov/grantsws/OppDetails?oppId='
document_url = 'http://www.grants.gov/grantsws/rest/oppdetails/att/download/'

open_df = pd.read_csv('closed_applications.csv')
open_id = list(open_df['id'])

def readPDF(filename):
    input = PdfFileReader(file(filename, "rb"))
    content = ''
    for page in input.pages:
        content += ' ' + page.extractText()
    return content

def download_file(url):
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
    f.write(str(data))
    f.close()
