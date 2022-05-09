from flask import Blueprint, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.models import User
from main import logger, session, docs
from main.schemas import UserSchema, AuthSchema
from main.base_view import BaseView


users = Blueprint('users', __name__)


@users.route('/sign_up', methods=['POST'])
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
    return {'success': 'True'}


@users.route('/auth', methods=['POST'])
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


class ProfileView(BaseView):
    @jwt_required
    @marshal_with(UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        try:
            user = User.query.get(user_id)
            if not user:
                raise Exception('User not found')
        except Exception as e:
            logger.warning(
                f'user:{user_id} - failed to read profile: {e}')
        return user


@users.errorhandler(422)
def handle_error(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid Request.'])
    logger.warning(f'Invalid input params: {messages}')
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(register, blueprint='users')
docs.register(login, blueprint='users')
ProfileView.register(users, docs, '/profile', 'profileview')
