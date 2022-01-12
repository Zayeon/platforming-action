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
import glfw


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

    rects = []

    box1_pos = np.array([0, 1])
    box1_size = np.array([2, 2])
    box = AABB(box1_pos, box1_size)
    rect = Rect(box1_pos, box1_size, (0, 0.5, 0.5, 1))
    rects.append(rect)

    def gen_box_rect(pos, size):
        world.add_box(AABB(pos, size))
        rects.append(Rect(pos, size, np.random.random(4)))

    gen_box_rect([1, -2], [2, 1])
    gen_box_rect([-15, -8], [0.5, 10])
    gen_box_rect([-14.5, -8], [2, 2])
    gen_box_rect([-12.5, -8], [2, 2])
    gen_box_rect([-10.5, -8], [2, 2])
    gen_box_rect([-8.5, -8], [2, 2])
    gen_box_rect([-6.5, -8], [2, 2])
    gen_box_rect([-4.5, -8], [2, 2])
    gen_box_rect([-2.5, -8], [17.5, 2])
    gen_box_rect([15, -8], [0.5, 10])
    gen_box_rect([-14, -4], [0.5, 0.5])

    # v1 = box1_pos + box1_size / 2
    # v2 = v1 + box1_vel
    # line = Line([*v1,  *v2], (0, 0.5, 0, 1), 5)

    gravity = np.array((0, -10), dtype=np.float32)

    def on_space_down():
        box.velocity[1] = 4

    display_manager.bind_key_down(glfw.KEY_SPACE, on_space_down)

    main_renderer = MainRenderer(projection_matrix)
    camera = Camera()

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        cursor_pos = window_to_projection(display_manager.get_cursor_pos(), [16, 9])

        if display_manager.get_key_state(glfw.KEY_A):
            box.velocity[0] = -5
        elif display_manager.get_key_state(glfw.KEY_D):
            box.velocity[0] = 5
        else:
            box.velocity[0] = 0

        box.velocity += gravity * display_manager.delta_time

        # moving box
        world.resolve_movement(box, display_manager.delta_time)

        box.position += display_manager.delta_time * box.velocity
        rect.set_position(box.position)


        main_renderer.render([], [], rects, [], camera)

        display_manager.update_display()


if __name__ == '__main__':
    main()