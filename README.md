# Robot_V2
This project consist of a program who can identify the size of a shoe through computer vision and start a routine in RoboDK for a shoe cleaning procedure.

[Showcase video](https://youtu.be/orsK2iC0slo)
[Showcase video with EDM music](https://youtu.be/9FuHWFlsXtw)

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
Nextly, we have to find the contours in the edge map which then will be followed by sorting the contours from left-to-right and initializing the 'pixels per metric' calibration variable
 ```
 cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None
 ```
Then, we will start the grind (the code will, so don't worry too much). The code wil loop through every contour individually in order to draw an outline of the shape we are measuring. ***Important note:*** , we will need a reference object on the top-left of the image in order to calibrate the camera. In this case it is a known-size green circle. 

The next step consist of creating a rectangle which encapsulates the already connected contours of the image, followed by calculating the midpoints of the rectangle. Then, it will be pixel measured based on the last circle reference, which will include the correct pixel-to-metric conversion.
```
	for (x, y) in box:
		cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
    	(tl, tr, br, bl) = box
	    (tltrX, tltrY) = midpoint(tl, tr)
	    (blbrX, blbrY) = midpoint(bl, br)
      (tlblX, tlblY) = midpoint(tl, bl)
	    (trbrX, trbrY) = midpoint(tr, br)
```
We will use the Euclidean distance between the midpoints in order to make the pixel-to-metric conversion.
```
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
```
Finally, we will display the rectangles, midpoints and the metric calculated distances over the original image: `"frame0.png"` and output the height of the last measured distance `"height"` to our `main.py` code.
### main.py
This is the final step, as well as the only code the user will need to interact with. This is because this code will call the last explained programs in order to simplify code structure and debugging.
The second statement imports our `visiontest.py` program and runs it as a secondary function. Next, we will create a delay between the finalization of the previous code in order to properly extract the `"height"` variable and printing it.

Finally, parting from RoboDK API we will run the following statement:
```
RDK.RunCode('final',True)
```
This will initialize any program contained in our RoboDK environment containing the name: 'final' and will try to run it. If the condition is satisfied, we will see our RoboDK program starting it's programmed routine.

## Further implementation
In order to complete and further develop this project, we could split the complete robot's code in mid stages in the ability of being able to call them individually. This will let us maintain the same elemental routine and be able to modify the shoe routes in order to select through a database the proper one. Taking this one step further, we could implement a deep learning computer analysis in order to identify the type of object which is shown to the camera along adaptative messages which will inform the end-user about the shoe's condition, alignment and colour in order to imporoving the experience through the machine.
