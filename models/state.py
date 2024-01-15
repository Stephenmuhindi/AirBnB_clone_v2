#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete-orphan", backref="state")
    else:
        name = ""

    @property
    def cities(self):
        import models
        from models.city import City
        """returns the list of City instances with
        state_id equals to the current State.id"""
        list_city = []

        cities = models.storage.all(City)
        for city in cities:
            if cities[city].state_id == self.id:
                list_city.append(cities[city])
        return list_city
