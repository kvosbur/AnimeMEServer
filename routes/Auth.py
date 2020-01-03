
from functools import wraps
from flask import request
from model.User import User
from flask_restplus import reqparse, Namespace

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

        sessionToken = request.headers.get('authCode', None)
        if sessionToken is None:
            return {"message": "missing 'authCode' in header"}, 401

        user = User.query.filter_by(sessionToken=sessionToken).first()
        if user is None:
            return {"message": "invalid 'authCode' in header"}, 401

        kwargs['userObj'] = user

        return function(*args, **kwargs)

    return decorated
