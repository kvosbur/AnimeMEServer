from .base import BaseTestCase, db
from model.User import User
from handlers.UserHandler import UserHandler

class UserBaseTestCase(BaseTestCase):
    def setUp(self):
        db.create_all()
        # create user object to use for testing
        userObj = User(email="a@a.com", username="AwesomeSauce", sessionToken="a", password="pass", adminType=0)
        db.session.add(userObj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestUserRegistration(UserBaseTestCase):

    def test_email_is_empty(self):
        payload = {'email': "",
                   'username': "WayDifferent",
                   'password': "Different",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Email must be non-empty', 'statusCode': 1, 'data': ''}

            userCreated = db.session.query(User).filter_by(username=payload["username"]).first()
            assert userCreated is None

    def test_email_is_incorrect_format(self):
        payload = {'email': "whatThe",
                   'username': "WayDifferent",
                   'password': "Different",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Email is not Valid', 'statusCode': 2, 'data': ''}

            userCreated = db.session.query(User).filter_by(username=payload["username"]).first()
            assert userCreated is None

    def test_email_is_not_unique(self):
        payload = {'email': "a@a.com",
                   'username': "WayDifferent",
                   'password': "Different",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Email already has another account', 'statusCode': 3, 'data': ''}

            userCreated = db.session.query(User).filter_by(username=payload["username"]).first()
            assert userCreated is None

    def test_username_is_not_unique(self):
        payload = {'email': "unique@a.com",
                   'username': "AwesomeSauce",
                   'password': "Different",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'UserName is already being used', 'statusCode': 4, 'data': ''}

            userCreated = db.session.query(User).filter_by(email=payload["email"]).first()
            assert userCreated is None

    def test_password_is_empty(self):
        payload = {'email': "unique@a.com",
                   'username': "WayDifferent",
                   'password': "",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Password must be non-empty', 'statusCode': 5, 'data': ''}

            userCreated = db.session.query(User).filter_by(username=payload["username"]).first()
            assert userCreated is None

    def test_correct(self):
        payload = {'email': "unique@a.com",
                   'username': "WayDifferent",
                   'password': "pass",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 200
            assert response.json["message"] == "OK"
            assert response.json["statusCode"] == 0

            authCode = response.json["data"]["authCode"]

            userCreated = db.session.query(User).filter_by(username=payload["username"]).first()
            assert userCreated is not None

            # check that authCode is a match
            authHash = UserHandler.generateHash(authCode)
            assert authHash == userCreated.sessionToken
