#!/usr/bin/python3
"""This is the file storage class for AirBnB"""

"""All Classes"""
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """

    # string - path to JSON file
    __file_path = "file.json"
    # empty dictionary
    __objects = {}

    def all(self, clase=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        if not clase:
            return self.__objects
        elif type(clase) == str:
            return {k: x for k, x in self.__objects.items()
                    if x.__class__.__name__ == clase}
        else:
            return {k: x for k, x in self.__objects.items()
                    if x.__class__ == clase}

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            del self.__objects[obj.__class__.__name__ + '.' + obj.id]
            self.save()
    def close(self):
        """Deserialize JSON file to objects"""
        self.reload()

