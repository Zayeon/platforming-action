from OpenGL.GL import *
from PIL import Image

class TextureAtlas:
    def __init__(self, file_path, dimensions):
        # Dimensions: [n, m]
        self.dimensions = dimensions

        image = Image.open(file_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        image_data = image.convert("RGBA").tobytes()

        self.width = image.width
        self.height = image.height

        self.texture_ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_ID)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glBindTexture(GL_TEXTURE_2D, 0)

    def get_ID(self):
        return self.texture_ID

    def get_top_left_tex_coords(self):
        return [
            0, 0,
            0, 1,
            1, 1,
            1, 0
        ]