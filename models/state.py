#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
import uuid


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City",
                              cascade="all, delete-orphan",
                              backref="state")
    else:
        name = ""

    @property
    def cities(self):
        """returns the list of City instances with
        state_id equals to the current State.id"""
        if getenv("HBNB_TYPE_STORAGE") != "db":
            import models
            from models.city import City
            list_city = []

            cities = models.storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    list_city.append(city)
            return list_city
    @property
        def cities(self):
            """update"""
            citiesList = []
            citiesAll = storage.all(City)
            for city in citiesAll.values():
                if city.state_id == self.id:
                    citiesList.append(city)
            return citiesList
