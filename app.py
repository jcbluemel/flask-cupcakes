"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template
from models import Cupcake, db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

# debug tool bar
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#TODO: add serialize function to our cupcake model
@app.get('/api/cupcakes')
def list_cupcakes():
    # query.all all the cupcakes
    # serialize data
    #return jsonify(cupcakes=[{info}, {info}, ...])


    # desserts = Dessert.query.all()
    # serialized = [d.serialize() for d in desserts]

    # return jsonify(desserts=serialized)
    #list of somethings

    return 42


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake():

    #query.get(cupcake_id) for single cupcake
    # return jsonify(cupcake={info})

    # dessert = Dessert.query.get(dessert_id)
    # serialized = dessert.serialize()

    # return jsonify(dessert=serialized)

    #single cupcake
    return 42

@app.post('/api/cupcakes')
def create_cupcake():

    #figure out how to pass data

    # create new cupcake from body data
    return 42