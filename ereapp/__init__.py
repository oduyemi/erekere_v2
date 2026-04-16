import os
from flask import Flask
from flask_pymongo import PyMongo
from markupsafe import Markup

starter = Flask(__name__, instance_relative_config=True)
starter.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
starter.config['MONGO_URI'] = os.getenv('MONGO_URI')
starter.config['CURRENCY'] = os.getenv('CURRENCY')
# starter.config.from_pyfile('config.py', silent=False)

mongo = PyMongo(starter)

if not starter.config['MONGO_URI']:
    raise ValueError("MONGO_URI is not set")

from ereapp import adminroutes, userroutes


