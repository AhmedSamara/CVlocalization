import numpy as np
import cv2
import time
from PIL import Image
from PIL import ImageEnhance

class block:
    def __init__(self, size, color):
        self.size = size
        self.color = color

def enhance_color(bgr):
    
    size = 320,240
    #crop and enhance the image for color
    rgb = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    
    pil_im = Image.fromarray(rgb)
    
    pil_im.thumbnail(size, Image.ANTIALIAS)
    
    w, h = pil_im.size
    w_3 = int(w/3)
    h_6 = int(w/6)
    
    pil_cropped = pil_im.crop((w_3,h_6,w-w_3, h- h_6))
    converter = ImageEnhance.Color(pil_cropped)
    enhanced = converter.enhance(3.0)
    pil_image = enhanced.convert('RGB') 
    open_cv_image = np.array(pil_image)
    
    # Convert RGB to BGR 
    rgb_enhanced = open_cv_image[:, :, ::-1].copy()
    bgr_enhanced = cv2.GaussianBlur(rgb_enhanced,(9,9),0)
    return bgr_enhanced

def num_to_color(number):
    if number == 0:
        return "red"
    if number == 1:
        return "blue"
    if number == 2:
        return "yellow"
    if number == 3:
        return "green"
    else:
        return None

def find_center(cnt):
    (x,y), r = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    return center

def check_color(hopper_pos):
    
    largest = None
    
    """
    #make sure it lack a color field
    if (self.hopper[hopper_pos] != None):
        if (self.hopper[hopper_pos].data != None:)
            print "Color already known."
            return 1
    #look at the hopper
    arm.Orientor(hopper_pos + 1)
    self.joints = [HOPPER_LOOK]
    time.sleep(3)
    """
    
    #get the image
    cap.grab()
    cap.grab()
    cap.grab()
    cap.grab()
    ret, bgr = cap.read()
    
    #enhance and show the image with gaussian and color
    bgr_enhanced = enhance_color(bgr)
    cv2.imshow("enhanced",bgr_enhanced)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return None
    
    # define the list of boundaries
    boundaries = [
        ([0,0,120], [230,50,255]),                          #red bgr  GOOD
        ([220,0,0], [255,150,150]),                         #blue bgr GOOD
        ([0,125,125], [100,255,255]),                       #yellow bgr GOOD
        ([75,120,0], [185,255,75])                           #green: bad
    ]
    
    # loop over the boundaries
    count = 0
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower)
        upper = np.array(upper)

        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(bgr_enhanced, lower, upper)
        mask = cv2.erode(mask, None, iterations=10)
        output = cv2.dilate(mask, None, iterations=5)
         
        #find contours of the masked output
        (cnts,_) = cv2.findContours(output.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        cnt = 0
        for contour in cnts:
            size = cv2.contourArea(contour)
            if largest != None:
                if (size > largest.size):
                    largest = block(size, num_to_color(count))
            else:
                largest = block(size, num_to_color(count))
                
            center = find_center(contour)
            cv2.circle(output, center, 5, (0,0,255), -1) 
            cnt += 1
            
        count += 1
    return largest
    
    
    
    
    
    
    
    
    
cap = cv2.VideoCapture(-1)
x = int(cap.get(3))
y = int(cap.get(4))

print "X = ", x
print "Y = ", y

x_mid = int(x/2)
y_mid = int(y/2)

x_third = int(x/3)

while True:
    largest = check_color(1)
    print largest
    if largest == None:
        continue
    print largest.color
    
cap.release()
cv2.destroyAllWindows()
    
    
    
    
    
    
    
    