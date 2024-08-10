from flask import Flask
from flask_restful import Api
from flask_cors import CORS
# from controller.products_controller import ProductsController
from controller.users_controller import UsersController

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
api = Api(app)

# api.add_resource(ProductsController, '/products', '/products/<string:productId>')
api.add_resource(UsersController, '/users', '/users/register')
# api.add_resource(OrdersController, '/orders', '/orders/<string:orderId>')

# from model.products import Products

if __name__ == "__main__":
    app.run(debug=True)
#     products = Products()
#     # print(products.findAllProducts())
#     print(products.generateId())
