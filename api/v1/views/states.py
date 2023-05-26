#!/usr/bin/python3
"""HAndles all default RESTFUL API"""


import request
import json
from flask import abort, jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve the list of all state objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieve a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a State"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, "Not a JSON")
        data = request.get_json()
        ignore_keys = ["id", "created_at", "update_at"]
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
    else:
        abort(404)
