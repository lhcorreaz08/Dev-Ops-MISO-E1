from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import Resource
from marshmallow import ValidationError
from modelos import db, Blacklist, BlacklistSchemaGet, BlacklistSchema
from dotenv import load_dotenv
from os import getenv
import json
import requests
import logging

black_list_schema = BlacklistSchema()
black_list_schema_get = BlacklistSchemaGet()


#Eliminar el jwt_required para que no se requiera token
class VistaBlacklist(Resource):

    def post(self):
        try:
            current_user = get_jwt_identity()
            data = request.get_json()
            data['email'] = current_user
            black_list = black_list_schema.load(data)
            db.session.add(black_list)
            db.session.commit()
            return black_list_schema.dump(black_list), 201
        except ValidationError as err:
            return err.messages, 422

    def get(self):
        try:
            current_user = get_jwt_identity()
            black_list = Blacklist.query.filter_by(email=current_user).all()
            return black_list_schema_get.dump(black_list), 200
        except ValidationError as err:
            return err.messages, 422


    def delete(self):
        try:
            current_user = get_jwt_identity()
            data = request.get_json()
            data['email'] = current_user
            black_list = black_list_schema.load(data)
            db.session.delete(black_list)
            db.session.commit()
            return black_list_schema.dump(black_list), 200
        except ValidationError as err:
            return err.messages, 422