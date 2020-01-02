from validate_email import validate_email
from model import db
from model import User


class UserValidation:

    @staticmethod
    def validateUserEmail(email):
        """Validates whether the email string is in the correct format or not"""
        if len(email) == 0:
            return False, "Email must be non-empty"
        elif not validate_email(email):
            return False, "Email is not Valid"
        else:
            return True, ""

    @staticmethod
    def validateEmailUniqueness(email):
        """Validates whether this is the first time the email is being used or not"""
        isFound = db.session.query(User).filter_by(email=email).first()
        if isFound is not None:
            return False, "Email already has another account"
        else:
            return True, ""

    @staticmethod
    def validateUserNameUniqueness(username):
        """Validates whether this is the first time the user name is being used or not"""
        isFound = db.session.query(User).filter_by(username=username).first()
        if isFound is not None:
            return False, "UserName is already being used"
        else:
            return True, ""

    @staticmethod
    def validatePasswordNonEmpty(password):
        """Validates whether the password is non-empty"""
        if len(password) == 0:
            return False, "Password must be non-empty"
        else:
            return True, ""


    @staticmethod
    def validateRegistration(email, username, password):
        # valid email correctness
        valid, err_msg = UserValidation.validateUserEmail(email)
        if not valid:
            return valid, err_msg

        # validate email uniqueness
        valid, err_msg = UserValidation.validateEmailUniqueness(email)
        if not valid:
            return valid, err_msg

        # validate username uniqueness
        valid, err_msg = UserValidation.validateUserNameUniqueness(username)
        if not valid:
            return valid, err_msg

        # validate that the password is non-empty
        valid, err_msg = UserValidation.validatePasswordNonEmpty(password)
        if not valid:
            return valid, err_msg

        return True, ""
