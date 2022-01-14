

class UIConstraints:
    # Constraints
    ABSOLUTE_CONSTRAINT = 0
    CENTRE_CONSTRAINT = 1  # Applies to only x or y
    RELATIVE_CONSTRAINT = 2
    ASPECT_CONSTRAINT = 3  # Applies to only width or height

    def __init__(self):
        self.x = (UIConstraints.RELATIVE_CONSTRAINT, 1)
        self.y = (UIConstraints.RELATIVE_CONSTRAINT, 1)
        self.width = (UIConstraints.RELATIVE_CONSTRAINT, 1)
        self.height = (UIConstraints.RELATIVE_CONSTRAINT, 1)

    def set_x_constraint(self, type, value):
        self.x = (type, value)

    def set_y_constraint(self, type, value):
        self.y = (type, value)

    def set_width_constraint(self, type, value):
        self.width = (type, value)

    def set_height_constraint(self, type, value):
        self.height = (type, value)