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
    ret, frame = cam.read()
   
    #im to zbar frame
    cv_im = cv2.cvtColor(frame, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    cv2.imshow('ca', cv_im)
    cv2.imshow('raw: ', frame)

    width = cam.get(3)
    height = cam.get(4)
    raw = cv_im.tostring()
    
    z_im = zbar.Image(int(width), int(height), 'Y800', raw) 
     
    # find all symbols in obj
    scanner.scan(z_im)
    cv2.imshow('frame: ', cv_im)
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
