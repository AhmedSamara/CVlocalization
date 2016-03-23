from sys import argv
import subprocess

import cv2


cmd = "readlink -f /dev/PSCAM"

process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
out = process.communicate()[0]

print "==========="
print out
print "========="

nums = [int(x) for x in out if x.isdigit()]

print "nums, ", nums[0]


cap = cv2.VideoCapture(nums[0])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('surf', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
