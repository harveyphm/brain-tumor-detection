
import cv2
import numpy as np

def edgeDetection(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #get bounding box for each contour
    boxes = [cv2.boundingRect(c) for c in cnts]
    return cnts
    

def findTumorContour(image, sigma=0.33):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, 0.7)
    # #Histogram equalization
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # gray = clahe.apply(gray)
    #Gaussian blur
    gray =  cv2.GaussianBlur(gray, (5, 5), 0)
    #Thresholding
    _, thresh = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
    _, threshInv = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    #thresh = (thresh + threshInv) //2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations = 19)
    closed = cv2.dilate(closed, None, iterations = 17)
    _,mask = cv2.threshold(closed, 155, 255, cv2.THRESH_BINARY) 
    final = cv2.bitwise_and(image,image,mask = mask) 
    cnts = edgeDetection(mask, sigma=sigma)
    boxes = [cv2.boundingRect(c) for c in cnts]

    return boxes, cnts, final