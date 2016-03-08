from sys import argv
import cv2

#n = int(argv[1])


cap = cv2.VideoCapture("/dev/video0")
# set resolution to low

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    print ret

    cv2.imshow('surf', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
