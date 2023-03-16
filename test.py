import cv2 as cv
import numpy as np

blank = np.zeros((500,500),dtype='uint8')
cv.rectangle(blank,(0,0),(250,250),(255,255,255), thickness=-1)

cv.imshow('Blank',blank)

cv.waitKey(0)