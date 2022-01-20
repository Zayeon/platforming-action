from engine.UI.UIConstraints import UIConstraints
from engine.UI.UIElement import UIElement


class UILabel(UIElement):
    def __init__(self, constraints, font, text, text_colour, scale):
        super().__init__(constraints)
        self.font = font
        self.text_vao, self.width, self.height = font.construct_text(text)
        self.text_colour = text_colour

    def calculate_pos_dims(self, window_width, window_height):
        # Calculate x constraints
        if self.constraints.x[0] == UIConstraints.PIXEL_CONSTRAINT:
            self.x = self.parent.x + self.constraints.x[1]
        elif self.constraints.x[0] == UIConstraints.RELATIVE_CONSTRAINT:
            self.x = self.parent.x + self.parent.width * self.constraints.x[1]
        elif self.constraints.x[0] == UIConstraints.CENTRE_CONSTRAINT:
            self.x = self.parent.x + self.parent.width / 2 - self.width / 2

        # Calculate y constraints
        if self.constraints.y[0] == UIConstraints.PIXEL_CONSTRAINT:
            self.y = self.parent.y + self.constraints.y[1]
        elif self.constraints.y[0] == UIConstraints.RELATIVE_CONSTRAINT:
            self.y = self.parent.y + self.parent.height * self.constraints.y[1]
        elif self.constraints.y[0] == UIConstraints.CENTRE_CONSTRAINT:
            self.y = self.parent.y + self.parent.height / 2 - self.height / 2
