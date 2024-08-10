from flask_restful import Resource, reqparse
from model.users import Users

modelUsers = Users()
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Parameter 'username' can not be blank")
parser.add_argument('password', type=str, required=True, help="Parameter 'password' can not be blank")
parser.add_argument('email', type=str, required=True, help="Parameter 'email' can not be blank")
parser.add_argument('age', type=str, required=True, help="Parameter 'age' can not be blank")


class UsersController(Resource):
    def get(self):
        return modelUsers.findAllUsers()

    def post(self):
        args = parser.parse_args()
        data = {'username': args['username'], 'password': args['password'], 'email': args['email'], 'age': args['age']}
        # print(f"{modelUsers.findAllUsers()}")
        listUser = []
        try: 
            for user in modelUsers.findAllUsers()['data']:
                listUser.append(user['username'])
        except:
            listUser = []
        # print(listUser)
        if args['username'] in listUser:
            return {'status': False, 'data': None, 'message': 'Username sudah ada'}, 400
        else: 
            resultInsert = modelUsers.insertUser(data)
        
                
        if resultInsert.get('status') == True:
            return resultInsert, 200
        else:
            return resultInsert, 400
        
    def put(self,userId):
        args = parser.parse_args()
        data = {'username': args['username'], 'password': args['password'], 'email': args['email'], 'age': args['age']}
        resultUpdate = modelUsers.updateUser(userId, data)
        
        if resultUpdate.get('status') == True:
            return resultUpdate, 200
        else:
            return resultUpdate, 400