import numpy as np
# Class with static method
class math():

    def add(a, b):
        return a + b
    

print(math.add(1, 2))

# Class with instance method

class slope():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def calculate(self, x):
        return np.dot(self.a, x) + self.b
    
    def inverse(x):
        return 1/x

    
slope1 = slope(2, 1)
print(slope1.calculate(2))
print(slope.inverse(2))

import math
# Heritance
class parabola(slope):
    def __init__(self, a, b, c):
        super().__init__(a, b)
        self.c = c

    def calculate(self, x):
        return np.dot(self.a, math.pow(x, 2)) + np.dot(self.b, x) + self.c
    
parabola1 = parabola(1, 1, 2)
print(parabola1.calculate(2))
