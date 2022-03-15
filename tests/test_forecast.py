import unittest
from unittest import mock

from app import create_app, db, authentication, forecast
from app.models import User, City


class TestForecast(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        self.client = self.app.test_client()
        self.app.register_blueprint(authentication)
        self.app.register_blueprint(forecast)
        db.init_app(self.app)
        db.create_all()
        self.test_user = User(name='test_user', email='test@test.tst')
        self.test_user.set_password('test')
        db.session.add(self.test_user)
        self.city = City(id=777, owm_id=777, city="GOTHAM", city_state="", country="USA")
        db.session.add(self.city)
        db.session.commit()
        response = self.client.post('http://127.0.0.1:5000/auth/login',
                                    json={"email": "test@test.tst", "password": "test"})
        self.token = response.get_json()['token']

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()

    def test_get_forecast(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = self.client.get('http://127.0.0.1:5000/forecast/777', headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Gotham", response.get_json()['results'][0]['info']['city'])
        self.assertEqual("USA", response.get_json()['results'][0]['info']['country'])

    def test_add_city_to_user(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = self.client.post('http://127.0.0.1:5000/user/city/777', headers=headers)
        self.assertEqual(200, response.status_code)

    def test_delete_city_to_user(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = self.client.delete('http://127.0.0.1:5000/user/city/777', headers=headers)
        self.assertEqual(200, response.status_code)
