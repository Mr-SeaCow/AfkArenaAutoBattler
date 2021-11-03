# ./ImageProc/Util.py
import cv2


def hconcatResize(imgList, interpolation = cv2.INTER_CUBIC):

    hMin = min(img.shape[0] for img in imgList)
      
    imListResize = [cv2.resize(img, (int(img.shape[1] * hMin / img.shape[0]), hMin), interpolation = interpolation) for img in imgList]

    return cv2.hconcat(imListResize)