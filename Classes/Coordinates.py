# ./Classes/Coordinates

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