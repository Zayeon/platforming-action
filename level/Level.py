import numpy as np


class Level:
    def __init__(self):
        self.chunks = [
                {
                    "location": (0, 0),
                    "collision_data": np.zeros((32, 32), dtype=np.bool),
                    "layers": [
                        np.full((32, 32), -1)
                    ]
                },
                {
                    "location": (-1, 0),
                    "collision_data": np.zeros((32, 32), dtype=np.bool),
                    "layers": [
                        np.full((32, 32), -1)
                    ]
                },
            ]
        self.texture_atlas = None
        self.clear_colour = (0.13, 0, 0, 1)