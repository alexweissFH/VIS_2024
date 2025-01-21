
import inputfilereader
import body
from body import rigidBody
import constraint
import force
import measure
import dataobject
from parameter_config import wanted_parameters
import json
import os
import mbsObject

class mbsModel:
    def __init__(self):
        self.__mbsObjectList = []
    
    def importFddFile(self,filepath):
        file_name, file_extension = os.path.splitext(filepath)

        if(file_extension == ".fdd"):
            self.__mbsObjectList = inputfilereader.readInput(filepath)
        else:
            print("Wrong file type: " + file_extension)
            return False
        
        for object in self.__mbsObjectList:
            object.setModelContext(self)

        return True
        
    def exportFdsFile(self,filepath):
        f = open(filepath,"w")
        for object in self.__mbsObjectList:
            object.writeSolverInput(f)
        f.close()
        
    def loadDatabase(self,database2Load):
        f = open(database2Load)
        data = json.load(f)
        f.close()
        for modelObject in data["modelObjects"]:
            if(modelObject["type"] == "Body" and modelObject["subtype"] == "Rigid_EulerParameter_PAI"):
                self.__mbsObjectList.append(body.rigidBody(parameter=modelObject["parameter"]))
            elif(modelObject["type"] == "Constraint" and modelObject["subtype"] == "Generic"):
                self.__mbsObjectList.append(constraint.genericConstraint(parameter=modelObject["parameter"]))
            elif(modelObject["type"] == "Force"):
                if(modelObject["subtype"] == "GenericForce"):
                    self.__mbsObjectList.append(force.genericForce(parameter=modelObject["parameter"]))
                elif(modelObject["subtype"] == "GenericTorque"):
                    self.__mbsObjectList.append(force.genericTorque(parameter=modelObject["parameter"]))
            elif(modelObject["type"] == "Measure"):
                self.__mbsObjectList.append(measure.measure(parameter=modelObject["parameter"]))
            elif(modelObject["type"] == "DataObject" and modelObject["subtype"] == "Parameter"):
                self.__mbsObjectList.append(dataobject.parameter(parameter=modelObject["parameter"]))

        return True

    def saveDatabase(self,dataBasePath):
        # Serializing json
        modelObjects = []
        for object in self.__mbsObjectList:
            modelObject = {"type": object.getType(),
                           "subtype": object.getSubType(),
                           "parameter": object.parameter}
            modelObjects.append(modelObject)
        
        jDataBase = json.dumps({"modelObjects": modelObjects})

        with open(dataBasePath, "w") as outfile:
            outfile.write(jDataBase)

    def switch_to_json(self):

        # JSON-kompatible Datenstruktur vorbereiten
        modelObjects = []
        for object in self.__mbsObjectList:
            modelObject = {"type": object.getType(),
                           "subtype": object.getSubType(),
                           "parameter": object.parameter}
            modelObjects.append(modelObject)
        
        jDataBase = json.dumps({"modelObjects": modelObjects})
        

        # Daten als Python-Dictionary zurückgeben
        return jDataBase


        
    def showModel(self, renderer):
        for object in self.__mbsObjectList:
            object.show(renderer)


    def get_mbsObjectList(self):
        return self.__mbsObjectList

    def get_object_type_and_name(self, obj):
        """Gibt den Typ und den Namen des Objekts zurück."""
        if obj in self.__mbsObjectList:
            name = obj.parameter["name"]["value"] if "name" in obj.parameter else "Unbekannter Name"
            obj_type = obj.getType() 
            return obj_type, name
        else:
            raise ValueError("Das Objekt befindet sich nicht in der mbsObjectList")
    
    def get_object_parameters(self, obj, obj_type):
        """Gibt alle Parameter für ein bestimmtes Objekt zurück, basierend auf dem Typ."""
        # Direkt auf 'parameter' zugreifen, da es bereits ein Dictionary ist
        parameters = obj.parameter  # Kein .get() hier notwendig
        
        # Wenn keine Parameter gefunden werden, gib ein leeres Dictionary zurück
        if not parameters:
            return {}
        
        # Filterung der Parameter je nach Typ
        if obj_type == "Body":
            # Beispiel für spezielle Parameter für Body-Objekte
            return {key: value["value"] for key, value in parameters.items() if key in ["mass", "COG", "position", "x_axis", "y_axis", "z_axis"]}
        elif obj_type == "Constraint":
            return {key: value["value"] for key, value in parameters.items() if key in ["body1", "body2", "position", "dx", "dy", "dz","ax", "ay", "az"]}
        elif obj_type == "Force":
            return {key: value["value"] for key, value in parameters.items() if key in ["body1", "body2", "PointOfApplication_Body1","PointOfApplication_Body2","mode","direction","ForceExpression"]}
        elif obj_type == "Measure":
            return {key: value["value"] for key, value in parameters.items() if key in ["body1", "body2", "type","component","location_body1","location_body2", "type","use_initial_value"]}
        
        # Fallback: Gebe alle Parameter zurück, wenn kein spezifischer Typ gefunden wurde
        return {key: value["value"] for key, value in parameters.items()}
    
    
    