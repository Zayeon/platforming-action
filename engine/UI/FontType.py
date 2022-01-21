import numpy as np
import os.path

from engine.opengl.GLTextureAtlas import TextureAtlas
from engine.opengl.VAO import VAO

FONT_BITMAP_WIDTH = 512
FONT_BITMAP_HEIGHT = 512

FONT_LOCATION = os.path.join("res", "font")

class FontType:
    separator = " "
    quad_indices = np.array([
        0, 1, 3,
        1, 2, 3
    ], dtype=np.uint8)

    def __init__(self, font_name, aspect_ratio):
        font_path = os.path.join(FONT_LOCATION, font_name)
        self.font_bitmap = TextureAtlas(font_path + ".png", 1, 1, FONT_BITMAP_WIDTH, FONT_BITMAP_HEIGHT, flip=False)

        self.character_table = {}

        with open(font_path + ".fnt", "r") as font_file:
            for line in font_file:
                fragments = line.split(self.separator)
                if fragments[0] == "char":
                    character = Character(fragments)
                    character.normalise(aspect_ratio)
                    self.character_table[character.ID] = character

    def construct_text(self, text, line_spacing=1, char_spacing=0):
        vertices = []
        texture_coords = []
        indices = np.array([], dtype=np.uint8)  # may be too small
        char_counter = 0  # replace with (line_no + 1) * (char_no + 1) ?
        lines = text.split("\n")
        for line_no, line in enumerate(lines):
            cursor = 0
            line_offset = line_no * line_spacing
            for char_no, char in enumerate(line):
                char_id = ord(char)
                if char_id not in self.character_table:
                    char_id = 0
                char_info = self.character_table[char_id]
                char_vertex_data = [
                    cursor + char_info.norm_x_offset, -char_info.norm_y_offset - line_offset,
                    cursor + char_info.norm_x_offset + char_info.norm_width_AR, -char_info.norm_y_offset - line_offset,
                    cursor + char_info.norm_x_offset + char_info.norm_width_AR,
                    -char_info.norm_y_offset - char_info.norm_height - line_offset,
                    cursor + char_info.norm_x_offset, -char_info.norm_y_offset - char_info.norm_height - line_offset,
                ]
                vertices.extend(char_vertex_data)
                char_tex_coords = [
                    char_info.norm_x, char_info.norm_y,
                    char_info.norm_x + char_info.norm_width, char_info.norm_y,
                    char_info.norm_x + char_info.norm_width, char_info.norm_y + char_info.norm_height,
                    char_info.norm_x, char_info.norm_y + char_info.norm_height,
                ]
                texture_coords.extend(char_tex_coords)
                cursor += char_info.norm_x_advance + char_spacing
                new_indices = self.quad_indices + 4 * char_counter
                indices = np.append(indices, new_indices)
                char_counter += 1

        vertices = np.array(vertices, dtype=np.float32)
        texture_coords = np.array(texture_coords, dtype=np.float32)

        width = vertices[0::2].max()
        height = -vertices[1::2].min()

        text_vao = VAO(len(indices))
        text_vao.bind_indices_buffer(indices)
        text_vao.store_data_in_attribute_list(0, 2, vertices)
        text_vao.store_data_in_attribute_list(1, 2, texture_coords)

        return text_vao, width, height


class Character:
    def __init__(self, line_fragments):
        self.norm_x = 0
        self.norm_y = 0
        self.norm_width = 0
        self.norm_height = 0
        self.norm_width_AR = 0
        self.norm_x_offset = 0
        self.norm_y_offset = 0
        self.norm_x_advance = 0

        for fragment in line_fragments:
            if fragment.startswith("id"):
                self.ID = int(fragment.split("=")[1])
            elif fragment.startswith("xoffset"):
                self.x_offset = int(fragment.split("=")[1])
            elif fragment.startswith("yoffset"):
                self.y_offset = int(fragment.split("=")[1])
            elif fragment.startswith("xadvance"):
                self.x_advance = int(fragment.split("=")[1])
            elif fragment.startswith("width"):
                self.width = int(fragment.split("=")[1])
            elif fragment.startswith("height"):
                self.height = int(fragment.split("=")[1])
            elif fragment.startswith("x"):
                self.x = int(fragment.split("=")[1])
            elif fragment.startswith("y"):
                self.y = int(fragment.split("=")[1])

    def normalise(self, aspect_ratio, img_width=FONT_BITMAP_WIDTH, img_height=FONT_BITMAP_HEIGHT):
        a = img_width * aspect_ratio
        self.norm_x = self.x / img_width
        self.norm_y = self.y / img_height
        self.norm_width = self.width / img_width
        self.norm_height = self.height / img_height
        self.norm_width_AR = self.width / a
        self.norm_x_offset = self.x_offset / a
        self.norm_y_offset = self.y_offset / img_width
        self.norm_x_advance = self.x_advance / a