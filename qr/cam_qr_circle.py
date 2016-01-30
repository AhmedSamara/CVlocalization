import zbar
from PIL import Image
import cv2
import numpy as np



scanner = zbar.ImageScanner()
scanner.parse_config('enable')

cam = cv2.videoCapture(0)



while True:
    _, frame = cam.read()

    scanner.scan(frame)

    for symbol in frame:
        tl, tr, bl, br = [item for item in symbol.location]
        rec = cv2.minAreaRect
