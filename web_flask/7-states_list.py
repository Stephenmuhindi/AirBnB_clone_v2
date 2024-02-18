#!/usr/bin/python3
"""flask web app"""
from models import *
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from flask import Flask, render_template
app = Flask(__name__)
classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ display HTML"""
    states = storage.all(classes["State"]).values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def remove_SQLalc_session(exception):
    """ close sess"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
