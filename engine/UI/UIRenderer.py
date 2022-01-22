import os.path

import numpy as np
import pyrr
from OpenGL.GL import *

from engine.UI.UILabel import UILabel
from engine.UI.UIRect import UIRect
from engine.opengl.GLSLShader import GLSLShader


class UIRenderer:

    def __init__(self):
        text_shader_path = os.path.join("engine", "UI", "text_shader.txt")
        self.text_shader = GLSLShader(text_shader_path)
        rect_shader_path = os.path.join("engine", "UI", "rect_shader.txt")
        self.rect_shader = GLSLShader(rect_shader_path)

    def set_projection_matrix(self, window_width, window_height):
        matrix = pyrr.matrix44.create_orthogonal_projection(0, window_width, window_height, 0, 0, 100)
        self.text_shader.bind()
        self.text_shader.set_uniform_mat4fv("projection_matrix", pyrr.matrix44.create_orthogonal_projection(-1, 1, -1, 1, 0, 100))
        self.rect_shader.bind()
        self.rect_shader.set_uniform_mat4fv("projection_matrix", matrix)

    def render_label(self, label):
        # TODO: Please optimise this, setup happens for every label in the ui
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)

        self.text_shader.bind()
        model_matrix = np.matmul(label.scale, pyrr.matrix44.create_from_translation([label.x, label.y, 0]))
        self.text_shader.set_uniform_mat4fv("model_matrix", model_matrix)
        self.text_shader.set_uniform3f("colour", *label.text_colour)
        glBindTexture(GL_TEXTURE_2D, label.font.font_bitmap.get_ID())

        label.text_vao.bind()
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glDrawElements(GL_TRIANGLES, label.text_vao.get_vertex_count(), GL_UNSIGNED_BYTE, None)
        label.text_vao.unbind()

        # Clean up
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.text_shader.unbind()
        glDisable(GL_BLEND)

    def render_rect(self, rect):
        # Render rect
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.rect_shader.bind()
        self.rect_shader.set_uniform4f("colour_input", *rect.colour)
        rect.vao.bind()
        glEnableVertexAttribArray(0)
        glDrawElements(GL_TRIANGLES, rect.vao.get_vertex_count(), GL_UNSIGNED_BYTE, None)
        rect.vao.unbind()

        # Clean up
        glDisableVertexAttribArray(0)
        self.rect_shader.unbind()
        glDisable(GL_BLEND)

    def render(self, ui):
        if isinstance(ui, UILabel):
            self.render_label(ui)
        if isinstance(ui, UIRect):
            self.render_rect(ui)

        for element in ui.elements:
            self.render(element)