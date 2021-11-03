# ./AutoUploader/StageInfo.py
from AutoUploader.Enums import (StageTypes, ImageTypes)
from AutoUploader.Util import parseCamelCase

class StageInfo:
    def __init__(self, stageType: StageTypes, stage: str):
        self._stageType = stageType
        self.stage = stage # 25-15 / 505

    def buildImgPaths(self):
        type = parseCamelCase(self._stageType.name)
        fileStart = "Stage " if self._stageType.value == 0 else "Floor "
        imgAra = []
        for i in ImageTypes:
            imgAra.append(f'./Images/{i}/{type}/{fileStart}{self.stage}.png')
        
        return imgAra        
