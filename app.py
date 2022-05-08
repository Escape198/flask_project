from flask import Flask, jsonify, request

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


message = [
    {
        'id': 1,
        'message': 'Message #1. Intro',
        'status': 'Review'
    },
    {
        'id': 2,
        'message': 'Message #2. More features',
        'status': 'Review'
    }
]


@app.route('/message', methods=['GET'])
def get_list():
    messages = Message.query.all()
    serialized = []
    for message in messages:
        serialized.append({
            'id': message.id,
            'messages': message.messages,
            'status': message.status,
            'success': message.success
        })
    print('ok')
    return jsonify(serialized)


@app.route('/message', methods=['POST'])
def update_list():
    new_one = Message(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'messages': new_one.messages,
    }
    return jsonify(serialized)

'''
@app.route('/message/<int:tutorial_id>', methods=['PUT'])
def update_tutorial(tutorial_id):
    item = Message.query.filter(Message.id == tutorial_id).first()
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


@app.route('/message/<int:tutorial_id>', methods=['DELETE'])
def delete_tutorial(tutorial_id):
    item = Message.query.filter(Message.id == tutorial_id).first()
    if not item:
        return {'message': 'No message with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204
'''

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
