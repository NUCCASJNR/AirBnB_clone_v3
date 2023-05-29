#!/usr/bin/python3

"""
a new view for City objects that handles all default RESTFul API actions
"""

from models import storage
from models.state import State
from models.city import City
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def retrieve_city_using_stateid(state_id):
    """
    Retrieves the list of all city object of a state
    Raises a 404 error if the state id isnt linked to any state
    """

    cities_list = []
    state = storage.get(State, state_id)
    if state:
        for city in state.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)
    abort(404)
