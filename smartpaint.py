import cv2
import numpy as np
frameWidth = 1280
frameHeight = 720
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
myColors = [[0,101,194,40,169,255],
          [115,43,140,157,255,255],
          [40,97,100,255,133,255],
          [0,113,176,109,188,255],
          [99,107,166,255,143,255]
          ]
mypoints = []
colorNames = {0 : "Orange", 1:  "Purple", 2 : "Green", 3 : "Yellow", 4 : "Blue"}
colorValues = [[51,153,255], [255,0,255], [0,255,0], [0,255,255], [255,255,0]]
def getcolor(img, myColors, colorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        # upper = np.array(imgHSV, lower, upper)
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,colorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count = count+1
    return newpoints
        # cv2.imshow("img", mask)
def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValues):
    for point in mypoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)
while True:
    success, img = cap.read()
    imgResult = img.copy()
    newpoints = getcolor(img, myColors, colorValues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        drawOnCanvas(mypoints,colorValues)
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
