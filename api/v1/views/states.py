#!/usr/bin/python3
"""This module contains the view functions that handle all request
   on State resource
"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=["GET", "POST"])
def States():
    """retrieve all states"""
    if request.method == 'GET':
        allStates = [s.to_dict() for s in storage.all("State").values()]
        return jsonify(allStates)

    if request.method == 'POST':
        if not request.is_json:
            abort(400, description="Not a JSON")
        data = request.get_json()
        if "name" not in data:
            abort(400, description="missing name")
        else:
            new_state = State(**data)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<uuid:state_id>',
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def UniqueState(state_id):
    """Get the state with the specified id"""
    target_state = storage.get(State, state_id)
    if request.method == "GET":
        if target_state:
            return jsonify(target_state.to_dict()), 200
        abort(404)

    if request.method == "DELETE":
        if target_state is None:
            abort(404)
        target_state.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == "PUT":
        if target_state is None:
            abort(404)
        if not request.is_json:
            abort(400, description="Not a JSON")
        data = request.get_json()
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(target_state, k, v)
        target_state.save()
        return jsonify(target_state.to_dict()), 200
