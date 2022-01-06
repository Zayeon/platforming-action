import os.path
import pyrr
from OpenGL.GL import *
import numpy as np

from engine.opengl.GLSLShader import GLSLShader

class RectRenderer:
    def __init__(self):
        rect_shader_path = os.path.join("engine", "opengl", "shaders", "rect_shader.txt")
        self.rect_shader = GLSLShader(rect_shader_path)

    def set_projection_matrix(self, matrix):
        self.rect_shader.bind()
        self.rect_shader.set_uniform_mat4fv("projection_matrix", matrix)

    def render(self, rects, camera):
        view_matrix = pyrr.matrix44.create_from_translation(-camera.get_position())
        self.rect_shader.bind()
        self.rect_shader.set_uniform_mat4fv("view_matrix", view_matrix)

        for rect in rects:
            # Calculate model matrix
            translation = pyrr.matrix44.create_from_translation(rect.position)
            model_matrix = np.matmul(rect.scale, translation)
            self.rect_shader.set_uniform_mat4fv("model_matrix", model_matrix)
            self.rect_shader.set_uniform4f("colour_input", *rect.colour)
            # Render rects
            rect.vao.bind()
            glEnableVertexAttribArray(0)
            glDrawElements(GL_TRIANGLES, rect.vao.get_vertex_count(), GL_UNSIGNED_BYTE, None)
            rect.vao.unbind()

        # Clean up
        glDisableVertexAttribArray(0)
        self.rect_shader.unbind()
