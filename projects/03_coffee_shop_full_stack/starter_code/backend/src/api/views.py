import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from dotenv import load_dotenv
from flask_cors import CORS

from ..database.models import Drink
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
