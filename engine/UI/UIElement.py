from engine.UI.UIConstraints import UIConstraints

class UIElement:
    def __init__(self, constraints):
        self.constraints = constraints
        self.parent = None
        self.elements = []
        self.show = True

        # generated dynamically
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def add_element(self, element):
        self.elements.append(element)
        element.parent = self

    def calculate_pos_dims(self):
        # This is the root element and takes up the whole screen
        if self.parent is None:
            self.x = 0
            self.y = 0
            self.width = 1
            self.height = 1

        else:
            # Impossible to have height and width be aspect constraints
            if self.constraints.width[0] == UIConstraints.ASPECT_CONSTRAINT and self.constraints.height[0] == UIConstraints.ASPECT_CONSTRAINT:
                return

            # Check cases for absolute and relative constraints for width and height before aspect constraints
            if self.constraints.width[0] == UIConstraints.ABSOLUTE_CONSTRAINT:
                self.width = self.constraints.width[1]
            elif self.constraints.width[0] == UIConstraints.RELATIVE_CONSTRAINT:
                self.width = self.parent.width * self.constraints.width[1]

            if self.constraints.height[0] == UIConstraints.ABSOLUTE_CONSTRAINT:
                self.height = self.constraints.height[1]
            elif self.constraints.height[0] == UIConstraints.RELATIVE_CONSTRAINT:
                self.height = self.parent.height * self.constraints.height[1]

            # Can calculate aspect constraint now since the at least one of width or height has been calculated
            if self.constraints.width[0] == UIConstraints.ASPECT_CONSTRAINT:
                self.width = self.height * self.constraints.width[1]

            if self.constraints.height[0] == UIConstraints.ASPECT_CONSTRAINT:
                self.height = self.width * self.constraints.height[1]

            # Calculate x constraints
            if self.constraints.x[0] == UIConstraints.ABSOLUTE_CONSTRAINT:
                self.x = self.parent.x + self.constraints.x[1]
            elif self.constraints.x[0] == UIConstraints.RELATIVE_CONSTRAINT:
                self.x = self.parent.x + self.parent.width * self.constraints.x[1]
            elif self.constraints.x[0] == UIConstraints.CENTRE_CONSTRAINT:
                self.x = self.parent.x + self.parent.width / 2 - self.width / 2

            # Calculate y constraints
            if self.constraints.y[0] == UIConstraints.ABSOLUTE_CONSTRAINT:
                self.y = self.parent.y + self.constraints.y[1]
            elif self.constraints.y[0] == UIConstraints.RELATIVE_CONSTRAINT:
                self.y = self.parent.y + self.parent.height * self.constraints.y[1]
            elif self.constraints.y[0] == UIConstraints.CENTRE_CONSTRAINT:
                self.y = self.parent.y + self.parent.height / 2 - self.height / 2

        # Calculate position and dimensions for child elements as well
        for element in self.elements:
            element.calculate_pos_dims()