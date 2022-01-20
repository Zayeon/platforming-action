import numpy as np


class Level:
    def __init__(self):
        self.chunks = [
                {
                    "location": (0, 0),
                    "collision_data": np.zeros((32, 32), dtype=np.bool)
                },
                {
                    "location": (-1, 0),
                    "collision_data": np.zeros((32, 32), dtype=np.bool)
                },
            ]

