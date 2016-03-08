from math import sqrt
import cv2

cap = cv2.VideoCapture(0)
# set resolution to low


def center(cnt):

    (x,y), r = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    return center


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

    corner_squares = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)

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
                cv2.drawContours(frame_orig, [approx], -1, (0,0,255), 4)
                cp = center(c)
                corner_squares.append(cp)
                #cv2.circle(frame_orig, c, 2, (0,255,0))

    corner_squares.sort(key=lambda tup:tup[1])
    
    i=0
    for crn in corner_squares:
        cv2.circle(frame_orig, crn, 5, (100,255,0))
        cv2.putText(frame_orig, str(i), crn, cv2.FONT_HERSHEY_PLAIN,1.0, (255,100,55))
        i += 1

    if len(corner_squares) > 2:
        # Find anchor
        anchor = corner_squares[0]
        copy_sq = list(corner_squares)
        del copy_sq[0]
        # Look for closest sq
        copy_sq.sort(key=lambda x: sqrt((anchor[0] - x[0])**2 
                                       + (anchor[1] - x[1])**2))

        # Closest square, guranteed to be same QR
        cv2.circle(frame_orig, copy_sq[0], 15, (100,255,255))

        # If same X
            # Look for same Y
        # Else
            # Look for same X


    cv2.imshow("screen", frame_orig)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
