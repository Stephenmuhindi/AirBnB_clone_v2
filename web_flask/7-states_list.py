#!/usr/bin/python3
"""flask web app"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    '''state list'''
    all_states = list(storage.all(State).values())
    all_states.sort(key=lambda x: x.name)
    ctxt = {
        'states': all_states
    }
    return render_template('7-states_list.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    '''close sess'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
