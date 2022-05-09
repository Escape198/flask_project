from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import use_kwargs, marshal_with
from flask import render_template

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Config

import logging

from schemas import MessageSchema, UserSchema, AuthSchema


app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)


app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})

from models import *

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


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/api/v1/message', methods=['GET'])
@jwt_required()
@marshal_with(MessageSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()
        messages = Message.query.filter(Message.user_id == user_id).all()
    except Exception as e:
        logger.warning(
            f'user:{user_id} message - read action failed with errors: {e}')
        return {'message': str(e)}, 400
    return messages


@app.route('/api/v1/message', methods=['POST'])
@jwt_required()
@use_kwargs(MessageSchema)
@marshal_with(MessageSchema)
def update_list(**kwargs):
    try:
        user_id = get_jwt_identity()
        new_one = Message(user_id=user_id, **kwargs)
        new_one.save()
    except Exception as e:
        logger.warning(
            f'user:{user_id} message - create action failed with errors: {e}')
        return {'message': str(e)}, 400
    return new_one


@app.route('/sign_up', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    try:
        user = User(**kwargs)
        session.add(user)
        session.commit()
        token = user.get_token()
    except Exception as e:
        logger.warning(
            f'registration failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'success': True}


@app.route('/auth', methods=['POST'])
@use_kwargs(UserSchema(only=('email', 'password')))
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.get_token()
    except Exception as e:
        logger.warning(
            f'login with email {kwargs["email"]} failed with errors: {e}')
        return {'message': str(e)}, 400
    return {'success': True, 'access_token': token}


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


@app.errorhandler(422)
def handle_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid Request.'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


if __name__ == '__main__':
    app.run()
