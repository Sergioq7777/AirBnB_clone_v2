#!/usr/bin/python3
"""This is the place class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.review import Review
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id',
                             String(60),
                             ForeignKey('places.id'),
                             nullable=False,
                             primary_key=True),
                      Column('amenity_id',
                             String(60),
                             ForeignKey('amenities.id'),
                             nullable=False,
                             primary_key=True))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
    city_id = Column(String(60),
                     ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128),
                  nullable=False)
    description = Column(String(1024),
                         nullable=True)
    number_rooms = Column(Integer,
                          nullable=False,
                          default=0)
    number_bathrooms = Column(Integer,
                              nullable=False,
                              default=0)
    max_guest = Column(Integer,
                       nullable=False,
                       default=0)
    price_by_night = Column(Integer,
                            nullable=False,
                            default=0)
    latitude = Column(Float,
                      nullable=True)
    longitude = Column(Float,
                       nullable=True)
    amenity_ids = []
    user = relationship("User", foreign_keys=[user_id])
    cities = relationship("City", foreign_keys=[city_id])
    reviews = relationship("Review", cascade="all")
    amenities = relationship("Amenity",
                             secondary="place_amenity",
                             viewonly=False)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            ''' Returns list of review instances '''
            results = models.storage.all(Review)
            review_list = []
            for review in results.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            ''' Returns list of amenity instances '''
            amenity_list = []
            results = models.storage.all(Amenity)
            for amenity in results.values():
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            ''' Appends place id for amenities '''
            if obj and isinstance(obj, Amenity):
                type(self).amenity_ids.append(obj.id)