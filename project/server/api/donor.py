# project/server/auth/views.py
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect
import datetime

from project.server import bcrypt, db
from project.server.models.Donor import Donor
from project.server.models.User import User

donor_blueprint = Blueprint('donors', __name__)

RECEIVE_MATCH = {
    'O-': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+'], 
    'O+': ['O+', 'B+', 'A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+','AB+'],
    'A-': ['B+', 'AB+'], 
    'A+': ['A+', 'AB+'], 
    'AB-': ['AB-', 'AB+'], 
    'AB+': ['AB+']
}

class DonorAPI(MethodView):
    """
    Donor resource
    """

    def get(self):
        # get the auth token
        print(request.json)
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
                donors_arr = []
                donors = Donor.query.all()
                for i in range(len(donors)):
                    donors_arr.append(donors[i]._return_data())
                    
                responseObject = {
                    'status': 'success',
                    'data': donors_arr
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

class DonorItemAPI(MethodView):
    """
    Donor Item Resource
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
                donor = Donor()
                donor.sn = post_data["sn"]
                donor.email = post_data["email"]
                donor.hospital_id = post_data["hospital_id"]
                donor.first_name = post_data["first_name"]
                donor.middle_name = post_data["middle_name"]
                donor.last_name = post_data["last_name"]
                donor.home_address = post_data["home_address"]
                donor.city = post_data["city"]
                donor.region = post_data["region"]
                donor.phone1 = post_data["phone1"]
                donor.phone2 = post_data["phone2"]
                donor.cni = post_data["cni"]
                donor.cni_doi = post_data["cni_doi"]
                donor.cni_poi = post_data["cni_poi"]
                donor.dob = post_data["dob"]
                donor.pob = post_data["pob"]
                donor.gender = post_data["gender"]
                donor.blood_group = post_data["blood_group"]
                donor.allergies = post_data["allergies"]
                donor.rhesus_factor = post_data["rhesus_factor"]
                donor.medical_conditions = mc
                donor.current_medications = post_data["current_medications"]
                donor.dolbd = post_data["dolbd"]
                donor.referrer_id = post_data["referrer_id"]

                db.session.add(donor)
                db.session.commit()
                donor.update_ndefbd()
                donor.update_status()

                data = donor._return_data()
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
                donor = Donor().query.filter(Donor.id == post_data['id']).first()
                print(donor)
                if donor:
                    donor_data = donor._return_data()
                    responseObject = {
                        'status': 'success',
                        'message': 'donor found',
                        'data': donor_data
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'donor not found'
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
                donor = Donor.query.filter_by(id=post_data['id']).first()

                donor.sn = post_data["sn"]
                donor.email = post_data["email"]
                donor.hospital_id = post_data["hospital_id"]
                donor.first_name = post_data["first_name"]
                donor.middle_name = post_data["middle_name"]
                donor.last_name = post_data["last_name"]
                donor.home_address = post_data["home_address"]
                donor.city = post_data["city"]
                donor.region = post_data["region"]
                donor.phone1 = post_data["phone1"]
                donor.phone2 = post_data["phone2"]
                donor.cni = post_data["cni"]
                donor.cni_doi = post_data["cni_doi"]
                donor.cni_poi = post_data["cni_poi"]
                donor.dob = post_data["dob"]
                donor.pob = post_data["pob"]
                donor.gender = post_data["gender"]
                donor.blood_group = post_data["blood_group"]
                donor.allergies = post_data["allergies"]
                donor.rhesus_factor = post_data["rhesus_factor"]
                donor.medical_conditions = post_data["medical_conditions"]
                donor.current_medications = post_data["current_medications"]
                donor.dolbd = post_data["dolbd"]
                donor.referrer_id = post_data["referrer_id"]
                
                db.session.add(donor)
                db.session.commit()
                donor.update_ndefbd()
                donor.update_status()

                data = donor._return_data()
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
                donor = Donor.query.filter_by(id=post_data['id']).first()
                db.session.delete(donor)
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
donors_api = DonorAPI.as_view('donors_api')
donor_item_api = DonorItemAPI.as_view('donor_item_api')

# add Rules for API Endpoints
donor_blueprint.add_url_rule(
    '/api/donors',
    view_func=donors_api,
    methods=['GET', 'DELETE']
)

donor_blueprint.add_url_rule(
    '/api/donor_item',
    view_func=donor_item_api,
    methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE']
)