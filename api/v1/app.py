#!/usr/bin/python3
"""This module contains the root http server application"""

from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def resource_not_found(error):
    """Customer hander for page not found"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def cleanup(exception):
    """do global cleanup at the end of app context"""
    storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
