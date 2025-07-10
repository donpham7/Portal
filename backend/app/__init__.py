from flask import Flask
from .routes import main
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
