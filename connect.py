from pymongo import MongoClient


class db_connect:

    def __init__(self):
        pass

    def mongo_connect(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client["com_manage_library"]["books"]
        #returning database
        return db
