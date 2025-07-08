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

UPLOAD_FOLDER = "uploads/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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

    @jwt_required()
    def post(self, userId=None):
        if request.path.endswith('/profile-picture'):
            image = request.files.get('profilePicture')

            if not image:
                return {'status': False, 'message': 'No image provided'}, 400
            
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)

                try:
                    image.save(image_path)
                    update_result = modelUsers.uploadProfilePicture(userId, {'profilePicture': image_path})
                    return update_result, 200 if update_result.get('status') else 400
                except Exception as e:
                    return {'status': False, 'message': str(e)}, 500
            
            return {'status': False, 'message': 'Invalid image file type'}, 400
        
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
        resultUpdate = modelUsers.updateUser(userId, data)
        
        if resultUpdate.get('status') == True:
            return resultUpdate, 200
        else:
            return resultUpdate, 400
