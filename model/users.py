from model import Database
from config import DATABASE_NAME, USERS_COLLECTION
import random
import string


class Users:
    def __init__(self):
        self.connection = Database(DATABASE_NAME)
        # print(self.connection.connection)
        
    def generateId(self):
        randomString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=12))
        filter = {'_id': randomString}
        _, data = self.connection.find(
            collection_name=USERS_COLLECTION, filter=filter)
        if data == None:
            return randomString
        return self.generateId()
    
    def findAllUsers(self):
        result = {'status': False, 'data': None, 'message': ''}
        status, data = self.connection.findMany(
            collection_name=USERS_COLLECTION, filter={})
        
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
            collection_name=USERS_COLLECTION, value=data)
        
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
            collection_name=USERS_COLLECTION,
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
