from OpenGL.raw.GL.VERSION.GL_1_1 import GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP

from engine.opengl.VAO import VAO

import numpy as np
import pyrr

class Line:
    LINE = GL_LINES
    LINE_STRIP = GL_LINE_STRIP
    LINE_LOOP = GL_LINE_LOOP

    def __init__(self, positions, colour, width, mode=LINE):
        self.colour = colour
        self.width = width
        self.mode = mode

        positions = np.array(positions, dtype=np.float32)
        self.vao = VAO(len(positions))

        self.set_positions(positions)

    def set_positions(self, positions):
        float_positions = np.array(positions, dtype=np.float32)
        self.vao.store_data_in_attribute_list(0, 2, float_positions)