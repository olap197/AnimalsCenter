import unittest
import json
import base64
from flask_sqlalchemy import SQLAlchemy
from app import app
from model import db, AccessRequest, Center, Animals, Species
login='test_Case12'
password='mycoolpassword'
class TestAddAnimal(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.db = SQLAlchemy(app)
    def open_with_auth(self, url, method, username, password):
        return self.app.open(url,
            method=method,
            headers={
            'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":"
            + password, 'ascii')).decode('ascii')
            }
        )
   
    def test_add(self):
        response = self.open_with_auth('/login', 'GET', login,
                            password)
        resp=response.json
        self.assertEqual(200, response.status_code) 
        login_token=resp['token']

        animal_payload = {
            "name":"bartek",
            "age":"12",
            "price":1000.5,
            "species":"pies"
        }
        # When
        response = self.app.post('/animals',
            headers={"Content-Type": "application/json", "X-Access-Token": login_token},
            data=json.dumps(animal_payload))
        print(response.json)
        # Then
        self.assertEqual(200, response.status_code)