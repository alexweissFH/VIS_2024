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

        # Neues Menü für Tools erstellen
        self.tools_menu = self.menu.addMenu("Tools")

        # Regenerieren-Aktion definieren
        regenerate_action = QAction("Regenerieren", self)
        regenerate_action.triggered.connect(self.regenerate_model)

        # Aktion zum Tools-Menü hinzufügen
        self.tools_menu.addAction(regenerate_action)

         # Registeriere die Änderungserkennung für den Baum
        self.tree_model.dataChanged.connect(self.on_tree_data_changed)


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
        self.setFixedSize(geometry.width() * 0.7, geometry.height() * 0.7)

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

        # Daten holen zum einlesen des Baumes
        self.update_tree_view()  # Aufruf der Methode update_tree_view()

        #Setze das Dock im Tree
        Qdock_widget.setWidget(tree_widget)

        return Qdock_widget
    def update_tree_view(self, file_name="Kategorie"):
        """Aktualisiert den Strukturbaum basierend auf dem geladenen Modell."""
        self.tree_model.clear()
        self.tree_model.setHorizontalHeaderLabels(["Parameter", "Wert"])  # Korrekt setzen!

        menu_category = QStandardItem(file_name)
        menu_category.setEditable(False)
        self.tree_model.appendRow(menu_category)

        menu_rigid_bodies = QStandardItem("Rigid Bodies")
        menu_rigid_bodies.setEditable(False)

        menu_constraints = QStandardItem("Constraints")
        menu_constraints.setEditable(False)

        menu_forces = QStandardItem("Forces")
        menu_forces.setEditable(False)

        menu_measures = QStandardItem("Measures")
        menu_measures.setEditable(False)

        for obj in self.model.get_mbsObjectList():
            obj_type, sub_type = self.model.get_object_type_and_name(obj)

            item_name = obj.parameter.get("name", {}).get("value", "Unbekannter Name")
            item_type = obj_type

            if isinstance(obj, object):
                item_name = str(item_name)

            item = QStandardItem(f"{item_name}")
            item.setEditable(True)

            # Holen der Parameter mit der neuen Methode
            parameters = self.model.get_object_parameters(obj, obj_type)

            if not parameters:
                parameters = {"Standard-Parameter": "Kein Wert"}

            for param_name, param_value in parameters.items():
                param_name_item = QStandardItem(param_name)
                param_name_item.setEditable(False)

                param_value_item = QStandardItem(str(param_value))
                param_value_item.setEditable(True)

                item.appendRow([param_name_item, param_value_item])

            # Objekte nach Typ sortieren
            if obj_type == "Body":
                menu_rigid_bodies.appendRow(item)
            elif obj_type == "Constraint":
                menu_constraints.appendRow(item)
            elif obj_type == "Force":
                menu_forces.appendRow(item)
            elif obj_type == "Measure":
                menu_measures.appendRow(item)

        menu_category.appendRow(menu_rigid_bodies)
        menu_category.appendRow(menu_constraints)
        menu_category.appendRow(menu_forces)
        menu_category.appendRow(menu_measures)

        # Baum erweitern
        self.tree_view.expandAll()


    def on_tree_data_changed(self, top_left, bottom_right):
        """Verarbeitet Änderungen in den Baumparametern und aktualisiert das Modell."""
        if top_left.row() == bottom_right.row() and top_left.column() == bottom_right.column():
            try:
                # Geänderten Wert abrufen
                item = self.tree_model.itemFromIndex(top_left)
                new_value = item.text()
                print(f"Geändertes Feld: Zeile={top_left.row()}, Spalte={top_left.column()}, Neuer Wert={new_value}")

                # Objektname (z. B. new_body_0) finden
                object_item = item
                while object_item.parent() and object_item.parent().text().strip().lower() != "rigid bodies":
                    object_item = object_item.parent()

                if not object_item.parent() or object_item.parent().text().strip().lower() != "rigid bodies":
                    print("Fehler: Das Objekt gehört nicht zu 'Rigid Bodies'.")
                    return

                object_name = object_item.text().strip()
                print(f"Erkanntes Objekt: {object_name}")

                # Zeilen (Parameter) basierend auf der Reihenfolge zuordnen
                row_to_param = {
                    2: "position",  # Zeile 2 für Position
                    3: "x_axis",    # Zeile 3 für X-Achse
                    4: "y_axis",    # Zeile 4 für Y-Achse
                    5: "z_axis"     # Zeile 5 für Z-Achse
                }

                # Den Parameter bestimmen
                param_name = row_to_param.get(top_left.row(), None)
                if not param_name:
                    print(f"Zeile {top_left.row()} hat keinen zugeordneten Parameter. Änderung wird ignoriert.")
                    return

                print(f"Erkannter Parameter: {param_name}")

                # Suche das entsprechende Objekt im Modell
                object_found = False
                for obj in self.model.get_mbsObjectList():
                    model_object_name = obj.parameter.get("name", {}).get("value", "").strip()
                    print(f"Vergleiche Baum-Objekt '{object_name}' mit Modell-Objekt '{model_object_name}'")

                    if model_object_name.lower() == object_name.lower():
                        print(f"Objekt {object_name} im Modell gefunden. Aktualisiere Parameter {param_name}...")

                        # Aktualisiere den Parameter
                        try:
                            if param_name == "position":
                                # Für 'position' wird der Wert als Liste gespeichert
                                vectorText = new_value.strip("[]")  # Entfernt die eckigen Klammern
                                obj.parameter[param_name]["value"] = list(map(float, vectorText.split(',')))  # Wandelt den String in eine Liste von Fließkommazahlen um
                            else:
                                # Für andere Parameter wird der Wert als float gesetzt
                                obj.parameter[param_name]["value"] = float(new_value)

                            print(f"Parameter {param_name} erfolgreich auf {new_value} gesetzt.")
                        except Exception as e:
                            print(f"Fehler beim Setzen von {param_name}: {str(e)}")
                        object_found = True
                        break

                if not object_found:
                    print(f"Fehler: Objekt {object_name} nicht im Modell gefunden!")

            except Exception as e:
                print(f"Fehler beim Verarbeiten der Änderung: {str(e)}")


    def regenerate_model(self):
        """Regeneriert das Modell und aktualisiert nur die Parameter 'position', 'x_axis', 'y_axis', 'z_axis'."""
        try:
            print("Start der Regenerierung des Modells...")
            
            # Durch alle Objekte im Modell iterieren
            for obj in self.model.get_mbsObjectList():
                obj_name = obj.parameter.get("name", {}).get("value", "").strip()
                print(f"Überprüfe Objekt: {obj_name}")

                # Durch die Baumstruktur iterieren
                for row in range(self.tree_model.rowCount()):
                    tree_item = self.tree_model.item(row, 0)
                    tree_name = tree_item.text().strip()

                    print(f"Vergleiche Baumobjekt '{tree_name}' mit Modellobjekt '{obj_name}'")

                    if tree_name.lower() == obj_name.lower():
                        print(f"Objekt '{obj_name}' gefunden. Aktualisiere Parameter...")

                        # Aktualisiere 'position'
                        position_item = tree_item.child(1, 1)
                        if position_item:
                            position_value = position_item.text()
                            try:
                                obj.parameter["position"]["value"] = [float(x) for x in position_value.split(",")]
                                print(f"Position für '{obj_name}' aktualisiert auf {position_value}")
                            except ValueError:
                                print(f"Fehler bei der Konvertierung von 'position': {position_value}")

                        # Aktualisiere 'x_axis', 'y_axis', 'z_axis'
                        for axis in ['x_axis', 'y_axis', 'z_axis']:
                            axis_item = tree_item.child(axis, 1)  # Nimm die entsprechende Spalte für Achsenwerte
                            if axis_item:
                                axis_value = axis_item.text()
                                try:
                                    obj.parameter[axis]["value"] = float(axis_value)
                                    print(f"{axis} für '{obj_name}' aktualisiert auf {axis_value}")
                                except ValueError:
                                    print(f"Fehler bei der Konvertierung von {axis}: {axis_value}")
            
            print("Aktualisiere den Renderer...")
            self.centralWidget().update_renderer(self.model)
            print("Modell erfolgreich regeneriert!")
        except Exception as e:
            print(f"Fehler beim Regenerieren des Modells: {str(e)}")