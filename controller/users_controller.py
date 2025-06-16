from bson import ObjectId
from flask_restful import Resource, reqparse
from model.users import Users
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os

modelUsers = Users()
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Parameter 'username' can not be blank")
parser.add_argument('password', type=str, required=True, help="Parameter 'password' can not be blank")
parser.add_argument('email', type=str, required=True, help="Parameter 'email' can not be blank")
parser.add_argument('age', type=str, required=True, help="Parameter 'age' can not be blank")
parser.add_argument('firstname', type=str, required=True, help="Parameter 'firstname' can not be blank")
parser.add_argument('lastname', type=str, required=True, help="Parameter 'lastname' can not be blank")

UPLOAD_FOLDER = "uploads/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class UsersController(Resource):
    def get(self):
        return modelUsers.findAllUsers()

    def post(self):
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
        
    def put(self,userId):
        args = parser.parse_args()
        data = {'username': args['username'], 'password': args['password'], 'email': args['email'], 'age': args['age'], 'firstname': args['firstname'], 'lastname': args['lastname']}
        resultUpdate = modelUsers.updateUser(userId, data)
        
        if resultUpdate.get('status') == True:
            return resultUpdate, 200
        else:
            return resultUpdate, 400
    
    @staticmethod
    def updateProfilePicture(user_id, filename):
        
        try:
            result = modelUsers.updateUser(
                user_id,
                {'profilePicture': filename}
            )
            
            if result.get('status') == True:
                return {
                    'status': True,
                    'message': 'Profile picture updated successfully',
                    'filePath' : filename
                }
            else:
                return {
                    'status': False,
                    'message': 'User not found or no changes made'
                }
        except Exception as e:
            return {
                'status': False,
                'message': str(e)
            }
