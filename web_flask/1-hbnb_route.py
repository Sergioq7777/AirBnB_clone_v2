#!/usr/bin/python3
'''Another simple flask web app'''
from flask import Flask
app = Flask('web_flask')


@app.route('/', strict_slashes=False)
def hello_route1():
    """Says 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hello_route2():
    """Return 'HBNB'"""
    return 'HBNB'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
