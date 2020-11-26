# project/server/__init__.py

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

application = Flask(__name__)
CORS(application)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
application.config.from_object(app_settings)

bcrypt = Bcrypt(application)
db = SQLAlchemy(application)

from project.server.auth.views import auth_blueprint
from project.server.api.donor import donor_blueprint
from project.server.api.subscriber import subscriber_blueprint
from project.server.api.hospital import hospital_blueprint
from project.server.api.transfusion import transfusion_blueprint
from project.server.api.donation import donation_blueprint
from project.server.api.deferral import deferral_blueprint

application.register_blueprint(auth_blueprint)
application.register_blueprint(donor_blueprint)
application.register_blueprint(subscriber_blueprint)
application.register_blueprint(hospital_blueprint)
application.register_blueprint(transfusion_blueprint)
application.register_blueprint(donation_blueprint)
application.register_blueprint(deferral_blueprint)