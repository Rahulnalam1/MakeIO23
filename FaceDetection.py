from djitellopy import tello
import cv2
import numpy as np
import time


ai = tello.Tello()
ai.connect()
print(ai.get_battery())
ai.streamon()

ai.takeoff()
ai.send_rc_control(0, 0, 26, 0)

w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
#Proporstional, Integral, Derivative
pError = 0


def faceFinder(image):
    faceCascade = cv2.CascadeClassifier("/Users/rahulnalam/PycharmProjects/Rahul's Projects/HackathonProjects/HackAi/Resources "
                                        "/Images/haarcascade_frontalface_default.xml")
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Converts image into gray
    faces = faceCascade.detectMultiScale(imageGray, 1.2, 8)

    myFaceListCenter = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        #w = width y = height
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 3)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(image, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListCenter.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        #Gives us the index of the max value and the max value area
        i = myFaceListArea.index(max(myFaceListArea))
        return image, [myFaceListCenter[i], myFaceListArea[i]]
    else:
        return image, [[0,0], 0]



#Drne Face Tracking

def faceTracking(info, w, pid, pError):

    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    # w // w is the center of our image, we want to find out how far object is from center
    speed = pid[0] * error + pid[1] * (error - pError)
    #Changing sensitivity with this error on top ^^
    speed = int(np.clip(speed, -100, 100))
    #making sure the speed doesn't leave those bounds




    #Condition to stay still
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    #If the face is too close, drone will move backwards
    elif area > fbRange[1]:
        fb = -20
    #If the face is too far, drone wil move forwards
    elif area < fbRange[0] and area != 0:
        #because 600 is greater than 0, it will just keep moving forwards, so it can't equal 0
        fb = 20

    ai.send_rc_control(0, fb, 0, speed)
    return error


#webcap = cv2.VideoCapture(0)

#While loop to make sure the output image of the webcam is being shown
while True:
    #_, image = webcap.read()
    image = ai.get_frame_read().frame
    image = cv2.resize(image, (360, 240))
    image, info = faceFinder(image)
    pError = faceTracking(info, w, pid, pError)
    #If someone is more forward to the camera, the area will increase, if not the area will decrease
    #Center values will be used when human is moving and drone is trying to rotate to reposition
    #Area values will be used to go forwards and backwards
    #print("Center", info[0], "Area", info[1])
    cv2.imshow("Output Image", image)

