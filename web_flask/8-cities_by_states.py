#!/usr/bin/python3
"""Another simple flask web app"""
from flask import Flask, render_template
from models import storage
app = Flask('web_flask')
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def list_of_states():
    """list all the states"""
    states = storage.all('State')
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(*args, **kwargs):
    """tear down the database"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
