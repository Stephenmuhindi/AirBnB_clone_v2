#!/usr/bin/python3
"""manage file storage for airbnbb clone"""
import json


class FileStorage:
    """manages storage of airbnb models in JSON"""
    __file_path = 'file.json'
    __objects = {}

    @property
    def cities(self):
        """Retruns Cities in state"""

    def delete(self, obj=None):
        """
        func doc
        """
        if obj:
            id = obj.to_dict()["id"]
            className = obj.to_dict()["__class__"]
            keyName = className+"."+id
            if keyName in FileStorage.__objects:
                del (FileStorage.__objects[keyName])
                self.save()

    def all(self, cls=None):
        """Returnsmodelsge"""
        print_dict = {}
        if cls:
            className = cls.__name__
            for k, v in FileStorage.__objects.items():
                if k.split('.')[0] == className:
                    print_dict[k] = str(v)
            return print_dict
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new objec"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """json dunp"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage without circular import"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """
        the update
        """
        self.reload()
