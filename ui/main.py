from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QOpenGLBuffer, QOpenGLVertexArrayObject, QOpenGLShaderProgram
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,QFileDialog
from OpenGL.GL import *
import sys
import numpy as np 
import qlwidget 
from box import Ui_MainWindow
import OBJ_loader
import physicsEngine
#from firstUItest import Ui_MainWindow


class MainWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.component_manager = OBJ_loader.component_manager()
        self.physics_engine = physicsEngine.phyiscsEngine(self.component_manager)
        
        self.checkBox.stateChanged.connect(self.on_state_changed)
        self.actionLoad_object.triggered.connect(self.on_click)
  
        self.show()

    def on_state_changed(self):
        if self.checkBox.isChecked():
            print("ja")
        else:
            print("noo")

    def on_click(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select OBJ File", "", "OBJ Files (*.obj);;All Files (*)", options=options)

        if file_name:
            print(f"Selected file: {file_name}")
            self.component_manager.load_component(file_name)
            self.openGLWidget.init_vbo_for_body()
            print(f"Component name = {self.component_manager.components[0].componentName}")
            print(f"number of of bodies in component {len(self.component_manager.components[0].bodies)}")
            print(f"Name of first body {self.component_manager.components[0].bodies[0].name}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window_instance = MainWindow()

    sys.exit(app.exec_())


if __name__ == "__main__":
    """app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)"""
    main()

    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)

    # openglWidget = ui.openGLWidget
    # component_manager = OBJ_loader.component_manager()
    # physics_engine = physicsEngine.phyiscsEngine(component_manager)
    # eventHandeler = UIFunctions.eventHandeler(ui,component_manager,openglWidget)

    # MainWindow.show()
    # sys.exit(app.exec_())
