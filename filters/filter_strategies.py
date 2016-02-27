import cv2

def no_filter(im):
    return im

def basic_filter(im):
    """Attempts to improve viewing by applying filters """
    # grayscale
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    im = cv2.bilateralFilter(im, 9, 75, 75) 
    return im


def blur_bw(im):
    # todo, expirement different threshholds
    im = cv2.GaussianBlur(im, (5,5), 0)
    im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
    return im

def blur_adaptive_thresh(im):
    im = cv2.GaussianBlur(im, (5,5), 0)
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    return im


    
