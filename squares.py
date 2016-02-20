import cv2

cap = cv2.VideoCapture(0)
# set resolution to low


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # gray and blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    edge = cv2.Canny(blur, 50, 150)

    cv2.imshow('edge', edge)

    (cnts,_) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL,
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
            solidity = area / float(hullArea)

            keepSolidity = solidity > 0.9
            keepAspectRatio = (aspectRatio >= 0.8 and aspectRatio <= 1.2 ) \
            or (aspectRatio >= 1.8 and aspectRatio <= 2.2)

            if keepSolidity and keepAspectRatio:
                cv2.drawContours(frame, [approx], -1, (0,0,255), 4)
                print "a"
    cv2.drawContours(frame, squares, -1, (0, 255,0), 3)
    cv2.imshow("screen", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
