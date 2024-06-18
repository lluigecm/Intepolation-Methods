# This file contains the RGB class, which is used to represent RGB colors from which pixel.

class RGB:

    r : int
    g : int
    b : int

    def __init__(self, r : int = 0, g: int = 0, b: int = 0):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return str(self.r) + ' ' + str(self.g) + ' ' + str(self.b)

    #overloading the + operator
    def __add__(self, other):
        return RGB(self.r + other.r, self.g + other.g, self.b + other.b)

    #overloading the - operator
    def __sub__(self, other):
        return RGB(self.r - other.r, self.g - other.g, self.b - other.b)