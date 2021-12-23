from engine.opengl.QuadRenderer import QuadRenderer
from engine.opengl.ConvexPolygonRenderer import ConvexPolygonRenderer

import pyrr

class MainRenderer:
    def __init__(self, projection_matrix):
        self.projection_matrix = projection_matrix  # pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)

        self.quad_renderer = QuadRenderer()
        self.quad_renderer.set_projection_matrix(self.projection_matrix)
        self.convex_polygon_renderer = ConvexPolygonRenderer()
        self.convex_polygon_renderer.set_projection_matrix(self.projection_matrix)

    def render(self, quads, polygons, camera):
        self.quad_renderer.render(quads, camera)
        self.convex_polygon_renderer.render(polygons, camera)