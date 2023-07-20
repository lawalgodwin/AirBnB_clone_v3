#!/usr/bin/python3
"""This module contains views that handles
   default CRUD operations on the Amenity objects
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.get('/amenities', strict_slashes=False)
def GetAllAmenities():
    """Retrieve all amenities"""
    amenities = storage.all("Amenity")
    all_amenities = [a.to_dict() for a in amenities.values()]
    return jsonify(all_amenities)


@app_views.get('/amenities/<uuid:amenity_id>', strict_slashes=False)
def GetAmenity(amenity_id):
    """Retrieve the amenity with the specified ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.delete('/amenities/<uuid:amenity_id>', strict_slashes=False)
def DeleteAmenity(amenity_id):
    """Delete the amenity with the specified ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.post('/amenities', strict_slashes=False)
def CreateAmenity():
    """Create new amenity"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.put('/amenities/<uuid:amenity_id>', strict_slashes=False)
def UpdateAmenity(amenity_id):
    """Update the amenity specified by the ID"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict())
