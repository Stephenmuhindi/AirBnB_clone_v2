#!/usr/bin/python3
"""
C is fun!
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def task0():
    """
    prints hello hbnb
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def task1():
    """
    prints hbnb
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def task2(text):
    """
    prints text C is fun!
    """
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0')
