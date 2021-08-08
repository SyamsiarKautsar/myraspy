# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
from matplotlib import pyplot as plt
import time
import cv2
import imutils

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

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
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
        
        
        cv2.rectangle(image, (0,140), (480,180), (0,255,0), 2)
        
        mask = cv2.inRange(hsv, lineLower, lineUpper)
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


        cv2.circle(image, center, 20, (255,0,0), 2)
        
        cv2.imshow('Frame', image)
        #cv2.imshow('Frame2', imgcr)
        
        
        cv2.imshow('Framecv', mask)
        
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

cv2.destroyAllWindows()

