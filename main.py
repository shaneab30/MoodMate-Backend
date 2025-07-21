import os
from flask import Flask, json, render_template, request, jsonify
from controller.emotion_controller import EmotionController
from controller.users_username_controller import UsersUsernameController
from controller.users_profile_picture_controller import UserProfilePictureController
from ml_model.ML import predict_image
from werkzeug.utils import secure_filename
from flask_restful import Api
from flask_cors import CORS, cross_origin
from controller.users_controller import UsersController
from controller.happiness_controller import HappinessController
from flask import send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from controller.login_controller import LoginController
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from controller.articles_controller import ArticlesController

class CustomApi(Api):
    def handle_error(self, e):
        if isinstance(e, NoAuthorizationError):
            return jsonify({'status': False, 'data': None, 'message': str(e)}), 401
        elif isinstance(e, ExpiredSignatureError):
            return jsonify({'status': False, 'data': None, 'message': 'Token has expired'}), 401
        elif isinstance(e, InvalidTokenError):
            return jsonify({'status': False, 'data': None, 'message': 'Invalid token'}), 422
        # Let default handler run for other errors
        return super().handle_error(e)

app = Flask(__name__)
CORS(app)
api = CustomApi(app)

api.add_resource(UsersController, '/users', '/users/register', '/users/me', '/users/<string:userId>')
api.add_resource(EmotionController, '/emotions', '/emotions/<string:emotionId>')
api.add_resource(HappinessController, '/happiness', '/happiness/<string:emotionId>')
api.add_resource(LoginController, '/login')
api.add_resource(UserProfilePictureController, '/users/<string:userId>/profile-picture')
api.add_resource(ArticlesController, '/articles', '/articles/<string:articleId>')
api.add_resource(UsersUsernameController, '/users/username/<string:username>/')

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["JWT_SECRET_KEY"] = "5h4n3en4h5" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=3) 

jwt = JWTManager(app)

@app.errorhandler(NoAuthorizationError)
def handle_no_auth_error(error):
    return jsonify({'status': False, 'data': None, 'message': str(error)}), 401

@app.errorhandler(ExpiredSignatureError)
def handle_expired_token(e):
    return jsonify({'status': False, 'data': None, "message": "Token has expired"}), 401

@app.errorhandler(InvalidTokenError)
def handle_invalid_token(e):
    return jsonify({'status': False, 'data': None, "message": "Invalid token"}), 422


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@jwt_required
@app.route('/upload', methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        try:
            file.save(file_path)
            label = predict_image(file_path)
            return jsonify({"message": "File successfully uploaded", "filename": filename, "label": label}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "File type not allowed"}), 400

@app.route('/predict', methods=['POST'])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    return jsonify({"message": "Prediction successful"}), 200


@app.route('/uploads/profile_pictures', methods=['GET'])
@jwt_required()
def serve_profile_picture():
    filename = request.args.get("filename")
    if not filename:
        return jsonify({"error": "Missing filename"}), 400

    filename = secure_filename(filename)  # sanitize!
    filepath = os.path.join('uploads/profile_pictures', filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory('uploads/profile_pictures', filename)

@app.route('/articles/images/<path:filename>', methods=['GET'])
def serve_article_image(filename):
    filename = secure_filename(filename)  # sanitize!
    filepath = os.path.join('uploads/articles', filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory('uploads/articles', filename)

if __name__ == "__main__":
    app.run(debug=True)

