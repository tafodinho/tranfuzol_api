# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.auth.views import auth_blueprint
from project.server.api.donor import donor_blueprint
from project.server.api.subscriber import subscriber_blueprint
from project.server.api.hospital import hospital_blueprint
from project.server.api.transfusion import transfusion_blueprint
from project.server.api.donation import donation_blueprint
from project.server.api.deferral import deferral_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(donor_blueprint)
app.register_blueprint(subscriber_blueprint)
app.register_blueprint(hospital_blueprint)
app.register_blueprint(transfusion_blueprint)
app.register_blueprint(donation_blueprint)
app.register_blueprint(deferral_blueprint)