from validate_email import validate_email
from model import db
from model.User import User


class UserValidation:

    @staticmethod
    def validateUserEmail(email):
        """Validates whether the email string is in the correct format or not"""
        if len(email) == 0:
            return 1, "Email must be non-empty"
        elif not validate_email(email):
            return 2, "Email is not Valid"
        else:
            return 0, ""

    @staticmethod
    def validateEmailUniqueness(email):
        """Validates whether this is the first time the email is being used or not"""
        isFound = db.session.query(User).filter_by(email=email).first()
        if isFound is not None:
            return 3, "Email already has another account"
        else:
            return 0, ""

    @staticmethod
    def validateUsername(username):
        """Validates whether the username is non-empty"""
        if len(username) == 0:
            return 6, "Username must be non-empty"
        else:
            return 0, ""

    @staticmethod
    def validateUserNameUniqueness(username):
        """Validates whether this is the first time the user name is being used or not"""
        isFound = db.session.query(User).filter_by(username=username).first()
        if isFound is not None:
            return 4, "UserName is already being used"
        else:
            return 0, ""

    @staticmethod
    def validatePasswordNonEmpty(password):
        """Validates whether the password is non-empty"""
        if len(password) == 0:
            return 5, "Password must be non-empty"
        else:
            return 0, ""

    @staticmethod
    def validateRegistration(email, username, password):
        # valid email correctness
        errorCode, err_msg = UserValidation.validateUserEmail(email)
        if errorCode != 0:
            return errorCode, err_msg

        # validate email uniqueness
        errorCode, err_msg = UserValidation.validateEmailUniqueness(email)
        if errorCode != 0:
            return errorCode, err_msg

        # validate username is non-empty
        errorCode, err_msg = UserValidation.validateUsername(username)
        if errorCode != 0:
            return errorCode, err_msg

        # validate username uniqueness
        errorCode, err_msg = UserValidation.validateUserNameUniqueness(username)
        if errorCode != 0:
            return errorCode, err_msg

        # validate that the password is non-empty
        errorCode, err_msg = UserValidation.validatePasswordNonEmpty(password)
        if errorCode != 0:
            return errorCode, err_msg

        return 0, ""

    @staticmethod
    def validateLogin(username, password):
        # validate username is non-empty
        errorCode, err_msg = UserValidation.validateUsername(username)
        if errorCode != 0:
            return errorCode, err_msg

        # validate that the password is non-empty
        errorCode, err_msg = UserValidation.validatePasswordNonEmpty(password)
        if errorCode != 0:
            return errorCode, err_msg

        return 0, ""
