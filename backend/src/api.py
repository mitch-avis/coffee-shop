import json

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth
from .database.models import Drink, db_drop_and_create_all, setup_db

app = Flask(__name__)
db = setup_db(app)
CORS(app)


# uncomment the following lines to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this function will add one
with app.app_context():
    db_drop_and_create_all()


# ROUTES
@app.route("/drinks", methods=["GET"])
def get_drinks():
    """get_drinks()
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of
    drinks or appropriate status code indicating reason for failure
    """
    drinks_results = db.session.query(Drink).order_by(Drink.title).all()
    drinks = []
    for drink in drinks_results:
        drinks.append(drink.short())
    if not drinks:
        abort(404)
    return {
        "success": True,
        "drinks": drinks,
    }


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_details(payload):
    """get_drink_details()
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of
    drinks or appropriate status code indicating reason for failure
    """
    print(f"payload: {payload}")
    drinks_results = db.session.query(Drink).order_by(Drink.title).all()
    drinks = []
    for drink in drinks_results:
        drinks.append(drink.long())
    if not drinks:
        abort(404)
    return {
        "success": True,
        "drinks": drinks,
    }


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(payload):
    """create_drink()
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink is an array
    containing only the newly created drink or appropriate status code indicating reason for failure
    """
    print(f"payload: {payload}")
    body = request.get_json()
    print(f"body: {body}")
    title = body.get("title")
    recipe = body.get("recipe")
    if title is None or recipe is None:
        abort(422)
    ingredient_keys = ("name", "color", "parts")
    # Multiple recipe ingredients
    if isinstance(recipe, list):
        for ingredient in recipe:
            print(f"ingredient: {ingredient}")
            if not all(key in ingredient for key in ingredient_keys):
                abort(422)
    # Single ingredient
    elif isinstance(recipe, dict):
        print(f"ingredient: {recipe}")
        if not all(key in recipe for key in ingredient_keys):
            abort(422)
        recipe = [recipe]
    # Unknown type
    else:
        abort(422)
    try:
        new_drink = Drink(
            title=title,
            recipe=json.dumps(recipe),
        )
        new_drink.insert()
        new_drink = [new_drink.long()]
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
    return {
        "success": True,
        "drinks": new_drink,
    }


@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(payload, id):
    """update_drink()
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array
    containing only the updated drink or appropriate status code indicating reason for failure
    """
    print(f"payload: {payload}")
    drink = db.session.query(Drink).filter_by(id=id).one_or_none()
    if drink is None:
        abort(404)
    body = request.get_json()
    print(f"body: {body}")
    drink.title = body.get("title") or drink.title
    recipe = body.get("recipe")
    if recipe is not None:
        ingredient_keys = ("name", "color", "parts")
        # Multiple recipe ingredients
        if isinstance(recipe, list):
            for ingredient in recipe:
                print(f"ingredient: {ingredient}")
                if not all(key in ingredient for key in ingredient_keys):
                    abort(422)
        # Single ingredient
        elif isinstance(recipe, dict):
            print(f"ingredient: {recipe}")
            if not all(key in recipe for key in ingredient_keys):
                abort(422)
            recipe = [recipe]
        # Unknown type
        else:
            abort(422)
        drink.recipe = json.dumps(recipe)
    try:
        drink.update()
        drink = [drink.long()]
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
    return {
        "success": True,
        "drinks": drink,
    }


@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload, id):
    """delete_drink()
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the
    deleted record or appropriate status code indicating reason for failure
    """
    print(f"payload: {payload}")
    drink = db.session.query(Drink).filter_by(id=id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
    except Exception:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
    return {
        "success": True,
        "delete": id,
    }


@app.errorhandler(400)
def bad_request_handler(error):
    """bad request - 400"""
    return (
        jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request",
                "description": error.description,
            }
        ),
        404,
    )


@app.errorhandler(401)
def unauthorized_handler(error):
    """unauthorized - 401"""
    return (
        jsonify(
            {
                "success": False,
                "error": 401,
                "message": "unauthorized",
                "description": error.description,
            }
        ),
        401,
    )


@app.errorhandler(403)
def forbidden_handler(error):
    """forbidden - 403"""
    return (
        jsonify(
            {
                "success": False,
                "error": 403,
                "message": "forbidden",
                "description": error.description,
            }
        ),
        403,
    )


@app.errorhandler(404)
def not_found_handler(error):
    """not found - 404"""
    return (
        jsonify(
            {
                "success": False,
                "error": 404,
                "message": "not found",
                "description": error.description,
            }
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed_handler(error):
    """method not allowed - 405"""
    return (
        jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed",
                "description": error.description,
            }
        ),
        405,
    )


@app.errorhandler(415)
def unsupported_media_type_handler(error):
    """unsupported media type - 415"""
    return (
        jsonify(
            {
                "success": False,
                "error": 415,
                "message": "unsupported media type",
                "description": error.description,
            }
        ),
        415,
    )


@app.errorhandler(422)
def unprocessable_handler(error):
    """unprocessable - 422"""
    return (
        jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable",
                "description": error.description,
            }
        ),
        422,
    )


@app.errorhandler(500)
def internal_server_error_handler(error):
    """internal server error - 500"""
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error",
                "description": error.description,
            }
        ),
        500,
    )


@app.errorhandler(AuthError)
def auth_error_handler(error):
    """internal server error - 500"""
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error,
            }
        ),
        error.status_code,
    )
