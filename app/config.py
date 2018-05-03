class BasicConfig:
    DEBUG = False
    MONGO_DBNAME = 'testapi'
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    SECRET = 'afadsfF3442345DAX32Z2'

class DevelopConfig(BasicConfig):
    DEBUG = True
    MONGO_DBNAME = 'testapi'