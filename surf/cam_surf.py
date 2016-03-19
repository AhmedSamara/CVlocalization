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
# matcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


rk, rdes = surf.detectAndCompute(red, None)
bk, bdes = surf.detectAndCompute(blue, None)
yk, ydes = surf.detectAndCompute(yellow, None)
gk, gdes = surf.detectAndCompute(green, None)

print "red:    ", len(rk)
print "blue:   ", len(bk)
print "yellow: ", len(yk)
print "green:  ", len(gk)



"""
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
"""
