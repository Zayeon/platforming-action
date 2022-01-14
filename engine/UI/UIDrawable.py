import numpy as np

from engine.UI.UIElement import UIElement
from engine.opengl.VAO import VAO


class UIDrawable(UIElement):
    indices = [0, 1, 2,
               2, 3, 0]

    def calculate_pos_dims(self):
        super().calculate_pos_dims()
        vertices = np.array([self.x, self.y,
                             self.x + self.width, self.y,
                             self.x + self.width, self.y + self.height,
                             self.x, self.y + self.height], dtype=np.float32)
        self.vao = VAO(len(self.indices))
        self.vao.bind_indices_buffer(self.indices)
        self.vao.store_data_in_attribute_list(0, 2, vertices)