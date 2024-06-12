import unittest
from flask import Flask
from flask_testing import TestCase
from main import app, get_price_data, get_crypto_info

class TestCryptoMicroservice(TestCase):
    def create_app(self):
        # Configuration de l'application pour les tests
        app.config['TESTING'] = True
        return app

    def test_hello(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Hello World, from crypto !")

    def test_get_crypto_data(self):
        response = self.client.get('/cryptodata')
        self.assertEqual(response.status_code, 200)
        data = response.json
        # Vérifiez que les données retournées contiennent les cryptomonnaies attendues
        self.assertIn('bitcoin', data)
        self.assertIn('ethereum', data)
        self.assertIn('litecoin', data)
        self.assertIn('solana', data)

    def test_get_transaction_data_btc(self):
        response = self.client.get('/transaction/BTC/sample_transaction_id')
        self.assertEqual(response.status_code, 200)

    def test_get_crypto_info(self):
        price = get_crypto_info('bitcoin')
        self.assertNotEqual(price, 0)

if __name__ == '__main__':
    unittest.main()