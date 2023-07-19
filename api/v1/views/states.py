#!/usr/bin/python3
"""This module contains the view functions that handle all request
   on State resource
"""
from flask import jsonify
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def getAllStates():
    """retrieve all states"""
    allStates = [state.to_dict() for state in storage.all("State").values()]
    print(allStates)
    return jsonify(allStates)

@app_views.route('/states/<uuid:state_id>', strict_slashes=False)
def getState(state_id):
    """Get the state with the specified id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict()), 200
    return jsonify({}), 404
