from sys import argv
import math

import zbar
from PIL import Image
import cv2
import numpy as np
import time
import qr_code as qr

from pid import PID

scanner = zbar.ImageScanner()
scanner.parse_config('enable')


def find_name(symlink):
    # find where symlink is pointing (/dev/vide0, video1, etc)
    cmd = "readlink -f /dev/" + symlink 
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    out = process.communicate()[0]

    # extract ints from name video0, etc
    nums = [int(x) for x in out if x.isdigit()]
    # There should not be more than one digit
    if len(nums) <= 0:
         return -1
    interface_num = nums[0]    
    return interface_num

    
    
cam_names = ["front_cam", "back_cam", "right_cam", "left_cam"]
cams = {}

for c in cam_names:
    num = find_name(c)
    cam = cv2.VideoCapture(num)
    cam.set(3, 500)
    cam.set(4, 300)
    cams[c] = cam
   


# Set calibration matrix. Look @ openCV docs on cam calibration for detail
# Note: These are supposed to be unique for every camera but data is still generally correct most of the time.
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
# Note: Units are defined by camera calibration file.
l = 1.5 
verts = np.float32([[-l/2, -l/2, 0],
                    [-l/2, l/2, 0],
                    [l/2, -l/2, 0],
                    [l/2, l/2, 0]])


def im_scan(this_cam):
    this_cam.grab()
    this_cam.grab()
    this_cam.grab()
    this_cam.grab()
    ret, frame = this_cam.read()

    # grayscale
    #ret, frame = cv2.threshold(gray, 127, 255, 0)
    
    cv2.imshow('before filter', frame)

    #frame = cv2.bilateralFilter(frame, 9, 75, 75) 
    # Image pre-processing to make sure it's readable.
    frame = cv2.GaussianBlur(frame, (5,5), 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('after filter', frame)
    frame = cv2.adaptiveThreshold(frame, 255 
            , cv2.ADAPTIVE_THRESH_MEAN_C
            , cv2.THRESH_BINARY, 19, 0)

    # Convert OpenCV images to ZBAR images.
    cv2.imwrite('buffer.png', frame)
    pil_im = Image.open('buffer.png').convert('L')
    width, height = pil_im.size
    raw = pil_im.tobytes()

    # zbar data
    z_im = zbar.Image(width, height, 'Y800', raw) 

    mag_vec = []
    mag_2d = []
    
    # find all symbols in obj (either barcodes or QR codes)
    scanner.scan(z_im)
    for symbol in z_im:
        # Find vertices of code
        # TODO(Find a non-dumb way of doing this)
        tl, bl, br, tr = [item for item in symbol.location]
        points = np.float32(np.float32(symbol.location))
        
        # draw around it
        #cv2.line(frame, tl, bl, (255,0,0), 8, 8)
        #cv2.line(frame, bl, br, (255,0,0), 8, 8)
        #cv2.line(frame, br, tr, (255,0,0), 8, 8)
        #cv2.line(frame, tr, tl, (255,0,0), 8, 8)

        ret, rvec, tvec = cv2.solvePnP(verts, points, this_cam_matrix, distcoeffs)
        print "Value:    ", symbol.data
        print "Rotation: ", rvec
        print "vec:      ", tvec

    # Manually delete images due to memory leaks.
    del(z_im)
    del(pil_im)  
                    
                    
while True:

   for cam in cams:
       im_scan(cam)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

for cam in cams:
    cam.release()
cv2.destroyAllWindows()
