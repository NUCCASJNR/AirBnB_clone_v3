#!/usr/bin/python3
"""Review objects view"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, Place, Review, User


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Place not found, raise 404 error
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)  # Review not found, raise 404 error
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)  # Review not found, raise 404 error
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Place not found, raise 404 error
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')  # Invalid JSON, raise 400 error
    if 'user_id' not in data:
        abort(400, 'Missing user_id')  # Missing user_id, raise 400 error
    if 'text' not in data:
        abort(400, 'Missing text')  # Missing text, raise 400 error
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)  # User not found, raise 404 error
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)  # Review not found, raise 404 error
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')  # Invalid JSON, raise 400 error
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
