# ./AutoUploader/main.py
import cv2
import numpy as np
import os

from AutoUploader.Util import *
from AutoUploader.StageInfo import *

from ImageProc.Util import hconcatResize

from ImageRec.Util import *


class AutoUploader:
    def __init__(self, battleStatsPath, heroInfoPath, stage):
        self._battleStats = cv2.imread(battleStatsPath)
        self._heroInfo = cv2.imread(heroInfoPath)

        self.stitchImages()

        cv2.imwrite('heroInfo.png', self._heroInfo)
        cv2.imwrite('battleStats.png', self._battleStats)
        #cv2.imwrite('stitchedImg.png', self._stitchedImage)

        self.prepImg()

        self._lvl = self.fetchLevel()
        cv2.imwrite(f'./Images/ReadyToUpload/RC {self._lvl} {stage}.png', self._stitchedImage)
    
    def prepImg(self):
        self._heroInfo = self.trimImgBorders(self._heroInfo)
        self._heroInfo = self.thresholdImg(self._heroInfo)

    def trimImgBorders(self, img):
        return autoCrop(img.copy(), 40)

    def thresholdImg(self, img):
        return Thresholding(img, low=125, upper=220)
    
    def stitchImages(self):
         self._stitchedImage = hconcatResize([self.trimImgBorders(self._heroInfo.copy()), self.trimImgBorders(self._battleStats.copy())])

    def fetchLevel(self):
        for i in range(len(possibleImgLocations)):
            croppedImg = cropImg(self._heroInfo.copy(), i)
            #print(croppedImg.shape)
            if croppedImg.shape[0] == 0 or croppedImg.shape[1] == 0:
                continue
            tempLevel = getHeroLevel(cropImg(self._heroInfo.copy(), i))

            if tempLevel.isdigit() == True:
                return int(tempLevel)

        return None


directory = r'./Images/HeroInfo/Campaign/'
for entry in os.scandir(directory):
    if (entry.path.endswith(".jpg") or entry.path.endswith(".png")) and entry.is_file() and '35' in entry.path:
        stage = entry.path.split("Stage ")[1].replace('.png', '')
        curStage = StageInfo(StageTypes(0), stage)
        imgPaths = curStage.buildImgPaths()
        print(stage)
        uploader = AutoUploader(imgPaths[0], imgPaths[1], stage)