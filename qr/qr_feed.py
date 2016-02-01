from sys import argv
import zbar
from PIL import Image
import cv2
import numpy as np


scanner = zbar.ImageScanner()
scanner.parse_config('enable')

if len(argv) < 2:
    cam = cv2.VideoCapture(0)
else:
    cam = cv2.imread(argv[1])

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


width = int(cam.get(3))
height = int(cam.get(4))



while True:
    ret, frame = cam.read()

    cv2.imshow('frame', frame)
   

    #im to zbar frame
    #cv_im = cv2.cvtColor(frame, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(im)

    raw = pil_im.tobytes()
    z_im = zbar.Image(width, height, 'Y800', raw) 
     
    # find all symbols in obj
    val = scanner.scan(z_im)
    print "scan val: ", val
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
