import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_users(self):
        """Test getting all users"""
        response = self.app.get('/api/users')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)

    def test_get_user(self):
        """Test getting a specific user"""
        response = self.app.get('/api/users/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)
        self.assertTrue('name' in data)
        self.assertTrue('email' in data)

    def test_get_nonexistent_user(self):
        """Test getting a non-existent user"""
        response = self.app.get('/api/users/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        """Test creating a new user"""
        new_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        response = self.app.post('/api/users',
                               data=json.dumps(new_user),
                               content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], new_user['name'])
        self.assertEqual(data['email'], new_user['email'])

    def test_get_products(self):
        """Test getting all products"""
        response = self.app.get('/api/products')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)

    def test_get_product(self):
        """Test getting a specific product"""
        response = self.app.get('/api/products/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)
        self.assertTrue('name' in data)
        self.assertTrue('price' in data)

if __name__ == '__main__':
    unittest.main() 