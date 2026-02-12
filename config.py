import os
from sqlalchemy import create_engine

class Config(object):
    SECRER_KEY = "ClaveSecreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://Jeypeeh:root@127.0.0.1/bdidgs801'
    SQLALCHEMY_TRACK_MODIFICATIONS = False