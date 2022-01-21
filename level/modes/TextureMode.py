import numpy as np

from engine.opengl.objects.Line import Line
from level.modes.TemplateMode import TemplateMode


class TextureMode(TemplateMode):
    def __init__(self, level_creator):
        super().__init__(level_creator)

        self.chunk_borders = []
        self.grid_lines = []

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
                horizontal = [root[0], root[1]+i, root[0]+32, root[1]+i]
                vertical = [root[0]+i, root[1], root[0]+i, root[1]+32]
                vertices.extend(horizontal)
                vertices.extend(vertical)
            self.grid_lines.append(Line(vertices, (0.5, 0.5, 0.5, 1), 1))

    def run(self):
        renderer = self.level_creator.main_renderer.line_renderer
        renderer.render(self.chunk_borders + self.grid_lines, self.level_creator.camera)