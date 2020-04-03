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

