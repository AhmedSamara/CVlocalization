#!/usr/bin/python
from sys import argv
import zbar
from PIL import Image
import cv2
import numpy as np

if len(argv) < 2: exit(1)

# create a reader
scanner = zbar.ImageScanner()

# configure the reader
scanner.parse_config('enable')
"""
cam_matrix = np.zeros((3,3), np.float32)

cam_matrix[0,0] = 1.9961704327353971e+03
cam_matrix[0,1] = 0.0
cam_matrix[0,2] = 3.1950000000000000e+02
cam_matrix[1,0] = 0. 
cam_matrix[1,1] = 1.9961704327353971e+03
cam_matrix[1,2] = 2.3950000000000000e+02
cam_matrix[2,0] = 0.
cam_matrix[2,1] = 0.
cam_matrix[2,2] = 1.

distcoeffs = np.zeros((1,5), np.float32)
distcoeffs[0,0] = 1.8175523764227883e+00
distcoeffs[0,1] = -8.7919484257162480e+01
distcoeffs[0,2] = 0.
distcoeffs[0,3] = 0.
distcoeffs[0,4] = 1.2459859993672681e+03
"""

cam_matrix = np.float64([[1.99, 0.0, 3.195e+02],
                         [0.0,  1.99, 2.395e+02],
                         [0.0,  0.0, 1.0]])
distcoeffs = np.zeros(4)

# Dimensions of QR code

# obtain image data
pil = Image.open(argv[1]).convert('L')
width, height = pil.size
raw = pil.tobytes()

# wrap image data
z_im = zbar.Image(width, height, 'Y800', raw)

# scan the image for barcodes
val = scanner.scan(z_im)
print "scan val: ", val

found_points = np.zeros((4,2), np.float32)
verts = np.zeros((4,2), np.float32)

l = 1.5
verts[0] = (-l/2, -l/2)
verts[1] = (-l/2, l/2)
verts[2] = (l/2, -l/2)
verts[3] = (l/2, l/2)

print "verts: ", verts

print "verts 0: ", verts[0][1]

# extract results
for symbol in z_im:
    # do something useful with results
    tl, bl, br, tr = [item for item in symbol.location]
    points = np.float32([[tl[0], tl[1], 0],
                         [tr[0], tr[1], 0],
                         [bl[0], bl[1], 0],
                         [br[0], br[1], 0]])

     
         
    ret, rvec, tvec = cv2.solvePnP(points, verts, cam_matrix, distcoeffs)
    print "rvec: ", rvec
    print "tvec: ", tvec
    print symbol.data

# clean up
del(z_im)
