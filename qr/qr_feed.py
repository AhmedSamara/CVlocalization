from sys import argv
import zbar
from PIL import Image
import cv2
import numpy as np
import time
import qr_code as qr


scanner = zbar.ImageScanner()
scanner.parse_config('enable')

if len(argv) < 2:
    cam = cv2.VideoCapture(0)
    # Set size of camera for logitech C270 camera
    cam.set(3,1280)
    cam.set(4,720)
else:
    cam = cv2.imread(argv[1])


# Set calibration matrix. Look @ openCV docs on cam calibration for detail
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
verts = np.float32([[-l/2, -l/2, 0],
                    [-l/2, l/2, 0],
                    [l/2, -l/2, 0],
                    [l/2, l/2, 0]])

while True:

    cam.grab()
    cam.grab()
    cam.grab()
    cam.grab()
    ret, frame = cam.read()

    cv2.imwrite('buffer.png', frame)   
    #im to zbar frame
    #cv_im = cv2.cvtColor(frame, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    pil_im = Image.open('buffer.png').convert('L')
    width, height = pil_im.size
    raw = pil_im.tobytes()

    # zbar data
    z_im = zbar.Image(width, height, 'Y800', raw) 

    codes = []
    # find all symbols in obj
    scanner.scan(z_im)
    for symbol in z_im:
       
        codes.append(qr.QRCode(symbol, l))


    for code in codes:
        #_, rvec, tvec = cv2.solvePnP(verts, code.points, cam_matrix, distcoeffs)
        _, code.rvec, code.tvec = cv2.solvePnP(verts, code.points, cam_matrix, distcoeffs)
        print code.centroid_location
        print code.centroid_location
         
        cv2.putText(frame, str(code.tvec) , code.centroid_location
                    , cv2.FONT_HERSHEY_SIMPLEX ,0.2, (100,50,255))
        
        cv2.imwrite('identified.png', frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
