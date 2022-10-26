from flask import request
from flask_restx import Namespace, Resource

from implemented import auth_service

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        data = request.json

        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            return "", 400

        tokens = auth_service.generate_token(username=username, password=password)

        return tokens, 201

    def put(self):
        data = request.json

        token = data.get("refresh_token")

        if token is None:
            return "", 400

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
