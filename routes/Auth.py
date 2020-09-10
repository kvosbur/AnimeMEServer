
from functools import wraps
from model.User import User
from flask_restx import reqparse, Namespace
from handlers.UserHandler import UserHandler

auth = Namespace('auth', description='User info page')

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('authCode', type=str, location='headers', required=True)


def auth_required(function):
    @auth.doc(responses={
        200: 'Success',
        401: 'Invalid or Empty authCode Given'
    })
    @auth.expect(auth_parser)
    @wraps(function)
    def decorated(*args, **kwargs):
        headers = auth_parser.parse_args()
        sessionToken = headers["authCode"]

        authHash = UserHandler.generateHash(sessionToken)
        user = User.query.filter_by(sessionToken=authHash).first()
        if user is None:
            return {"message": "invalid 'authCode' in header"}, 401

        kwargs['userObj'] = user

        return function(*args, **kwargs)

    return decorated
