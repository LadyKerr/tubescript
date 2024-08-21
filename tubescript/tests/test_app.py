# test_app.py

import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from app import main

class AppTestCase(unittest.TestCase):
    @patch('app.load_css')
    @patch('app.st.text_input')
    @patch('app.st.button')
    @patch('app.st.error')
    @patch('app.st.success')
    @patch('app.st.markdown')
    @patch('app.st.code')
    @patch('app.is_valid_youtube_url')
    @patch('app.get_video_id')
    @patch('app.get_video_transcript')
    def test_main(self, mock_get_video_transcript, mock_get_video_id, mock_is_valid_youtube_url, mock_code, mock_markdown, mock_success, mock_error, mock_button, mock_text_input, mock_load_css):
        # Mock the CSS loading
        main()
        mock_load_css.assert_called_once()

        # Test no URL entered
        mock_text_input.return_value = ""
        mock_button.return_value = True
        main()
        mock_error.assert_called_with("Please enter a YouTube URL.")

        # Test invalid URL entered
        mock_text_input.return_value = "invalid_url"
        mock_is_valid_youtube_url.return_value = False
        main()
        mock_error.assert_called_with("Invalid YouTube URL. Please enter a valid URL.")

        # Test valid URL and successful transcript retrieval
        mock_text_input.return_value = "valid_url"
        mock_is_valid_youtube_url.return_value = True
        mock_get_video_id.return_value = "valid_video_id"
        mock_get_video_transcript.return_value = ("transcript text", "Success")
        main()
        mock_success.assert_called_with("Success")
        mock_markdown.assert_called_with("### Here's your transcript:")
        mock_code.assert_called_with("transcript text", language="text")

        # Test ValueError in get_video_id
        mock_get_video_id.side_effect = ValueError("Invalid YouTube URL")
        main()
        mock_error.assert_called_with("Invalid YouTube URL")

        # Test unexpected exception
        mock_get_video_id.side_effect = Exception("Unexpected error")
        main()
        mock_error.assert_called_with("An unexpected error occurred: Unexpected error")

if __name__ == '__main__':
    unittest.main()