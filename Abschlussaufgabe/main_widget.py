# main_widget.py
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Widget(QWidget):
    def __init__(self, model):
        super().__init__()

        # VTK Renderer Setup
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(self.renderer)

        # Strukturbaum erstellen
        self.tree_view = QTreeView(self)
        self.tree_model = QStandardItemModel(self)
        self.tree_model.setHorizontalHeaderLabels(["Name", "Type"])
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setHeaderHidden(False)

        # Layout Setup
        layout = QHBoxLayout()
        layout.addWidget(self.tree_view, 2)  # Der Baum erhält 2 Teile des Platzes
        layout.addWidget(self.vtk_widget, 8)  # Der VTK-Renderer erhält 8 Teile des Platzes
        self.setLayout(layout)

    def update_renderer(self, model):
        """Aktualisiert den Renderer und die Baumstruktur."""
        # Aktualisiere den VTK-Renderer
        model.showModel(self.renderer)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

        # Aktualisiere den Strukturbaum
        self.update_tree_view(model)

    def update_tree_view(self, model):
        """Aktualisiert den Strukturbaum basierend auf dem Modell."""
        self.tree_model.clear()  # Entferne vorherige Daten
        self.tree_model.setHorizontalHeaderLabels(["Name", "Type"])

        for obj in model.getObjects():
            item_name = QStandardItem(obj.name)
            item_type = QStandardItem(obj.type)
            self.tree_model.appendRow([item_name, item_type])