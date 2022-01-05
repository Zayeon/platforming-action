import numpy as np
import pyrr
from math import radians
from engine.opengl.VAO import VAO

class Quad:
    indices = [0, 1, 2,
               0, 2, 3]

    vertex_data = [
        -0.5, -0.5, 0.0,
        -0.5, 0.5, 0.0,
        0.5, 0.5, 0.0,
        0.5, -0.5, 0.0,
    ]

    def __init__(self, texture_atlas):
        self.position = pyrr.Vector3([0, 0, 0])
        self.rotation = pyrr.matrix44.create_from_z_rotation(radians(0))
        self.scale = pyrr.matrix44.create_from_scale(np.array([1, 1, 1]))
        self.vao = VAO(len(self.indices))
        self.set_positions(self.vertex_data)

        # set the default indices
        self.set_indices(self.indices)

        self.texture_atlas = texture_atlas
        self.set_tex_coords(self.texture_atlas.get_tex_coords())

    def set_positions(self, positions):
        float_positions = np.array(positions, dtype=np.float32)
        self.vao.store_data_in_attribute_list(0, 3, float_positions)

    def set_tex_coords(self, tex_coords):
        float_tex_coords = np.array(tex_coords, dtype=np.float32)
        self.vao.store_data_in_attribute_list(1, 2, float_tex_coords)

    def set_indices(self, indices):
        uint_indices = np.array(indices, dtype=np.uint8)
        self.vao.bind_indices_buffer(uint_indices)

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def set_rotation(self, rotation):
        self.rotation = pyrr.matrix44.create_from_z_rotation(radians(rotation))

    def set_scale(self, scale_x, scale_y):
        self.scale = pyrr.matrix44.create_from_scale(np.array([scale_x, scale_y, 1]))