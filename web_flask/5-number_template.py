#!/usr/bin/python3
'''Simple flask web app'''
from flask import Flask, render_template
app = Flask('web_flask')
app.url_map.strict_slashes = False


@app.route('/')
def hello_route1():
    """Says Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hello_route2():
    """HBNB"""
    return 'HBNB'


@app.route('/c/<text>')
def hello_route3(text):
    """c/<text> from html request"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>')
@app.route('/python/', defaults={'text': 'is cool'})
def hello_route4(text):
    """python text from html request"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def hello_route5(number):
    """Number html request"""
    return '{:d} is a number'.format(number)


@app.route('/number_template/<int:n>')
def hello_route6(number):
    """Return html template containing the number `number`"""
    return render_template('5-number.html', number=number)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
