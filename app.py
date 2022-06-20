"""Flask app for Cupcakes"""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, jsonify
from models import Cupcake, db, connect_db, DEFAULT_IMG_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

# debug tool bar
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.get('/api/cupcakes')
def list_cupcakes():
    """ Data for all cupcakes in db.
        Return JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Data for a single cupcake based on id.
    Return JSON {'cupcake': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Create cupcake from JSON data & return it.
        Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"],
    size = request.json["size"],
    rating = request.json["rating"],
    image = request.json["image"] if request.json["image"] else None

    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image,
    )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Update cupcake from JSON data & return it.
        Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    json = request.json

    cupcake.flavor = json.get('flavor', cupcake.flavor)
    cupcake.size = json.get('size', cupcake.size)
    cupcake.rating = json.get('rating', cupcake.rating)
    image_val = json.get('image', cupcake.image)
    if image_val == "":
        cupcake.image = DEFAULT_IMG_URL
    else:
        cupcake.image = image_val


    db.session.commit()
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Delete cupcake from based on id.
        Returns {'deleted': cupcake_id}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted = cupcake_id)
