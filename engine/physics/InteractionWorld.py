import numpy as np
from math import radians, cos, sin

class InteractionWorld:
    def __init__(self):
        self.convex_polygons = []

    def add_polygon(self, polygon):
        self.convex_polygons.append(polygon)

    def react_to_movement(self, polygon_a, proposed_movement):
        reaction = np.array([0, 0], dtype=np.float32)
        movement_length = (proposed_movement[0] ** 2 + proposed_movement[1] ** 2) ** -1 / 2
        for polygon_b in self.convex_polygons:
            intersections = self.intersect_convex_polygon(polygon_a, polygon_b)
            if len(intersections) > 0:
                for face_pair in intersections:
                    normal = polygon_b.normals[face_pair[1]]
                    dot = normal[0] * proposed_movement[0] + normal[1] * proposed_movement[1]
                    cos_theta = dot / movement_length
                    # if alpha = pi - theta, cos(alpha) = -cos(theta)
                    reaction += proposed_movement * -cos_theta
        reaction_length = (reaction[0] ** 2 + reaction[1] ** 2) ** -1 / 2
        scaled_reaction = reaction * (movement_length / reaction_length)
        return scaled_reaction

    # def intersect_convex_polygon(self, polygon_a, polygon_b):
    #     # Works by brute force checking the line equations of each face of each polygon and looking for intersections
    #     face_pairs = []
    #
    #     # We need to transform the vertices of polygon b relative to polygon a
    #     translationAB = polygon_b.position - polygon_a.position
    #     # translationAB.resize(3)  # Add a z coordinate of 0
    #     rotationAB = polygon_b.rotation - polygon_a.rotation
    #     r = radians(rotationAB)
    #     rotation_matrix = np.array([[cos(r), -sin(r)], [sin(r), cos(r)]])
    #     # rotation_matrix = pyrr.matrix33.create_from_z_rotation(radians(rotationAB))
    #     polygon_b_vertices = polygon_b.vertices[:, 0:2].copy()
    #     for i in range(len(polygon_b_vertices)):
    #         polygon_b_vertices[i] += translationAB
    #         polygon_b_vertices[i] = np.matmul(rotation_matrix, polygon_b_vertices[i])
    #
    #     for i in range(len(polygon_a.vertices)):
    #         face_a_origin = polygon_a.vertices[i][0:2]
    #         face_a_direction = polygon_a.vertices[(i + 1) % len(polygon_a.vertices)] - polygon_a.vertices[i]
    #         for j in range(len(polygon_b_vertices)):
    #             face_b_origin = polygon_b_vertices[j]
    #             next_vertex = polygon_b_vertices[(j + 1) % len(polygon_b_vertices)]
    #             face_b_direction = next_vertex - polygon_b_vertices[j]
    #
    #             # Calculate line intersection
    #             m = np.array([[-face_b_direction[1], face_b_direction[0]], [-face_a_direction[1], face_a_direction[0]]])
    #             o = (face_b_origin - face_a_origin)
    #             o.reshape(2, 1)
    #             d = -face_a_direction[0] * face_b_direction[1] + face_a_direction[1] * face_b_direction[0]
    #             t = np.matmul(m, o) / d
    #             if 0 <= t[0] <= 1 and 0 <= t[1] <= 1:
    #                 face_pairs.append([i, j])
    #
    #     return face_pairs

    def intersect_convex_polygon(self, a, b, m):
        # a and b are polygons, m is the proposed movement
        collided_face = self.vertex_face_collision(a, b, m)
        if not collided_face:
            collided_face = self.vertex_face_collision(b, a, -m)
        if not collided_face:
            return


    def vertex_face_collision(self, a, b, m):
        # a and b are polygons, m is the proposed movement
        for vertex_a in a.vertices:
            for i in range(len(b.vertices)):
                face_direction = b.vertices[(i + 1) % len(b.vertices)] - b.vertices[i]
                t = self.ray_intersect_ray(vertex_a, m, b.vertices[i], face_direction)
                if 0 <= t[0] <= 1 and 0 <= t[1] <= 1:
                    return i

    def ray_intersect_ray(self, o1, d1, o2, d2):
        m = np.array([[-d2[1], d2[0]], [-d1[1], d1[0]]])
        o = (o2 - o1)
        o.reshape(2, 1)
        d = -d1[0] * d2[1] + d1[1] * d2[0]
        t = np.matmul(m, o) / d
        return t