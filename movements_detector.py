import imutils
import math
import cv2
import numpy as np
import picamera
import picamera.array
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("--keep", help="Keep only image bounds.", action="store_true")
args = ap.parse_args()

def testIntersectionIn(x, y):
    res = -450 * x + 400 * y + 157500
    if((res >= -550) and  (res < 550)):
        print (str(res))
        return True
    return False



def testIntersectionOut(x, y):
    res = -450 * x + 400 * y + 180000
    if ((res >= -550) and (res <= 550)):
        print (str(res))
        return True

    return False

camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.rotation = 270
camera.framerate = 32

firstFrame = None
movement_detected = 0

while True:
    stream = picamera.array.PiRGBArray(camera)
    camera.capture(stream, format='bgr')

    # resize the frame, convert it to grayscale, and blur it
    frame = stream.array
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    # After compute update the firstFrame to get only change
    firstFrame = gray
 
    
    bounds_item = 0
    time_shot = time.time()

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) > 12000:
            # Add to counter
            print ("New movement detected {}".format(movement_detected))

            # Draw bound in the image
            (x, y, w, h) = cv2.boundingRect(c)
            
            if not args.keep:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rectagleCenterPont = ((x + x + w) /2, (y + y + h) /2)
                # Write image to disk (with bound in it)
                cv2.imwrite('result_{0}.jpg'.format(time_shot), frame)
            else:
                # Extract bound
                cv2.imwrite('bounds_{0}_{1}.jpg'.format(bounds_item, time_shot), frame[y:y+h, x:x+w])

            bounds_item = bounds_item + 1
            movement_detected = movement_detected + 1
