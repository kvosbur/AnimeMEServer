from model import db
import hashlib
import secrets
import string
from model.User import User

class UserHandler:

    @staticmethod
    def generateRandomCharacters(amount):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(amount))

    @staticmethod
    def generateSalt():
        salt = UserHandler.generateRandomCharacters(64)
        return salt

    @staticmethod
    def generateHash(value):
        """Assume input is a string"""
        return hashlib.sha512(value.encode("utf-8")).hexdigest()

    @staticmethod
    def generateSaltedHash(salt, password):

        valueToHash = salt + password
        hashValue = UserHandler.generateHash(valueToHash)
        # return the value to store in db -> salt $ (separator) and the hash
        return salt + "$" + hashValue

    @staticmethod
    def registerNewUser(email, username, password):
        # at this point assume all validation has already occurred on the input
        # create hash of password with salt
        salt = UserHandler.generateSalt()
        hashedPassword = UserHandler.generateSaltedHash(salt, password)

        # create auth-code and stored hashed version on server
        authCode = UserHandler.generateRandomCharacters(128)
        authHash = UserHandler.generateHash(authCode)

        # add new user object to the db
        userObj = User(email=email, username=username, sessionToken=authHash, password=hashedPassword, adminType=0)
        db.session.add(userObj)
        db.session.commit()

        return authCode

    @staticmethod
    def comparePasswords(passwordObj, passwordInput):
        salt, passHash = passwordObj.split("$")

        attemptHash = UserHandler.generateHash(salt + passwordInput)
        return secrets.compare_digest(passHash, attemptHash)

    @staticmethod
    def loginUser(username, password):
        # check if username exists
        userObj = db.session.query(User).filter_by(username=username).first()
        if userObj is None:
            return 1, "Incorrect Username or Password"
        # get password with salt from db and check if given password matches stored password
        passwordObj = userObj.password
        if not UserHandler.comparePasswords(passwordObj, password):
            return 1, "Incorrect Username or Password"

        # set new authCode for user
        authCode = UserHandler.generateRandomCharacters(128)
        authHash = UserHandler.generateHash(authCode)
        userObj.sessionToken = authHash
        db.session.commit()

        # return authcode and user adminType
        return 0, {"authCode": authCode, "adminType": userObj.adminType}
