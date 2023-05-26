#!/usr/bin/python3
"""Flask API app"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

# Create a CORS instance and allow all origins for now
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """Error handler for 404 not found"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage"""
    storage.close()

if __name__ == "__main__":
    """run the Flask with"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
