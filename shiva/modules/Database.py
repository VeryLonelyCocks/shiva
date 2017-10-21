"""
PyMongo

Docs: http://api.mongodb.com/python/current/tutorial.html
"""
from pymongo import MongoClient


class Database:

    connection = None

    def __init__(self):
        self.connection = MongoClient()

    def get(self, dbname):
        return self.connection[dbname]
