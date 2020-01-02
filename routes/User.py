
from flask_restplus import Resource, reqparse, Namespace, fields
from validation.UserValidation import UserValidation
from handlers.UserHandler import UserHandler
from util.HTTPResponse import HTTPResponse

user = Namespace('user', description='User info page')

authResponseModel = user.model("AuthResponse", {"authCode": fields.String(example="BCtiAMdQe0AXlj3sKD22xDquFI2njzRb2BjWy9ISpI6xkCHqINhZUQIv0Pk6ZYNNlvV9wXpXMWc611LeERnXrTT9HnWb5Ivz0XiX5Zp1PYopUQ16NIRTezGo76c9lzll")})


@user.route("/register")
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, location='form', required=True)
    parser.add_argument('username', type=str, location='form', required=True)
    parser.add_argument('password', type=str, location='form', required=True)

    @user.expect(parser)
    @user.doc()
    @user.response(200, "Account was created correctly", user.model("RegistrationResponse",
                                                                    {"message": fields.String(example="OK"),
                                                                     "statusCode": fields.Integer(example=0),
                                                                     "data": fields.Nested(authResponseModel)}))
    @user.response(418, "There was an issue that occurred that prevented Account creation", user.model("RegistrationResponseError",
                                                                    {"message": fields.String(example="Email must be non-empty"),
                                                                     "statusCode": fields.Integer(example=1),
                                                                     "data": fields.String(example="")}))
    def post(self):
        arguments = self.parser.parse_args()
        email = arguments["email"]
        username = arguments["username"]
        password = arguments["password"]
        errorCode, errMsg = UserValidation.validateRegistration(email, username, password)
        # Input did not pass input validation
        if errorCode != 0:
            return HTTPResponse.makeResponse(418, errMsg, errorCode, "")

        # create a new user account
        authToRet = UserHandler.registerNewUser(email, username, password)

        return HTTPResponse.makeResponse(200, "OK", 0, {"authCode":authToRet})
