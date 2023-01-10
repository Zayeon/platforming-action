from engine.GLFWDisplayManager import DisplayManager
from engine.UI.FontType import FontType
from engine.UI.UIRenderer import UIRenderer
from engine.opengl.GLTextureAtlas import TextureAtlas
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
import os.path

from level.Level import Level
from level.modes.CollisionMode import CollisionMode
from level.modes.WorldMode import WorldMode
from level.ui.MenuBar import MenuBar


class LevelCreator:
    def __init__(self):
        self.display_manager = DisplayManager()
        self.display_manager.create_window(1280, 720, "Level Creator")

        self.display_manager.bind_key_down(glfw.KEY_C, lambda: self.switch_mode(self.collision_mode))
        self.display_manager.bind_key_down(glfw.KEY_T, lambda: self.switch_mode(self.texture_mode))
        self.display_manager.bind_key_down(glfw.KEY_ESCAPE, lambda: switch_menu_bar())

        # Level
        self.level = Level()
        texture_path = os.path.join("res", "example_atlas.png")
        texture_atlas = TextureAtlas(texture_path, 16, 4, 32, 32)
        self.level.texture_atlas = texture_atlas

        # Rendering
        self.camera = Camera()
        projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)
        self.main_renderer = MainRenderer(projection_matrix)
        self.ui_renderer = UIRenderer()
        self.ui_renderer.set_projection_matrix(self.display_manager.width, self.display_manager.height)

        # Modes
        self.active_mode = None
        self.collision_mode = CollisionMode(self)
        self.texture_mode = WorldMode(self)
        self.switch_mode(self.collision_mode)

        # UI
        self.font_8bit = FontType("8BitOperator", self.display_manager.width / self.display_manager.height)
        self.menu_bar = MenuBar(self)
        self.menu_bar_shown = False
        self.menu_bar.get_ui().show = self.menu_bar_shown

        def switch_menu_bar():
            self.menu_bar_shown = not self.menu_bar_shown
            self.menu_bar.get_ui().show = self.menu_bar_shown

    def switch_mode(self, mode):
        self.active_mode = mode
        self.active_mode.on_switch()

    def run(self):
        glClearColor(*self.level.clear_colour)
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

            if self.menu_bar_shown:
                self.ui_renderer.render(self.menu_bar.get_ui())
            else:
                self.active_mode.update()

            self.active_mode.render()

            self.display_manager.update_display()