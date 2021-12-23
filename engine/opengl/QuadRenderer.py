import os.path
import pyrr
from OpenGL.GL import *
import numpy as np

from engine.opengl.GLSLShader import GLSLShader

class QuadRenderer:
    def __init__(self):
        self.quad_shader_path = os.path.join("engine", "opengl", "shaders", "quad_shader.txt")
        self.quad_shader = None

        self.load_shader()

    def set_projection_matrix(self, matrix):
        self.quad_shader.bind()
        self.quad_shader.set_uniform_mat4fv("projection_matrix", matrix)

    def load_shader(self):
        self.quad_shader = GLSLShader(self.quad_shader_path)

    def sort_quads_by_texture(self, quads):
        # Organise quads by texture so that we only have to bind each texture once
        sorted_quads = {}
        for quad in quads:
            texture_ID = quad.texture_atlas.get_ID()
            if texture_ID not in sorted_quads:
                sorted_quads[texture_ID] = []

            sorted_quads[texture_ID].append(quad)

        return sorted_quads

    def render_quad(self, quad):
        quad.vao.bind()
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        translation = pyrr.matrix44.create_from_translation(quad.position)
        model_matrix = np.matmul(quad.scale, np.matmul(quad.rotation, translation))
        self.quad_shader.set_uniform_mat4fv("model_matrix", model_matrix)

        glDrawElements(GL_TRIANGLES, quad.vao.get_vertex_count(), GL_UNSIGNED_BYTE, None)
        quad.vao.unbind()

    def render(self, quads, camera):
        # Move the scene not the camera
        view_matrix = pyrr.matrix44.create_from_translation(-camera.get_position())
        self.quad_shader.bind()
        self.quad_shader.set_uniform_mat4fv("view_matrix", view_matrix)

        sorted_quads = self.sort_quads_by_texture(quads)

        for texture_ID in sorted_quads:
            glBindTexture(GL_TEXTURE_2D, texture_ID)
            for quad in sorted_quads[texture_ID]:
                self.render_quad(quad)

        # Clean up
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.quad_shader.unbind()