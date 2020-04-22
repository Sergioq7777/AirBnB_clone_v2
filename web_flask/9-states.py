#!/usr/bin/python3
'''Flask app to generate html list of all states from storage'''
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


def get_state_list():
    '''gets dict of states from storage'''
    storage.reload()
    return [[v.id, v.name] for v in storage.all("State").values()]


@app.route('/states', strict_slashes=False)
def states_list():
    '''list all states'''
    states = get_state_list()
    return render_template('9-states.html', states=states, cities=None)


@app.route('/states/<id>', strict_slashes=False)
def cs_by_id(id=None):
    '''list cities'''
    states = get_state_list()
    state = None
    for x in states:
        if x[0] == id:
            state = x[1]
    if state is None:
        return render_template('9-states.html', states=None)
    citiesdict = storage.all("City")
    cities = []
    for _, v in citiesdict.items():
        if v.state_id == id:
            cities.append([v.id, v.name])
    return render_template('9-states.html',
                           states=state,
                           cities=cities)


@app.teardown_appcontext
def teardown_db(exception):
    '''teardown database'''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
