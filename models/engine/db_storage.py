#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with a mysql+mysqldb database
connection.
"""

import json
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """SQL DB Engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DB Engine"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        test = getenv('HBNB_MYSQL_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user,
                                             pwd,
                                             host,
                                             db),
                                      pool_pre_ping=True)
        if test == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Queries the current db session"""
        return_dict = {}
        if cls:
            query_result = []
            try:
                if isinstance(cls, str):
                    query_result = self.__session.query(eval(cls)).all()
                else:
                    query_result = self.__session.query(cls).all()
            except:
                pass
        else:
            query_result = []
            query_result += self.__session.query(State).all()
            query_result += self.__session.query(City).all()
            query_result += self.__session.query(User).all()
            query_result += self.__session.query(Place).all()
        for obj in query_result:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            return_dict[key] = obj
        return return_dict

    def new(self, obj):
        """Adds object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from current DB session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the DB"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()

    def close(self):
        """Close the current session"""
        self.__session.close()
