# main_widget.py
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkActor
from mbsModel import mbsModel
from vtkmodules.all import vtkRenderer, vtkInteractorStyleTrackballCamera
import main_window


class Widget(QWidget):
    def __init__(self, model):
        super().__init__()

        # VTK Renderer Setup
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtkRenderer()
        #self.renderer.SetBackground(1.0, 1.0, 1.0)
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(self.renderer)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)

    def GetRenderer(self):
        """Gibt den Renderer zurück."""
        return self.renderer

    
    def update_renderer(self, model):
        """Aktualisiert den Renderer mit dem Modell."""
        try:
            # Vorher das alte Modell löschen
            self.clear_renderer()

            # Jetzt das neue Modell anzeigen
            model.showModel(self.renderer)  # Das Modell neu im Renderer anzeigen
            self.renderer.ResetCamera()  # Kamera zurücksetzen
            self.vtk_widget.GetRenderWindow().Render()  # Rendern
        except Exception as e:
            print(f"Fehler beim Aktualisieren des Renderers: {str(e)}")

    #Funktioniert nicht richtig. Wird eigentlich über das "mbsModel" richtig gemacht
    def clear_renderer(self):
        """Versteckt alle dargestellten Objekte im Renderer."""
        try:
            # Alle Actors im Renderer entfernen
            render_window = self.vtk_widget.GetRenderWindow()
            renderer = render_window.GetRenderers().GetFirstRenderer()

            # Löschen der Actors im Renderer
            while renderer.GetActors().GetNumberOfItems() > 0:
                actor = renderer.GetActors().GetItemAsObject(0)
                renderer.RemoveActor(actor)  # Entferne den Actor
                print(f"Actor {actor} entfernt.")

            # Falls noch andere ViewProps existieren, könnten wir auch diese entfernen:
            # Clear all other props
            renderer.RemoveAllViewProps()
            print("Alle ViewProps entfernt.")

            # Renderer zurücksetzen und leeren
            renderer.ResetCamera()
            render_window.Render()
            print("Renderer erfolgreich geleert.")

        except Exception as e:
            print(f"Fehler beim Leeren des Renderers: {str(e)}")