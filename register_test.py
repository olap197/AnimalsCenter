import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from model import db, AccessRequest, Center, Animals, Species

login='test_Case1234'

class RegisterTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = SQLAlchemy(app)

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "login":login,
            "password": "mycoolpassword",
            "address": "test@gmail.com"
        })

        # When
        response = self.app.post('/register', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        print(response.json)
        self.assertEqual(int, type(response.json['c_id']))
        self.assertEqual(200, response.status_code)


