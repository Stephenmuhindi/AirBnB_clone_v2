#!/usr/bin/python3
"""
HBNB
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def task0():
    """
    prints hello HBNB
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def task1():
    """
    prints HBNB
    """
    return 'HBNB'


if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0')
