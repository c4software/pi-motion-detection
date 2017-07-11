import picamera
import cv2
import time
import picamera.array

# Import the face detection haar file
face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')


with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.rotation = 270
    camera.framerate = 32

    while True:
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            frame = stream.array
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 2, 5)
            if (len(faces) > 0):
                print ("Face detected")
            else:
                print ("No face")
