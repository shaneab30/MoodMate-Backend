from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from model.users import Users
import bcrypt

modelUsers = Users()

class LoginController(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        result = modelUsers.findUserByUsername(username)
        user = result.get('data')

        if not user:
            return {"status": False, 'message': 'Invalid credentials'}, 401

        stored_hashed_password = user.get('password', '').encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
            return {"status": False, 'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=str(user['_id']))
        return {"status": True, 'access_token': access_token}, 200

    
