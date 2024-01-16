#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns the list of objects of one type of class"""
        if cls:
            my_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    my_dict[key] = value
            return my_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            for key, val in self.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            from models import classes
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    class_name = val['__class__']
                    model_class = classes.get(class_name)
                    if model_class:
                        key = "{}.{}".format(class_name, val['id'])
                        self.__objects[key] = model_class(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Public instance method to delete obj from __objects
        if obj is equal to None, do nothing"""
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
            self.save()
