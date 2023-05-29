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


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def retrieve_city_using_cityid(city_id):
    """
    Retrieves a city using the city id
    returns a 404 error if the id doesn't match any city
    """

    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state_using_stateid(state_id):
    """
    Deletes a city using the city id
    Raises a 404 error If the city_id is not linked to any city object
    Returns an empty dictionary with the status code 200
    """

    city = storage.get(City, city_id)
    if state:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404)
