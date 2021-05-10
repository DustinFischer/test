import json
import os

from dotenv import load_dotenv
from flask import request, jsonify, abort
from marshmallow import Schema, fields, ValidationError

from . import api
from .auth import requires_auth
from ..database.models import Drink, db_session

BASE_DIR = os.path.abspath('.')
load_dotenv(os.path.join(BASE_DIR, os.getenv('DOT_ENV', '.env')))


def validate_positive_int(n):
    if n <= 0:
        raise ValidationError("Must be greater than 0.")


class RecipeSchema(Schema):
    name = fields.String(required=True)
    color = fields.String(required=True)
    parts = fields.Int(required=True, validate=validate_positive_int)


class DrinkSchema(Schema):
    title = fields.String(required=True)
    recipe = fields.Nested(RecipeSchema, many=True, required=True)


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


@api.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(_):
    data = request.get_json()
    data.pop('id', None)

    # Validation
    try:
        schema = DrinkSchema()
        result = schema.load(data)
    except ValidationError as exc:
        abort(400, exc.messages)

    # Create the drink
    try:
        result['recipe'] = json.dumps(result['recipe'])  # JSON serialize recipe
        with db_session():
            drink = Drink(**result)
            drink.insert()
            return jsonify(drink.long())
    except:
        abort(422)


@api.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(_, drink_id):
    # Retrieve the drink, or 404 if not found
    drink = Drink.query.filter_by(id=drink_id) \
        .first_or_404('Drink not found matching ID')

    # Parse request data
    data = request.get_json()
    data.pop('id', None)

    # Validation
    try:
        schema = DrinkSchema(partial=('title', 'recipe'))
        result = schema.load(data)
    except ValidationError as exc:
        abort(400, exc.messages)

    # Update the relevant fields
    try:
        if result.get('recipe', None):
            result['recipe'] = json.dumps(result['recipe'])  # JSON serialize recipe
        with db_session():
            # Update the fields
            for key, value in result.items():
                setattr(drink, key, value)
            drink.update()
            return jsonify(drink.long())
    except:
        abort(422)


@api.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(_, drink_id):
    # Retrieve the drink, or 404 if not found
    drink = Drink.query.filter_by(id=drink_id) \
        .first_or_404('Drink not found matching ID')
    try:
        with db_session():
            drink.delete()
    except:
        abort(500)

    return jsonify({}), 204
