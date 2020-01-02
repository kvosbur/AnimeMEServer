
from flask_restplus import Resource, reqparse, Namespace
from validation.UserValidation import UserValidation
from handlers.UserHandler import UserHandler
from util.HTTPResponse import HTTPResponse

user = Namespace('User', description='User info page')


@user.route("/register")
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='json', required=True)
    parser.add_argument('username', type=str, location='json', required=True)
    parser.add_argument('password', type=str, location='json', required=True)

    @user.expect(parser)
    @user.doc(responses={
        0: "OK",
        -1: "No user found"
    })
    def post(self):
        arguments = self.parser.parse_args()
        email = arguments["email"]
        username = arguments["username"]
        password = arguments["password"]
        isValid, errMsg = UserValidation.validateRegistration(email, username, password)
        # Input did not pass input validation
        if not isValid:
            return HTTPResponse.makeResponse(418, errMsg, 0, "")

        # create a new user account
        authToRet = UserHandler.registerNewUser(email, username, password)

        return HTTPResponse.makeResponse(200, "OK", 0, authToRet)
