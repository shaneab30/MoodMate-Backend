import os
from flask import Flask, json, render_template, request, jsonify
from controller.emotion_controller import EmotionController
from ml_model.ML import predict_image
from werkzeug.utils import secure_filename
from flask_restful import Api
from flask_cors import CORS, cross_origin
from controller.users_controller import UsersController
from controller.happiness_controller import HappinessController
from flask import send_from_directory

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(UsersController, '/users', '/users/register', '/users/<string:userId>', '/users/<string:userId>/profile-picture')
api.add_resource(EmotionController, '/emotions', '/emotions/<string:emotionId>')
api.add_resource(HappinessController, '/happiness', '/happiness/<string:emotionId>')
# api.add_resource(PredictController, '/predict', '/predict/<string:userId>')
# api.add_resource(OrdersController, '/orders', '/orders/<string:orderId>')

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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

@app.route('/uploads/profile_pictures/<filename>', methods=['GET'])
def serve_profile_picture(filename):
    return send_from_directory('uploads/profile_pictures', filename)

# if __name__ == "__main__":
#     app.run(debug=True)

