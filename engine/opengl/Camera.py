import pyrr

class Camera:
    def __init__(self):
        self.position = pyrr.Vector3([0, 0, 0])

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def get_position(self):
        return self.position