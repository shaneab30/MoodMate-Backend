from config import MONGO_URI
from pymongo import MongoClient, errors
import certifi

class Database:
    def __init__(self, dbname):
        try:
            # Use certifi for SSL certificate verification
            self.connection = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
            self.db = self.connection[dbname]
        except errors.ConnectionFailure as conn_fail:
            print(f"Gagal membuat koneksi (connection failure) | {conn_fail}")
        except Exception as error:
            print(f"Gagal membuat koneksi | {error}")

    def find(self, collection_name, filter):
        status = False
        data = None
        try:
            collection = self.db[collection_name]
            resultFind = collection.find_one(filter)
            data = resultFind
            status = True
        except errors.PyMongoError as pymongoerror:
            print(f"Gagal find data, error pymongo: {pymongoerror}")
        except Exception as err:
            print(f"Gagal find data, other error: {err}")
        return status, data

    def findMany(self, collection_name, filter, skip=0, limit=0):
        status = False
        data = None
        try:
            collection = self.db[collection_name]
            cursor = collection.find(filter)

            if skip > 0:
                cursor = cursor.skip(skip)
            if limit > 0:
                cursor = cursor.limit(limit)

            data = list(cursor)
            status = True
        except errors.PyMongoError as pymongoerror:
            print(f"Gagal find data, error pymongo: {pymongoerror}")
        except Exception as err:
            print(f"Gagal find data, other error: {err}")
        return status, data


    def insert(self, collection_name, value):
        status = False
        data = None
        try:
            collection = self.db[collection_name]
            resultInsert = collection.insert_one(value)
            data = resultInsert.inserted_id
            status = True
        except errors.PyMongoError as pymongoerror:
            print(f"Gagal find data, error pymongo: {pymongoerror}")
        except Exception as err:
            print(f"Gagal find data, other error: {err}")
        return status, data

    def update(self, collection_name, filter, value, upsert=False):
        status = False
        data = None
        try:
            collection = self.db[collection_name]
            resultUpdate = collection.update_one(filter=filter, update=value, upsert=upsert)
            data = {'modified_count': resultUpdate.modified_count}
            status = True
        except errors.PyMongoError as pymongoerror:
            print(f"Gagal find data, error pymongo: {pymongoerror}")
        except Exception as err:
            print(f"Gagal find data, other error: {err}")
        return status, data

    def delete(self, collection_name, filter):
        status = False
        data = None
        try:
            collection = self.db[collection_name]
            resultDelete = collection.delete_one(filter=filter)
            data = {'deleted_count': resultDelete.deleted_count}
            status = True
        except errors.PyMongoError as pymongoerror:
            print(f"Gagal find data, error pymongo: {pymongoerror}")
        except Exception as err:
            print(f"Gagal find data, other error: {err}")
        return status, data
