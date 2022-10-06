#!/usr/bin/env python

from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"name": "john", "email": "john.doe@gmail.com"})


app.run(debug=True)
