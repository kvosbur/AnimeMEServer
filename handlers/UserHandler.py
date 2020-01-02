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
