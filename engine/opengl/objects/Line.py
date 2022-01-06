from engine.opengl.VAO import VAO

import numpy as np
import pyrr

class Line:
    def __init__(self, positions, colour, width):
        self.colour = colour
        self.width = width

        positions = np.array(positions, dtype=np.float32)
        self.vao = VAO(len(positions))

        self.set_positions(positions)

    def set_positions(self, positions):
        float_positions = np.array(positions, dtype=np.float32)
        self.vao.store_data_in_attribute_list(0, 2, float_positions)