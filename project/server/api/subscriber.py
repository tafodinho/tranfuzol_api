# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect
import datetime
import json

from project.server import bcrypt, db
from project.server.models.Subscriber import Subscriber
from project.server.models.User import User

subscriber_blueprint = Blueprint('subscribers', __name__)

class SubscriberAPI(MethodView):
    """
    Subscriber resource
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
                sub_arr = []
                subscribers = Subscriber.query.all()
                for i in range(len(subscribers)):
                    sub_arr.append(subscribers[i]._return_data())
                    
                responseObject = {
                    'status': 'success',
                    'data': sub_arr
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

class SubscriberItemAPI(MethodView):
    """
    Subscriber Item Resource
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
                mc = ', '.join([obj['value'] for obj in post_data["medical_conditions"]])
                subscriber = Subscriber()

                subscriber.sn = post_data["sn"]
                subscriber.email = post_data["email"]
                subscriber.first_name = post_data["first_name"]
                subscriber.hospital_id = post_data["hospital_id"]
                subscriber.middle_name = post_data["middle_name"]
                subscriber.last_name = post_data["last_name"]
                subscriber.home_address = post_data["home_address"]
                subscriber.region = post_data["region"]
                subscriber.city = post_data["city"]
                subscriber.phone1 = post_data["phone1"]
                subscriber.phone2 = post_data["phone2"]
                subscriber.cni = post_data["cni"]
                subscriber.cni_doi = post_data["cni_doi"]
                subscriber.cni_poi = post_data["cni_poi"]
                subscriber.dob = post_data["dob"]
                subscriber.pob = post_data["pob"]
                subscriber.gender = post_data["gender"]
                subscriber.blood_group = post_data["blood_group"]
                subscriber.medical_conditions = mc
                subscriber.current_medications = post_data["current_medications"]
                subscriber.allergies = post_data["allergies"]
                subscriber.rhesus_factor = post_data["rhesus_factor"]

                db.session.add(subscriber)
                db.session.commit()
                data = subscriber._return_data()
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
                subscriber = Subscriber().query.filter(Subscriber.c.id == post_data['id']).first()
                if subscriber:
                    responseObject = {
                        'status': 'success',
                        'message': 'subscriber found',
                        'data': subscriber._return_data()
                    }
                    return make_response(json.dumps(responseObject, default=str)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'subscriber not found'
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
                subscriber = Subscriber.query.filter_by(id=post_data['id']).first()

                subscriber.sn = post_data["sn"]
                subscriber.email = post_data["email"]
                subscriber.first_name = post_data["first_name"]
                subscriber.hospital_id = post_data["hospital_id"]
                subscriber.middle_name = post_data["middle_name"]
                subscriber.last_name = post_data["last_name"]
                subscriber.home_address = post_data["home_address"]
                subscriber.region = post_data["region"]
                subscriber.city = post_data["city"]
                subscriber.phone1 = post_data["phone1"]
                subscriber.phone2 = post_data["phone2"]
                subscriber.cni = post_data["cni"]
                subscriber.cni_doi = post_data["cni_doi"]
                subscriber.cni_poi = post_data["cni_poi"]
                subscriber.dob = post_data["dob"]
                subscriber.pob = post_data["pob"]
                subscriber.gender = post_data["gender"]
                subscriber.blood_group = post_data["blood_group"]
                subscriber.medical_conditions = post_data["medical_conditions"]
                subscriber.current_medications = post_data["current_medications"]
                subscriber.allergies = post_data["allergies"]
                subscriber.rhesus_factor = post_data["rhesus_factor"]

                db.session.add(subscriber)
                db.session.commit()
                data = subscriber._return_data()
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
                subscriber = Subscriber.query.filter_by(id=post_data['id']).first()
                db.session.delete(subscriber)
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
subscribers_api = SubscriberAPI.as_view('subscribers_api')
subscriber_item_api = SubscriberItemAPI.as_view('subscribers_item_api')

# add Rules for API Endpoints
subscriber_blueprint.add_url_rule(
    '/api/subscribers',
    view_func=subscribers_api,
    methods=['GET', 'DELETE']
)

subscriber_blueprint.add_url_rule(
    '/api/subscriber_item',
    view_func=subscriber_item_api,
    methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
)