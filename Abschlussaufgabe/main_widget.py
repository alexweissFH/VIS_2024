# main_widget.py
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkRenderer
from mbsModel import mbsModel
from vtkmodules.all import vtkRenderer, vtkInteractorStyleTrackballCamera


class Widget(QWidget):
    def __init__(self, model):
        super().__init__()

        # VTK Renderer Setup
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(self.renderer)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)

    def update_renderer(self, model):
        """Aktualisiert den Renderer und die Baumstruktur."""
        #Aktualisiere den VTK-Renderer
        model.showModel(self.renderer)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

 
