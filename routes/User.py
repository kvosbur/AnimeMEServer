
from app import api
from flask_restplus import Resource, reqparse

user = api.namespace('user', description='User info page')


@user.route("/register")
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='json', required=True)
    parser.add_argument('username', type=str, location='json', required=True)
    parser.add_argument('password', type=str, location='json', required=True)

    @user.expect(parser)
    @api.doc(responses={
        0: "OK",
        -1: "No user found"
    })
    def post(self):
        a = 0
        # cool shit
