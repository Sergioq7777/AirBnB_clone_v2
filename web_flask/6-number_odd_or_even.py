#!/usr/bin/python3
"""Simple flask web app"""
from flask import Flask, render_template
app = Flask('web_flask')
app.url_map.strict_slashes = False


@app.route('/')
def hello_route1():
    """'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb')
def hello_route2():
    """'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>')
def hello_route3(text):
    """c/<text>"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/<text>')
@app.route('/python/', defaults={'text': 'is cool'})
def hello_route4(text):
    """Returns 'Python text'"""
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def hello_route5(n):
    """Returns number"""
    return '{:d} is a number'.format(n)


@app.route('/number_template/<int:n>')
def hello_route6(n):
    """Returns html template with number `n`"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>')
def hello_route7(n):
    """Returns rendered html and displays result in an <h1> tag"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
