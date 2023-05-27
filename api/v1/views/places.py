#!/usr/bin/python3
"""Place objects view"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, City, Place, User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)  # City not found, raise 404 error
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Place not found, raise 404 error
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Place not found, raise 404 error
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)  # City not found, raise 404 error
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')  # Invalid JSON, raise 400 error
    if 'user_id' not in data:
        abort(400, 'Missing user_id')  # Missing user_id, raise 400 error
    if 'name' not in data:
        abort(400, 'Missing name')  # Missing name, raise 400 error
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)  # User not found, raise 404 error
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Place not found, raise 404 error
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')  # Invalid JSON, raise 400 error
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
