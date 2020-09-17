import os
import sqlalchemy

from sshtunnel import SSHTunnelForwarder

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''
    config for running the server LOCALLY but still accessing the remote Google Cloud Postgresql database
    IMPORTANT: TURN OFF ANY VPN SINCE IT IS IP ACCESS RESTRICTED!
    '''
    from settings import DATABASE_LOCATION

    if DATABASE_LOCATION == 'local':
        from settings import LOCAL_DATABASE_CONNECTION
        with open(LOCAL_DATABASE_CONNECTION, 'rt', encoding='utf-8') as f:
            SQLALCHEMY_DATABASE_URI = f.readline()
    elif DATABASE_LOCATION == 'remote':
        # create ssh tunnel
        from settings import REMOTE_IP
        from settings import REMOTE_USER
        from settings import BIND_PORT
        from settings import REMOTE_DB_NAME
        from settings import REMOTE_DB_USER
        from settings import REMOTE_DB_PSW
        from settings import REMOTE_PRIVATE_KEY
        from settings import REMOTE_PRIVATE_KEY_PSW

        server = SSHTunnelForwarder(
            (REMOTE_IP, 22),
            ssh_username=REMOTE_USER,
            ssh_pkey=REMOTE_PRIVATE_KEY,
            ssh_private_key_password=REMOTE_PRIVATE_KEY_PSW,
            remote_bind_address=('127.0.0.1', BIND_PORT)
        )
        server.start()
        local_port = str(server.local_bind_port)
        SQLALCHEMY_DATABASE_URI = f'postgresql://{REMOTE_DB_USER}:{REMOTE_DB_PSW}@{"127.0.0.1"}:{local_port}/{REMOTE_DB_NAME}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '17cÄ£_^AE'   #34kö$_^AC
