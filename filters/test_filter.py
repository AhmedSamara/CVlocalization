import os
from fnmatch import fnmatch

import cv2
import numpy as np
import zbar
from PIL import Image

import filter_strategies


images = []
#Get all images
for path, subdir, files in os.walk('test_images'):
    for name in files:
        if fnmatch(name, "*.jpg"):
            path = os.path.join(path, name)
            cv_im = cv2.imread(path)
            images.append(cv_im)


# get list of all fitler strategies.
filter_strats = [f for f in filter_strategies.__dict__.values() if hasattr(f,'__call__')]


for strategy in filter_strats:
    # track number of found qr codes, in how many images
    qr_count = 0
    im_count = 0
    for im in images:
        im_count += 1
        f = strategy.__call__(im)
        print f
        break         
        cv2.imwrite('buffer.png', cleaned_im)
        #im to zbar frame
        print cleaned_im
        cv2.imshow('cleaned_im')

        pil_im = Image.open('buffer.png').convert('L')
        width, height = pil_im.size
        raw = pil_im.tobytes()
        # zbar data
        z_im = zbar.Image(width, height, 'Y800', raw)
        for symbol in z_im:
            qr_count += 1
        if qr_count == 0:
            print "strategy: {}, found no QR in: {}".format(strategy, im)
