import unittest
from app import create_app
from flask import jsonify
from unittest.mock import patch, MagicMock

class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test client and other necessary configurations."""
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    @patch('app.client.chat.completions.create')
    def test_answer_success(self, mock_create):
        """Test the /answer endpoint with a successful response."""
        # Mock the response from OpenAI API
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(delta=MagicMock(content='Hello, I am fine!'))]
        mock_create.return_value = [mock_response]
        
        # Send a POST request to /answer endpoint
        response = self.client.post('/answer', json={'message': 'Hello, how are you?'})
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Hello, I am fine!')
    
    @patch('app.client')
    def test_answer_invalid_input(self, mock_client):
        mock_client.chat.completions.create.side_effect = Exception("API error")

        response = self.client.post('/answer', json={"message": "Hello, bot!"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Error occurred while processing your request.')
    
    def test_index(self):
        """Test the / route."""
        response = self.client.get('/')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)

if __name__ == '__main__':
    unittest.main()
