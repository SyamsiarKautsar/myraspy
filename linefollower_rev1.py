# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
from matplotlib import pyplot as plt
import time
import cv2
import imutils

ex =0
er = 0
laster = 0

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 0.7
color = (255, 0, 0)
pwmkiri = 0
pwmkanan = 0
  
# Line thickness of 2 px
thickness = 2

flagserial = 0
   

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480, 320)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(480, 320))
# allow the camera to warmup
time.sleep(0.1)

lineLower = (20, 100,100)
lineUpper = (30, 255,255)

#def pickRGB(event, x, y, flags, param):
#    if event == cv2.EVENT_MOUSEMOVE :  # checks mouse moves
#        colorsBGR = image[y, x]
#        colorsRGB=tuple(reversed(colorsBGR)) #Reversing the OpenCV BGR format to RGB format
#        print("RGB Value at ({},{}):{} ".format(x,y,colorsRGB))

        
#cv2.namedWindow('Frame')
#cv2.setMouseCallback('Frame', pickRGB)


##################################################################
#trackbar
#trackbar callback fucntion to update HSV value
def callback(x):
   global H_low,H_high,S_low,S_high,V_low,V_high
   #assign trackbar position value to H,S,V High and low variable
   H_low = cv2.getTrackbarPos('low H','controls')
   H_high = cv2.getTrackbarPos('high H','controls')
   S_low = cv2.getTrackbarPos('low S','controls')
   S_high = cv2.getTrackbarPos('high S','controls')
   V_low = cv2.getTrackbarPos('low V','controls')
   V_high = cv2.getTrackbarPos('high V','controls')


#create a seperate window named 'controls' for trackbar
cv2.namedWindow('controls',2)
cv2.resizeWindow("controls", 300,10);


#global variable
H_low = 5
H_high = 45
S_low= 100
S_high = 255
V_low= 60
V_high = 255
kon = 0

#create trackbars for high,low H,S,V 
cv2.createTrackbar('low H','controls',5,179,callback)
cv2.createTrackbar('high H','controls',45,179,callback)

cv2.createTrackbar('low S','controls',100,255,callback)
cv2.createTrackbar('high S','controls',255,255,callback)

cv2.createTrackbar('low V','controls',60,255,callback)
cv2.createTrackbar('high V','controls',255,255,callback)
###################################################################

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        kon = kon + 1
        image = frame.array
        #crop
        #cimg = image[120:200, 80:160]
        #cv2.imshow("cropped", cimg)
        imgcr = image[140:180,0:480]

        colorsBGR = image[160, 240]
        print("BGR Value {} ".format(colorsBGR))
        
        hsv = cv2.cvtColor(imgcr, cv2.COLOR_BGR2HSV)
        #colorsHSV= hsv[160, 240]
        #print("HSV Value {} ".format(colorsHSV))
        hsv_low = np.array([H_low, S_low, V_low], np.uint8)
        hsv_high = np.array([H_high, S_high, V_high], np.uint8)
        
        cv2.rectangle(image, (0,140), (480,180), (0,255,0), 2)
        
        #mask = cv2.inRange(hsv, lineLower, lineUpper)
        mask = cv2.inRange(hsv, hsv_low, hsv_high)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        if len(cnts) > 0:
           c = max(cnts, key=cv2.contourArea)
           ((x, y), radius) = cv2.minEnclosingCircle(c)
           M = cv2.moments(c)
           center = (int(M["m10"] / M["m00"]), 160)
           
           ex = center[0]
           

        cv2.circle(image, center, 20, (255,0,0), 2)
        #ex = center
        
        
        ######################################################
        #pid code
        maxpwm = 100

        pwmkiri = maxpwm
        pwmkanan = maxpwm
        ts = 0.1
        
        if ex > 220 and ex <260:
            er = 0
        else:
            er = -1*(240 - ex)

        #er = er / 10

        #pwmkiri = er/
        if er<0:
            
            pwmkiri = int(maxpwm + (er/240.0 * maxpwm))
        if er>0:
            
            pwmkanan = int(maxpwm - (er/240.0 * maxpwm))
            

        laster = er
        cv2.putText(image, "ex= " + str(ex), (50,50), font, fontScale, color, 2)
        cv2.putText(image, "eror= " + str(er), (50,100), font, fontScale, color, 2)
        cv2.putText(image, "pki= " + str(pwmkiri), (240,50), font, fontScale, color, 2)
        cv2.putText(image, "pka= " + str(pwmkanan), (240,100), font, fontScale, color, 2)
        cv2.putText(image, "flag= " + str(flagserial), (240,240), font, fontScale, color, 2)
        cv2.putText(image, "kon= " + str(kon), (240,290), font, fontScale, color, 2)
        #pid code
        ######################################################

        cv2.imshow('Frame', image)
        #cv2.imshow('Frame2', imgcr)
        cv2.imshow('Framecv', mask)
        #####################################################
        
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop

        if kon >30:
                kon = 0
        
        if key == ord("1"):
                flagserial = 1
                
        if key == ord("0"):
                flagserial = 0
                
        if key == ord("q"):
                break

cv2.destroyAllWindows()

