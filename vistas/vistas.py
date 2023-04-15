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
import socket

black_list_schema = BlacklistSchema()
black_list_schema_get = BlacklistSchemaGet()


class VistaBlacklist(Resource):

    def post(self):
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header is not None and 'Bearer' in authorization_header:
                token = authorization_header.split(' ')[1]
                if token != 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz':
                    return {"msg": "Token Invalid"}, 412
                if request.json["email"] is None or request.json["app_uuid"] is None:
                    return {"msg": "Missing fields"}, 400    
                requestEmail = Blacklist.query.filter(Blacklist.email == request.json["email"]).first()
                if requestEmail is None:
                    blacklist = Blacklist(
                    email=request.json['email'],
                    app_uuid=request.json['app_uuid'],
                    blocked_reason=request.json['blocked_reason'],
                    ip_origin=obtener_direccion_ip()
                    )
                    db.session.add(blacklist)
                    db.session.commit()
                    return {"msg": "Email added in bl@ckl!st"}, 201
                else:
                    return {"msg": "Email already exists"}, 400
            else:
                return {"msg": "Token Missing"}, 410
        except TypeError:
            return {"msg": "Error values"}, 400
        except KeyError:
            return {"msg": "Error values"}, 400


class VistaBlacklistInformacion(Resource):
    
    def get(self):
        try:      
            if request and request.args and 'email' in request.args and request.args.get('email') is not None and request.args.get('email') != '':
                email = request.args.get('email')
                authorization_header = request.headers.get('Authorization')
                if authorization_header is not None and 'Bearer' in authorization_header:
                    token = authorization_header.split(' ')[1]
                    if token != 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz':
                        return {"msg": "Token Invalid"}, 412
                    requestEmail = Blacklist.query.filter(Blacklist.email == email).first()
                    if requestEmail is not None and email == requestEmail.email:
                        return {"reported": "TRUE", "Blocked_reason": requestEmail.blocked_reason}, 201
                    else:
                        return {"reported": "FALSE", "msg": "Email not reported"}, 210  
                   
                else:
                    return {"msg": "Token Missing"}, 410
            else:
                return {"msg": "Missing fields"}, 400
        except TypeError:
            return {"msg": "Error values"}, 400
        except KeyError:
            return {"msg": "Error values"}, 400



def obtener_direccion_ip():
    direccion_ip = ''
    try:
        direccion_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        pass
    return direccion_ip

