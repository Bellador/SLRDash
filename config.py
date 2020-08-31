import os
import sqlalchemy
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''
    config for running the server LOCALLY but still accessing the remote Google Cloud Postgresql database
    IMPORTANT: TURN OFF ANY VPN SINCE IT IS IP ACCESS RESTRICTED!
    '''
    with open('database.txt', 'rt', encoding='utf-8') as f:
        SQLALCHEMY_DATABASE_URI = f.readline()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '17cÄ£_^AE'   #34kö$_^AC
