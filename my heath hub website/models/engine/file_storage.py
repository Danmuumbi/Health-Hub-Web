""" import json
from models.base_model import BaseModel
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication

class FileStorage:
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        ""Returns a dictionary of all objects or objects of a specific class""
        if cls:
            return {key: val for key, val in self.__objects.items() if isinstance(val, cls)}
        return self.__objects

    def new(self, obj):
        ""Adds a new object to the storage dictionary""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        ""Serializes the storage dictionary to a JSON file""
        with open(self.__file_path, 'w') as f:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, f)

    def reload(self):
        ""Deserializes the JSON file to the storage dictionary""
        try:
            with open(self.__file_path, 'r') as f:
                objects = json.load(f)
                for key, val in objects.items():
                    cls_name = val['__class__']
                    self.__objects[key] = globals()[cls_name](**val)
        except FileNotFoundError:
            pass

    def get(self, cls, id):
        ""Retrieves an object based on class and id""
        return self.__objects.get(f"{cls}.{id}")

    def delete(self, cls, id):
        ""Deletes an object based on class and id""
        key = f"{cls}.{id}"
        if key in self.__objects:
            del self.__objects[key]
            return True
        return False """
import json
from models.base_model import BaseModel
from models.patient import Patient
#from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication

class FileStorage:
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects or objects of a specific class"""
        if cls:
            return {key: val for key, val in self.__objects.items() if isinstance(val, cls)}
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serializes the storage dictionary to a JSON file"""
        with open(self.__file_path, 'w') as f:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, f)

    def reload(self):
        """Deserializes the JSON file to the storage dictionary"""
        try:
            with open(self.__file_path, 'r') as f:
                objects = json.load(f)
                for key, val in objects.items():
                    cls_name = val['__class__']
                    self.__objects[key] = globals()[cls_name](**val)
        except FileNotFoundError:
            pass

    def get(self, cls, id):
        """Retrieves an object based on class and id"""
        return self.__objects.get(f"{cls}.{id}")

    def delete(self, cls, id):
        """Deletes an object based on class and id"""
        key = f"{cls}.{id}"
        if key in self.__objects:
            del self.__objects[key]
            return True
        return False

    def classes(self):
        """Returns a dictionary mapping class names to their corresponding model classes"""
        return {
            'BaseModel': BaseModel,
            'Patient': Patient,
            #'Doctor': Doctor,
            'Appointment': Appointment,
            'Medication': Medication,
        }
