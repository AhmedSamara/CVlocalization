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

rvec = np.zeros((3,1), np.float32)
tvec = np.zeros((3,1), np.float32)
# obtain image data
pil = Image.open(argv[1]).convert('L')
width, height = pil.size
raw = pil.tobytes()

# wrap image data
image = zbar.Image(width, height, 'Y800', raw)

# scan the image for barcodes
scanner.scan(image)

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
for symbol in image:
    # do something useful with results
    tl, bl, br, tr = [item for item in symbol.location]

    points = symbol.location
    print "points: ", points
    """
    found_points[0] = topLeftCorners 
    found_points[1] = bottomLeftCorners 
    found_points[2] = bottomRightCorners 
    found_points[3] = topRightCorners
    """
    print "tl: ", tl

    print "found_points: ", found_points
    #print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
    #print topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners 

    rect = cv2.minAreaRect(found_points)

    ret, rvec, tvec = cv2.solvePnP(verts, verts, cam_matrix, distcoeffs)

# clean up
del(image)
