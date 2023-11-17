# ./ImageRec/ImageStitch.py
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np

from ImageRec.Util import getGrayscale

def cropImg(img, top=200, bottom=600):
    return img[top:img.shape[0]-bottom :].copy()

def trimBlankSpace(frame):
    if not np.sum(frame[0]):
        return trimBlankSpace(frame[1:])
    if not np.sum(frame[-1]):
        return trimBlankSpace(frame[:-2])
    if not np.sum(frame[:,0]):
        return trimBlankSpace(frame[:,1:])
    if not np.sum(frame[:,-1]):
        return trimBlankSpace(frame[:,:-2])
    return frame

def floodFillBackground(img, seedPoints, d):

    cv2.floodFill(img, None, seedPoint=seedPoints[0], newVal=(0, 0, 0), loDiff=(d,d,d,d), upDiff=(d,d,d,d))
    cv2.floodFill(img, None, seedPoint=seedPoints[1], newVal=(0, 0, 0), loDiff=(d,d,d,d), upDiff=(d,d,d,d))

    return img

def stitchImages(imgAra, topCrop, bottomCrop, outputName='./Images/ScreenShots/StitchTest.png', difference=15):
    img_ = cropImg(cv2.imread(imgAra[0]), topCrop, bottomCrop)
    seedPoints = [(10, 10)]
    for imgNumber in range(1, len(imgAra)):
        print(img_.shape[0])
        img = cropImg(cv2.imread(imgAra[imgNumber]), topCrop, bottomCrop)

        img1 = getGrayscale(img_.copy())
        img2 = getGrayscale(img.copy())

        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)

        match = cv2.BFMatcher()
        matches = match.knnMatch(des1,des2,k=2)#2)

        good = []
        for m,n in matches:
            if .03*m.distance < 0.03*n.distance:
                good.append(m)
    
        MIN_MATCH_COUNT = 10
        if len(good) > MIN_MATCH_COUNT:
            srcPts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,2,1)
            dstPts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,2,1)

            M, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)

            h,w = img1.shape
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts, M)

        else:
            print("Not enought matches are found - %d/%d", (len(good)/MIN_MATCH_COUNT))

        dst = cv2.warpPerspective(img_,M,(img.shape[1], img.shape[0]))
        trimmedDst= trimBlankSpace(dst)
        imgToBeConcat = img_[0:img_.shape[0]-trimmedDst.shape[0] :].copy()
        seedPoints.append((10, img_.shape[0]))
        img_ = cv2.vconcat([imgToBeConcat, img])

    outputImg = floodFillBackground(img_, seedPoints, difference)

    cv2.imwrite(outputName, outputImg)


def battleStitch(imgList):
    imgAra = []

    maxRowSize = len(imgList) if len(imgList) < 4 else math.ceil(len(imgList) / 2)

    for name in imgList:
        imgAra.append(cv2.imread(name))

    length = len(imgAra)
    rowCount = math.ceil(len(imgAra)/4)
    extraTiles = rowCount*maxRowSize - length

    rows = []
    for _ in range(0, extraTiles):
        imgAra.append(np.zeros((imgAra[0].shape[0],imgAra[0].shape[1],3), np.uint8))

    for row in range(0, rowCount):
        rows.append(cv2.hconcat(imgAra[row*maxRowSize:row*maxRowSize+maxRowSize]))

    cv2.imwrite('./Images/ScreenShots/vconcatTest.png', cv2.vconcat(rows))
