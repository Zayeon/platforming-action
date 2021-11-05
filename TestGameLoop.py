from engine.GLFWDisplayManager import DisplayManager
from OpenGL.GL import *
import numpy as np


def main():

    display_manager = DisplayManager()
    display_manager.create_window(1280, 720, "Untitled Platformer")

    # Test OpenGL
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertex_data = np.array([
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0, 0.5, 0.0
    ], dtype=np.float32)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    while not display_manager.window_should_close():
        display_manager.start_frame()

        glBindVertexArray(vao)
        glEnableVertexAttribArray(0)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisableVertexAttribArray(0)

        display_manager.update_display()


if __name__ == '__main__':
    main()