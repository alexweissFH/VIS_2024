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
        jason_path, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "JSON Files (*.json);;All Files (*)")
        if jason_path:
            if jason_path.lower().endswith(".json"):
                self.model.loadDatabase(Path(jason_path))
                newModel.loadDatabase(jason_path)
                self.centralWidget().update_renderer(self.model)
                QMessageBox.information(self, "Success", f"Database loaded successfully: {jason_path}")
            else:
                QMessageBox.warning(self, "Failed", "Failed to load the database.")
        else:
                QMessageBox.critical(self, "Error", f"Error loading database:\n{str(e)}")

    def select_and_import_fdd(self):
        """Öffnet den Dateidialog und importiert die ausgewählte FDD-Datei, konvertiert sie in JSON."""
        fddfilename, _ = QFileDialog.getOpenFileName(self, "Import Fdd File", "", "Fdd Files (*.fdd);;All Files (*)")

        if fddfilename.lower().endswith(".fdd"):
            try:
                # Importiere die FDD-Datei
                self.model.importFddFile(Path(fddfilename))

                # Konvertiere die FDD-Daten in JSON-kompatibles Format (Python-Dictionary)
                json_data = self.model.switch_to_json()

                # JSON-Daten ausgeben (optional für Debugging)
                print(json.dumps(json_data, indent=4))  # Dies zeigt die JSON-Daten im Terminal an

                # Renderer aktualisieren
                self.centralWidget().update_renderer(self.model)

                # Erfolgsmeldung
                QMessageBox.information(self, "Success", f"Fdd file imported and converted to JSON successfully: {fddfilename}")
            except Exception as e:
                # Fehlerbehandlung, wenn etwas schiefgeht
                QMessageBox.critical(self, "Error", f"An error occurred while importing and converting the Fdd file:\n{str(e)}")
        else:
            # Fehler, wenn die Datei keine FDD-Datei ist
            QMessageBox.warning(self, "Failed", "Failed to import the Fdd file.")


    def save_to_file(self):
        """Speichert die Datenbank als JSON-Datei."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Database", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
                self.model.saveDatabase(Path(file_path))
                QMessageBox.information(self, "Success", f"Database saved successfully: {file_path}")


    def export_fds_file(self):
        """Exportiert das Modell als FDS-Datei."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export FDS File", "", "FDS Files (*.fds);;All Files (*)")
        if file_path:
            try:
                self.model.exportFdsFile(Path(file_path))
                QMessageBox.information(self, "Success", f"FDS File exported successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error exporting FDS file:\n{str(e)}")