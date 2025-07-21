from bson import ObjectId
from flask_restful import Resource, reqparse
from model.users import Users
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


modelUsers = Users()
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Parameter 'username' can not be blank")
parser.add_argument('password', type=str, required=True, help="Parameter 'password' can not be blank")
parser.add_argument('email', type=str, required=True, help="Parameter 'email' can not be blank")
parser.add_argument('age', type=str, required=True, help="Parameter 'age' can not be blank")
parser.add_argument('firstname', type=str, required=True, help="Parameter 'firstname' can not be blank")
parser.add_argument('lastname', type=str, required=True, help="Parameter 'lastname' can not be blank")

class UsersController(Resource):
    @jwt_required()
    def get(self):
        if request.path.endswith('/me'):
            userId = get_jwt_identity()
            result = modelUsers.findUserById(userId)
            if result['status']:
                return result['data'], 200
            return {'message': result['message']}, 404
        return modelUsers.findAllUsers()

    # @jwt_required()
    def post(self, userId=None):
        args = parser.parse_args()
        data = {
            'username': args['username'],
            'password': args['password'],
            'email': args['email'],
            'age': args['age'],
            'firstname': args['firstname'],
            'lastname': args['lastname']
        }
        
        # Check for existing username
        listUser = []
        try:
            users_data = modelUsers.findAllUsers()
            if users_data.get('data'):
                listUser = [user['username'] for user in users_data['data']]
        except Exception as e:
            return {"status": False, "error": str(e)}, 500

        if args['username'] in listUser:
            return {'status': False, 'data': None, 'message': 'Username sudah ada'}, 400

        resultInsert = modelUsers.insertUser(data)
        return resultInsert, 200 if resultInsert.get('status') == True else 400
    
    @jwt_required()
    def put(self,userId):
        args = parser.parse_args()
        data = {'username': args['username'], 'password': args['password'], 'email': args['email'], 'age': args['age'], 'firstname': args['firstname'], 'lastname': args['lastname']}
        
        existing_username = modelUsers.findUserByUsername(args['username'])
        if existing_username.get('status') == True and existing_username.get('data').get('_id') != userId:
            return {'status': False, 'data': None, 'message': 'Username Already Exists'}, 400
        
        existing_email = modelUsers.findUserByEmail(args['email'])
        if existing_email.get('status') == True and existing_email.get('data').get('_id') != userId:
            return {'status': False, 'data': None, 'message': 'Email Already Exists'}, 400
        
        resultUpdate = modelUsers.updateUser(userId, data)
        
        if resultUpdate.get('status') == True:
            return resultUpdate, 200
        else:
            return resultUpdate, 400
