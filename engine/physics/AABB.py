import numpy as np

class AABB:
    def __init__(self, pos, size):
        self.position = np.array(pos, dtype=np.float32)
        self.size = np.array(size, dtype=np.float32)
        self.velocity = np.zeros(2)

    def set_velocity(self, vel):
        self.velocity = np.array(vel, dtype=np.float32)