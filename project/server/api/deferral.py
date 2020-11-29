# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect
import datetime
import json

from project.server import bcrypt, db
from project.server.models.Donor import Donor
from project.server.models.Deferral import Deferral
from project.server.models.User import User

deferral_blueprint = Blueprint('deferrals', __name__)

class DeferralAPI(MethodView):
    """
    Deferral resource
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
                deff_arr = []
                deferrals = Deferral.query.all()
                for i in range(len(deferrals)):
                    deff_arr.append(deferrals[i]._asdict())
                    deff_arr[i]['donor'] =  deferrals[i].donor._asdict()

                responseObject = {
                    'status': 'success',
                    'data': deff_arr
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

class DeferralItemAPI(MethodView):
    """
    Deferral Item Resource
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
                deferral = Deferral()
                deferral.donor_id = post_data["donor_id"]
                deferral.reason = post_data["reason"]
                deferral.ndefbd = post_data["ndefbd"]

                db.session.add(deferral)
                db.session.commit()
                deferral.update_donor_ndefbd()

                data = deferral._asdict()
                data['donor'] = deferral.donor._asdict()
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
                deferral = Deferral().query.filter(Deferral.c.id == post_data['id']).first()
                data = deferral._asdict()
                data['donor'] = deferral.donor._asdict()
                if deferral:
                    responseObject = {
                        'status': 'success',
                        'message': 'deferral found',
                        'data': data
                    }
                    return make_response(json.dumps(responseObject, default=str)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'deferral not found'
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
                deferral = Deferral.query.filter_by(id=post_data['id']).first()

                deferral.donor_id = post_data["donor_id"]
                deferral.reason = post_data["reason"]
                deferral.ndefbd = post_data["ndefbd"]

                db.session.add(deferral)
                db.session.commit()
                deferral.update_donor_ndefbd()

                data = deferral._asdict()
                data['donor'] = deferral.donor._asdict()
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
                deferral = Deferral.query.filter_by(id=post_data['id']).first()
                db.session.delete(deferral)
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
deferrals_api = DeferralAPI.as_view('deferrals_api')
deferral_item_api = DeferralItemAPI.as_view('deferrals_item_api')

# add Rules for API Endpoints
deferral_blueprint.add_url_rule(
    '/api/deferrals',
    view_func=deferrals_api,
    methods=['GET', 'DELETE']
)

deferral_blueprint.add_url_rule(
    '/api/deferral_item',
    view_func=deferral_item_api,
    methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
)