#!/usr/bin/python3
"""
webtermis hanging
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/states_list')
def states_list():
    """
    Fucking hell
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(exc):
    """
    close sess
    """
    storage.close()

if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0')
