import numpy as np
from math import radians, cos, sin

import warnings

from engine.physics.AABB import AABB

class InteractionWorld:
    def __init__(self):
        self.convex_polygons = []
        self.boxes = []

    def add_polygon(self, polygon):
        self.convex_polygons.append(polygon)

    def add_box(self, box):
        self.boxes.append(box)

    # def react_to_movement(self, polygon_a, proposed_movement):
    #     reaction = np.array([0, 0], dtype=np.float32)
    #     movement_length = (proposed_movement[0] ** 2 + proposed_movement[1] ** 2) ** -1 / 2
    #     for polygon_b in self.convex_polygons:
    #         intersections = self.intersect_convex_polygon(polygon_a, polygon_b)
    #         if len(intersections) > 0:
    #             for face_pair in intersections:
    #                 normal = polygon_b.normals[face_pair[1]]
    #                 dot = normal[0] * proposed_movement[0] + normal[1] * proposed_movement[1]
    #                 cos_theta = dot / movement_length
    #                 # if alpha = pi - theta, cos(alpha) = -cos(theta)
    #                 reaction += proposed_movement * -cos_theta
    #     reaction_length = (reaction[0] ** 2 + reaction[1] ** 2) ** -1 / 2
    #     scaled_reaction = reaction * (movement_length / reaction_length)
    #     return scaled_reaction

    def intersect_convex_polygon(self, polygon_a, polygon_b):
        # Works by brute force checking the line equations of each face of each polygon and looking for intersections
        face_pairs = []

        # We need to transform the vertices of polygon b relative to polygon a
        translationAB = polygon_b.position - polygon_a.position
        # translationAB.resize(3)  # Add a z coordinate of 0
        rotationAB = polygon_b.rotation - polygon_a.rotation
        r = radians(rotationAB)
        rotation_matrix = np.array([[cos(r), -sin(r)], [sin(r), cos(r)]])
        # rotation_matrix = pyrr.matrix33.create_from_z_rotation(radians(rotationAB))
        polygon_b_vertices = polygon_b.vertices[:, 0:2].copy()
        for i in range(len(polygon_b_vertices)):
            polygon_b_vertices[i] += translationAB
            polygon_b_vertices[i] = np.matmul(rotation_matrix, polygon_b_vertices[i])

        for i in range(len(polygon_a.vertices)):
            face_a_origin = polygon_a.vertices[i][0:2]
            face_a_direction = polygon_a.vertices[(i + 1) % len(polygon_a.vertices)] - polygon_a.vertices[i]
            for j in range(len(polygon_b_vertices)):
                face_b_origin = polygon_b_vertices[j]
                next_vertex = polygon_b_vertices[(j + 1) % len(polygon_b_vertices)]
                face_b_direction = next_vertex - polygon_b_vertices[j]

                # Calculate line intersection
                t = self.ray_intersect_ray(face_a_origin, face_a_direction, face_b_origin, face_b_direction)
                if 0 <= t[0] <= 1 and 0 <= t[1] <= 1:
                    face_pairs.append([i, j])

        return face_pairs

    # def intersect_convex_polygon(self, a, b, m):
    #     # a and b are polygons, m is the proposed movement
    #     collided_face = self.vertex_face_collision(a, b, m)
    #     if not collided_face:
    #         collided_face = self.vertex_face_collision(b, a, -m)
    #     if not collided_face:
    #         return


    # def vertex_face_collision(self, a, b, m):
    #     # a and b are polygons, m is the proposed movement
    #     for vertex_a in a.vertices:
    #         for i in range(len(b.vertices)):
    #             face_direction = b.vertices[(i + 1) % len(b.vertices)] - b.vertices[i]
    #             t = self.ray_intersect_ray(vertex_a, m, b.vertices[i], face_direction)
    #             if 0 <= t[0] <= 1 and 0 <= t[1] <= 1:
    #                 return i

    def ray_intersect_ray(self, o1, d1, o2, d2):
        m = np.array([[-d2[1], d2[0]], [-d1[1], d1[0]]])
        o = (o2 - o1)
        o.reshape(2, 1)
        d = -d1[0] * d2[1] + d1[1] * d2[0]
        t = np.matmul(m, o) / d
        return t

    # Source: https://github.com/OneLoneCoder/olcPixelGameEngine/blob/master/Videos/OneLoneCoder_PGE_Rectangles.cpp
    def ray_intersect_rect(self, ray_origin, ray_dir, target):

        # Divide by 0 is ok just suppress warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Calculate intersections with AABB axes
            t_near = (target.position - ray_origin) / ray_dir
            t_far = (target.position + target.size - ray_origin) / ray_dir

        if np.isnan(t_near[0]) or np.isnan(t_near[1]) or np.isnan(t_far[0]) or np.isnan(t_far[1]):
            return

        # Swap near and far if near > far
        if t_near[0] > t_far[0]:
            t_near[0], t_far[0] = t_far[0], t_near[0]
        if t_near[1] > t_far[1]:
            t_near[1], t_far[1] = t_far[1], t_near[1]

        # Reject if ray doesn't intersect AABB for all values of t
        if t_near[0] > t_far[1] or t_near[1] > t_far[0]:
            return

        # Time of intersection will be max of near x and y
        t_hit_near = max(t_near[0], t_near[1])
        t_hit_far = max(t_far[0], t_far[1])

        # Reject if intersection happens behind ray
        if t_hit_far < 0:
            return

        contact_point = ray_origin + ray_dir * t_hit_near

        # Calculate the normal of the edge collided
        contact_normal = np.zeros(2, dtype=np.float32)
        if t_near[0] > t_near[1]:
            if ray_dir[0] < 0:
                contact_normal = np.array([1, 0], dtype=np.float32)
            else:
                contact_normal = np.array([-1, 0], dtype=np.float32)
        elif t_near[0] < t_near[1]:
            if ray_dir[1] < 0:
                contact_normal = np.array([0, 1], dtype=np.float32)
            else:
                contact_normal = np.array([0, -1], dtype=np.float32)

        return t_hit_near, contact_point, contact_normal

    def dynamic_rect_intersect_rect(self, r_dynamic, frame_time, r_static):
        # Check if dynamic aabb is actually moving - We assume the rectangles are not in collision to start
        if r_dynamic.velocity[0] == 0 and r_dynamic.velocity[1] == 0:
            return

        # Expand target rectangle by source dimensions
        pos = r_static.position - r_dynamic.size / 2
        size = r_static.size + r_dynamic.size
        expanded_target = AABB(pos, size)

        intersect = self.ray_intersect_rect(r_dynamic.position + r_dynamic.size / 2, r_dynamic.velocity * frame_time, expanded_target)
        if intersect and 0 <= intersect[0] <= 1:
            return intersect

    # Resolve dynamic rect intersect rect
    # def resolve_DRIR(self, r_dynamic, frame_time, r_static):
    #     intersect = self.dynamic_rect_intersect_rect(r_dynamic, frame_time, r_static)
    #     if intersect:
    #         t_hit, contact_point, contact_normal = intersect
    #         r_dynamic.velocity += contact_normal * np.abs(r_dynamic.velocity) * (1-t_hit)

    def resolve_movement(self, r_dynamic, frame_time):
        collisions = []

        # Work out collision with each box, add it to list along with rect id
        for i, r_static in enumerate(self.boxes):
            intersect = self.dynamic_rect_intersect_rect(r_dynamic, frame_time, r_static)
            if intersect:
                collisions.append(intersect)

        # Sort the collisions by time of intersection
        collisions.sort(key=lambda x: x[0])

        for intersect in collisions:
            t_hit, contact_point, contact_normal = intersect
            r_dynamic.velocity += contact_normal * np.abs(r_dynamic.velocity) * (1-t_hit)
