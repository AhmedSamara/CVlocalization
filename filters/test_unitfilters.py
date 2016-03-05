import cv2
import unittest



def im_loop(images):
    for im in images:
        im_count += 1
        _, cleaned_im = strategy_function(im)

        cv2.imwrite('buffer.png', cleaned_im)
        #im to zbar frame
        cv2.imshow('cleaned_im', cleaned_im)
        cv2.waitKey(0)

        pil_im = Image.open('buffer.png').convert('L')
        width, height = pil_im.size
        raw = pil_im.tobytes()
        # zbar data
        z_im = zbar.Image(width, height, 'Y800', raw)
        for symbol in z_im:
            qr_count += 1
 


def process_im(im):
        cleaned_im = function(im)
        cv2.imwrite('buffer.png', cleaned_im)
        pil_im = Image.open('buffer.png').convert('L')
        width, height = pil_im.size
        raw = pil_im.tobytes()
        # zbar data
        z_im = zbar.Image(width, height, 'Y800', raw)

        q
        for symbol in z_im:
            qr_count += 1
             


def no_filter(images):
    cleaned_ims = []
    for im in images:
        cleaned_ims.append(im)
    return cleaned_ims

def basic_filter(im):
    """Attempts to improve viewing by applying filters """
    # grayscale

    cleaned_ims = []
    for im in images:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        im = cv2.bilateralFilter(im, 9, 75, 75) 
        cleaned_ims.append(im)


    return cleaned_ims


def blur_bw(im):
    cleaned_ims = []
    for im in images:
        # todo, expirement different threshholds
        im = cv2.GaussianBlur(im, (5,5), 0)
        im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
        cleaned_ims.append(im)

    return cleaned_ims


def blur_adaptive_thresh(im):
    cleaned_ims = []
    for im in images:
        im = cv2.GaussianBlur(im, (5,5), 0)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        cleaned_ims.append(im)


    return cleaned_ims



class TestFilters(unittest.Testcase):

    def setup
    def no_filter(im):
        return im



        
