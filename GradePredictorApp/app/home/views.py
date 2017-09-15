from flask import request, abort, jsonify, url_for,render_template
from . import home
@home.route('/')
def homepage():
    return render_template('home/index.html')

