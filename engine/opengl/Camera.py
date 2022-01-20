import numpy as np

class Camera:
    def __init__(self):
        self.position = np.zeros(3, dtype=np.float32)

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def get_position(self):
        return self.position