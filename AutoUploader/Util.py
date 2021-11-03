# ./AutoUploader/Util.py
import numpy as np
import cv2
possibleImgLocations = [(355, -949, 122, 141), (390, -928, 132, 151), (405, -950, 170, 185)]

def cropImg(img, loc=0):
    x1, x2, y1, y2 = possibleImgLocations[loc]
    retImg = img[x1:x2, y1:y2].copy()
    #cv2.imwrite(f'tempLevel{loc}.png', retImg)
    return img[x1:x2, y1:y2].copy()

def autoCrop(image, threshold=40):
    if len(image.shape) == 3:
      flatImage = np.max(image, 2)
    else:
      flatImage = image
    assert len(flatImage.shape) == 2
    
    rows = np.where(np.max(flatImage, 0) > threshold)[0]
    if rows.size:
      cols = np.where(np.max(flatImage, 1) > threshold)[0]
      image = image[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
    else:
      image = image[:1, :1]
    
    return image

def parseCamelCase(str):
    return ''.join(map(lambda x: x if x.islower() else " "+x, str)).strip()