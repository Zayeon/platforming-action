from engine.GLFWDisplayManager import DisplayManager
from engine.opengl.GLSLShader import GLSLShader
from engine.opengl.GLTextureAtlas import TextureAtlas
from engine.opengl.VAO import VAO
from engine.opengl.Quad import Quad
from engine.opengl.ConvexPolygon import ConvexPolygon
from engine.opengl.MainRenderer import MainRenderer
from engine.opengl.Camera import Camera

from OpenGL.GL import *
import pyrr
import numpy as np
import glfw
import os.path
from math import radians

def main():

    display_manager = DisplayManager()
    display_manager.create_window(1280, 720, "Untitled Platformer")

    # Test OpenGL
    vertex_data = [
        -0.5, -0.5, 0.0,
        -0.5, 0.5, 0.0,
        0.5, 0.5, 0.0,
        0.5, -0.5, 0.0,
    ]

    texture_path = os.path.join("res", "jerma_sus.jpg")
    jerma_texture = TextureAtlas(texture_path, 1, 1, 360, 450)
    texture_path = os.path.join("res", "troll_despair.png")
    troll_despair = TextureAtlas(texture_path, 44, 5, 128, 128)
    texture_path = os.path.join("res", "dink_donk.png")
    dink_donk = TextureAtlas(texture_path, 3, 3, 128, 128)

    dink_quad = Quad(vertex_data, dink_donk)
    dink_quad.set_position(-5, 0)
    dink_quad.set_scale(5, 5)
    troll_quad = Quad(vertex_data, troll_despair)
    troll_quad.set_position(0, 0)
    troll_quad.set_scale(5, 5)
    jerma_quad = Quad(vertex_data, jerma_texture)
    jerma_quad.set_position(5, 0)
    jerma_quad.set_scale(5, 5)

    polygon_a_vertices = [[0, 1, 0], [-0.95, 0.31, 0], [-0.59, -0.81, 0], [0.59, -0.81, 0], [0.95, 0.31, 0]]
    polygon_a = ConvexPolygon(polygon_a_vertices, [224/255, 187/255, 228/255, 1])
    polygon_a.set_position(-2, 0)
    polygon_a.set_rotation(18)
    polygon_b_vertices = [[-0.5, 0.87, 0], [-1, 0, 0], [-0.5, -0.87, 0], [0.5, -0.87, 0], [1, 0, 0], [0.5, 0.87, 0]]
    polygon_b = ConvexPolygon(polygon_b_vertices, [149 / 255, 125 / 255, 173 / 255, 1])
    polygon_b.set_position(2, 0)
    polygon_b.set_rotation(0)

    main_renderer = MainRenderer()
    camera = Camera()

    # Bind right arrow to advancing frame
    # def on_right_arrow_press():
    #     troll_despair.next_frame()
    #     example_quad.set_tex_coords(troll_despair.get_tex_coords())
    #
    # display_manager.bind_key_down(glfw.KEY_RIGHT, on_right_arrow_press)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        main_renderer.render([], [polygon_a, polygon_b], camera)

        # dink_donk.next_frame()
        # dink_quad.set_tex_coords(dink_donk.get_tex_coords())
        # troll_despair.next_frame()
        # troll_quad.set_tex_coords(troll_despair.get_tex_coords())
        # jerma_texture.next_frame()
        # jerma_quad.set_tex_coords(jerma_texture.get_tex_coords())

        display_manager.update_display()


if __name__ == '__main__':
    main()