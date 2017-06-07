# /api/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy



import config as api_config

app = Flask(__name__)

app_settings = api_config.AppConfig


app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


from stream_api.stream.views import stream_blueprint
app.register_blueprint(stream_blueprint)
