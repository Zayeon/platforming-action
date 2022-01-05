from engine.GLFWDisplayManager import DisplayManager
from engine.opengl.MainRenderer import MainRenderer
from engine.opengl.Camera import Camera

from engine.physics.InteractionWorld import InteractionWorld
from engine.physics.AABB import AABB

from OpenGL.GL import *
import pyrr
import numpy as np


def main():

    display_manager = DisplayManager()
    display_manager.create_window(1280, 720, "Physics test")

    projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)

    # Test OpenGL

    world = InteractionWorld()

    def window_to_projection(pos, proj):
        pos = np.array(pos, dtype=np.float32)
        proj = np.array(proj, dtype=np.float32)
        dims = np.array([display_manager.width, display_manager.height], dtype=np.float32)
        pos = pos / dims
        pos = pos * 2 - 1
        pos = pos * proj
        return pos

    box = AABB([0, 1], [2, 2])
    box.set_velocity([1, -3])
    box2 = AABB([1, -2], [2, 1])

    intersect = world.dynamic_rect_intersect_rect(box, 1, box2)
    if intersect:
        t_hit, contact_point, contact_normal = intersect


    main_renderer = MainRenderer(projection_matrix)
    camera = Camera()

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        cursor_pos = window_to_projection(display_manager.get_cursor_pos(), [16, 9])
        print(cursor_pos)

        main_renderer.render([], [], camera)

        display_manager.update_display()


if __name__ == '__main__':
    main()