import unittest
from unittest.mock import patch, MagicMock
from flask import jsonify
from app import create_app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    @patch('app.client')
    def test_answer_success(self, mock_client):
        mock_stream = MagicMock()
        mock_stream.__iter__.return_value = [
            MagicMock(choices=[MagicMock(delta=MagicMock(content="Hello"))])
        ]
        mock_client.chat.completions.create.return_value = mock_stream

        response = self.client.post('/answer', json={"message": "Hello, bot!"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello')

    @patch('app.client')
    def test_answer_error(self, mock_client):
        mock_client.chat.completions.create.side_effect = Exception("API error")

        response = self.client.post('/answer', json={"message": "Hello, bot!"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Error occurred while processing your request.')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

if __name__ == '__main__':
    unittest.main()
