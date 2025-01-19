# main.py
from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLineEdit
from PySide6.QtGui import QIcon
from main_window import MainWindow
from main_widget import Widget

import mbsModel
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera


# Qt Application
app = QApplication(sys.argv)

# Erstelle das Modell
newModel = mbsModel.mbsModel()

# Erstelle das zentrale Widget (mit VTK-Renderer)
widget = Widget(newModel)  # Übergibt das Modell an das Widget

# Erstelle das Hauptfenster mit Statusleiste und Menüs
window = MainWindow(widget)
window.show()

# Start des Qt-Event-Loops
sys.exit(app.exec())

#C:\Users\alexa/AppData/Local/Programs/Python/Python313/python.exe "QT_Tutorial/main.py" -f "QT_Tutorial/all_day.csv" unten im powershell eingeben
#C:\Users\alexa/AppData/Local/Programs/Python/Python312/python.exe -m pip install pandas