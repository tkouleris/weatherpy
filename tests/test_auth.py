import unittest

import requests

from app import db
from app.models import User


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.test_user = User(name='test_user', email='test@test.tst')
        self.test_user.set_password('test')
        db.session.add(self.test_user)
        db.session.commit()
        pass

    def tearDown(self):
        db.session.delete(self.test_user)
        db.session.commit()
        pass

    def test_login(self):
        response = requests.post('http://127.0.0.1:5000/auth/login',
                                 json={"email": "test@test.tst", "password": "test"})
        self.assertEqual(200, response.status_code)
