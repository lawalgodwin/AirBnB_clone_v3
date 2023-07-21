#!/usr/bin/python3
"""This module contains the views that handle
   the default RESTful operations on places Review objects
"""
from flask import request, abort, jsonify, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.get("/places/<uuid:place_id>/reviews", strict_slashes=False)
def GetAllReviewsAt(place_id):
    """Retrieve all the reviews about the specified place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_reviews = place.reviews
    place_reviews = [review.to_dict() for review in place_reviews]
    return make_response(jsonify(place_reviews), 200)


@app_views.get("/reviews/<uuid:review_id>", strict_slashes=False)
def GetReview(review_id):
    """Retrieve the review specided by the ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.delete("/reviews/<uuid:review_id>", strict_slashes=False)
def DeleteReview(review_id):
    """Delete the review specified by the ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.post("/places/<uuid:place_id>/reviews", strict_slashes=False)
def CreateAReview(place_id):
    """Create a review for a given place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, description="Missing text")
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.put("/reviews/<uuid:review_id>", strict_slashes=False)
def UpdateReview(review_id):
    """Update the review given by review_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict())
