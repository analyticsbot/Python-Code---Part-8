from PIL import ImageChops
from PIL import Image
import shutil
import requests
import csv

def downloadImage(url):
    filename = url.split('/')[-1]
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return filename


def equal(imageName):
    im1 = Image.open(imageName)
    im2 = Image.open('1199W1427.jpg')
    try:
        return ImageChops.difference(im1, im2).getbbox() is None
    except:
        return False
    
f = open('InputSample.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]

o = open('outputFile.csv', 'wb')
writer = csv.writer(o)
writer.writerow(['url', 'imageName', 'sameImage'])

for line in data:
    try:
        imageName = downloadImage(line)
        sameImage = equal(imageName)
        writer.writerow([line, imageName, sameImage])
    except:
        pass

f.close()
o.close()
