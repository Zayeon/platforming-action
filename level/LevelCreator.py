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

from level.Level import Level
from level.modes.CollisionMode import CollisionMode
from level.modes.TextureMode import TextureMode


class LevelCreator:
    def __init__(self):
        self.display_manager = DisplayManager()
        self.display_manager.create_window(1280, 720, "Level Creator")

        self.display_manager.bind_mouse_button_event(self.on_mouse_left)
        self.display_manager.bind_key_down(glfw.KEY_C, lambda: self.switch_mode(self.collision_mode))
        self.display_manager.bind_key_down(glfw.KEY_T, lambda: self.switch_mode(self.texture_mode))

        projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)
        self.main_renderer = MainRenderer(projection_matrix)

        self.camera = Camera()
        self.level = Level()

        # Modes
        self.active_mode = None
        self.collision_mode = CollisionMode(self)
        self.texture_mode = TextureMode(self)
        self.switch_mode(self.collision_mode)

    def switch_mode(self, mode):
        self.active_mode = mode
        self.active_mode.on_switch()

    def window_to_projection(self, pos, proj):
        pos = np.array(pos, dtype=np.float32)
        proj = np.array(proj, dtype=np.float32)
        dims = np.array([self.display_manager.width, self.display_manager.height], dtype=np.float32)
        pos = pos / dims  # 0 to 1
        pos = pos * 2 - 1  # -1 to 1
        pos[1] *= -1  # Since y goes up not down
        pos = pos * proj
        return pos

    def on_mouse_left(self, button, action):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            cursor_pos = self.window_to_projection(self.display_manager.get_cursor_pos(), [16, 9])
            world_pos = cursor_pos + self.camera.position[:2]
            for chunk in self.level.chunks:
                if 32 * chunk["location"][0] < world_pos[0] < 32 * (chunk["location"][0] + 1) and 32 * chunk["location"][
                        1] < world_pos[1] < 32 * (chunk["location"][1] + 1):
                    cursor_tile = np.floor(world_pos).astype(np.int32)
                    chunk["collision_data"][cursor_tile[0], cursor_tile[1]] = not chunk["collision_data"][
                        cursor_tile[0], cursor_tile[1]]
                    break

    def run(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        while not self.display_manager.window_should_close():
            self.display_manager.start_frame()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)

            if self.display_manager.get_key_state(glfw.KEY_A):
                self.camera.position[0] -= 0.5
            elif self.display_manager.get_key_state(glfw.KEY_D):
                self.camera.position[0] += 0.5
            elif self.display_manager.get_key_state(glfw.KEY_W):
                self.camera.position[1] += 0.5
            elif self.display_manager.get_key_state(glfw.KEY_S):
                self.camera.position[1] -= 0.5

            self.active_mode.run()

            self.display_manager.update_display()