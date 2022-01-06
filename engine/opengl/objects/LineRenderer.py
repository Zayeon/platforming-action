import os.path
import pyrr
from OpenGL.GL import *
import numpy as np

from engine.opengl.GLSLShader import GLSLShader

class LineRenderer:
    def __init__(self):
        line_shader_path = os.path.join("engine", "opengl", "shaders", "line_shader.txt")
        self.line_shader = GLSLShader(line_shader_path)

    def set_projection_matrix(self, matrix):
        self.line_shader.bind()
        self.line_shader.set_uniform_mat4fv("projection_matrix", matrix)

    def render(self, lines, camera):
        view_matrix = pyrr.matrix44.create_from_translation(-camera.get_position())
        self.line_shader.bind()
        self.line_shader.set_uniform_mat4fv("view_matrix", view_matrix)

        for line in lines:
            # Calculate model matrix
            glLineWidth(line.width)
            self.line_shader.set_uniform4f("colour_input", *line.colour)
            self.line_shader.set_uniform1f("width", line.width)
            # Render lines
            line.vao.bind()
            glEnableVertexAttribArray(0)
            glDrawArrays(GL_LINES, 0, line.vao.get_vertex_count())
            line.vao.unbind()

        # Clean up
        glDisableVertexAttribArray(0)
        self.line_shader.unbind()
