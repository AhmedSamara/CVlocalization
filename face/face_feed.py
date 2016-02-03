import sys
from sys import argv
import zbar
from PIL import Image
import cv2
import numpy as np
import time


cam = cv2.VideoCapture(0)
casc = sys.argv[1]



faceCascade = cv2.CascadeClassifier(casc)

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

face_height = 10
face_width = 5

verts = np.float32([[-face_width/2, -face_height/2, 0],
                    [-face_width/2, face_height/2, 0],
                    [face_width/2, -face_height/2, 0],
                    [face_width/2, face_height/2, 0]])

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces  = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30,30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255, 0), 2)

        points = np.float32([[x, y],
                             [x, y+h],
                             [x+w, y],
                             [x+w,y+h]])

        ret, rvec, tvec = cv2.solvePnP(verts, points 
                                      , cam_matrix, distcoeffs)

        print "dist: ", tvec
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
