#!/usr/bin/python
from sys import argv
import zbar
from PIL import Image

if len(argv) < 2: exit(1)

# create a reader
scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')

# obtain image data
pil = Image.open(argv[1]).convert('L')
width, height = pil.size
raw = pil.tobytes()

# wrap image data
image = zbar.Image(width, height, 'Y800', raw)

# scan the image for barcodes
scanner.scan(image)

# extract results
for symbol in image:
    # do something useful with results
    topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in symbol.location]

    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
    print topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners 
# clean up
del(image)
