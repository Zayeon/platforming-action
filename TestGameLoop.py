from engine.GLFWDisplayManager import DisplayManager
from engine.opengl.GLSLShader import GLSLShader
from engine.opengl.GLTextureAtlas import TextureAtlas

from OpenGL.GL import *
import pyrr
import numpy as np
import os.path
from math import radians


def main():

    display_manager = DisplayManager()
    display_manager.create_window(1280, 720, "Untitled Platformer")

    # Test OpenGL
    vertex_data = np.array([
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        -0.5, 0.5, 0.0,
        -0.5, 0.5, 0.0,
        0.5, 0.5, 0.0,
        0.5, -0.5, 0.0
    ], dtype=np.float32)

    texture_coords = np.array([
        0, 0,
        1, 0,
        0, 1,
        0, 1,
        1, 1,
        1, 0
    ], dtype=np.float32)

    texture_path = os.path.join("res", "jerma_sus.jpg")
    jerma_texture = TextureAtlas(texture_path, [1, 1])
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)


    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertex_data.itemsize * 3, ctypes.c_void_p(0))
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    vbo2 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBufferData(GL_ARRAY_BUFFER, texture_coords.nbytes, texture_coords, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, texture_coords.itemsize * 2, ctypes.c_void_p(0))
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    glBindVertexArray(0)

    coloured_shader_path = os.path.join("engine", "opengl", "shaders", "coloured_shader.txt")
    coloured_shader = GLSLShader(coloured_shader_path)

    textured_shader_path = os.path.join("engine", "opengl", "shaders", "textured_shader.txt")
    textured_shader = GLSLShader(textured_shader_path)

    # position: (0.25, 0) rotation: 20degrees scale: 0.5
    translation = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    rotation = pyrr.matrix44.create_from_z_rotation(radians(0))
    scale = pyrr.matrix44.create_from_scale(np.array([5, 5, 5]))

    model_matrix = np.matmul(scale, np.matmul(rotation, translation))

    camera_pos = pyrr.Vector3([0, 0, 0])
    # Move the scene not the camera
    view_matrix = pyrr.matrix44.create_from_translation(-camera_pos)

    projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)

    # coloured_shader.bind()
    # coloured_shader.set_uniform_mat4fv("projection_matrix", projection_matrix)
    # coloured_shader.set_uniform_mat4fv("view_matrix", view_matrix)
    # coloured_shader.set_uniform_mat4fv("model_matrix", model_matrix)
    #
    # coloured_shader.set_uniform4f("colour_input", 0, 0.7, 0, 1)
    # coloured_shader.unbind()

    textured_shader.bind()
    textured_shader.set_uniform_mat4fv("projection_matrix", projection_matrix)
    textured_shader.set_uniform_mat4fv("view_matrix", view_matrix)
    textured_shader.set_uniform_mat4fv("model_matrix", model_matrix)
    textured_shader.unbind()

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Use shader
        textured_shader.bind()

        glBindVertexArray(vao)
        glBindTexture(GL_TEXTURE_2D, jerma_texture.get_ID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindTexture(GL_TEXTURE_2D, 0)

        textured_shader.unbind()

        display_manager.update_display()


if __name__ == '__main__':
    main()