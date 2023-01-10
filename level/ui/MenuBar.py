from engine.UI.UIButton import UIButton
from engine.UI.UIConstraints import UIConstraints
from engine.UI.UIElement import UIElement
from engine.UI.UILabel import UILabel
from engine.UI.UIRect import UIRect


class MenuBar:
    def __init__(self, level_creator):
        self.level_creator = level_creator
        self.root = UIElement(UIConstraints())

        self.collision_button = CollisionButton(level_creator)
        self.texture_button = WorldButton(level_creator)

        self.collision_button.set_callback(self.on_collision_button_press)
        self.texture_button.set_callback(self.on_texture_button_press)

        self.root.add_element(self.collision_button)
        self.root.add_element(self.texture_button)

        self.root.calculate_pos_dims(level_creator.display_manager.width, level_creator.display_manager.height)
        level_creator.display_manager.bind_mouse_button_event(self.root.on_mouse_button_event)
        level_creator.display_manager.bind_mouse_move_event(self.root.on_mouse_move)

    def get_ui(self):
        return self.root

    def on_button_press(self, button):
        self.collision_button.rect.colour = (1, 1, 1, 1)
        self.texture_button.rect.colour = (1, 1, 1, 1)

        button.rect.colour = (0.5, 0.5, 0.5, 1)

    def on_collision_button_press(self, button):
        self.on_button_press(button)
        self.level_creator.switch_mode(self.level_creator.collision_mode)

    def on_texture_button_press(self, button):
        self.on_button_press(button)
        self.level_creator.switch_mode(self.level_creator.texture_mode)


class CollisionButton(UIButton):
    def __init__(self, level_creator):
        constraints = UIConstraints()
        constraints.set_x_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0)
        constraints.set_y_constraint(UIConstraints.PIXEL_CONSTRAINT, 0)
        constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.1)
        constraints.set_height_constraint(UIConstraints.PIXEL_CONSTRAINT, 50)
        super().__init__(constraints)

        constraints = UIConstraints()
        constraints.set_x_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0)
        constraints.set_y_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0)
        constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 1)
        constraints.set_height_constraint(UIConstraints.RELATIVE_CONSTRAINT, 1)
        self.rect = UIRect(constraints, (0.5, 0.5, 0.5, 1))
        constraints = UIConstraints()
        constraints.set_x_constraint(UIConstraints.CENTRE_CONSTRAINT, 0)
        constraints.set_y_constraint(UIConstraints.CENTRE_CONSTRAINT, 0)
        constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.7)
        constraints.set_height_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.5)
        self.text = UILabel(constraints, level_creator.font_8bit, "Collision", (0, 0, 0))
        self.add_element(self.rect)
        self.add_element(self.text)


class WorldButton(UIButton):
    def __init__(self, level_creator):
        constraints = UIConstraints()
        constraints.set_x_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.1)
        constraints.set_y_constraint(UIConstraints.PIXEL_CONSTRAINT, 0)
        constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.1)
        constraints.set_height_constraint(UIConstraints.PIXEL_CONSTRAINT, 50)
        super().__init__(constraints)

        constraints = UIConstraints()
        constraints.set_x_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0)
        constraints.set_y_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0)
        constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 1)
        constraints.set_height_constraint(UIConstraints.RELATIVE_CONSTRAINT, 1)
        self.rect = UIRect(constraints, (1, 1, 1, 1))
        constraints = UIConstraints()
        constraints.set_x_constraint(UIConstraints.CENTRE_CONSTRAINT, 0)
        constraints.set_y_constraint(UIConstraints.CENTRE_CONSTRAINT, 0)
        constraints.set_width_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.7)
        constraints.set_height_constraint(UIConstraints.RELATIVE_CONSTRAINT, 0.5)
        self.text = UILabel(constraints, level_creator.font_8bit, "World", (0, 0, 0))
        self.add_element(self.rect)
        self.add_element(self.text)


