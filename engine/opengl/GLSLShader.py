from OpenGL.GL import *
import os.path

class GLSLShader:
    def __init__(self, file_path):
        self.shader_ID = 0
        self.uniforms = {}

        self.create_shader(file_path)

    def create_shader(self, file_path):
        vertex_shader_code = ""
        fragment_shader_code = ""
        writing_to_vertex = True

        # Open the shader, read lines and append to the relevant code buffer
        with open(file_path, "r") as shader_file:
            for line in shader_file:
                if line.startswith("##VERTEX"):
                    writing_to_vertex = True
                elif line.startswith("##FRAGMENT"):
                    writing_to_vertex = False
                else:
                    if writing_to_vertex:
                        vertex_shader_code += line
                    else:
                        fragment_shader_code += line

        # Create shader in OpenGl
        self.shader_ID = glCreateProgram()
        vertex_id = self.add_shader(vertex_shader_code, GL_VERTEX_SHADER)
        fragment_id = self.add_shader(fragment_shader_code, GL_FRAGMENT_SHADER)

        # Combining the shaders into one program
        glAttachShader(self.shader_ID, vertex_id)
        glAttachShader(self.shader_ID, fragment_id)
        glLinkProgram(self.shader_ID)

        # If there is an error with the shader program, exit
        if glGetProgramiv(self.shader_ID, GL_LINK_STATUS) != GL_TRUE:
            # Get info of error and delete all shaders
            info = glGetProgramInfoLog(self.shader_ID)
            glDeleteProgram(self.shader_ID)
            glDeleteShader(vertex_id)
            glDeleteShader(fragment_id)
            raise RuntimeError('Error linking program: %s' % info)

        # Cleanup vertex and fragment shaders since they have been bound to the shader program
        glDeleteShader(vertex_id)
        glDeleteShader(fragment_id)

    def add_shader(self, source, shader_type):
        # Creating the specific shaders, i.e vertex, fragment
        shader_id = glCreateShader(shader_type)
        glShaderSource(shader_id, source)
        glCompileShader(shader_id)

        # If there is an error with this shader, exit
        if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
            info = glGetShaderInfoLog(shader_id)
            raise RuntimeError('Shader compilation failed: %s' % info)
        return shader_id

    def bind(self):
        glUseProgram(self.shader_ID)

    def unbind(self):
        glUseProgram(0)

    # Uniforms

    def get_uniform_location(self, uniform_name):
        # Creates a buffer of previously used uniforms to reduce calls of glGetUniformLocation
        # if not (uniform_name in self.uniforms):
        #     location = glGetUniformLocation(self.shader_ID, uniform_name)
        #     self.uniforms[uniform_name] = location
        # else:
        #     location = self.uniforms[uniform_name]
        # return location
        return glGetUniformLocation(self.shader_ID, uniform_name)

    def set_uniform4f(self, uniform_name, v1, v2, v3, v4):
        location = self.get_uniform_location(uniform_name)
        glUniform4f(location, v1, v2, v3, v4)

    def set_uniform_mat4fv(self, uniform_name, matrix):
        location = self.get_uniform_location(uniform_name)
        glUniformMatrix4fv(location, 1, GL_FALSE, matrix)

    def set_uniform1f(self, uniform_name, v):
        location = self.get_uniform_location(uniform_name)
        glUniform1f(location, v)

    def set_uniform2f(self, uniform_name, v1, v2):
        location = self.get_uniform_location(uniform_name)
        glUniform2f(location, v1, v2)

    def set_uniform3f(self, uniform_name, v1, v2, v3):
        location = self.get_uniform_location(uniform_name)
        glUniform3f(location, v1, v2, v3)

