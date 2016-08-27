from pyPdf import PdfFileWriter, PdfFileReader
from pyPdf.generic import NameObject, createStringObject

OUTPUT = 'ml1.pdf'
INPUT = 'NOFO.pdf'

# There is no interface through pyPDF with which to set this other then getting
# your hands dirty like so:
output = PdfFileWriter()
fin = file(INPUT, 'rb')
pdf_in = PdfFileReader(fin)
infoDict = output._info.getObject()
print infoDict
infoDict.update({
    NameObject('/Title'): createStringObject(u'title'),
    NameObject('/Author'): createStringObject(u'author'),
    NameObject('/Subject'): createStringObject(u'subject'),
    NameObject('/Creator'): createStringObject(u'a script')
})
print infoDict
for page in range(pdf_in.getNumPages()):
    output.addPage(pdf_in.getPage(page))
    
outputStream = file(OUTPUT, 'wb')
output.write(outputStream)
outputStream.close()


from pyPdf import PdfFileReader, PdfFileWriter

pdf = PdfFileReader(open(OUTPUT, 'rb'))

print pdf.getDocumentInfo()
