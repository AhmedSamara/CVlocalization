import cv2

cap = cv2.VideoCapture(0)
# set resolution to low


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    frame_orig = frame

    # gray and blur
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (7,7), 0)
    cv2.imshow('blur', frame)
    #frame = cv2.adaptiveThreshold(frame ,255  
    #        , cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    frame = cv2.Canny(frame, 50, 150)

    cv2.imshow('edge', frame)

    (cnts,_) = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    squares = []
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
            or (aspectRatio >= 1.8 and aspectRatio <= 2.2)

            if keepSolidity :
                cv2.drawContours(frame_orig, [approx], -1, (0,0,255), 4)
    cv2.drawContours(frame_orig, squares, -1, (0, 255,0), 3)
    cv2.imshow("screen", frame_orig)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
