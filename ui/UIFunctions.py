from box import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLShaderProgram
from PyQt5.QtCore import Qt
from OpenGL.GL import *
import sys
import numpy as np 
from PyQt5.QtWidgets import QMainWindow,QFileDialog

class eventHandeler(QMainWindow):    
    def __init__(self,ui,componentManager,qtWidget):
        super().__init__()
        self.ui = ui
        self.componentManager = componentManager
        self.qtWidget = qtWidget
        self.set_up()

    def set_up(self):

        #
        self.ui.checkBox.stateChanged.connect(self.on_checkBox_stateChanged)

        self.ui.actionLoad_object.triggered.connect(self.on_click)


    def on_click(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select OBJ File", "", "OBJ Files (*.obj);;All Files (*)", options=options)

        if file_name:
            print(f"Selected file: {file_name}")
            self.componentManager.load_component(file_name) 

    def on_checkBox_stateChanged(self):
        if self.ui.checkBox.isChecked():
            print("ja")
        else:
            print("noo")