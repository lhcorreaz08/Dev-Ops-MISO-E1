import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

## Blacklist
class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(140))
    app_uuid = db.Column(db.String(140))
    blocked_reason = db.Column(db.String(255), nullable=True)
    ip_origin = db.Column(db.String(255))
    createdat = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

class BlacklistSchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Length(min=1, max=140))
    app_uuid = fields.String(required=True, validate=validate.Length(min=1, max=140))
    blocked_reason = fields.String(required=False, validate=validate.Length(min=1, max=255))
    ip_origin = fields.String(required=True, validate=validate.Length(min=1, max=255))
    createdat = fields.DateTime(dump_only=True)

    class Meta:
        model = Blacklist
        load_instance = True


class BlacklistSchemaGet(SQLAlchemyAutoSchema):
    id = fields.Integer(load_only=True)
    email = fields.String(required=True, validate=validate.Length(min=1, max=140))
    app_uuid = fields.String(required=True, validate=validate.Length(min=1, max=140))
    blocked_reason = fields.String(dump_only=True, validate=validate.Length(min=1, max=255))
    ip_origin = fields.String(required=True, validate=validate.Length(min=1, max=255))
    createdat = fields.DateTime(load_only=True)

    class Meta:
        model = Blacklist
        load_instance = True
