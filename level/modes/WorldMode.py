import numpy as np

from engine.opengl.objects.Line import Line
from engine.opengl.objects.Quad import Quad
from level.modes.TemplateMode import TemplateMode


class WorldMode(TemplateMode):
    def __init__(self, level_creator):
        super().__init__(level_creator)

        self.chunk_borders = []
        self.grid_lines = []

    def on_switch(self):
        # Create chunk borders
        self.chunk_borders = []
        chunks = self.level_creator.level.chunks
        for chunk in chunks:
            vertices = [
                chunk["location"][0] * 32, chunk["location"][1] * 32,
                chunk["location"][0] * 32, (chunk["location"][1] + 1) * 32,
                (chunk["location"][0] + 1) * 32, (chunk["location"][1] + 1) * 32,
                (chunk["location"][0] + 1) * 32, chunk["location"][1] * 32,
            ]
            line = Line(vertices, (0, 0, 0, 1), 5, mode=Line.LINE_LOOP)
            self.chunk_borders.append(line)

        # Create grid lines
        for chunk in chunks:
            root = [chunk["location"][0] * 32, chunk["location"][1] * 32]
            vertices = []
            for i in range(1, 32):
                horizontal = [root[0], root[1]+i, root[0]+32, root[1]+i]
                vertical = [root[0]+i, root[1], root[0]+i, root[1]+32]
                vertices.extend(horizontal)
                vertices.extend(vertical)
            line = Line(vertices, (0.5, 0.5, 0.5, 1), 1)
            self.grid_lines.append(line)

    def gen_quads(self):
        quads = []
        level = self.level_creator.level
        chunks = level.chunks
        for chunk in chunks:
            root = [chunk["location"][0] * 32, chunk["location"][1] * 32]
            for layer in chunk["layers"]:
                for i in range(len(layer)):
                    for j in range(len(layer[i])):
                        atlas_index = layer[i][j]
                        if atlas_index != -1:
                            level.texture_atlas.set_frame(atlas_index)

                            quad = Quad(level.texture_atlas)

                            pos = [root[0] + i, root[1] + j]
                            quad.set_position(*pos)

                            quads.append(quad)

        return quads

    def render(self):
        camera = self.level_creator.camera

        renderer = self.level_creator.main_renderer.line_renderer
        renderer.render(self.chunk_borders + self.grid_lines, camera)

        quads = self.gen_quads()
        renderer = self.level_creator.main_renderer.quad_renderer
        renderer.render(quads, camera)