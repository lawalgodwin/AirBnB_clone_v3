#!/usr/bin/python3
"""This module contains views that handles
   default CRUD operations on the User objects
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.get('/users', strict_slashes=False)
def GetAllUsers():
    """Retrieve all users"""
    users = storage.all("User")
    all_users = [u.to_dict() for u in users.values()]
    return jsonify(all_users)


@app_views.get('/users/<uuid:user_id>', strict_slashes=False)
def GetUser(user_id):
    """Retrieve the user with the specified ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.delete('/users/<uuid:user_id>', strict_slashes=False)
def DeleteUser(user_id):
    """Delete the user with the specified ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.post('/users', strict_slashes=False)
def CreateUser():
    """Create new user"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.put('/users/<uuid:user_id>', strict_slashes=False)
def UpdateUser(user_id):
    """Update the user specified by the ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict())
