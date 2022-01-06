from engine.opengl.objects.QuadRenderer import QuadRenderer
from engine.opengl.objects.ConvexPolygonRenderer import ConvexPolygonRenderer
from engine.opengl.objects.RectRenderer import RectRenderer
from engine.opengl.objects.LineRenderer import LineRenderer


class MainRenderer:
    def __init__(self, projection_matrix):
        # self.projection_matrix = pyrr.matrix44.create_orthogonal_projection(-16, 16, -9, 9, 0, 100)

        self.quad_renderer = QuadRenderer()
        self.convex_polygon_renderer = ConvexPolygonRenderer()
        self.rect_renderer = RectRenderer()
        self.line_renderer = LineRenderer()

        self.set_projection_matrix(projection_matrix)

    def set_projection_matrix(self, matrix):
        self.quad_renderer.set_projection_matrix(matrix)
        self.convex_polygon_renderer.set_projection_matrix(matrix)
        self.rect_renderer.set_projection_matrix(matrix)
        self.line_renderer.set_projection_matrix(matrix)

    def render(self, quads, polygons, rects, lines, camera):
        self.quad_renderer.render(quads, camera)
        self.convex_polygon_renderer.render(polygons, camera)
        self.rect_renderer.render(rects, camera)
        self.line_renderer.render(lines, camera)