import os.path
import pyrr
from OpenGL.GL import *
import numpy as np

from engine.opengl.GLSLShader import GLSLShader


class ConvexPolygonRenderer:
    def __init__(self):
        convex_polygon_shader_path = os.path.join("engine", "opengl", "shaders", "convex_polygon_shader.txt")
        self.convex_polygon_shader = GLSLShader(convex_polygon_shader_path)

    def set_projection_matrix(self, matrix):
        self.convex_polygon_shader.bind()
        self.convex_polygon_shader.set_uniform_mat4fv("projection_matrix", matrix)

    def render(self, polygons, camera):
        view_matrix = pyrr.matrix44.create_from_translation(-camera.get_position())
        self.convex_polygon_shader.bind()
        self.convex_polygon_shader.set_uniform_mat4fv("view_matrix", view_matrix)

        for polygon in polygons:
            # Render polygon
            polygon.vao.bind()
            glEnableVertexAttribArray(0)
            translation = pyrr.matrix44.create_from_translation(polygon.position)
            model_matrix = np.matmul(polygon.scale, np.matmul(polygon.rotation, translation))
            self.convex_polygon_shader.set_uniform_mat4fv("model_matrix", model_matrix)

            self.convex_polygon_shader.set_uniform4f("colour_input", *polygon.colour)

            glDrawElements(GL_TRIANGLES, polygon.vao.get_vertex_count(), GL_UNSIGNED_BYTE, None)
            polygon.vao.unbind()

        # Clean up
        glDisableVertexAttribArray(0)
        self.convex_polygon_shader.unbind()