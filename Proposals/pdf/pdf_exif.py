from pyPdf import PdfFileWriter, PdfFileReader
from pyPdf.generic import NameObject, createStringObject
import os

## filename with column A as filename and B as the tag
tag_filename = 'filename.csv'
tag_dict = {}
f = open(tag_filename, 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]

for line in data:
    line_split = line.split(',')
    tag_dict[line_split[0]] = line_split[1]

## name of the directory in which updated files will be stored
directory = 'edited'

## create the above folder if does not exists
if not os.path.exists(directory):
    os.makedirs(directory)

## find all the files in the current directory.
## place this script within the same folder
## if the pdf files are in some other folder, add the address
files = os.listdir('.')

def editPDF(filename):
    """ function to add metadata to pdf files"""
    INPUT = filename
    OUTPUT = filename[:-4] + '_updated.pdf'

    output = PdfFileWriter()
    fin = file(INPUT, 'rb')
    pdf_in = PdfFileReader(fin)
    infoDict = output._info.getObject()

    ###########################################################
    # I've added random tags here, use what needs to be added #
    #                                                         #
    ###########################################################
    infoDict.update({
        NameObject('/Tags'): createStringObject(tag_dict[filename]),
        NameObject('/Keywords'): createStringObject(tag_dict[filename])
    })
    for page in range(pdf_in.getNumPages()):
        output.addPage(pdf_in.getPage(page))
    
    outputStream = file(os.path.join(directory, OUTPUT), 'wb')
    output.write(outputStream)
    fin.close()
    outputStream.close()


for filename in files:
    if filename.endswith('pdf'):
        try:
            editPDF(filename)
        except Exception,e:
            print str(e)
            pass
