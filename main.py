import os
from flask import Flask, json, render_template, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
from controller.users_controller import UsersController

app = Flask(__name__)
CORS(app)
api = Api(app)

# api.add_resource(ProductsController, '/products', '/products/<string:productId>')
api.add_resource(UsersController, '/users', '/users/register')
# api.add_resource(PredictController, '/predict', '/predict/<string:userId>')
# api.add_resource(OrdersController, '/orders', '/orders/<string:orderId>')


@app.route('/predict', methods=['POST'])
def predict():
    # print(request.files)
    print(json.dumps(request.files.to_dict(flat=False), indent=4))
    if 'file' not in request.files:
        return "No file part", 400  # Return a 400 Bad Request if file is missing

    f = request.files['file']
    if f.filename == '':
        return "No selected file", 400  # Handle empty file selection

    f.save(f.filename)   
    return "File uploaded successfully"


if __name__ == "__main__":
    app.run(debug=True)

