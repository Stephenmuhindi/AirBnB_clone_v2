#!/usr/bin/python3
"""
web_flask
"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def task0():
    """
    hello hbnb
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def task1():
    """
    hbnb
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def task2(text):
    """
    c is fun
    """
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def task3(text='is cool'):
    """
    python is cool
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def task4(n):
    """
    is a number
    """
    return f"{n:d} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def task5(n):
    """
    number template
    """
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0')
