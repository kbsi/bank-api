from flask_pymongo import PyMongo
from app import mongo

def get_user_collection():
    return mongo.db.users

def get_account_collection():
    return mongo.db.accounts

def get_log_collection():
    return mongo.db.logs
