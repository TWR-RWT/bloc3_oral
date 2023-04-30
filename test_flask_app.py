import unittest
from flask import url_for, Flask, current_app
from flask_testing import TestCase
from app import app


class TestRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app
    
    def test_index(self):
        response = self.client.get(url_for('index'))
        self.assert200(response)


    def test_create_user(self):
        response = self.client.get(url_for('create_user'))
        self.assert200(response)

    def test_login(self):
        response = self.client.get(url_for('login'))
        self.assert200(response)
  
    def test_logout(self):
        response = self.client.get(url_for('logout'))
        self.assert200(response)

    def test_connexion(self):
        with app.app_context():
            response = self.client.get(url_for('connexion'))
            self.assert200(response)
            self.assert_template_used('/authentification/login.html')

    def test_comptes(self):
        with app.app_context():
            response = self.client.get(url_for('comptes'))
            self.assert200(response)
            self.assert_template_used('/authentification/comptes.html')

    def test_produit(self):
        response = self.client.get(url_for('produit'))
        self.assert200(response)
        self.assert_template_used('/main/product.html')

    def test_create_product_js(self):
        with app.app_context():
            response = self.client.get(url_for('create_product_js'))
            self.assert200(response)

    def test_products(self):
        response = self.client.get(url_for('products'))
        self.assert200(response)
        self.assert_template_used('/main/catalogues.html')

    def test_produits_liste_promotions(self):
        response = self.client.get(url_for('produits_liste_promotions'))
        self.assert200(response)
        self.assert_template_used('/main/discount.html')

    def test_submit_promotion(self):
        with app.app_context():
            response = self.client.get(url_for('submit_promotion'))
            self.assert200(response)

if __name__ == '__main__':
    unittest.main()
