#!/usr/bin/python3
"""This is the user class"""
import models
from models.base_model import BaseModel
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class User(BaseModel):
    """This is the class for user
    Attributes:
        email: email address
        password: password for you login
        first_name: first name
        last_name: last name
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
