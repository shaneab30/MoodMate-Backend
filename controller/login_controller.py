from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from model.users import Users

modelUsers = Users()

class LoginController(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        result = modelUsers.findUserByUsername(username)
        user = result.get('data')

        if not user or user.get("password") != password:
            return {"status": False, 'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user['_id'])
        return {"status": True, 'access_token': access_token}, 200
    
