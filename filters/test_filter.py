import os
from fnmatch import fnmatch
import inspect

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



# get list of names of all filter strategies.
filter_strats = [func_name for func_name, func \
     in filter_strategies.__dict__.iteritems() \
      if inspect.isfunction(func)]

#get actual function object from str name
f0 = getattr(filter_strategies, filter_strats[0])
im0 = images[0]

print "=======================================================+"
_, res = f0(im0)
print res
#cv2.imshow('res', np.float32(res))
#cv2.waitKey(0)

print "======================================================"


for strategy_name in filter_strats:
   #get actual function object from str name
   strategy_function = getattr(filter_strategies, strategy_name)

   # track number of found qr codes, in how many images
   qr_count = 0
   im_count = 0

   for im in images:
        im_count += 1
        _, cleaned_im = strategy_function(im)

        cv2.imwrite('buffer.png', cleaned_im)
        #im to zbar frame
        cv2.imshow('cleaned_im', cleaned_im)
        cv2.waitKey(0)

        pil_im = Image.open('buffer.png').convert('L')
        width, height = pil_im.size
        raw = pil_im.tobytes()
        # zbar data
        z_im = zbar.Image(width, height, 'Y800', raw)
        for symbol in z_im:
            qr_count += 1
        if qr_count == 0:
            #print "strategy: {}, found no QR in: {}".format(strategy_name, str(im))
            print "||||||||||||||||||||||||||||||||"
