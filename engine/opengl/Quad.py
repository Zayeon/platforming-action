import numpy as np
from engine.opengl.VAO import VAO

class Quad:
    indices = [0, 1, 2,
               2, 3, 0]

    def __init__(self, positions, texture_atlas):
        self.vao = VAO(len(self.indices))
        self.set_positions(positions)

        # set the default indices
        self.set_indices(self.indices)

        self.texture_atlas = texture_atlas
        self.set_tex_coords(self.texture_atlas.get_tex_coords())

    def set_positions(self, positions):
        float_positions = np.array(positions, dtype=np.float32)
        self.vao.bind()
        self.vao.store_data_in_attribute_list(0, 3, float_positions)

    def set_tex_coords(self, tex_coords):
        float_tex_coords = np.array(tex_coords, dtype=np.float32)
        self.vao.bind()
        self.vao.store_data_in_attribute_list(1, 2, float_tex_coords)

    def set_indices(self, indices):
        uint_indices = np.array(indices, dtype=np.uint8)
        self.vao.bind()
        self.vao.bind_indices_buffer(uint_indices)