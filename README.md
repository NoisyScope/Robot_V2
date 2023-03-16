# Robot_V2
This project consist of a program who can identify the size of a shoe through computer vision and start a routine in RoboDK for a shoe cleaning procedure.

[Showcase video](https://youtu.be/orsK2iC0slo)

## System Explanation:
The main.py code constructs parting from 2 elemental funcions ( visiontest.py  &  takepic.py ) which have the function of taking a picture of a selected COM device, processing it, start looking for contours in order to measure the size of an object and resulting in outputting the object's size as well as running a command in RoboDK which will result in a specific routine inicialization.

## Code basics
Starting with the code analysis and explanation, firstable, we will need to take a picture. This will lead us to the first code we will need to use:
### takepic.py
This code's funcion rely on communicating with the camera through a COM port and displaying the camera's perspective.
```
cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
```
While the image is being displayed on real time, the system will be waiting for the 'SPACE' key press in order to take a picture which will be saved as: 'frame0.png'. When the picture is taken, the terminal will showcase the message " written! ". In order to exit the camera preview and entering the next step, we will need to press the 'ESC' key. This will lead us to the next step
### visiontest.py
As soon as `takepic.py` ends, we will start by loading the original image taken by this code. Then, we will need to pre-process the image in order to facilitate the computer recognition system with the following statements:
```
image = cv2.imread('frame0.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
cv2.rectangle(gray,(0,0),(129,480),(0,0,0),thickness = -1)
cv2.rectangle(gray,(460,0),(640,480),(0,0,0),thickness = -1)
cv2.circle(gray,(332,360),40,(0,0,0),thickness=-1)
cv2.imshow('Previo',gray)
```
Partig from the second line, we have modified the image colour profile to grayscale using `cv2.COLOR_BGR2GRAY` statement, followed by blurring the image with the objective of eliminating grain from the camera lens as well as any imperfection on the surface. The next step is creating black figures around the vital processing area in order to simplify the contour recognition system. This is particulary importantdue due to the code being configured to export the last measured distance. The last figure consist of a circle in charge of covering the shoe insole which usually contains the brand and will disrupt the measurement process.

The following statements will perform the edge detection, followed by a dilation + erosion of the image with the objective of closing the gap between the object edges.
```
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
```

