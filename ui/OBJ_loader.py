import numpy as np
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLShaderProgram
class component:
    def __init__(self,filepath):
        self.mass = None
        self.COM = []
        self.bodies = []
        self.filepath = filepath
        self.componentName = filepath.split("/")[-1].split(".")[0]
        self.load_bodies(filepath)
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

if __name__ == "__main__":
    filepath ="reinforcement_learning/ui/test2.txt"
    component_1 = component(filepath)
