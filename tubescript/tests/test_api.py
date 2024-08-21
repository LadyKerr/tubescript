# test_api.py

import unittest
from flask import Flask
from api import app
from unittest.mock import patch

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_missing_url_parameter(self):
        response = self.app.get('/api/transcript')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing YouTube URL parameter', response.get_json()['error'])

    @patch('api.get_video_id')
    def test_invalid_youtube_url(self, mock_get_video_id):
        mock_get_video_id.side_effect = ValueError("Invalid YouTube URL")
        response = self.app.get('/api/transcript?url=invalid_url')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid YouTube URL', response.get_json()['error'])

    @patch('api.get_video_id')
    @patch('api.get_video_transcript')
    def test_successful_transcript_retrieval(self, mock_get_video_transcript, mock_get_video_id):
        mock_get_video_id.return_value = 'valid_video_id'
        mock_get_video_transcript.return_value = ('transcript text', 'Success')
        
        response = self.app.get('/api/transcript?url=valid_url')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['transcript'], 'transcript text')
        self.assertEqual(response.get_json()['message'], 'Success')

    @patch('api.get_video_id')
    @patch('api.get_video_transcript')
    def test_failed_transcript_retrieval(self, mock_get_video_transcript, mock_get_video_id):
        mock_get_video_id.return_value = 'valid_video_id'
        mock_get_video_transcript.return_value = (None, 'Transcript not found')
        
        response = self.app.get('/api/transcript?url=valid_url')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Transcript not found', response.get_json()['error'])

    @patch('api.get_video_id')
    @patch('api.get_video_transcript')
    def test_unexpected_error(self, mock_get_video_transcript, mock_get_video_id):
        mock_get_video_id.side_effect = Exception("Unexpected error")
        
        response = self.app.get('/api/transcript?url=valid_url')
        self.assertEqual(response.status_code, 500)
        self.assertIn('An unexpected error occurred', response.get_json()['error'])

if __name__ == '__main__':
    unittest.main()