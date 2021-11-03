# ./Classes/ImageInfo
from Classes.Coordinates import Coordinates
from Classes.Util import npToStr

class ImageInfo(Coordinates):
    def __init__(self, key, found=False, x=0, y=0):

        super().__init__(x, y)

        self._key = key
        self._found = found

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def found(self):
        return self._found

    @found.setter
    def found(self, value):
        self._found = value

    def setCoords(self, img):
        self.x, self.y = img
        self.found = True
    
    def __str__(self):
        if self.found == True:
            return 'Key: ' + self.key + ' X: ' + npToStr(self.x) + ' Y: ' + npToStr(self.y)
        return 'Key: ' + self.key