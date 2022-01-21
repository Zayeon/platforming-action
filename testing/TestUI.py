from engine.GLFWDisplayManager import DisplayManager
from engine.UI.FontType import FontType
from engine.UI.UIConstraints import UIConstraints
from engine.UI.UIElement import UIElement
from engine.UI.UILabel import UILabel
from engine.UI.UIRect import UIRect
from engine.UI.UIRenderer import UIRenderer
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
    display_manager.create_window(1280, 720, "UI test")

    projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)

    # Test OpenGL

    def window_to_projection(pos, proj):
        pos = np.array(pos, dtype=np.float32)
        proj = np.array(proj, dtype=np.float32)
        dims = np.array([display_manager.width, display_manager.height], dtype=np.float32)
        pos = pos / dims  # 0 to 1
        pos = pos * 2 - 1  # -1 to 1
        pos[1] *= -1  # Since y goes up not down
        pos = pos * proj
        return pos

    def to_text_space(pos, display_width, display_height):
        # For some reason text can't use the same projection matrix
        # as the rest of the gui so i have to convert it into -1 to 1 space
        pos = np.array(pos, dtype=np.float32)
        dims = np.array([display_width, display_height], dtype=np.float32)
        pos = pos / dims  # 0 to 1
        pos = pos * 2 - 1  # -1 to 1
        pos[1] *= -1  # Since y goes up not down
        return pos

    font_8bit = FontType("8BitOperator", display_manager.width / display_manager.height)

    # Example GUI
    root = UIElement(UIConstraints())

    text_constraints = UIConstraints()
    text_constraints.set_x_constraint(UIConstraints.CENTRE_CONSTRAINT, 100)
    text_constraints.set_y_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.1)
    text_constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.8)
    text_constraints.set_height_constraint(UIConstraints.PIXEL_CONSTRAINT, 50)
    text = UILabel(text_constraints, font_8bit, "foobar", (1, 0, 0), 1)

    rect_constraints = UIConstraints()
    rect_constraints.set_x_constraint(UIConstraints.PIXEL_CONSTRAINT, 50)
    rect_constraints.set_y_constraint(UIConstraints.PIXEL_CONSTRAINT, 50)
    rect_constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.2)
    rect_constraints.set_height_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.8)
    rect = UIRect(rect_constraints, (0, 1, 0, 1))

    rect.add_element(text)
    root.add_element(rect)

    root.calculate_pos_dims(display_manager.width, display_manager.height)


    main_renderer = MainRenderer(projection_matrix)
    camera = Camera()

    ui_renderer = UIRenderer()
    ui_renderer.set_projection_matrix(display_manager.width, display_manager.height)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    while not display_manager.window_should_close():
        display_manager.start_frame()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        print(to_text_space(display_manager.get_cursor_pos(), display_manager.width, display_manager.height))

        # main_renderer.render([], [], [], [line], camera)

        ui_renderer.render(root)

        display_manager.update_display()


if __name__ == '__main__':
    main()