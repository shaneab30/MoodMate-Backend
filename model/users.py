from model import Database
from config import Config
import random
import string
import hashlib


class Users:
    def __init__(self):
        self.connection = Database(Config.DATABASE_NAME)
        # print(self.connection.connection)
        
    def generateId(self):
        randomString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=12))
        filter = {'_id': randomString}
        _, data = self.connection.find(
            collection_name=Config.USERS_COLLECTION, filter=filter)
        if data == None:
            return randomString
        return self.generateId()
    
    def findAllUsers(self):
        result = {'status': False, 'data': None, 'message': ''}
        status, data = self.connection.findMany(
            collection_name=Config.USERS_COLLECTION, filter={})
        
        if len(data) == 0:
            result['message'] = "Data tidak ditemukan"
        elif status == False:
            result['message'] = "Terjadi kesalahan saat mengambil semua data user"
        
        if status == True and len(data) != 0:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil semua data user"
        # print(result)
        return result

    def insertUser(self, data):
        result = {'status': False, 'data': None, 'message': ''}
        data['_id'] = self.generateId()
        
        statusInsert, dataInsert = self.connection.insert(
            collection_name=Config.USERS_COLLECTION, value=data)
        
        if statusInsert == False:
            result['message'] = "Terjadi kesalahan saat insert data user"
            
        if statusInsert == True and dataInsert != None:
            result['status'] = True
            result['message'] = "Berhasil insert data user"
        return result
    
    def updateUser(self, id, data):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'_id': id}
        value = {'$set': data}

        statusUpdate, dataUpdate = self.connection.update(
            collection_name=Config.USERS_COLLECTION,
            filter=filter,
            value=value
        )

        if dataUpdate.get('modified_count', 0) == 0:
            result['message'] = "Tidak ada perubahan data"
            result['status'] = True
        elif statusUpdate == False:
            result['message'] = "Gagal update data user"
            return result 

        if statusUpdate == True and dataUpdate.get('modified_count', 0) != 0:
            result['status'] = True
            result['message'] = "Berhasil update data user"

        return result
    
    def uploadProfilePicture(self, id, data):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'_id': id}
        value = {'$set': data}
        
        statusUpdate, dataUpdate = self.connection.update(
            collection_name=Config.USERS_COLLECTION,
            filter=filter,
            value=value
        )
        if dataUpdate.get('modified_count', 0) == 0:
            result['message'] = "Tidak ada perubahan data"
            result['status'] = True
            result['filePath'] = data['profilePicture']
        elif statusUpdate == False:
            result['message'] = "Gagal update data user"
            return result 

        if statusUpdate == True and dataUpdate.get('modified_count', 0) != 0:
            result['status'] = True
            result['message'] = "Berhasil update data user"
            result['filePath'] = data['profilePicture']

        return result
    
    def findUserByUsername(self, username):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'username': username}
        status, data = self.connection.find(
            collection_name=Config.USERS_COLLECTION, filter=filter
        )
        
        if status == False:
            result['message'] = "Terjadi kesalahan saat mengambil data user"
        
        if status == True and data != None:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil data user"
        return result
    
    def findUserByEmail(self, email):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'email': email}
        status, data = self.connection.find(
            collection_name=Config.USERS_COLLECTION, filter=filter
        )
        
        if status == False:
            result['message'] = "Terjadi kesalahan saat mengambil data user"
        
        if status == True and data != None:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil data user"
        return result
    
    def findUserById(self, user_id):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'_id': user_id}
        status, data = self.connection.find(
            collection_name=Config.USERS_COLLECTION, filter=filter
        )
        if status == False:
            result['message'] = "Terjadi kesalahan saat mengambil data user"
        elif data:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil data user"
        else:
            result['message'] = "User tidak ditemukan"
        return result
