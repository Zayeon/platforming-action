import numpy as np
import pyrr

class ConvexPolygonHitbox:
    def __init__(self, vertices, position, rotation):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.position = position

        # Rotation in degrees
        self.rotation = rotation

        self.normals = []
        for i in range(len(self.vertices)):
            face = self.vertices[(i + 1) % len(self.vertices)] - self.vertices[i]
            normal = pyrr.vector3.cross(face, np.array([0, 0, 1], dtype=np.float32))
            normal = pyrr.vector3.normalise(normal)
            self.normals.append(normal)