from flask import Flask
from flask_pymongo import PyMongo
from markupsafe import Markup

starter = Flask(__name__, instance_relative_config=True)
starter.config.from_pyfile('config.py', silent=False)

mongo = PyMongo(starter)

from ereapp import adminroutes, userroutes


