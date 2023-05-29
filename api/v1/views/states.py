#!/usr/bin/python3

"""
a new view for State objects that handles all default RESTFul API actions
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_state():
    """
    Retrieves all the states
    """

    state_list = []
    states = storage.all(State)
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)
