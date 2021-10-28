import numpy as np
import cv2 as cv
import sys
from numpy.core.fromnumeric import size
from scipy.ndimage import label

def func(img):
    img = cv.bilateralFilter(img, 15, 75, 75)
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    #зелённая часть листа
    healthy_part = cv.inRange(hsv_img, (36, 25, 25), (86, 255, 255))
    #находим тень 
    t = cv.inRange(hsv_img, (0, 0, 0), (360, 255, 50))
    tt = cv.add(cv.bitwise_not(t), healthy_part)

    mark = np.zeros((img.shape[0], img.shape[1]), dtype = "int32")
    mark[0:20, 0:20] = 1
    mark[236:255, 0:20] = 1
    mark[0:20, 236:255] = 1
    mark[236:255, 236:255] = 1
    mark[90:140, 90:140] = 255
    cv.watershed(img, mark)
    lt = cv.convertScaleAbs(mark)

    list = cv.bitwise_and(lt, tt)

    ill_part = list - healthy_part
    mask = np.zeros_like(img, np.uint8)
    mask[list > 1] = (255, 0, 255)
    mask[ill_part > 1] = (0, 0, 255)

    return mask

print("Введите номер картинки")
n = input() 

img = cv.imread('assets/test/{}.jpg'.format(n))
if img is None :
    sys.exit( "Could not re ad the image . " )

cv.imshow('img', img)
cv.imshow('result', func(img))
cv.waitKey(0)