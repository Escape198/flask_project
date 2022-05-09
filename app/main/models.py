from . import db, session, Base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt


class Message(Base):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='review')
    success = db.Column(db.String(10), nullable=False, default='False')

    @classmethod
    def get_user_list(cls, user_id):
        try:
            messages = cls.query.filter(cls.user_id == user_id).all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return messages

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get_list(cls):
        try:
            messages = cls.query.all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return messages

    @classmethod
    def get(cls, message_id, user_id):
        try:
            video = cls.query.filter(
                cls.id == message_id,
                cls.user_id == user_id
            ).first()
            if not video:
                raise Exception('No messages with this id')
        except Exception:
            session.rollback()
            raise
        return video

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise



class User(Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    messages = relationship('Message', backref='user', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user
