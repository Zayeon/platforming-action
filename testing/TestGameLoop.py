from engine.GLFWDisplayManager import DisplayManager
from engine.opengl.GLSLShader import GLSLShader
from engine.opengl.GLTextureAtlas import TextureAtlas
from engine.opengl.VAO import VAO
from engine.opengl.Quad import Quad
from engine.opengl.ConvexPolygon import ConvexPolygon
from engine.opengl.MainRenderer import MainRenderer
from engine.opengl.Camera import Camera

from engine.physics.ConvexPolygonHitbox import ConvexPolygonHitbox
from engine.physics.InteractionWorld import InteractionWorld

from engine.UI.FontType import FontType
from engine.UI.UIRenderer import UIRenderer

from OpenGL.GL import *
import pyrr
import numpy as np
import glfw
import os.path
from math import radians

def main():

    display_manager = DisplayManager()
    display_manager.create_window(1280, 720, "Untitled Platformer")

    projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)

    # Test OpenGL

    texture_path = os.path.join("res", "jerma_sus.jpg")
    jerma_texture = TextureAtlas(texture_path, 1, 1, 360, 450)
    texture_path = os.path.join("res", "troll_despair.png")
    troll_despair = TextureAtlas(texture_path, 44, 5, 128, 128)
    texture_path = os.path.join("res", "dink_donk.png")
    dink_donk = TextureAtlas(texture_path, 3, 3, 128, 128)

    dink_quad = Quad(dink_donk)
    dink_quad.set_position(-5, 0)
    dink_quad.set_scale(5, 5)
    troll_quad = Quad(troll_despair)
    troll_quad.set_position(0, 0)
    troll_quad.set_scale(5, 5)
    jerma_quad = Quad(jerma_texture)
    jerma_quad.set_position(5, 0)
    jerma_quad.set_scale(5, 5)

    polygon_a_vertices = [[0, 1, 0], [-0.95, 0.31, 0], [-0.59, -0.81, 0], [0.59, -0.81, 0], [0.95, 0.31, 0]]
    polygon_a_position = np.array([-1, 0], dtype=np.float32)
    polygon_a_rotation = 0
    polygon_a = ConvexPolygon(polygon_a_vertices, [224/255, 187/255, 228/255, 1])
    polygon_a.set_position(polygon_a_position[0], polygon_a_position[1])
    polygon_a.set_rotation(polygon_a_rotation)
    polygon_a_hitbox = ConvexPolygonHitbox(polygon_a_vertices, polygon_a_position, polygon_a_rotation)

    polygon_b_vertices = [[-0.5, 0.87, 0], [-1, 0, 0], [-0.5, -0.87, 0], [0.5, -0.87, 0], [1, 0, 0], [0.5, 0.87, 0]]
    polygon_b_position = np.array([2, 0], dtype=np.float32)
    polygon_b_rotation = 30
    polygon_b = ConvexPolygon(polygon_b_vertices, [197/255, 217/255, 252/255, 1])
    polygon_b.set_position(polygon_b_position[0], polygon_b_position[1])
    polygon_b.set_rotation(polygon_b_rotation)
    polygon_b_hitbox = ConvexPolygonHitbox(polygon_b_vertices, polygon_b_position, polygon_b_rotation)

    world = InteractionWorld()
    world.add_polygon(polygon_a_hitbox)
    world.add_polygon(polygon_b_hitbox)

    main_renderer = MainRenderer(projection_matrix)
    UI_renderer = UIRenderer()
    UI_renderer.set_projection_matrix(projection_matrix)
    camera = Camera()

    # Bind right arrow to advancing frame
    # def on_right_arrow_press():
    #     troll_despair.next_frame()
    #     example_quad.set_tex_coords(troll_despair.get_tex_coords())
    #
    # display_manager.bind_key_down(glfw.KEY_RIGHT, on_right_arrow_press)

    font_8bit = FontType("8BitOperator", display_manager.width / display_manager.height)
    text_1 = font_8bit.construct_text("Hello\nWorld!", 10, [0, 0, 0.7], line_spacing=0.2, char_spacing=-0.01)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)

        proposed_movement = np.zeros(2)
        if display_manager.get_key_state(glfw.KEY_UP) == glfw.PRESS:
            proposed_movement[1] = 0.05
            polygon_a_position += proposed_movement
            reaction = world.react_to_movement(polygon_a_hitbox, proposed_movement)
            polygon_a_position -= reaction
            polygon_a.set_position(polygon_a_position[0], polygon_a_position[1])
        elif display_manager.get_key_state(glfw.KEY_DOWN) == glfw.PRESS:
            proposed_movement[1] = -0.05
            polygon_a_position += proposed_movement
            reaction = world.react_to_movement(polygon_a_hitbox, proposed_movement)
            polygon_a_position -= reaction
            polygon_a.set_position(polygon_a_position[0], polygon_a_position[1])
        elif display_manager.get_key_state(glfw.KEY_LEFT) == glfw.PRESS:
            proposed_movement[0] = -0.05
            polygon_a_position += proposed_movement
            reaction = world.react_to_movement(polygon_a_hitbox, proposed_movement)
            polygon_a_position -= reaction
            polygon_a.set_position(polygon_a_position[0], polygon_a_position[1])
        elif display_manager.get_key_state(glfw.KEY_RIGHT) == glfw.PRESS:
            proposed_movement[0] = 0.05
            polygon_a_position += proposed_movement
            reaction = world.react_to_movement(polygon_a_hitbox, proposed_movement)
            polygon_a_position -= reaction
            polygon_a.set_position(polygon_a_position[0], polygon_a_position[1])
        # if len(world.intersect_convex_polygon(polygon_a_hitbox, polygon_b_hitbox)) <= 0:
        #     polygon_a.colour = [201/255, 241/255, 255/255, 1]
        # else:
        #     polygon_a.colour = [224/255, 187/255, 228/255, 1]


        main_renderer.render([], [polygon_b, polygon_a], camera)
        UI_renderer.render([text_1], font_8bit)

        dink_donk.next_frame()
        dink_quad.set_tex_coords(dink_donk.get_tex_coords())
        troll_despair.next_frame()
        troll_quad.set_tex_coords(troll_despair.get_tex_coords())
        jerma_texture.next_frame()
        jerma_quad.set_tex_coords(jerma_texture.get_tex_coords())

        display_manager.update_display()


if __name__ == '__main__':
    main()