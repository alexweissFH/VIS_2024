# Aufgabe 2: Darstellen eines MKS Modells

## Ziel
Arbeiten mit VTK, CAD file reader und eingebauten Geometriequellen, Transformationen.

## Aufgabe

1. **Verwenden Sie die Klassen aus /VIS_2024/inputfilereader (`mbsObject`)**
   - Importieren Sie die Klasse `mbsObject`, die Sie in Aufgabe 2 erstellt haben.

2. **Modularisieren Sie den `inputFileReader`**
   - Erweitern Sie `inputFileReader` so, dass er als Modul verwendet werden kann (`import inputFileReader`).

3. **Erweitern Sie die Klassen `mbsObject` (Konstruktor)**:
   - **Bodies**: Fügen Sie VTK-Objekte zur Darstellung der Geometrie hinzu (z. B. OBJ-Dateien).
   - **Constraints**: Fügen Sie Darstellungen oder `Actor(s)` für die Zwangsbedingungen hinzu.
   - **Forces**: Erstellen Sie geeignete Darstellungen:
     - *Gravity*: Darstellung als Pfeil.
     - *GenericTorque*: Darstellung des Drehmoments (im Schwerpunkt des Körpers, an dem es angreift).
   - **Measures**: Erweitern Sie diese um geeignete Darstellungen.

4. **`show()` Methode für `mbsObject` hinzufügen**
   - Erweitern Sie die Mutterklasse `mbsObject`, indem Sie eine Methode `show()` zum Anzeigen der Eigenschaften (`Props`) hinzufügen.

5. **Erstellen Sie `mbsModel.py`**
   - Dieses Skript implementiert die Klasse `mbsModel`, welche eine Liste mit Objekten der Klasse `mbsObject` enthält und so ein gesamtes Modell beschreibt.
   - Überlegen Sie, wie vom `inputfilereader` gelesene Elemente in `mbsModel` verwalten werden können.

6. **Erstellen Sie `main.py`**
   - Schreiben Sie ein Skript, in dem `inputfilereader` aufgerufen wird und alle Objekte in `mbsModel` in einem vtkRenderWindow angezeigt werden. `main.py` soll mit dem Pfad zu einem Inputfile als Argument aufgerufen werden können.

---

## Hinweise
- Verwenden Sie **VTK** zur Darstellung und Transformation der Geometrie und der physischen Eigenschaften (Kräfte, Drehmomente etc.).
- Überlegen Sie, wie die verschiedenen Komponenten eines MKS-Modells (Körper, Zwänge, Kräfte, Messungen) visuell dargestellt werden können, um die Simulation nachvollziehbar zu machen.


---

## Abgabe
- Bis 26.11.2024 vor Lehrveranstaltung per Pull-Request

---

## Beispiel für den Aufruf von `main.py`
```bash
python main.py /path/to/your/inputfile
