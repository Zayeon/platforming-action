import glfw
from OpenGL.GL import glViewport

class DisplayManager:

    def __init__(self):
        if not glfw.init():
            print("Error: GLFW failed to initialise")
            glfw.terminate()
            exit(0)

        glfw.set_error_callback(self.error_callback)


        self.window_ID = None
        self.width = 0
        self.height = 0
        self.title = None
        self.delta_time = 0
        self.last_frame = 0
        self.fullscreen = False
        self.on_key_press_methods = {}

    def create_window(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title

        glfw.window_hint(glfw.RESIZABLE, False)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window_ID = glfw.create_window(self.width, self.height, self.title, None, None)

        glfw.make_context_current(self.window_ID)

        glfw.set_key_callback(self.window_ID, self.key_callback)

        self.last_frame = glfw.get_time()

        if not self.window_ID:
            glfw.terminate()
            exit(0)

    def error_callback(self, error, description):
        print("Error: " + description)

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_F11 and action == glfw.PRESS:
            self.toggle_fullscreen()

        # Goes through all the bound functions by key and executes them if that key was pressed
        for k in self.on_key_press_methods:
            if key == k and action == glfw.PRESS:
                for f in self.on_key_press_methods[k]:
                    f()

    def bind_key_down(self, key, function):
        if not key in self.on_key_press_methods:
            self.on_key_press_methods[key] = []

        self.on_key_press_methods[key].append(function)

    def toggle_fullscreen(self):
        if not self.fullscreen:
            monitor = glfw.get_primary_monitor()
            width = glfw.get_video_mode(monitor).size[0]
            height = glfw.get_video_mode(monitor).size[1]
            refresh_rate = glfw.get_video_mode(monitor).refresh_rate
            glfw.set_window_monitor(self.window_ID, monitor, 0, 0, width, height, refresh_rate)

            # Separate from glfw if necessary
            glViewport(0, 0, width, height)

        else:
            glfw.set_window_monitor(self.window_ID, None, 50, 50, self.width, self.height, glfw.DONT_CARE)
            # Separate from glfw if necessary
            glViewport(0, 0, self.width, self.height)

        self.fullscreen = not self.fullscreen

    def start_frame(self):
        glfw.poll_events()
        current_time = glfw.get_time()
        self.delta_time = current_time - self.last_frame
        self.last_frame = current_time

    def update_display(self):
        glfw.swap_buffers(self.window_ID)

    def get_cursor_pos(self):
        return glfw.get_cursor_pos(self.window_ID)

    def get_key_state(self, key):
        return glfw.get_key(self.window_ID, key) == glfw.PRESS

    def get_mouse_click(self, button):
        return glfw.get_mouse_button(self.window_ID, button)

    def set_cursor_lock(self, lock):
        glfw.set_input_mode(self.window_ID, glfw.CURSOR, glfw.CURSOR_DISABLED if lock else glfw.CURSOR_NORMAL)

    def window_should_close(self):
        return glfw.window_should_close(self.window_ID)

    def close(self):
        glfw.terminate()
        glfw.destroy_window(self.window_ID)
