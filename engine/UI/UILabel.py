import numpy as np
import pyrr

from engine.UI.UIConstraints import UIConstraints
from engine.UI.UIElement import UIElement


class UILabel(UIElement):
    def __init__(self, constraints, font, text, text_colour, scale):
        super().__init__(constraints)
        self.font = font
        self.text_vao, self.width, self.height = font.construct_text(text)
        self.text_colour = text_colour
        self.scale = pyrr.matrix44.create_identity()

    def to_text_space(self, pos, display_width, display_height):
        # For some reason text can't use the same projection matrix
        # as the rest of the gui so i have to convert it into -1 to 1 space
        pos = np.array(pos, dtype=np.float32)
        dims = np.array([display_width, display_height], dtype=np.float32)
        pos = pos / dims  # 0 to 1
        pos = pos * 2 - 1  # -1 to 1
        pos[1] *= -1  # Since y goes up not down
        return pos

    def calculate_pos_dims(self, window_width, window_height):
        # Impossible to have height and width be aspect constraints
        if self.constraints.width[0] == UIConstraints.ASPECT_CONSTRAINT and self.constraints.height[
                0] == UIConstraints.ASPECT_CONSTRAINT:
            return

        # Check cases for absolute and relative constraints for width and height before aspect constraints
        if self.constraints.width[0] == UIConstraints.PIXEL_CONSTRAINT:
            width = self.constraints.width[1]
        elif self.constraints.width[0] == UIConstraints.RELATIVE_CONSTRAINT:
            width = self.parent.width * self.constraints.width[1]

        if self.constraints.height[0] == UIConstraints.PIXEL_CONSTRAINT:
            height = self.constraints.height[1]
        elif self.constraints.height[0] == UIConstraints.RELATIVE_CONSTRAINT:
            height = self.parent.height * self.constraints.height[1]

        # Can calculate aspect constraint now since the at least one of width or height has been calculated
        if self.constraints.width[0] == UIConstraints.ASPECT_CONSTRAINT:
            width = height * self.constraints.width[1]

        if self.constraints.height[0] == UIConstraints.ASPECT_CONSTRAINT:
            height = width * self.constraints.height[1]

        # Calculate x constraints
        if self.constraints.x[0] == UIConstraints.PIXEL_CONSTRAINT:
            self.x = self.parent.x + self.constraints.x[1]
        elif self.constraints.x[0] == UIConstraints.RELATIVE_CONSTRAINT:
            self.x = self.parent.x + self.parent.width * self.constraints.x[1]
        elif self.constraints.x[0] == UIConstraints.CENTRE_CONSTRAINT:
            self.x = self.parent.x + self.parent.width / 2 - width / 2

        # Calculate y constraints
        if self.constraints.y[0] == UIConstraints.PIXEL_CONSTRAINT:
            self.y = self.parent.y + self.constraints.y[1]
        elif self.constraints.y[0] == UIConstraints.RELATIVE_CONSTRAINT:
            self.y = self.parent.y + self.parent.height * self.constraints.y[1]
        elif self.constraints.y[0] == UIConstraints.CENTRE_CONSTRAINT:
            self.y = self.parent.y + self.parent.height / 2 - height / 2

        self.x, self.y = self.to_text_space((self.x, self.y), window_width, window_height)
        width = (width / window_width) * 2
        height = (height / window_height) * 2

        self.scale = pyrr.matrix44.create_from_scale((width/self.width, height/self.height, 1))