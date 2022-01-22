import glfw

from engine.UI.UIElement import UIElement


class UIButton(UIElement):
    def __init__(self, constraints, callback):
        super().__init__(constraints)
        self.callback = callback
        self.mouse_over = False

    def on_mouse_move(self, xpos, ypos):
        # Check if mouse inside button
        self.mouse_over = self.x <= xpos <= self.x + self.width and self.y <= ypos <= self.y + self.height

    def on_mouse_button_event(self, button, action):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS and self.mouse_over:
            # Button has been clicked
            self.callback()