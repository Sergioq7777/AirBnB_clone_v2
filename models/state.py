#!/usr/bin/python3
"""This is the state class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128),
                      nullable=False)
        cities = relationship("City",
                              cascade="all")

    else:
        name = ""

        @property
        def cities(self):
            ''' Returns list of city instances '''
            results = models.storage.all(models.City)
            city_list = []
            for v in results.values():
                if v.state_id == self.id:
                    city_list.append(v)
            return city_list