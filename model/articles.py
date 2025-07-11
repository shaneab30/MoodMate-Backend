from model import Database
from config import DATABASE_NAME, ARTICLES_COLLECTION
import random
import string

class Articles:
    def __init__(self):
        self.connection = Database(DATABASE_NAME)
    
    def generateId(self):
        randomString = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=12))
        filter = {'_id': randomString}
        _, data = self.connection.find(
            collection_name=ARTICLES_COLLECTION, filter=filter)
        if data == None:
            return randomString
        return self.generateId()
    
    def findAllArticles(self, skip=0, limit=8):
        result = {'status': False, 'data': None, 'message': ''}
        status, data = self.connection.findMany(
            collection_name=ARTICLES_COLLECTION, filter={}, skip=skip, limit=limit)
        if status == False:
            result['message'] = "Terjadi kesalahan saat mengambil data artikel"
        elif data:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil data artikel"
        else:
            result['message'] = "Artikel tidak ditemukan"
        return result
    
    def insertArticles(self, data):
        result = {'status': False, 'data': None, 'message': ''}
        data['_id'] = self.generateId()
        
        statusInsert, dataInsert = self.connection.insert(
            collection_name=ARTICLES_COLLECTION, value=data)
        
        if statusInsert == False:
            result['message'] = "Terjadi kesalahan saat insert data artikel"
            
        if statusInsert == True and dataInsert != None:
            result['status'] = True
            result['message'] = "Berhasil insert data artikel"
        return result
    
    def updateArticles(self, article_id, data):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'_id': article_id}
        statusUpdate, dataUpdate = self.connection.update(
            collection_name=ARTICLES_COLLECTION, filter=filter, value=data)
        
        if statusUpdate == False:
            result['message'] = "Terjadi kesalahan saat update data artikel"
            
        if statusUpdate == True and dataUpdate != None:
            result['status'] = True
            result['message'] = "Berhasil update data artikel"
        return result
    
    def findArticleById(self, article_id):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'_id': article_id}
        status, data = self.connection.find(
            collection_name=ARTICLES_COLLECTION, filter=filter
        )
        if status == False:
            result['message'] = "Terjadi kesalahan saat mengambil data artikel"
        elif data:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil data artikel"
        else:
            result['message'] = "Artikel tidak ditemukan"
        return result
    
    def findArticlesByUsername(self, username):
        result = {'status': False, 'data': None, 'message': ''}
        filter = {'username': username}
        status, data = self.connection.find(
            collection_name=ARTICLES_COLLECTION, filter=filter
        )
        if status == False:
            result['message'] = "Terjadi kesalahan saat mengambil data artikel"
        elif data:
            result['status'] = True
            result['data'] = data
            result['message'] = "Berhasil mengambil data artikel"
        else:
            result['message'] = "Artikel tidak ditemukan"
        return result