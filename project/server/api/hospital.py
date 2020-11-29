# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect
import datetime
import json

from project.server import bcrypt, db
from project.server.models.Donor import Donor
from project.server.models.Hospital import Hospital
from project.server.models.User import User

hospital_blueprint = Blueprint('hospitals', __name__)

class HospitalAPI(MethodView):
    """
    Hospital resource
    """

    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(json.dumps(responseObject, default=str)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                hosp_arr = []
                hospitals = Hospital.query.all()
                for i in range(len(hospitals)):
                    hosp_arr.append(hospitals[i]._return_data())

                responseObject = {
                    'status': 'success',
                    'data': hosp_arr
                }
                return make_response(json.dumps(responseObject, default=str)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(json.dumps(responseObject, default=str)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(json.dumps(responseObject, default=str)), 401

    def delete(self):
       """ delete goes here """

class HospitalItemAPI(MethodView):
    """
    Hospital Item Resource
    """

    def post(self):
        """ post an item here """

        # check if user already exists
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.json
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(json.dumps(responseObject, default=str)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                hospital = Hospital()
                hospital.hospital_name = post_data["name"]
                hospital.city = post_data["city"]
                hospital.region = post_data["region"]
                hospital.address = post_data["address"]
                hospital.unit_blood_pile = post_data["unit_blood_pile"]
                hospital.phone1 = post_data["phone1"]
                hospital.phone2 = post_data["phone2"]

                db.session.add(hospital)
                db.session.commit()
                data = hospital._return_data()
                responseObject = {
                    'status': 'success',
                    'data': data
                }
                return make_response(json.dumps(responseObject, default=str)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(json.dumps(responseObject, default=str)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(json.dumps(responseObject, default=str)), 401
        
    def get(self):
        """ get an by id """
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.get_json()
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(json.dumps(responseObject, default=str)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                hospital = Hospital().query.filter(Hospital.c.id == post_data['id']).first()
                if hospital:
                    responseObject = {
                        'status': 'success',
                        'message': 'hospital found',
                        'data': hospital._return_data()
                    }
                    return make_response(json.dumps(responseObject, default=str)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'hospital not found'
                    }
                    return make_response(json.dumps(responseObject, default=str)), 402
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(json.dumps(responseObject, default=str)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(json.dumps(responseObject, default=str)), 401

    def put(self):
        """ put an item here """

        # check if user already exists
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.json
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(json.dumps(responseObject, default=str)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                hospital = Hospital.query.filter_by(id=post_data['id']).first()

                hospital.hospital_name = post_data["name"]
                hospital.city = post_data["city"]
                hospital.region = post_data["region"]
                hospital.address = post_data["address"]
                hospital.unit_blood_pile = post_data["unit_blood_pile"]

                db.session.add(hospital)
                db.session.commit()
                data = hospital._return_data()
                responseObject = {
                    'status': 'success',
                    'data': data
                }
                return make_response(json.dumps(responseObject, default=str)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(json.dumps(responseObject, default=str)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(json.dumps(responseObject, default=str)), 401
    def patch(self):
        """ update an item here """
    def delete(self):
        """ delete an item here """
         # check if user already exists
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.json
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(json.dumps(responseObject, default=str)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                hospital = Hospital.query.filter_by(id=post_data['id']).first()

                db.session.delete(hospital)
                db.session.commit()
            
                responseObject = {
                    'status': 'success',
                }
                return make_response(json.dumps(responseObject, default=str)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(json.dumps(responseObject, default=str)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(json.dumps(responseObject, default=str)), 401

# define the API resources
hospitals_api = HospitalAPI.as_view('hospitals_api')
hospital_item_api = HospitalItemAPI.as_view('hospitals_item_api')

# add Rules for API Endpoints
hospital_blueprint.add_url_rule(
    '/api/hospitals',
    view_func=hospitals_api,
    methods=['GET', 'DELETE']
)

hospital_blueprint.add_url_rule(
    '/api/hospital_item',
    view_func=hospital_item_api,
    methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
)