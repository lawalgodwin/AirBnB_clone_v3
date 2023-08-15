#!/usr/bin/python3
"""This module contains the views for handling
   the default RESTful operation on the Place objects
"""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from api.v1.views import app_views


@app_views.get("/cities/<uuid:city_id>/places", strict_slashes=False)
def GetAllPlaces(city_id):
    """get all places within the city specified by city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    place_objs = city.places
    places = [p.to_dict() for p in place_objs]
    return jsonify(places)


@app_views.get("/places/<uuid:place_id>", strict_slashes=False)
def GetPlace(place_id):
    """get the place specified by the ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.delete("/places/<uuid:place_id>", strict_slashes=False)
def DeletePlace(place_id):
    """delete the specified place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.post("/cities/<uuid:city_id>/places", strict_slashes=False)
def CreatePlace(city_id):
    """create a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.put("/places/<uuid:place_id>", strict_slashes=False)
def UpdatePlace(place_id):
    """update the place object specified by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())
