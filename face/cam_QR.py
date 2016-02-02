from sys import argv
import numpy as np
import cv2
import imutils
import zbar
from PIL import Image


# Capture frame-by-frame
#ret, frame = cap.read()
frame = cv2.imread('all.png')
#convert to PUL im
pil_im = Image.fromarray(frame)
width, height = pil_im.size
raw = pil_im.tobytes()
# Convert im to zbar
z_im = zbar.Image(width, height, 'Y800', raw)


proc = zbar.Processor()
proc.parse_config('enable')

proc.process_image(z_im)
sumbols = proc.get_results()

for symbol in z_im:
    print "a"





# When everything done, release the capture
cv2.destroyAllWindows()
