import cv2
import numpy as np
import pytesseract
import os, os.path
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def getImageText(imgName):
    img = cv2.imread(imgName)
    img = Thresholding(img)
    return pytesseract.image_to_string(img, config=r'-l eng --psm 6').split('\n', 1)[0].replace('\n', '')

def Thresholding(img):
    return cv2.threshold(get_grayscale(img), 220, 255, cv2.THRESH_BINARY_INV)[1]

def getFloor(text):
    newstr = ''.join((ch if ch in '0123456789' else ' ') for ch in text)
    return [int(i) for i in newstr.split()][0]