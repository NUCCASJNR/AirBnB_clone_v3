#!/usr/bin/python3

"""
contains the end route status
"""

from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def show_status():
    """
    shows the status
    """
    return jsonify({"status": "OK"})
