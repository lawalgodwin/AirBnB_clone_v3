#!/usr/bin/python3
"""This module contains view for City objects that handles
   all default RESTful actions
"""
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.get('/states/<uuid:state_id>/cities', strict_slashes=False)
def GetAllCities(state_id):
    """Retrieve all states in a state with the specified ID"""
    # get the state first
    state = storage.get(State, state_id)
    if state:
        cities = state.cities
        cities = [city.to_dict() for city in cities]
        return jsonify(cities)
    abort(404)


@app_views.get('/cities/<uuid:city_id>', strict_slashes=False)
def GetCity(city_id):
    """Retieve the city with the specified ID"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.delete('/cities/<uuid:city_id>', strict_slashes=False)
def DeleteCity(city_id):
    """Delete the city with the specified ID"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.post('/states/<uuid:state_id>/cities', strict_slashes=False)
def CreateCity(state_id):
    """Create a city within the State with the specified ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict())


@app_views.put('/cities/<uuid:city_id>', strict_slashes=False)
def UpdateCity(city_id):
    """Update the city with the specified ID with new data"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if data and (data != {}):
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(city, k, v)
        city.save()
    return jsonify(city.to_dict())
