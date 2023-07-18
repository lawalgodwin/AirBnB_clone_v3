#!/usr/bin/python3
"""A module that contains the index view functions"""
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """returns the response status in json"""
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def counts():
    """Retrieve the count of all objects by type"""
    all_obj_stats = {
               "amenities": storage.count("Amenity"),
               "cities": storage.count("City"),
               "places": storage.count("Place"),
               "reviews": storage.count("Review"),
               "states": storage.count("State"),
               "users": storage.count("User")
              }
    return all_obj_stats
