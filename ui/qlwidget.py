from PyQt5.QtWidgets import QOpenGLWidget
import numpy as np
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLShaderProgram
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLShaderProgram
from PyQt5.QtCore import Qt
from OpenGL.GL import *
import sys
import numpy as np  
import qlwidget
import OBJ_loader 

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.zoom = -5.0  # Initial zoom (distance from the screen)
        self.last_mouse_position = None  # For rotation tracking
        self.x_rotation = 0.0  # Rotation around the x-axis
        self.y_rotation = 0.0  # Rotation around the y-axis
        #self.object_vertices, self.object_indices = load_obj('reinforcement_learning/test.obj')
        self.component_1 = OBJ_loader.component("reinforcement_learning/test.obj")
        self.components = [self.component_1]
        self.vao = QOpenGLVertexArrayObject()  # Initialize VAO
        self.vbo = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)  # Initialize VBO
        self.ebo = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)  # Initialize EBO (Index Buffer)
        self.current_VBO_size = None
        self.current_EBO_size = None
        self.current_new_vertex_offset = 0
        self.current_new_index_offset = 0
        
    def initializeGL(self):
        print("Initializing OpenGL...")  
        try:
            glClearColor(0.0, 0.0, 0.0, 1.0)
            glEnable(GL_DEPTH_TEST)

            for component in self.components:
                for body in component.bodies:

                    body.vao.create()
                    body.vao.bind()

                    body.vbo.create()
                    body.vbo.bind()
                    body.vbo.allocate(body.get_vertices().nbytes)
                    body.vbo.allocate(body.get_vertices(),body.get_vertices().nbytes)
                    #body.vbo.write(0,body.get_vertices(),body.get_vertices.nbytes)

                    body.ebo.create()
                    body.ebo.bind()
                    body.ebo.allocate(body.get_indices(),body.get_indices().nbytes)
                    #body.ebo.write(0,body.get_indices())

                    glEnableClientState(GL_VERTEX_ARRAY)
                    glVertexPointer(3,GL_FLOAT,0,None)

                    body.vao.release()
                    body.vbo.release()
                    body.ebo.release()

            # Initialize VAO
            self.vao.create()
            self.vao.bind()

            # Initialize VBO
            self.vbo.create()
            self.vbo.bind()

            # Allocate and fill VBO with vertex data
            vertex_data_size = self.component_1.bodies[0].get_vertices().nbytes  # Get size of the vertex data in bytes
            self.current_VBO_size = vertex_data_size*10+(vertex_data_size*10) % 512
            self.vbo.allocate(self.current_VBO_size)

            # Initialize EBO
            self.ebo.create()
            self.ebo.bind()

            # Allocate and fill EBO with index data
            index_data_size = self.component_1.bodies[0].get_indices().nbytes  # Get size of the index data in bytes
            self.current_EBO_size = index_data_size*10+(index_data_size*10) % 512
            self.ebo.allocate(self.current_EBO_size)

            # Enable vertex attributes (position)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, None)

            # Unbind VAO and buffers
            self.vao.release()
            self.vbo.release()
            self.ebo.release()
            
            print("OpenGL initialization complete.")  # Debugging statement
        except Exception as e:
            print("Error initializing OpenGL:", e)  # Error checking

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)  # Set the viewport to cover the whole widget
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect_ratio = w / h if h != 0 else 1
        fov_y = 45.0  # Field of view in y direction, in degrees
        near_plane = 0.1  # Near clipping plane
        far_plane = 100.0  # Far clipping plane
        
        glFrustum(-aspect_ratio * near_plane, aspect_ratio * near_plane, -near_plane, near_plane, near_plane, far_plane)

        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
        glLoadIdentity()  # Reset transformations

        # Apply zoom and rotations
        glTranslatef(0.0, 0.0, self.zoom)  # Move into the screen based on zoom
        glRotatef(self.x_rotation, 1.0, 0.0, 0.0)  # Rotate around the x-axis
        glRotatef(self.y_rotation, 0.0, 1.0, 0.0)  # Rotate around the y-axis

        for component in self.components:
            for body in component.bodies:
                body.vao.bind()
                glDrawElements(GL_TRIANGLES,len(body.get_indices()),GL_UNSIGNED_INT,None)
                body.vao.release()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom += delta * 0.1
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_mouse_position is not None:
            dx = event.x() - self.last_mouse_position.x()
            dy = event.y() - self.last_mouse_position.y()

            self.x_rotation += dy * 0.5
            self.y_rotation += dx * 0.5

            self.last_mouse_position = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_position = None

    def draw_grid(self):
        pass

    def add_body(self):
        
        self.vao.bind()
        
        self.vbo.bind()
        self.vbo.allocate()

        self.ebo.bind()
        self.ebo.allocate()

        self.vao.release()
        self.vbo.release()
        self.ebo.release()

        self.uppdate()

    def uppdate_body(self):
        pass

    def uppdate_vbo(self):
        pass