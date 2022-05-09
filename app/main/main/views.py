from flask import Blueprint, jsonify, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import logger, docs
from main.schemas import MessageSchema
from main.base_view import BaseView
from main.models import Message


messages = Blueprint('messages', __name__)


class ListView(BaseView):
    @marshal_with(MessageSchema(many=True))
    def get(self):
        try:
            messages = Message.get_list()
        except Exception as e:
            logger.warning(
                f'message - read action failed with errors: {e}')
            return {'message': str(e)}, 400
        return messages

@messages.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@messages.route('/api/v1/message', methods=['GET'])
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


@messages.route('/api/v1/message', methods=['POST'])
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


@messages.errorhandler(422)
def handle_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid Request.'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list, blueprint='messages')
docs.register(update_list, blueprint='messages')
ListView.register(messages, docs, '/main', 'listview')
