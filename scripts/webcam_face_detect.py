#! //anaconda/bin/python
# python webcam_face_detect.py #haarcascade_frontalface_default.xml

import cv2
import sys
import numpy as np
import scipy.misc

haarPath = '/usr/local/Cellar/opencv/2.4.12/share/OpenCV/haarcascades'
#cascPath = sys.argv[1]
face_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_frontalface_default.xml')#cascPath)
eye_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_eye.xml')
body_cascade = cv2.CascadeClassifier(haarPath+'/haarcascade_fullbody.xml')
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    body = body_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for (x,y,w,h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    for (x,y,w,h) in body:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
        # Draw a rectangle around the faces
        #for (x, y, w, h) in faces:
        #    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', np.fliplr(scipy.misc.imresize(frame,25)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
