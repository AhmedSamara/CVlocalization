from math import sqrt
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# set resolution to low


def find_center(cnt):

    (x,y), r = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    return center

def distance(a, b):
   return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

THRESH_X = 0.5
THRESH_Y = 0.5

Y_DIST = 2.5
X_DIST = 2.5

def same_qr(marker1, marker2):
    """Checks to see if markers are on same qr.
    """
    # Assume that both markers are roughly similair size
    dist = distance(marker1.center, marker2.center)     
    height = marker1.height 
    width  = marker1.width 

    dx = abs(marker1.x - marker2.x) 
    dy = abs(marker1.y - marker2.y)
    
    #markers are expected to be 2.5 marker lengths apart
    # marker is on same Y, but 
    
    #check that y displacement is in correct range
    vert_range = abs( dy - Y_DIST) > THRESH_Y
    horiz_range = abs(dx - X_DIST) > THRESH_X
    
    # marker is diagonal from current
    if vert_range and horiz_range:
        return True
    #vertical from current
    elif vert_range and not horiz_range:
        return True
    elif not vert_range and horiz_range:
        return True
    
    return False

#idk if we should use this
class Marker(object):
    def __init__(self, contour):
        peri = cv2.arcLength(contour, True)
        self.contour = contour
        #co-ords based on center of marker
        self.center = find_center(contour)

        self.x = self.center[0]
        self.y = self.center[1]
        

        self.approx = cv2.approxPolyDP(contour, 0.02*peri, True)

        #optimize
        (rx, ry, w, h) = cv2.boundingRect(self.approx) 
        self.width = w
        self.height = h
        self.length = (w + h)/2

class PartialQR(object):
    
    def __init__(self, a, b, c):
        self.marker1 = a
        self.marker2 = b
        self.marker3 = c


def is_marker(contour):

    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02*peri, True)
    #if contour has 4 points, 
    if len(approx) >= 4 and len(approx) <= 6:
        (x, y, w, h) = cv2.boundingRect(approx)
        aspectRatio = w/ float(h)


        # find areas
        area = cv2.contourArea(c)
        hullArea = cv2.contourArea(cv2.convexHull(c))

        #cv2.drawContours(frame, [cv2.convexHull(c)], 0, (0,0,255),2)
        solidity = area / float(hullArea)

        keepSolidity = solidity > 0.9
        keepAspectRatio = (aspectRatio >= 0.8 and aspectRatio <= 1.2 ) \

        keepSize = cv2.arcLength(c, True) > 60

        if keepSolidity and keepAspectRatio and keepSize:
            return True
        else:
            return False
 

def find_matching_marker(marker, marker_list):
    """finds all markers in the same list."""
    marker_list.remove(marker)

    matches = [m for m in marker_list if same_qr(marker, m)]
    return matches
        


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    frame_orig = frame

    # gray and blur
    frame = cv2.GaussianBlur(frame,(5,5),0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    #frame = cv2.adaptiveThreshold(frame ,255  
    #        , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    frame = cv2.Canny(frame, 50, 150)

    cv2.imshow('edge', frame)

    (cnts,_) = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)


    # This is the pythonic way I swear
    markers = [Marker(c) for c in cnts if is_marker(c)]

    cv2.drawContours(frame_orig, [m.contour for m in markers], -1, (0,255,0))

    # Sort Markers by Y axis
    markers.sort(key=lambda x: x.y)
    
    # Number squares by height
    #i=0
    #for mrk in markers:
    #    cv2.circle(frame_orig, mrk.center, 5, (100,255,0))
    #    cv2.putText(frame_orig, str(i), mrk.center, cv2.FONT_HERSHEY_PLAIN,1.0, (255,100,55))
    #    i += 1
 
    
    qr_list = []
    for mrk in markers:
        # Exclude current from search.
        markers.remove(mrk)

        # Search for matching markers.
        # Should return 2 markers if it's the corner one (both other markers are across)
        # only one otherwise.
        matches = [m for m in markers if same_qr(mrk, m)]
        for m in matches:
            markers.remove(m)    
        if len(matches) > 2:
            #print "error: too many matches"
            n =0
        elif len(matches) == 2:
            qr_list.append(PartialQR(mrk, matches[0], matches[1]))
            
            t = np.array([mrk.center, 
                          matches[0].center, 
                          matches[1].center])
            cv2.fillConvexPoly(frame_orig, t, (0,0,255))
        elif len(matches) == 1:
            #print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<weird"
            # Find the next marker based on new marker
            found=0
            for m in markers:
                if same_qr(matches[0], m):
                    matches.append(m)
                    markers.remove(m)
                    found=1
            if found==0:
                print "error, no matches"
        elif len(matches) == 0:
            n=0
            #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>no matches"
            #qr_list.append(PartialQR(mrk, None, None))

    cv2.imshow("screen", frame_orig)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
