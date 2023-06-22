import cv2
from matplotlib import pyplot as plt

path='/home/raspberrypi/Desktop/pycar/testflask/objectDetection/models/'
def detect(img):
    # OpenCV opens images as BRG 
    # but we want it as RGB We'll 
    # also need a grayscale version
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = img
    
    
    # Use minSize because for not 
    # bothering with extra-small 
    # dots that would look like STOP signs
    lowerbody = cv2.CascadeClassifier(path+'haarcascade_lowerbody.xml')
    profileface = cv2.CascadeClassifier(path+'haarcascade_profileface.xml')

    
    found_lowerbody = lowerbody.detectMultiScale(img_gray, 
                                    minSize =(10, 10))
    found_profileface = profileface.detectMultiScale(img_gray, 
                                    minSize =(10, 10))
    
    # Don't do anything if there's 
    # no sign
    amount_found_lowerbody = len(found_lowerbody)
    amount_found_profileface = len(found_profileface)
    
    if amount_found_lowerbody != 0:
        
        # There may be more than one
        # sign in the image
        for (x, y, width, height) in found_lowerbody:
            
            # We draw a green rectangle around
            # every recognized sign
            cv2.rectangle(img_rgb, (x, y), 
                        (x + height, y + width), 
                        (0, 0, 255), 3)
    if amount_found_profileface != 0:
        
        # There may be more than one
        # sign in the image
        for (x, y, width, height) in found_profileface:
            
            # We draw a green rectangle around
            # every recognized sign
            cv2.rectangle(img_rgb, (x, y), 
                        (x + height, y + width), 
                        (0, 255, 0), 3)
        
    return img_rgb
    # Creates the environment of 
    # the picture and shows it
    """ plt.subplot(1, 1, 1)
    plt.imshow(img_rgb)
    plt.show() """