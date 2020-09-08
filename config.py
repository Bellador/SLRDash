import os
import sqlalchemy
from sshtunnel import SSHTunnelForwarder

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''
    config for running the server LOCALLY but still accessing the remote Google Cloud Postgresql database
    IMPORTANT: TURN OFF ANY VPN SINCE IT IS IP ACCESS RESTRICTED!
    '''
    DATABASE_LOCATION = 'remote' #local

    if DATABASE_LOCATION == 'local':
        with open('database.txt', 'rt', encoding='utf-8') as f:
            SQLALCHEMY_DATABASE_URI = f.readline()
    elif DATABASE_LOCATION == 'remote':
        # create ssh tunnel
        from database_remote import remote_ip
        from database_remote import remote_user
        from database_remote import bind_port
        from database_remote import remote_db_name
        from database_remote import remote_db_user
        from database_remote import remote_db_psw
        from database_remote import remote_private_key
        from database_remote import remote_private_key_psw

        server = SSHTunnelForwarder(
            (remote_ip, 22),
            ssh_username=remote_user,
            ssh_pkey=remote_private_key,
            ssh_private_key_password=remote_private_key_psw,
            remote_bind_address=('127.0.0.1', bind_port)
        )
        server.start()
        local_port = str(server.local_bind_port)
        SQLALCHEMY_DATABASE_URI = f'postgresql://{remote_db_user}:{remote_db_psw}@{"127.0.0.1"}:{local_port}/{remote_db_name}'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or '17cÄ£_^AE'   #34kö$_^AC
