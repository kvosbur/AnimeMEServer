from .base import BaseTestCase, db
from model.User import User
from handlers.UserHandler import UserHandler
from parameterized import parameterized

USEAUTHCODE = "ROAMGdIz6K8zRiWYMQFZyxfMd4u96dqobs5eiAF1DuYTnANEfNJnu5vuvGGzN2aCeIe4sUdTPpqsBlEQYmuTUr7RV4nFk81po4QPEry4YeQVQtOnqy58zzFbnmub7s5B"
USEPASSWORD = "pass"


class UserBaseTestCase(BaseTestCase):
    def setUp(self):
        db.create_all()
        # create user object to use for testing
        userObj = User(email="a@a.com",
                       username="AwesomeSauce",
                       sessionToken="69f6f1e7eddcb33b790474e010e7476ee15a7950527b50271f9892fcc7100a99ec752826363893be2c7e43b4b5935e1965d09178bacf10e1fbbd317a6aa86b6d",
                       password="w01sdXe24fhb13Vs9QVfARBfjy8mvTvPj6z9iExgJWYA7tvBzdz9tUKQCGC8yrAT$df23b65963ae7852854aef5c729a8eb3ef9b5dd24f87abaf517a3882a2dbff763ca8a9a5b132d8984356587dd23f0e914a7f5eee652cba0fe5aba5b175333f8c",
                       adminType=0)
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

    def test_username_is_empty(self):
        payload = {'email': "unique@a.com",
                   'username': "",
                   'password': "pass",
                   }

        with self.client:
            response = self.client.post(
                "user/register",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Username must be non-empty', 'statusCode': 6, 'data': ''}

            userCreated = db.session.query(User).filter_by(username=payload["email"]).first()
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


class TestUserLogin(UserBaseTestCase):

    def test_username_is_empty(self):
        payload = {'username': "",
                   'password': "pass",
                   }

        with self.client:
            response = self.client.post(
                "user/login",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Username must be non-empty', 'statusCode': 6, 'data': ''}

    def test_password_is_empty(self):
        payload = {'username': "AwesomeSauce",
                   'password': "",
                   }

        with self.client:
            response = self.client.post(
                "user/login",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Password must be non-empty', 'statusCode': 5, 'data': ''}

    @parameterized.expand([("weird", "pass"),
                            ("AwesomeSauce", "incorrect")])
    def test_incorrect_username_password(self, username, password):
        payload = {'username': username,
                   'password': password,
                   }

        userObj = db.session.query(User).filter_by(username="AwesomeSauce").first()
        originalAuth = userObj.sessionToken

        with self.client:
            response = self.client.post(
                "user/login",
                data=payload
            )
            assert response.status_code == 418
            assert response.json == {'message': 'Incorrect Username or Password', 'statusCode': 1, 'data': ''}

            userAfter = db.session.query(User).filter_by(username="AwesomeSauce").first()
            assert userAfter.sessionToken == originalAuth

    def test_correct_login_without_auth(self):
        payload = {'username': "AwesomeSauce",
                   'password': USEPASSWORD,
                   }

        userObj = db.session.query(User).filter_by(username="AwesomeSauce").first()
        originalAuth = userObj.sessionToken

        with self.client:
            response = self.client.post(
                "user/login",
                data=payload
            )
            assert response.status_code == 200
            assert response.json["message"] == "OK"
            assert response.json["statusCode"] == 0
            assert response.json["data"]["adminType"] == 0

            retAuth = response.json["data"]["authCode"]
            authHash = UserHandler.generateHash(retAuth)

            userAfter = db.session.query(User).filter_by(username="AwesomeSauce").first()
            # check that authCode has been altered like it should
            assert userAfter.sessionToken != originalAuth
            # check that correct value is stored as altered authCode
            assert authHash == userAfter.sessionToken


class TestUserLoginWithAuth(UserBaseTestCase):

    def test_empty_auth_code(self):
        headers = {}

        userObj = db.session.query(User).filter_by(username="AwesomeSauce").first()
        originalAuth = userObj.sessionToken

        with self.client:
            response = self.client.get(
                "user/loginWithAuth",
                headers=headers
            )
            assert response.status_code == 400
            assert response.json == {'errors': {'authCode': 'Missing required parameter in the HTTP headers'},
                                        'message': 'Input payload validation failed'}

            userAfter = db.session.query(User).filter_by(username="AwesomeSauce").first()
            # check that authCode has not been altered
            assert userAfter.sessionToken == originalAuth

    def test_invalid_auth_code(self):
        headers = {"authCode": "incorrect"}

        userObj = db.session.query(User).filter_by(username="AwesomeSauce").first()
        originalAuth = userObj.sessionToken

        with self.client:
            response = self.client.get(
                "user/loginWithAuth",
                headers=headers
            )
            assert response.status_code == 401
            assert response.json == {'message': "invalid 'authCode' in header"}

            userAfter = db.session.query(User).filter_by(username="AwesomeSauce").first()
            # check that authCode has not been altered
            assert userAfter.sessionToken == originalAuth

    def test_correct_login_with_auth(self):

        headers = {"authCode": USEAUTHCODE}

        userObj = db.session.query(User).filter_by(username="AwesomeSauce").first()
        originalAuth = userObj.sessionToken

        with self.client:
            response = self.client.get(
                "user/loginWithAuth",
                headers=headers
            )
            assert response.status_code == 200
            assert response.json["message"] == "OK"
            assert response.json["statusCode"] == 0
            assert response.json["data"]["adminType"] == 0

            userAfter = db.session.query(User).filter_by(username="AwesomeSauce").first()
            # check that authCode has not been altered
            assert userAfter.sessionToken == originalAuth

