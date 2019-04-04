import os

class Config(object):
    DEBUG = True
    TESTING = os.environ.get("JORRVASKR_TESTING") == "true"
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:@db_test:5432/jorrvaskr"
        if os.environ.get("JORRVASKR_TESTING") == "true" else
        "postgresql://postgres:@db:5432/jorrvaskr"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
