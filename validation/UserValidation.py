from validate_email import validate_email
from app import db
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
        if isFound is None:
            return False, "Email already has another account"
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


        # validate that the password is non-empty