#!/usr/bin/python3
'''
the wonakear
'''
import os
import models
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    '''
    state thung
    '''
    __tablename__ = 'states'
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete-orphan',
                               backref='state')
    else:
        name = ""

    if os.getenv('HBNB_TYPE_STORAGE') == 'fs':
        @property
        def cities(self):
            """
            Returns list
            """
            res = []
            city_inst = models.storage.all(models.classes['City']).values()
            for k in city_inst:
                if k.state_id == self.id:
                    res.append(k)
            return res
