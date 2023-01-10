import numpy as np
from OpenGL.GL import *
import glfw

from engine.opengl.objects.Line import Line
from engine.opengl.objects.Rect import Rect
from level.modes.TemplateMode import TemplateMode


class CollisionMode(TemplateMode):
    def __init__(self, level_creator):
        super().__init__(level_creator)

        self.cursor_rect = Rect((0, 0), (1, 1), (1, 0, 0, 0.5))

        self.chunk_borders = []
        self.grid_lines = []

        self.wireframe = False

        def f():
            self.wireframe = not self.wireframe
        self.level_creator.display_manager.bind_key_down(glfw.KEY_F, f)
        self.level_creator.display_manager.bind_mouse_button_event(self.on_mouse_left)

    def window_to_projection(self, pos, proj):
        pos = np.array(pos, dtype=np.float32)
        proj = np.array(proj, dtype=np.float32)
        dims = np.array([self.level_creator.display_manager.width, self.level_creator.display_manager.height], dtype=np.float32)
        pos = pos / dims  # 0 to 1
        pos = pos * 2 - 1  # -1 to 1
        pos[1] *= -1  # Since y goes up not down
        pos = pos * proj
        return pos

    def on_switch(self):
        # Create chunk borders
        self.chunk_borders = []
        for chunk in self.level_creator.level.chunks:
            vertices = [
                chunk["location"][0] * 32, chunk["location"][1] * 32,
                chunk["location"][0] * 32, (chunk["location"][1] + 1) * 32,
                (chunk["location"][0] + 1) * 32, (chunk["location"][1] + 1) * 32,
                (chunk["location"][0] + 1) * 32, chunk["location"][1] * 32,
            ]
            self.chunk_borders.append(Line(vertices, (0, 0, 0, 1), 10, mode=Line.LINE_LOOP))

        # Create grid lines
        for chunk in self.level_creator.level.chunks:
            root = [chunk["location"][0] * 32, chunk["location"][1] * 32]
            vertices = []
            for i in range(1, 32):
                horizontal = [root[0], root[1] + i, root[0] + 32, root[1] + i]
                vertical = [root[0] + i, root[1], root[0] + i, root[1] + 32]
                vertices.extend(horizontal)
                vertices.extend(vertical)
            self.grid_lines.append(Line(vertices, (0.5, 0.5, 0.5, 1), 1))

    def gen_rects(self, collision_chunks, chunk_pos):
        rects = []
        checked = np.zeros(collision_chunks.shape, dtype=np.bool)
        for i in range(len(collision_chunks)):
            for j in range(len(collision_chunks[i])):
                if not checked[i, j] and collision_chunks[i, j]:
                    x = 1
                    y = 1
                    while i+x < 32 and np.all(collision_chunks[i:i+x+1, j:j+y]) and not checked[i+x, j+y-1]:
                        x += 1
                    while j+y < 32 and np.all(collision_chunks[i:i+x, j:j+y+1]) and not checked[i+x-1, j+y]:
                        y += 1
                    checked[i:i+x, j:j+y] = True
                    rects.append(Rect((i + 32 * chunk_pos[0], j + 32 * chunk_pos[1]), (x, y), (0, 0, 1, 1)))

        return rects

    def on_mouse_left(self, button, action):
        if not self.level_creator.menu_bar_shown and self.level_creator.active_mode == self:
            if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
                cursor_pos = self.window_to_projection(self.level_creator.display_manager.get_cursor_pos(), [16, 9])
                world_pos = cursor_pos + self.level_creator.camera.position[:2]
                for chunk in self.level_creator.level.chunks:
                    if 32 * chunk["location"][0] < world_pos[0] < 32 * (chunk["location"][0] + 1) and 32 * chunk[
                            "location"][1] < world_pos[1] < 32 * (chunk["location"][1] + 1):
                        cursor_tile = np.floor(world_pos).astype(np.int32)
                        chunk["collision_data"][cursor_tile[0], cursor_tile[1]] = not chunk["collision_data"][
                            cursor_tile[0], cursor_tile[1]]
                        break

    def update(self):
        cursor_pos = self.window_to_projection(self.level_creator.display_manager.get_cursor_pos(), [16, 9])
        self.cursor_world_pos = cursor_pos + self.level_creator.camera.position[:2]
        cursor_tile = np.floor(self.cursor_world_pos).astype(np.int32)
        cursor_tile.resize((1, 3))
        self.cursor_rect.position = cursor_tile

        self.rects = []
        for chunk in self.level_creator.level.chunks:
            self.rects.extend(self.gen_rects(chunk["collision_data"], chunk["location"]))

    def render(self):
        self.level_creator.main_renderer.line_renderer.render(self.chunk_borders + self.grid_lines, self.level_creator.camera)

        if self.wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Enable wireframe
        self.level_creator.main_renderer.rect_renderer.render(self.rects, self.level_creator.camera)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Disable wireframe

        for chunk in self.level_creator.level.chunks:
            if 32 * chunk["location"][0] < self.cursor_world_pos[0] < 32 * (chunk["location"][0] + 1) and 32 * chunk["location"][
                    1] < self.cursor_world_pos[1] < 32 * (chunk["location"][1] + 1):
                self.level_creator.main_renderer.rect_renderer.render([self.cursor_rect], self.level_creator.camera)
                break