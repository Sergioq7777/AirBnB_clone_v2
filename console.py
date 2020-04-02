#!/usr/bin/python3
"""This is the console for AirBnB"""

import cmd
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex
from shlex import split

"""All Classes"""
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """this class is entry point of the command interpreter
    """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Quit command to exit the program at end of file"""
        return True

    def emptyline(self):
        """Ignores empty spaces"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in classes:
            print("** class doesn't exist **")
            return False
        else:
            kwargs = {}
            for arg in args[1:]:
                match = re.fullmatch('(?P<key>[a-zA-Z_]\w*)=(?:',
                                     arg)
                match = match.groupdict()
                if match['string']:
                    kwargs[match['key']] = match['string'].replace('_', ' ')
                elif match['float']:
                    if match['float'] == '.':
                        continue
                    kwargs[match['key']] = float(match['float'])
                else:
                    kwargs[match['key']] = int(match['int'])

        instance = classes[args[0]](**kwargs)
        try:
            instance.save()
        except Exception as e:
            print("** could not save [{}] object **".format(args[0]))
            print(e)
            return False
        else:
            print(instance.id)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


    def do_show(self, arg):
        """Prints the string representation of an instance
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")
    
    def do_update(self, arg):
        """Updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        """
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) >= 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) >= 2:
                        if len(args) >= 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances
        Exceptions:
            NameError: when there is no object taht has the name
        """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            for value in models.storage.all().values():
                obj_list.append(str(value))
        elif args[0] in classes:
            for key in models.storage.all():
                if key.startswith(args[0]):
                    obj_list.append(str(models.storage.all()[key]))
        else:
            print("** class doesn't exist **")
            return False
        print(obj_list)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
