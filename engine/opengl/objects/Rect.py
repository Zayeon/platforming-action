from engine.opengl.VAO import VAO

import numpy as np
import pyrr

class Rect:
    indices = [0, 1, 2,
               0, 2, 3]

    vertex_data = [
        0, 0, 0,
        0, 1, 0,
        1, 1, 0,
        1, 0, 0,
    ]

    def __init__(self, position, size, colour):
        self.colour = colour
        self.scale = pyrr.matrix44.create_from_scale(np.array([size[0], size[1], 1]))
        self.position = np.array([position[0], position[1], 0], dtype=np.float32)

        self.vao = VAO(len(self.indices))

        self.set_positions(self.vertex_data)
        self.set_indices(self.indices)

    def set_positions(self, positions):
        float_positions = np.array(positions, dtype=np.float32)
        self.vao.store_data_in_attribute_list(0, 3, float_positions)

    def set_tex_coords(self, tex_coords):
        float_tex_coords = np.array(tex_coords, dtype=np.float32)
        self.vao.store_data_in_attribute_list(1, 2, float_tex_coords)

    def set_indices(self, indices):
        uint_indices = np.array(indices, dtype=np.uint8)
        self.vao.bind_indices_buffer(uint_indices)

    def set_position(self, position):
        self.position = self.position = np.array([position[0], position[1], 0], dtype=np.float32)

    def set_size(self, size):
        self.scale = pyrr.matrix44.create_from_scale(np.array([size[0], size[1], 1]))
