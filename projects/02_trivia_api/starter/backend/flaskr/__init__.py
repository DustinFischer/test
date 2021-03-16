from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from .models import setup_db


def create_app(config_class=None):
    # create and configure the app
    app = Flask(__name__)
    # Configure the app
    app.config.from_object(config_class or Config)
    # Setup the db
    setup_db(app)

    # Register app blueprints
    from flaskr.api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Add CORS protection to api endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Welcome to Trivia!'

    @app.route('/api/')
    def api_index():
        """List api endpoints and their allowed methods."""
        routes = []
        for _route in app.url_map.iter_rules():
            if str(_route).startswith('/api'):
                routes.append(f"{_route.rule}: {_route.methods}")

        return jsonify({
            'endpoints': [routes]
        })

    return app
