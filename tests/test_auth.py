import unittest

from app import create_app, db, authentication, forecast
from app.models import User


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client()
        self.app.register_blueprint(authentication)
        db.init_app(self.app)
        db.create_all()
        self.test_user = User(name='test_user', email='test@test.tst')
        self.test_user.set_password('test')
        db.session.add(self.test_user)
        db.session.commit()
        pass

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()
        pass

    def test_login_succeeds(self):
        response = self.client.post('http://127.0.0.1:5000/auth/login',
                                    json={"email": "test@test.tst", "password": "test"})
        self.assertEqual(200, response.status_code)
        self.assertTrue('token' in response.get_data(as_text=True))

    def test_login_fails(self):
        response = self.client.post('http://127.0.0.1:5000/auth/login',
                                    json={"email": "test1@test.tst", "password": "test"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('user does not exist', response.get_json()['message'])

    def test_registration_succeeds(self):
        response = self.client.post('http://127.0.0.1:5000/auth/register',
                                    json={"username": "demouser", "email": "demo@gmail.com",
                                          "password": "RedGreenBlue11@"})
        self.assertEqual(200, response.status_code)
        self.assertEqual('user created',response.get_json()['results']['message'])

    def test_registration_fails(self):
        response = self.client.post('http://127.0.0.1:5000/auth/register',
                                    json={"username": "demouser", "email": "demo@gmail.com",
                                          "password": "test"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Password empty or not valid',response.get_json()['message'][0])

