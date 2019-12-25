import math

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __mul__(self, n):
        return Vec(self.x * n, self.y * n)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def unit(self):
        m = self.mag()
        return Vec(self.x / m, self.y / m) if m else Vec(0, 0)