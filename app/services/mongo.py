from flask import Flask
from flask_pymongo import PyMongo
import logging

logger = logging.getLogger(__name__)

mongo = PyMongo()


def init_app(app):
    mongo.init_app(app)


def get_user_collection():
    return mongo.db.users


def get_account_collection():
    return mongo.db.accounts


def get_log_collection():
    return mongo.db.logs


def get_transaction_collection():
    return mongo.db.transactions


def get_analytics_collection():
    return mongo.db.analytics


def get_roles_collection():
    return mongo.db.roles
