import numpy as np
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLShaderProgram
from OpenGL.GL import *
from singelton import singleton

from typing import Callable
from ev_manager import Event



@singleton
class component_manager:

    def __init__(self,renderer):
        self.components = []
        self.renderer = renderer
        self.events = {}

    def load_component(self,filepath):
        temp_component = component(filepath)
        self.components.append(temp_component)
        self.init_vbo(temp_component)
    
    def init_vbo(self,temp_component):
        for body in temp_component.bodies:
            print(f"initiating vbo for body {body.name}")
            self.renderer.init_vbo_for_body(body)

class component:
    def __init__(self,filepath):
        self.mass = None
        self.COM = []
        self.bodies = []
        self.filepath = filepath
        self.componentName = self.filepath.split("/")[-1].split(".")[0]
        self.load_bodies(self.filepath)
        self.volume = None
        self.enable = True
        
    def load_bodies(self,filepath):
        vertices = []
        indices = []
        bodyname = None
        previous_vertices = 0

        with open(filepath, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Vertex data
                    parts = line.split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])

                elif line.startswith('f '):  # Face data
                    parts = line.split()
                    for part in parts[1:]:
                        indices.append(int(part.split('/')[0]) - 1 - np.uint32(previous_vertices))  # OBJ files are 1-indexed

                elif line.startswith('g '):  # Group (new body)
                    if bodyname is not None:  # If it's not the first group, create a body
                        self.bodies.append(OBJ_body(body_name=bodyname,
                                                    vertices=np.array(vertices, dtype=np.float32),
                                                    indices=np.array(indices, dtype=np.uint32)))
                        previous_vertices += len(vertices)
                        vertices = []  # Reset vertices for the new body
                        indices = []  # Reset indices for the new body
                    bodyname = line.split()[1]  # Capture the new group name

            # Append the last body after the loop
            if bodyname is not None:
                self.bodies.append(OBJ_body(body_name=bodyname,
                                            vertices=np.array(vertices, dtype=np.float32),
                                            indices=np.array(indices, dtype=np.uint32)))
                
    def calculate_center_of_mass(self):
        pass

    def calculate_mass(self):
        pass

    def isVisable(self):
        return self.enable

class OBJ_body:
    def __init__(self,vertices,body_name,indices):
        self.vertices = vertices
        self.indices = indices
        self.name = body_name
        self.mass = None
        self.cetnerOfMass = []
        self.origin = [1,1,1]
        self.vertex = []
        self.Enable = True
        self.vertex_offset = None
        self.index_offset = None
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        self.ebo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)


    def get_vertices(self):
        return self.vertices
    
    def get_indices(self):
        return self.indices
    
    def uppdate_vertex(self):
        pass

    def isVisable(self):
        return self.Enable

    def uppdate_vbo(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices['vertices'])
    
if __name__ == "__main__":
    filepath ="reinforcement_learning/ui/test2.txt"
    component_1 = component(filepath)
    print("runs")
