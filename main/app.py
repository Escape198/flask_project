from flask import Flask, jsonify, request

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

jwt = JWTManager(app)

from models import *

Base.metadata.create_all(bind=engine)



@app.route('/message', methods=['GET'])
@jwt_required()
def get_list():
    user_id = get_jwt_identity()
    messages = Message.query.filter(Message.user_id == user_id).all()
    serialized = []
    for message in messages:
        serialized.append({
            'id': message.id,
            'messages': message.messages,
            'status': message.status,
            'success': message.success
        })
    return jsonify(serialized)


@app.route('/message_confirmation', methods=['POST'])
@jwt_required()
def update_list():
    user_id = get_jwt_identity()
    new_one = Message(user_id=user_id, **request.json)

    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'messages': new_one.messages,
    }
    return jsonify(serialized)

'''
@app.route('/message/<int:message_id>', methods=['PUT'])
@jwt_required()
def update_message(message_id):
    user_id = get_jwt_identity()
    item = Message.query.filter(
        Message.id == message_id,
        Message.user_id == user_id
    ).first()
    params = request.json

    if not item:
        return {'message': 'No message with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': message.id,
        'messages': message.messages,
        'status': message.status,
        'success': message.success
    }
    return serialized


@app.route('/message/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    user_id = get_jwt_identity()
    item = Message.query.filter(
        Message.id == message_id,
        Message.user_id == user_id).first()
    if not item:
        return {'message': 'No message with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204
'''

@app.route('/register', methods=['POST'])
def register():
    params = request.json
    user = User(**params)
    session.add(user)
    session.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    user = User.authenticate(**params)
    token = user.get_token()
    return {'access_token': token}


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
