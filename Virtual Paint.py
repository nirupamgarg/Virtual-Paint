import cv2
import numpy as np
frameWidth = 640
frameHeight = 480

cap=cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)


myColors = [[69, 144, 0, 179, 255, 255], [0, 0, 0, 179, 71, 81]]
colorvalues = [[255, 0, 0], [255, 255, 255]]
mypoints = []  #[x, y, colorId]

def findcolor(img, myColors, colorvalues):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newpoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_HSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, colorvalues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x, y, count])
        count+=1
        #cv2.imshow(str(color[0]), mask)
    return newpoints
    
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)    
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def draw(mypoints, colorvalues):
    for point in mypoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, colorvalues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newpoints = findcolor(img, myColors, colorvalues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        draw(mypoints, colorvalues)
            
    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
