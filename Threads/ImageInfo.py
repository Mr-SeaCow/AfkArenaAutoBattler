import numpy as np

def to_str(var):
    return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]

class Coordinates:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x;

    @property
    def y(self):
        return self._y;

    @x.setter
    def x(self, val):
        self._x = val
    
    @y.setter
    def y(self, val):
        self._y = val

    @property
    def location(self):
        return self._x, self._y

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
            return 'Key: ' + self.key + ' X: ' + to_str(self.x) + ' Y: ' + to_str(self.y)
        return 'Key: ' + self.key