import numpy as np
from OpenGL.GL import *

from engine.opengl.objects.Line import Line
from engine.opengl.objects.Rect import Rect


class CollisionMode:
    def __init__(self, main_renderer):
        self.main_renderer = main_renderer

        self.cursor_rect = Rect((0, 0), (1, 1), (1, 0, 0, 0.5))

        self.chunk_borders = []

    def on_switch(self, level_creator):
        self.chunk_borders = []
        for chunk in level_creator.level.chunks:
            vertices = [
                chunk["location"][0] * 32, chunk["location"][1] * 32,
                chunk["location"][0] * 32, (chunk["location"][1] + 1) * 32,
                (chunk["location"][0] + 1) * 32, (chunk["location"][1] + 1) * 32,
                (chunk["location"][0] + 1) * 32, chunk["location"][1] * 32,
            ]
            self.chunk_borders.append(Line(vertices, (0, 0, 0, 1), 10, mode=Line.LINE_LOOP))

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

    def run(self, level_creator):
        cursor_pos = level_creator.window_to_projection(level_creator.display_manager.get_cursor_pos(), [16, 9])
        world_pos = cursor_pos + level_creator.camera.position[:2]
        cursor_tile = np.floor(world_pos).astype(np.int32)
        cursor_tile.resize((1, 3))
        self.cursor_rect.position = cursor_tile

        rects = []
        for chunk in level_creator.level.chunks:
            rects.extend(self.gen_rects(chunk["collision_data"], chunk["location"]))

        self.main_renderer.line_renderer.render(self.chunk_borders, level_creator.camera)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Enable wireframe
        self.main_renderer.rect_renderer.render(rects, level_creator.camera)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Disable wireframe

        for chunk in level_creator.level.chunks:
            if 32 * chunk["location"][0] < world_pos[0] < 32 * (chunk["location"][0] + 1) and 32 * chunk["location"][
                    1] < world_pos[1] < 32 * (chunk["location"][1] + 1):
                self.main_renderer.rect_renderer.render([self.cursor_rect], level_creator.camera)
                break