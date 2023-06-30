"""
    api.py
"""
import json
import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from sqlalchemy import exc

from .auth.auth import AuthError, requires_auth
from .database.models import Drink, db_drop_and_create_all, setup_db

app = Flask(__name__)
setup_db(app)
CORS(app)


# @TODO: uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# !! Running this funciton will add one
with app.app_context():
    db_drop_and_create_all()


# ROUTES
@app.route("/drinks", methods=["GET"])
def get_drinks():
    """TODO: implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks or
    appropriate status code indicating reason for failure
    """
    return "Not implemented", 200


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_details():
    """TODO: implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks or
    appropriate status code indicating reason for failure
    """
    return "Not implemented", 200


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink():
    """TODO: implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly
    created drink or appropriate status code indicating reason for failure
    """
    return "Not implemented", 200


@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(id):
    """TODO: implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated
    drink or appropriate status code indicating reason for failure
    """
    return "Not implemented", 200


@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(id):
    """TODO: implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record or
    appropriate status code indicating reason for failure
    """
    return "Not implemented", 200


@app.errorhandler(400)
def bad_request_handler():
    """bad request - 400"""
    return (
        jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request",
            }
        ),
        404,
    )


@app.errorhandler(401)
def unauthorized_handler():
    """unauthorized - 401"""
    return (
        jsonify(
            {
                "success": False,
                "error": 401,
                "message": "unauthorized",
            }
        ),
        401,
    )


@app.errorhandler(403)
def forbidden_handler():
    """forbidden - 403"""
    return (
        jsonify(
            {
                "success": False,
                "error": 403,
                "message": "forbidden",
            }
        ),
        403,
    )


@app.errorhandler(404)
def not_found_handler():
    """not found - 404"""
    return (
        jsonify(
            {
                "success": False,
                "error": 404,
                "message": "not found",
            }
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed_handler():
    """method not allowed - 405"""
    return (
        jsonify(
            {
                "success": False,
                "error": 405,
                "message": "method not allowed",
            }
        ),
        405,
    )


@app.errorhandler(415)
def unsupported_media_type_handler():
    """unsupported media type - 415"""
    return (
        jsonify(
            {
                "success": False,
                "error": 415,
                "message": "unsupported media type",
            }
        ),
        415,
    )


@app.errorhandler(422)
def unprocessable_handler():
    """unprocessable - 422"""
    return (
        jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable",
            }
        ),
        422,
    )


@app.errorhandler(500)
def internal_server_error_handler():
    """internal server error - 500"""
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "internal server error",
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
