from __future__ import annotations
from pathlib import Path
import json
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import mbsModel
import os
import main_widget


newModel = mbsModel.mbsModel()

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Inputfilereader")
        self.setCentralWidget(widget)
        self.setGeometry(100, 100, 1200, 900)

        # Instanz des Modells
        self.model = mbsModel.mbsModel()

        # Menü erstellen
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

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