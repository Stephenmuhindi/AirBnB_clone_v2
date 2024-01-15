#!/usr/bin/python3
"""New engine DBStorage"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage():
    """An alternative storage to JSON"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the storage system"""
        from models.base_model import Base
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries current database session"""
        import models
        class_list = []
        if cls is None:
            for key, value in models.classes.items():
                class_list.append(value)
        else:
            if cls in models.classes.values():
                class_list = [cls]
        new_dict = {}
        for search in class_list:
            try:
                saved_inst = self.__session.query(search).all()
            except:
                continue
            for instance in saved_inst:
                key = f"{instance.__class__.__name__}.{instance.id}"
                new_dict[key] = instance.to_dict()
        return new_dict

    def new(self, obj):
        '''adds the object to current db session'''
        self.__session.add(obj)

    def save(self):
        '''commits all changes of the current db session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''deletes from current db session'''
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        '''creates all tables in database'''
        from models.base_model import Base
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        ''' Closes the current session and reloads the databases '''
        self.__session.remove()