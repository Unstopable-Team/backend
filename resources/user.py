from flask import Response, request
from flask_restful import Resource
from core.models import UserModel
from blacklist import BLACKLIST
from libs.strings import gettext

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)


class UserManagement(Resource):
    """ '/user' endpoint. """

    def get(self):
        pass

    def post(self):
        """ Create new user """

        user_data = request.get_json()

        if UserModel.find_by_username(user_data["user_name"]):
            return {"message": gettext("error_user_exists")}, 400

        if UserModel.find_by_email(user_data["email"]):
            return {"message": gettext("error_user_exists")}, 400

        user = UserModel(**user_data)
        try:
            user.save()
        except Exception:
            return {"message": gettext("error_user_creating")}, 500

        return Response(user.to_json(),
                        mimetype="application/json", status=200)

    def delete(self):
        """ Delete user """

        user_data = request.get_json()

        user = UserModel.find_by_username(user_data["user_name"])
        if user is None:
            user = UserModel.find_by_email(user_data["email"])
            if user is None:
                return {"message": gettext("error_user_not_found")}, 404

        try:
            user.delete()
        except Exception:
            return {"message": gettext("error_user_deleting")}, 500

        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    """ '/login' endpoint."""

    def post(self):
        user_data = request.get_json()
        print(user_data)
        user = UserModel.find_by_username(user_data["user_name"])

        if user and safe_str_cmp(user.password, user_data["password"]):
            access_token = create_access_token(user.user_name, fresh=True)
            refresh_token = create_refresh_token(user.user_name)
            return (
                {"access_token": access_token,
                 "refresh_token": refresh_token
                 }, 200,
            )
        return {"message": gettext("error_user_invalid_credentials")}, 401


class UserLogout(Resource):
    """ '/logout' endpoint. """
    @jwt_required
    def post(self):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_jwt()["jti"]
        user_name = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": gettext("user_logged_out").format(user_name)}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_name = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=user_name)
        }
