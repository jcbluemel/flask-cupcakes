"""Flask app for Cupcakes"""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, jsonify
from models import Cupcake, db, connect_db, DEFAULT_IMG_URL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

# debug tool bar
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)


@app.get('/')
def cupcakes_page():
    """Show homepage with list of all cupcakes
        and form to add new cupcake.
    """

    return render_template('index.html')


@app.get('/api/cupcakes')
def list_cupcakes():
    """ Return all cupcakes in db.
        Returns JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.post('/api/cupcakes')
def create_cupcake():
    """Create cupcake from JSON & return data about it.
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

    return (jsonify(cupcake=serialized), 201)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Data for a single cupcake based on id.
    Returns JSON {'cupcake': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Update cupcake from JSON data & return updated data.
        Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    image_val = data.get('image', cupcake.image)

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
