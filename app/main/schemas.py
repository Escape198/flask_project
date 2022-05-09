from marshmallow import Schema, validate, fields


class MessageSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    message = fields.String(required=True, validate=[
        validate.Length(max=500)])
    status = fields.String(required=True, validate=[
        validate.Length(max=10)], dump_only=True)
    success = fields.String(dump_only=True)


class UserSchema(Schema):
    name = fields.String(required=True, validate=[
        validate.Length(max=50)])
    email = fields.String(required=True, validate=[
        validate.Length(max=50)])
    password = fields.String(required=True, validate=[
        validate.Length(max=50)], load_only=True)
    messages = fields.Nested(MessageSchema, many=True, dump_only=True)


class AuthSchema(Schema):
    access_token = fields.String(dump_only=True)
    message = fields.String(dump_only=True)
