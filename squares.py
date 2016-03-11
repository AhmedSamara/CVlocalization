from math import sqrt
import cv2

cap = cv2.VideoCapture(0)
# set resolution to low


THRESH_X = 15
THRESH_Y = 15

def find_center(cnt):

    (x,y), r = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    return center

def distance(a, b):
   return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


#idk if we should use this
class marker(object):
    def __init__(contour):
        self.contour = contour
        self.center = find_center(contour)
        self.approx = cv2.approxPolyDP(contour, 0.02*peri, True)
        self.dims = cv2.boundingRect(self.approx)

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

        cv2.drawContours(frame, [cv2.convexHull(c)], 0, (0,0,255),2)
        solidity = area / float(hullArea)

        keepSolidity = solidity > 0.9
        keepAspectRatio = (aspectRatio >= 0.8 and aspectRatio <= 1.2 ) \

        keepSize = cv2.arcLength(c, True) > 60

        if keepSolidity and keepAspectRatio and keepSize:
            return True
        else:
            return False
 


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    frame_orig = frame

    # gray and blur
    frame = cv2.GaussianBlur(frame,(5,5),0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    cv2.imshow('blur', frame)
    #frame = cv2.adaptiveThreshold(frame ,255  
    #        , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    frame = cv2.Canny(frame, 50, 150)

    cv2.imshow('edge', frame)

    (cnts,_) = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    qr_list = []
    
    markers = []
    for c in cnts:
        if is_marker(c):
            cv2.drawContours(frame_orig, [c], -1, (0,0,255), 4)
            cp = find_center(c)
            markers.append(cp)

    # Sort squares in order by Y axis
    markers.sort(key=lambda tup:tup[1])
    
    # Number squares by height
    i=0
    for crn in markers:
        cv2.circle(frame_orig, crn, 5, (100,255,0))
        #cv2.putText(frame_orig, str(i), crn, cv2.FONT_HERSHEY_PLAIN,1.0, (255,100,55))
        i += 1

    # enough squares for QR found
    if len(markers) > 2:
        # Find anchor
        anchor = markers[0]
        copy_sq = list(markers)


        # Look for closest sq
        del copy_sq[0]
        copy_sq.sort(key=lambda x: sqrt((anchor[0] - x[0])**2 
                                       + (anchor[1] - x[1])**2))

        # next square
        # Closest square, guranteed to be same QR
        anchor2 = copy_sq[0]
        expected_dist = sqrt((anchor[0] - anchor2[0])**2 \
                           + (anchor[1] - anchor2[1])**2)


        print "distance: ", expected_dist
        cv2.circle(frame_orig, copy_sq[0], 15, (100,255,255))
        sameX = abs(anchor[0]-anchor2[0]) < THRESH_X
        sameY = abs(anchor[1]-anchor2[1]) < THRESH_Y
        # If same X
        if abs(anchor[0]-anchor2[0]) < THRESH_X:
            
            # Look for next in same Y
            copy_sq.sort(key=lambda q: abs(q[1]-anchor[1]))
            
            # Look for same Y, but also at expected location
            # Optimization: No need to iterate past first few
            for q in copy_sq:
                print "here"
                sameY = abs(q[1]-anchor[1]) < THRESH_Y
                if sameY:
                    anchor3 = q
                    print "part 3 found"
                    pts = [anchor, anchor2, anchor2]
                    #cv2.fillPoly(frame_orig, pts, (255,255,255))
                
                    

        # Else
            # Look for same X


    cv2.imshow("screen", frame_orig)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
