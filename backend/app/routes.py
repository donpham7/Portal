from flask import Blueprint, jsonify

main = Blueprint("main", __name__)


@main.route("/api/hello")
def hello():
    print("HERE")
    return jsonify({"message": "Hello, World!"})
