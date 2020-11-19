# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect
import datetime

from project.server import bcrypt, db
from project.server.models.Donor import Donor
from project.server.models.Transfusion import Transfusion
from project.server.models.User import User

transfusion_blueprint = Blueprint('transfusions', __name__)

class TransfusionAPI(MethodView):
    """
    Transfusion resource
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
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            print("AUTH", resp)
            if not isinstance(resp, str):
                trans_arr = []
                transfusions = Transfusion.query.all()
                for i in range(len(transfusions)):
                    trans_arr.append(transfusions[i]._return_data())

                responseObject = {
                    'status': 'success',
                    'data': trans_arr
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

    def delete(self):
       """ delete goes here """

class TransfusionItemAPI(MethodView):
    """
    Transfusion Item Resource
    """

    def post(self):
        """ post an item here """

        # check if user already exists
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.json
        print("JSON DATA", post_data)
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                mc = ', '.join([obj['value'] for obj in post_data["medical_conditions"]])
                transfusion = Transfusion()
                transfusion.hospital_id = post_data["hospital_id"]
                transfusion.subscriber_id = post_data["subscriber_id"]["value"]
                transfusion.hosp_unit = post_data["hosp_unit"]
                transfusion.medical_conditions = mc
                transfusion.hem_level = post_data["hem_level"]
                transfusion.bp_requested = post_data["bp_requested"]
                transfusion.bp_received = post_data["bp_received"]
                transfusion.ubpt = post_data["ubpt"]
                transfusion.id_ut = post_data["id_ut"]
                transfusion.onset_time = datetime.datetime.strptime(post_data["onset_time"], '%H:%M')
                transfusion.termination_time = datetime.datetime.strptime(post_data["termination_time"], '%H:%M')
                transfusion.effect_of_transfusion = post_data["effect_of_transfusion"]
                transfusion.date_requested = post_data["date_requested"]
                transfusion.date_delivered = post_data["date_delivered"]
                transfusion.patient_end_status = post_data["patients_end_status"]
                transfusion.diagnosis = post_data["diagnosis"]

                db.session.add(transfusion)
                db.session.commit()
                data = transfusion._return_data()
                responseObject = {
                    'status': 'success',
                    'data': data
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
        
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
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                transfusion = Transfusion().query.filter(Transfusion.c.id == post_data['id']).first()
                if transfusion:
                    responseObject = {
                        'status': 'success',
                        'message': 'transfusion found',
                        'data': transfusion._return_data()
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'transfusion not found'
                    }
                    return make_response(jsonify(responseObject)), 402
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

    def put(self):
        """ put an item here """

        # check if user already exists
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.json
        print("JSON DATA", post_data)
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                transfusion = Transfusion.query.filter_by(id=post_data['id']).first()

                transfusion.hospital_id = post_data["hospital_id"]
                transfusion.subscriber_id = post_data["subscriber_id"]
                transfusion.hosp_unit = post_data["hosp_unit"]
                transfusion.medical_condition = post_data["medical_conditions"]
                transfusion.hem_level = post_data["hem_level"]
                transfusion.bp_requested = post_data["bp_requested"]
                transfusion.bp_received = post_data["bp_received"]
                transfusion.ubpt = post_data["ubpt"]
                transfusion.id_ut = post_data["id_ut"]
                transfusion.onset_time = post_data["onset_time"]
                transfusion.termination_time = post_data["termination_time"]
                transfusion.effect_of_transfusion = post_data["effect_of_transfusion"]
                transfusion.date_requested = post_data["date_requested"]
                transfusion.date_delivered = post_data["date_delivered"]
                transfusion.patient_end_status = post_data["patient_end_status"]
                transfusion.diagnosis = post_data["diagnosis"] 

                db.session.add(transfusion)
                db.session.commit()
                data = transfusion._return_data()
                responseObject = {
                    'status': 'success',
                    'data': data
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
    def patch(self):
        """ update an item here """
    def delete(self):
        """ delete an item here """
         # check if user already exists
        auth_header = request.headers.get('Authorization')
        # get the post data
        post_data = request.json
        print("JSON DATA", post_data)
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:

                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                transfusion = Transfusion.query.filter_by(id=post_data['id']).first()
                db.session.delete(transfusion)
                db.session.commit()
            
                responseObject = {
                    'status': 'success',
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

# define the API resources
transfusions_api = TransfusionAPI.as_view('transfusions_api')
transfusion_item_api = TransfusionItemAPI.as_view('transfusions_item_api')

# add Rules for API Endpoints
transfusion_blueprint.add_url_rule(
    '/api/transfusions',
    view_func=transfusions_api,
    methods=['GET', 'DELETE']
)

transfusion_blueprint.add_url_rule(
    '/api/transfusion_item',
    view_func=transfusion_item_api,
    methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
)