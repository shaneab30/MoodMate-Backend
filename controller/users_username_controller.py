from bson import ObjectId
from flask_restful import Resource, reqparse
from model.users import Users
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

modelUsers = Users()

class UsersUsernameController(Resource):
    
    def get(self, username):
        result = modelUsers.findUserByUsername(username)
        user = result.get('data')
        if user:
            filtered_data = [
                {
                    "username": user.get("username"),
                    "profilePicture": user.get("profilePicture"),
                    "age": user.get("age")
                }
                ]
            return {'status': True, 'data': filtered_data, 'message': 'User found'}, 200
        return {'status': False, 'data': None, 'message': result['message']}, 404
