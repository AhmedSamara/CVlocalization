from sys import argv
import numpy as np
import cv2
import imutils
import zbar
from matplotlib import pyplot as plt

surf = cv2.SURF(400)
cap = cv2.VideoCapture(0)

#init colors
blue   = cv2.imread('blue.png')
yellow = cv2.imread('yellow.png')
red    = cv2.imread('red.png')
green  = cv2.imread('green.png')

color_qrs = [blue, yellow, red, green]
qr_surf = []


k_blue, blue_des = surf.detectAndCompute(blue, None)

# matcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


cam_matrix = np.zeros((3,3), np.float32)
distcoeffs = np.zeros((1,5), np.float32)

cam_matrix[0,0] = 1.9961704327353971e+03
cam_matrix[0,1] = 0.0
cam_matrix[0,2] = 3.1950000000000000e+02
cam_matrix[1,0] = 0 
cam_matrix[1,1] = 1.9961704327353971e+03
cam_matrix[1,2] = 2.3950000000000000e+02
cam_matrix[2,0] = 0
cam_matrix[2,1] = 0
cam_matrix[2,2] = 1

distcoeffs[0,0] = 1.8175523764227883e+00
distcoeffs[0,1] = -8.7919484257162480e+01
distcoeffs[0,2] = 0.
distcoeffs[0,3] = 0.
distcoeffs[0,4] = 1.2459859993672681e+03

rvec = np.zeros((3,1), np.float32)
tvec = np.zeros((3,1), np.float32)

dc = np.zeros(4)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    kp, des = surf.detectAndCompute(frame, None)

    surf_points = cv2.drawKeypoints(frame, kp, None,(255,0,0),4)
    cv2.imwrite('cam_points.png', surf_points)
    
    cv2.imshow('surf', surf_points)

#    ret, rvec, tvec = cv2.solvePnP(qr_surf[2], surf_points, cam_matrix, dc)
    
    matches = bf.match(blue_des, des)
    matches = sorted(matches, key = lambda x:x.distance)
    
    match_im = cv2.drawMatches(blue, blue_k, frame, kp, matches[:10], flags=2)
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
