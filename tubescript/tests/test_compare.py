import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
from compare import main

class CompareTestCase(unittest.TestCase):

    @patch('compare.load_css')
    @patch('compare.st')
    @patch('compare.compare_transcripts')
    def test_main(self, mock_compare_transcripts, mock_st, mock_load_css):
        # Mocking Streamlit functions
        mock_st.text_input.side_effect = ["https://www.youtube.com/watch?v=video1", "https://www.youtube.com/watch?v=video2"]
        mock_st.button.return_value = True

        # Run the main function
        main()

        # Check if load_css is called
        mock_load_css.assert_called_once()

        # Check if title and subheader are set correctly
        mock_st.title.assert_called_once_with("TubeScript Comparison 📝")
        mock_st.subheader.assert_called_once_with("Compare transcripts of two YouTube videos")

        # Check if text inputs are called
        mock_st.text_input.assert_any_call("Enter first YouTube URL:")
        mock_st.text_input.assert_any_call("Enter second YouTube URL:")

        # Check if compare_transcripts is called with correct arguments
        mock_compare_transcripts.assert_called_once_with("https://www.youtube.com/watch?v=video1", "https://www.youtube.com/watch?v=video2")

    @patch('compare.load_css')
    @patch('compare.st')
    def test_main_missing_urls(self, mock_st, mock_load_css):
        # Mocking Streamlit functions
        mock_st.text_input.side_effect = ["", ""]
        mock_st.button.return_value = True

        # Run the main function
        main()

        # Check if load_css is called
        mock_load_css.assert_called_once()

        # Check if error is shown when URLs are missing
        mock_st.error.assert_called_once_with("Please enter both YouTube URLs.")

if __name__ == "__main__":
    unittest.main()