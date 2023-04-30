import os
import unittest
import psycopg2
from dotenv import load_dotenv
from flask import jsonify
import jwt
from functools import wraps
from jinja2 import Template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import app

# Chargement des variables d'environnement
load_dotenv()

class TestOS(unittest.TestCase):
    def test_path_exists(self):
        self.assertTrue(os.path.exists('C:/Users/tgp/Documents'))
        
    def test_file_exists(self):
        self.assertTrue(os.path.isfile('C:/Users/tgp/Documents/apostolou.jpg'))

class TestPsycopg2(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(
            host=os.getenv("POSTGRES_DB_HOST"),
            port=os.getenv("POSTGRES_DB_PORT"),
            dbname=os.getenv("POSTGRES_DB_NAME"),
            user=os.getenv("POSTGRES_DB_USER"),
            password=os.getenv("POSTGRES_DB_PASS")
        )
        self.cur = self.conn.cursor()
    
    def tearDown(self):
        self.cur.close()
        self.conn.close()
        
    def test_database_connection(self):
        self.assertIsNotNone(self.conn)
        
    def test_select_query(self):
        self.cur.execute("SELECT * FROM mercadona.produits")
        rows = self.cur.fetchall()
        self.assertGreater(len(rows), 0)

class TestDotenv(unittest.TestCase):
    def test_env_var_exists(self):
        self.assertIsNotNone(os.getenv("UPLOAD_FOLDER"))
        
class TestJsonify(unittest.TestCase):
    def test_jsonify_output(self):
        data = {'key': 'value'}
        with app.test_request_context():
            response = jsonify(data)
        self.assertIsInstance(response.get_data(), bytes)

class TestJWT(unittest.TestCase):
    def test_jwt_encode_decode(self):
        payload = {'user_id': 123}
        encoded_token = jwt.encode(payload, os.getenv("SECRET_KEY"))
        decoded_payload = jwt.decode(encoded_token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
        self.assertEqual(decoded_payload['user_id'], payload['user_id'])

class TestFunctools(unittest.TestCase):
    def test_wraps_decorator(self):
        def my_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        
        @my_decorator
        def my_function():
            pass
        
        self.assertEqual(my_function.__name__, 'my_function')
        
class TestJinja2(unittest.TestCase):
    def test_jinja2_render_template(self):
        template_string = "Hello {{ name }}!"
        template = Template(template_string)
        rendered_template = template.render(name="World")
        self.assertEqual(rendered_template, "Hello World!")
        
class TestWerkzeug(unittest.TestCase):
    def test_password_hashing(self):
        password = 'my_password'
        hashed_password = generate_password_hash(password)
        self.assertTrue(check_password_hash(hashed_password, password))
        
class TestDatetime(unittest.TestCase):
    def test_datetime_now(self):
        now = datetime.now()
        self.assertIsNotNone(now)

if __name__ == '__main__':
    unittest.main()
