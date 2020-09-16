from flask import Flask
from model import db
from config import Config
import os, sys
from flask_jwt_extended import JWTManager



app = Flask(__name__)

def create_app(config_filename):
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    db.init_app(app)
    jwt = JWTManager(app)
    currentdir = os.path.dirname(os.path.realpath(__file__))
    parentdir = os.path.dirname(currentdir)
    sys.path.append(parentdir)
    return app


if __name__ == "__main__":
    app = create_app(Config)
    app.run(debug=True)