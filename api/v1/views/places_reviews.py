#!/usr/bin/python3

"""
a new view for Review object that handles all default RESTFul API actions
"""

from models import storage
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from flask import jsonify, abort, make_response


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def retrieve_review_uisng_placeid(place_id):
    """
    retrieves all review objects of a place
    raises a 404 error if the place_id isnt linked to any place
    """

    review_list = []
    place = storage.get(Place, place_id)
    if place:
        for reviewid in place.reviews:
            review_list.append(reviewid.to_dict())
        return jsonify(review_list)
    abort(404)
