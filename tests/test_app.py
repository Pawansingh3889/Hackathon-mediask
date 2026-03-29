import unittest
from app import create_app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About Us', response.data)

    def test_contact_page(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact', response.data)

    def test_non_existent_page(self):
        response = self.client.get('/non_existent')
        self.assertEqual(response.status_code, 404)

    def test_post_request(self):
        response = self.client.post('/submit', data={'name': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Success', response.data)

if __name__ == '__main__':
    unittest.main()