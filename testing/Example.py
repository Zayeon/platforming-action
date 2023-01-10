import pyrr
import numpy as np
from math import radians
class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class B:
    def __init__(self, a):
        self.a = a

a = A(1, 2)
b1 = B(a)
a = A(2, 2)
b2 = B(a)

pass