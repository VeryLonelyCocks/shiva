"""
PyMongo

Docs: http://api.mongodb.com/python/current/tutorial.html
"""
from pymongo import MongoClient

"""
Database class

Get database
>>> db = Database().get('db_name')

Get table
>>> table = db['chats']

Run action
>>> table.insert_one(data)
>>> table.find_one({'id': data['id']})
"""
class Database:

    connection = None

    def __init__(self):
        self.connection = MongoClient()

    def get(self, dbname):
        return self.connection[dbname]
