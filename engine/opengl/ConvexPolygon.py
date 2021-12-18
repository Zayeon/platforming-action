from engine.opengl.VAO import VAO

import numpy as np
import pyrr
from math import radians

class ConvexPolygon:

    def __init__(self, positions, colour):
        vertex_data = np.concatenate(positions)
        indices = self.generate_indices(len(positions))
        self.colour = colour
        self.position = pyrr.Vector3([0, 0, 0])
        self.rotation = pyrr.matrix44.create_from_z_rotation(radians(0))
        self.scale = pyrr.matrix44.create_from_scale(np.array([1, 1, 1]))

        self.vao = VAO(len(indices))
        self.set_positions(vertex_data)

        self.set_indices(indices)

    def set_positions(self, positions):
        float_positions = np.array(positions, dtype=np.float32)
        self.vao.store_data_in_attribute_list(0, 3, float_positions)

    def set_indices(self, indices):
        uint_indices = np.array(indices, dtype=np.uint8)
        self.vao.bind_indices_buffer(uint_indices)


    def generate_indices(self, vertex_count):
        indices = []
        for i in range(1, vertex_count-1):
            index = [0, i, i+1]
            indices.extend(index)

        return indices

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def set_rotation(self, rotation):
        self.rotation = pyrr.matrix44.create_from_z_rotation(radians(rotation))

    def set_scale(self, scale_x, scale_y):
        self.scale = pyrr.matrix44.create_from_scale(np.array([scale_x, scale_y, 1]))