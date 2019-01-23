from flask import Flask, render_template, jsonify
from flask_restful import Api, Resource
from functools import wraps
from flask import Response
import csv
from flask_basicauth import BasicAuth

import datetime
import os

import time
from hashlib import md5

import json
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

movies = []



app = Flask(__name__)
app.secret_key = "Thanks for the semester!"
api = Api(app, prefix="/api")

#app.config['BASIC_AUTH_USERNAME'] = 'admin'
#app.config['BASIC_AUTH_PASSWORD'] = 'plaintextboo'

basic_auth = BasicAuth(app)

auth_user = [{
    "name": "admin",
    "password": generate_password_hash("plaintextboo")
}]

## Auth Decorator and Helpers
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    items = list(filter(lambda auth_user: auth_user['name'] == username and check_password_hash(auth_user['password'], password), auth_user))
    #print(items)
    return len(items) != 0
    #return username == 'admin' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
@requires_auth
def landing():
    return render_template('base.html')

## Flask Routes



## Flask-RESTful Resources and Routes

# Create Movie Collection Resource
class MovieListResource(Resource):
    def get(self):
        return jsonify(movies)


# Create Movie Item Resource
class MovieResource(Resource):
    def get(self, movie_id=None):
        movie = [m for m in movies if m["id"] == movie_id][0]
        return jsonify(movie)


api.add_resource(MovieListResource, "/movies/", endpoint="movies")
api.add_resource(MovieResource, "/movies/<int:movie_id>", endpoint="movie")

## Populate Movie List from CSV
with open("./data/bo.csv", "r") as bo:
    read_bo = csv.DictReader(bo, delimiter=",")
    for m in read_bo:
        try:
            ot = int(m["Opening Theaters"].replace(",", ""))
        except:
            ot = None
        try:
            tt = int(m["Theaters"].replace(",", ""))
        except:
            tt = None
        try:
            tg = float(m["Total Gross"].strip().replace("$", "").replace(",", ""))
        except:
            tg = None
        try:
            og = float(m["Opening"].strip().replace("$", "").replace(",", ""))
        except:
            og = None
        movies.append(
            {
                "id": int(m["ID"]),
                "title": m["Movie Title"],
                "studio": m["Studio"],
                "total_gross": tg,
                "total_theaters": tt,
                "opening_gross": og,
                "opening_theaters": ot,
            }
        )

if __name__ == "__main__":
    app.run()
