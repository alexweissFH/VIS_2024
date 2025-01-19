# main_widget.py
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow, QMenuBar, QMessageBox
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import mbsModel
from vtkmodules.all import vtkRenderer, vtkInteractorStyleTrackballCamera


class Widget(QWidget):
    def __init__(self, model):
        super().__init__()
        
        # VTK Renderer Setup
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1.,1.,1.)
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(self.renderer)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)

    def update_renderer(self, model):
        """Initialisiert das Modell und rendert es im VTK-Renderer."""
        # Zeige das Modell im Renderer
        model.showModel(self.renderer)
        
        # Kamera zurücksetzen, um die Ansicht zu optimieren
        self.renderer.ResetCamera()

        # Rendern des Fensters
        self.vtk_widget.GetRenderWindow().Render()