from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
from model.users import Users

modelUsers = Users()

UPLOAD_FOLDER = "uploads/profile_pictures"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class UserProfilePictureController(Resource):
    @jwt_required()
    def post(self, userId):
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
