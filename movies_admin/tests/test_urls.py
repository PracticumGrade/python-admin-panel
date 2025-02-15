# posts/tests/test_urls.py
from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/admin')
        self.assertEqual(response.status_code, 301)
