import os
import json
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from dotenv import load_dotenv
from flask_cors import CORS

from ..database.models import Drink, db_session
from .auth import AuthError, requires_auth
from . import api

BASE_DIR = os.path.abspath('.')
load_dotenv(os.path.join(BASE_DIR, os.getenv('DOT_ENV', '.env')))


@api.route('/drinks')
def drinks():
    return jsonify({
        'drinks': [drink.short() for drink in Drink.query],
        'success': True
    }), 200


@api.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail(_):
    return jsonify({
        'drinks': [drink.long() for drink in Drink.query],
        'success': True
    }), 200


def validate_required_fields(required_fields):
    errors = []
    for field, val in required_fields.items():
        if val is None:
            errors.append({field: 'Field is required'})

    if errors:
        abort(400, errors)


def validate_recipe_ingredients_list(ingredients_list):
    try:
        ingredient_fields = ('name', 'color', 'parts')
        if isinstance(ingredients_list, dict):
            ingredients_list = [ingredients_list]
        for ingredient in ingredients_list:
            for field in ingredient_fields:
                assert bool(ingredient[field])  # strings cant be empty, ints can't be 0, null
    except KeyError:
        abort(400, [{'recipe': 'One or more recipe ingredient bodies is malformed'}])
    except AssertionError:
        abort(400, [{'recipe': 'All recipe ingredient list field values must be set'}])


@api.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(_):
    data = request.get_json()

    fields = {
        'title': data.get('title') or None,
        'recipe': data.get('recipe') or None
    }

    # Validation
    validate_required_fields(fields)
    validate_recipe_ingredients_list(fields['recipe'])

    # Create the drink
    fields['recipe'] = json.dumps(fields['recipe'])  # JSON serialize recipe
    try:
        with db_session():
            drink = Drink(**fields)
            drink.insert()
            return jsonify(drink.long())
    except:
        abort(422)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
