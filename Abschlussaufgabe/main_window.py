from __future__ import annotations
from pathlib import Path
import json
from PySide6.QtGui import QAction, QKeySequence, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDockWidget, QListView, QVBoxLayout, QWidget, QTreeView
from PySide6.QtCore import Qt
import mbsModel
import os
import main_widget


newModel = mbsModel.mbsModel()

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Darstellung eines 3D-Modells mit VTK")
        self.setCentralWidget(widget)
        self.setGeometry(100, 100, 1200, 900)

        # Zuweisen des richtigen mbsModels
        self.model = mbsModel.mbsModel()

        # Menü erstellen
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Statusleiste wird initsialisiert
        self.statusBar().showMessage("Wählen Sie ein JSON oder FDD File aus, um es zu laden und anzuzeigen")

        #Modell-Tree erstellen
        self.model_tree = self._create_model_tree()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.model_tree)


        # Menüaktionen definieren
        load_action = QAction("Load Database", self)
        import_fdd_action = QAction("Import Fdd", self)
        save_action = QAction("Save", self)
        export_fds_action = QAction("Export FDS File", self)
        exit_action = QAction("Exit", self)

        # Aktionen verbinden
        load_action.triggered.connect(self.select_and_load_database)
        import_fdd_action.triggered.connect(self.select_and_import_fdd)
        save_action.triggered.connect(self.save_to_file)
        export_fds_action.triggered.connect(self.export_fds_file)

        # Exit-Action
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Aktionen zum Menü hinzufügen
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(import_fdd_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(export_fds_action)
        self.file_menu.addAction(exit_action)

        # Statusleiste
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # Fenstergröße festlegen
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def select_and_load_database(self):
        """Lädt eine JSON-Datenbankdatei."""
        json_path, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "JSON Files (*.json);;All Files (*)")
        if json_path:
            try:
                # Datenbank ins Modell laden
                self.model.loadDatabase(Path(json_path))

                # Renderer und Baum im Widget aktualisieren
                self.centralWidget().update_renderer(self.model)
                self.update_tree_view(Path(json_path).name)


                # Erfolgsmeldung
                QMessageBox.information(self, "Success", f"Database loaded successfully: {json_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading database:\n{str(e)}")

    def select_and_import_fdd(self):
        """Importiert eine FDD-Datei und konvertiert sie in JSON."""
        fdd_path, _ = QFileDialog.getOpenFileName(self, "Import Fdd File", "", "Fdd Files (*.fdd);;All Files (*)")
        if fdd_path:
            try:
                # Importiere die FDD-Datei
                self.model.importFddFile(Path(fdd_path))

                # Renderer und Baum im Widget aktualisieren
                self.centralWidget().update_renderer(self.model)
                self.update_tree_view(Path(fdd_path).name)

                # Erfolgsmeldung
                QMessageBox.information(self, "Success", f"Fdd file imported successfully: {fdd_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error importing Fdd file:\n{str(e)}")

    def save_to_file(self):
        """Speichert die Datenbank als JSON-Datei."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Database", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            try:
                self.model.saveDatabase(Path(file_path))
                QMessageBox.information(self, "Success", f"Database saved successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving database:\n{str(e)}")

    def export_fds_file(self):
        """Exportiert das Modell als FDS-Datei."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export FDS File", "", "FDS Files (*.fds);;All Files (*)")
        if file_path:
            try:
                self.model.exportFdsFile(Path(file_path))
                QMessageBox.information(self, "Success", f"FDS File exported successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error exporting FDS file:\n{str(e)}")

    def _create_model_tree(self):
        """Erstellt das Dock-Widget für den Strukturbaum."""
        Qdock_widget = QDockWidget("Strukturbaum", self)
        Qdock_widget.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

        # Erstelle ein Widget für den Strukturbaum
        tree_widget = QWidget()
        layout = QVBoxLayout(tree_widget)

        self.tree_view = QTreeView(self)
        self.tree_model = QStandardItemModel(self)
        self.tree_view.setModel(self.tree_model)
        layout.addWidget(self.tree_view)
        
        #Daten holen zum einlesen des Baumes
        self.update_tree_view()  # Aufruf der Methode update_tree_view()

        #Setze das Dock im Tree
        Qdock_widget.setWidget(tree_widget)

        return Qdock_widget

    def update_tree_view(self, file_name="Fdd-File-Bezeichnung"):
        """Aktualisiert den Strukturbaum basierend auf dem Modell."""
        self.tree_model.clear()  # Entferne vorherige Daten
        self.tree_model.setVerticalHeaderLabels(["dkjfkj"])

        # Root-Element für die Kategorien
        menu_category = QStandardItem(file_name)
        menu_category.setEditable(False)  # Verhindert Bearbeitung des Root-Elements
        self.tree_model.appendRow(menu_category)

        # Unterkategorien hinzufügen
        menu_rigid_bodies = QStandardItem("Rigid Bodies")
        menu_rigid_bodies.setEditable(False)

        menu_constraints = QStandardItem("Constraints")
        menu_constraints.setEditable(False)

        menu_forces = QStandardItem("Forces")
        menu_forces.setEditable(False)

        menu_measures = QStandardItem("Measures")
        menu_measures.setEditable(False)

        # Schleife über alle Objekte im Modell
        for obj in self.model.get_mbsObjectList():
            obj_type, name = self.model.get_object_type_and_name(obj)
            item = QStandardItem(name)

            # Wenn der Typ des Objekts "Body" ist, dann wird es als Rigid Body hinzugefügt
            if obj_type == "Body":
                menu_rigid_bodies.appendRow(item)
            elif obj_type == "Constraint":
                menu_constraints.appendRow(item)
            elif obj_type == "Force":
                menu_forces.appendRow(item)
            elif obj_type == "Measure":
                menu_measures.appendRow(item)

        # Die Kategorien werden zum Root-Element hinzugefügt
        menu_category.appendRow(menu_rigid_bodies)
        menu_category.appendRow(menu_constraints)
        menu_category.appendRow(menu_forces)
        menu_category.appendRow(menu_measures)

        # Alle Kategorien erweitern, sodass sie aufklappbar sind
        self.tree_view.expandAll()