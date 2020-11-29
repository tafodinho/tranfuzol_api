# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect
import datetime
import json

from project.server import bcrypt, db
from project.server.models.Donor import Donor
from project.server.models.Donation import Donation
from project.server.models.User import User

donation_blueprint = Blueprint('donations', __name__)

class DonationAPI(MethodView):
    """
    Donation resource
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
                trans_arr = []
                donations = Donation.query.all()
                for i in range(len(donations)):
                    trans_arr.append(donations[i]._asdict())
                    trans_arr[i]['hospital'] = donations[i].hospital._asdict()
                    trans_arr[i]['donor'] = donations[i].donor._asdict()

                responseObject = {
                    'status': 'success',
                    'data': trans_arr
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

class DonationItemAPI(MethodView):
    """
    Donation Item Resource
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

                donation = Donation()
                donation.hospital_id = post_data["hospital_id"]
                donation.donor_id = post_data["donor_id"]
                donation.volume_of_blood = post_data["volume_of_blood"]
                donation.onset_time = post_data["onset_time"]
                donation.termination_time = post_data["termination_time"]
                donation.torfru = post_data["torfru"]
                donation.donor.update_dolbd(donation.created_at)
                
                db.session.add(donation)
                db.session.commit()
                data = donation._asdict()
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
                donation = Donation().query.filter(Donation.c.id == post_data['id']).first()
                if donation:
                    responseObject = {
                        'status': 'success',
                        'message': 'donation found',
                        'data': donation._asdict()
                    }
                    return make_response(json.dumps(responseObject, default=str)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'donation not found'
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
                donation = Donation.query.filter_by(id=post_data['id']).first()

                donation.hospital_id = post_data["hospital_id"]
                donation.donor_id = post_data["donor_id"]
                donation.volume_of_blood = post_data["volume_of_blood"]
                donation.onset_time = post_data["onset_time"]
                donation.termination_time = post_data["termination_time"]
                donation.torfru = post_data["torfru"]

                db.session.add(donation)
                db.session.commit()
                data = donation._asdict()
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
                donation = Donation.query.filter_by(id=post_data['id']).first()
                db.session.delete(donation)
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
donations_api = DonationAPI.as_view('donations_api')
donation_item_api = DonationItemAPI.as_view('donations_item_api')

# add Rules for API Endpoints
donation_blueprint.add_url_rule(
    '/api/donations',
    view_func=donations_api,
    methods=['GET', 'DELETE']
)

donation_blueprint.add_url_rule(
    '/api/donation_item',
    view_func=donation_item_api,
    methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
)