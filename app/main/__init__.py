from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import use_kwargs, marshal_with

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from .config import Config

import logging


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

docs = FlaskApiSpec()

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='main',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger-ui.html/'
})



from .models import *

Base.metadata.create_all(bind=engine)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('main/log/api.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


from .main.views import messages
from .users.views import users

app.register_blueprint(messages)
app.register_blueprint(users)


docs.init_app(app)
jwt.init_app(app)
