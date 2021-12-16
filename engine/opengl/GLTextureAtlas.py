from OpenGL.GL import *
from PIL import Image

class TextureAtlas:

    all_textures = {}

    def __init__(self, file_path, n_frames, columns, unit_width, unit_height):
        # Don't need to know rows since they can be calculated from n_textures and columns
        self.n_frames = n_frames
        self.columns = columns

        image = Image.open(file_path)

        self.current_frame = 0
        rows = n_frames - 1 // columns
        self.normal_width = unit_width / image.width
        self.normal_height = unit_height / image.height

        # Texture coordinates of the first frame
        self.tex_coords = [
            0, 1 - self.normal_height,
            0, 1,
            self.normal_width, 1,
            self.normal_width, 1 - self.normal_height
        ]

        # If we have already loaded this texture into the gpu then there's no need to load it again
        if file_path not in self.all_textures:
            image = Image.open(file_path)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

            image_data = image.convert("RGBA").tobytes()
            self.gen_texture(image_data, image.width, image.height)

            self.all_textures[file_path] = self.texture_ID

        else:
            self.texture_ID = self.all_textures[file_path]

    def gen_texture(self, image_data, width, height):
        self.texture_ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_ID)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glBindTexture(GL_TEXTURE_2D, 0)

    def get_ID(self):
        return self.texture_ID

    def next_frame(self):
        self.current_frame += 1
        if self.current_frame >= self.n_frames:
            self.current_frame = 0
        self.calculate_tex_coords(self.current_frame)

    def calculate_tex_coords(self, frame):
        column = frame % self.columns
        row = frame // self.columns
        width_offset = column * self.normal_width
        height_offset = row * self.normal_height
        self.tex_coords = [
            width_offset, 1 - self.normal_height - height_offset,
            width_offset, 1 - height_offset,
            self.normal_width + width_offset, 1 - height_offset,
            self.normal_width + width_offset, 1 - self.normal_height - height_offset
        ]

    def get_tex_coords(self):
        return self.tex_coords