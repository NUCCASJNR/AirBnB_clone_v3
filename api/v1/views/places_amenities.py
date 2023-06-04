#!/usr/bin/python3
"""
a new view for the link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def retrieve_amenity_using_placeid(place_id):
    """
    Retrieves all Amenity objects of a Place
    Raises a 404 error if the place_id is not linked to any Place object
    """
    amenity_list = []
    place = storage.get(Place, place_id)
    if place:
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    abort(404)
