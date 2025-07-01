import random
import string
from model import Database
from config import DATABASE_NAME, HAPPINESS_COLLECTION


class Happiness:
    def __init__(self):
        self.connection = Database(DATABASE_NAME)
    
    def generateId(self):
        randomString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=12))
        filter = {'_id': randomString}
        _, data = self.connection.find(
            collection_name=HAPPINESS_COLLECTION, filter=filter)
        if data == None:
            return randomString
        return self.generateId()

    def findAllEmotions(self):
        result = {'status': False, 'data': None, 'message': ''}
        status, data = self.connection.findMany(
            collection_name=HAPPINESS_COLLECTION, filter={})

        if len(data) == 0:
            result['message'] = "Data tidak ditemukan"
        elif status == False:
            result['message'] = "Terjadi kesalahan saat mengambil semua data happiness"

        if status == True and len(data) != 0:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil semua data happiness"
        return result

    def insertEmotion(self, data):
        result = {'status': False, 'data': None, 'message': ''}
        data['_id'] = self.generateId()

        statusInsert, dataInsert = self.connection.insert(
            collection_name=HAPPINESS_COLLECTION, value=data)

        if statusInsert == False:
            result['message'] = "Terjadi kesalahan saat insert data happiness"

        if statusInsert == True and dataInsert != None:
            result['status'] = True
            result['data'] = {'_id': data['_id'], 'username': data['username'], 'date': data['date'], 'level': data['level']}
            result['message'] = "Berhasil insert data happiness"
        return result