# ./ImageRec/Util.py
import os, os.path

import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def getGrayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def getImageText(imgName):
    img = imgName
    if not isinstance(img, np.ndarray):
        img = cv2.imread(imgName)

    img = Thresholding(img)
    return pytesseract.image_to_string(img, config=r'-l eng --psm 6').split('\n', 1)[0].replace('\n', '')

def Thresholding(img, low=220, upper=255):
    return cv2.threshold(getGrayscale(img), low, upper, cv2.THRESH_BINARY_INV)[1]

def getHeroLevel(imgName):
    img = imgName
    if not isinstance(img, np.ndarray):
        img = cv2.imread(imgName)
    return pytesseract.image_to_string(img, config=r'--psm 6').split('\n', 1)[0].replace('\n', '')

def getFloor(text):
    newstr = ''.join((ch if ch in '0123456789' else ' ') for ch in text)
    return [int(i) for i in newstr.split()][0]