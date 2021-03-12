from flask import jsonify

from flaskr.api import api


@api.app_errorhandler(400)
def not_found(err=''):
    return jsonify({
        'success': False,
        'error': 400,
        'message': err or 'Bad Request'
    }), 400


@api.app_errorhandler(404)
def not_found(err=''):
    return jsonify({
        'success': False,
        'error': 404,
        'message': err or 'Not found'
    }), 404


@api.app_errorhandler(405)
def method_not_allowed(err=''):
    return jsonify({
        'success': False,
        'error': 405,
        'message': err or 'Method not allowed'
    }), 405


@api.app_errorhandler(422)
def unprocessable_entity(err=''):
    return jsonify({
        'success': False,
        'error': 422,
        'message': err or 'Unprocessable entity'
    }), 422


@api.app_errorhandler(500)
def unprocessable_entity(err=''):
    return jsonify({
        'success': False,
        'error': 500,
        'message': err or 'Server error'
    }), 500
