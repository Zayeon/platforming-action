import os.path
import pyrr
from OpenGL.GL import *

from engine.opengl.GLSLShader import GLSLShader


class UIRenderer:

    # def sort_quads_by_texture(self, quads):
    #     # Organise quads by texture so that we only have to bind each texture once
    #     sorted_quads = {}
    #     for quad in quads:
    #         texture_ID = quad.texture_atlas.get_ID()
    #         if texture_ID not in sorted_quads:
    #             sorted_quads[texture_ID] = []
    #
    #         sorted_quads[texture_ID].append(quad)
    #
    #     return sorted_quads



    def __init__(self):
        text_shader_path = os.path.join("engine", "UI", "text_shader.txt")
        self.text_shader = GLSLShader(text_shader_path)

    def set_projection_matrix(self, matrix):
        self.text_shader.bind()
        self.text_shader.set_uniform_mat4fv("projection_matrix", matrix)

    # def sort_text_by_font(self, texts):
    #     # Organise texts by font so that we only have to bind each texture once
    #     sorted_texts = {}
    #     for text in texts:
    #         font_bitmap_ID = text.

    def render(self, texts, font):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)

        self.text_shader.bind()
        self.text_shader.set_uniform_mat4fv("model_matrix", pyrr.matrix44.create_from_scale([10, 5, 1]))
        glBindTexture(GL_TEXTURE_2D, font.font_bitmap.get_ID())

        for text_vao in texts:
            text_vao.bind()
            glEnableVertexAttribArray(0)
            glEnableVertexAttribArray(1)
            glDrawElements(GL_TRIANGLES, text_vao.get_vertex_count(), GL_UNSIGNED_BYTE, None)
            text_vao.unbind()

        # Clean up
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.text_shader.unbind()
        glDisable(GL_BLEND)