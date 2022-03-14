import unittest
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

        pass

    def tearDown(self):
        db.drop_all()
        self.app_ctx.pop()
        pass

    def test_get_forecast(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token)
        }
        response = self.client.get('http://127.0.0.1:5000/forecast/777', headers=headers)
        print(response.status_code)
        print(response.get_data())
        pass
