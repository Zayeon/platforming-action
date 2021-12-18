from OpenGL.GL import *

class VAO:

    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.vao_ID = glGenVertexArrays(1)

    def store_data_in_attribute_list(self, attribute_number, coordinate_size, data):
        glBindVertexArray(self.vao_ID)
        vbo_ID = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_ID)
        glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        # Could replace 0 with data.itemsize * coordinate_size
        glVertexAttribPointer(attribute_number, coordinate_size, GL_FLOAT, GL_FALSE, 0,
                              ctypes.c_void_p(0))
        glBindVertexArray(0)

    def bind_indices_buffer(self, indices):
        glBindVertexArray(self.vao_ID)
        ibo_ID = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo_ID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        glBindVertexArray(0)

    def bind(self):
        glBindVertexArray(self.vao_ID)

    def unbind(self):
        glBindVertexArray(0)

    def get_ID(self):
        return self.vao_ID

    def get_vertex_count(self):
        return self.vertex_count
