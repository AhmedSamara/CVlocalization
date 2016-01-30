import zbar
from PIL import Image
import cv2
import numpy as np


scanner = zbar.ImageScanner()
scanner.parse_config('enable')

cam = cv2.VideoCapture(0)

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


# Dimensions of QR code
l = 1.5
verts = np.float32([[-l/2, -l/2],
                    [-l/2, l/2],
                    [l/2, -l/2],
                    [l/2, l/2]])


while True:
    _, frame = cam.read()
   
    cv2.imshow('frame: ', frame) 
    # convert frame to im 
    pil_im = Image.fromarray(frame)
    
    #im to zbar frame
    raw = pil_im.tobytes()
    width, height = pil_im.size
    z_im = zbar.Image(width, height, 'Y800', raw)
    
    # find all symbols in obj
    scanner.scan(z_im)

    for symbol in z_im:
        
        print "scanning im"        
        # Find vertices of code
        # TODO(Find a non-dumb way of doing this)
        tl, bl, br, tr = [item for item in symbol.location]
        points = np.float32([[tl[0], tl[1], 0],
                             [tr[0], tr[1], 0],
                             [bl[0], bl[1], 0],
                             [br[0], br[1], 0]])
        ret, rvec, tvec = cv2.solvePnP(points, verts, cam_matrix, distcoeffs)
        print "Value:    ", symbol.data
        print "Rotation: ", rvec
        print "vec:      ", tvec
        del(z_im) 

