import os


class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = 'static/uploads/'
    SERVER_PATH = ROOT + UPLOAD_PATH

    USER = os.environ.get('POSTGRES_USER', 'codervlad')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'codervlad')
    HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    PORT = os.environ.get('POSTGRES_PORT', 5532)
    DATABASE = os.environ.get('POSTGRES_DB', 'mydb')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    SECRET_KEY = 'sdhsdhsdfhLDGHl543567jkhjkh3kj64h5'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
