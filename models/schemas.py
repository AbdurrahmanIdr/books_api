from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
