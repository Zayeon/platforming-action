from engine.GLFWDisplayManager import DisplayManager
from engine.opengl.MainRenderer import MainRenderer
from engine.opengl.Camera import Camera
from engine.opengl.objects.Rect import Rect
from engine.opengl.objects.Line import Line

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
        pos = pos / dims  # 0 to 1
        pos = pos * 2 - 1  # -1 to 1
        pos[1] *= -1  # Since y goes up not down
        pos = pos * proj
        return pos

    box1_pos = np.array([0, 1])
    box1_size = np.array([2, 2])
    box1_vel = np.array([1.1, -3.1])
    box = AABB(box1_pos, box1_size)
    box.set_velocity(box1_vel)
    rect = Rect(box1_pos, box1_size, (0, 0, 0.5, 1))

    box2_pos = np.array([1, -2])
    box2_size = np.array([2, 1])
    box2 = AABB(box2_pos, box2_size)
    rect2 = Rect(box2_pos, box2_size, (0, 0, 0.5, 1))

    v1 = box1_pos + box1_size / 2
    v2 = v1 + box1_vel
    line = Line([*v1,  *v2], (0, 0.5, 0, 1), 5)

    intersect = world.dynamic_rect_intersect_rect(box, 1, box2)
    if intersect:
        t_hit, contact_point, contact_normal = intersect
        box.position = contact_point
        rect.set_position(contact_point)

    main_renderer = MainRenderer(projection_matrix)
    camera = Camera()

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        cursor_pos = window_to_projection(display_manager.get_cursor_pos(), [16, 9])

        # moving box


        main_renderer.render([], [], [rect, rect2], [line], camera)

        display_manager.update_display()


if __name__ == '__main__':
    main()