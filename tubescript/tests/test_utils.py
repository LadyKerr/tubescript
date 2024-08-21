import unittest
from unittest.mock import patch, MagicMock, mock_open
from utils import (
    load_css, highlight_diff, is_valid_youtube_url, get_video_id,
    sanitize_filename, save_transcript, get_video_transcript,
    display_transcript, compare_transcripts
)
from youtube_transcript_api import NoTranscriptFound

class UtilsTestCase(unittest.TestCase):

    @patch('streamlit.markdown')
    def test_load_css(self, mock_markdown):
        load_css()
        mock_markdown.assert_called_once_with("""
        <style>
        .stApp {
            background-color: #fee3e8;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
        }
        .stButton > button {
            background-color: #ff4b4b;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    def test_highlight_diff(self):
        text1 = "line1\nline2\nline3"
        text2 = "line1\nline2\nline4"
        highlighted1, highlighted2 = highlight_diff(text1, text2)
        self.assertIn("<span style='background-color: #ffcccc'>line3</span>", highlighted1)
        self.assertIn("<span style='background-color: #ffcccc'>line4</span>", highlighted2)

    def test_is_valid_youtube_url(self):
        valid_urls = [
            "https://www.youtube.com/watch?v=abcdefghijk",
            "https://youtu.be/abcdefghijk"
        ]
        invalid_urls = [
            "https://www.example.com/watch?v=abcdefghijk",
            "https://youtube.com"
        ]
        for url in valid_urls:
            self.assertTrue(is_valid_youtube_url(url))
        for url in invalid_urls:
            self.assertFalse(is_valid_youtube_url(url))

    def test_get_video_id(self):
        valid_url = "https://www.youtube.com/watch?v=abcdefghijk"
        invalid_url = "https://www.example.com/watch?v=abcdefghijk"
        self.assertEqual(get_video_id(valid_url), "abcdefghijk")
        with self.assertRaises(ValueError):
            get_video_id(invalid_url)

    def test_sanitize_filename(self):
        filename = "unsafe<>:\"/\\|?*filename"
        sanitized = sanitize_filename(filename)
        self.assertEqual(sanitized, "unsafefilename")

    @patch('builtins.open', new_callable=mock_open)
    def test_save_transcript(self, mock_file):
        transcript = [{'text': 'line1'}, {'text': 'line2'}]
        save_transcript(transcript, 'dummy_path.txt')
        mock_file.assert_called_once_with('dummy_path.txt', 'w', encoding='utf-8')
        mock_file().write.assert_any_call("line1\n")
        mock_file().write.assert_any_call("line2\n")

    @patch('utils.YouTubeTranscriptApi.get_transcript')
    @patch('utils.YouTube')
    @patch('utils.save_transcript')
    def test_get_video_transcript(self, mock_save_transcript, mock_youtube, mock_get_transcript):
        mock_get_transcript.return_value = [{'text': 'line1'}, {'text': 'line2'}]
        mock_youtube.return_value.title = "Test Video"
        transcript, message = get_video_transcript("valid_video_id")
        self.assertIn("line1", transcript)
        self.assertIn("line2", transcript)
        self.assertIn("The transcript is saved at:", message)

        mock_get_transcript.side_effect = NoTranscriptFound
        transcript, message = get_video_transcript("valid_video_id")
        self.assertIsNone(transcript)
        self.assertEqual(message, "A transcript is not available for this video.")

        mock_get_transcript.side_effect = Exception("Unexpected error")
        transcript, message = get_video_transcript("valid_video_id")
        self.assertIsNone(transcript)
        self.assertIn("An error occurred:", message)

    @patch('streamlit.subheader')
    @patch('streamlit.success')
    @patch('streamlit.text_area')
    @patch('streamlit.error')
    def test_display_transcript(self, mock_error, mock_text_area, mock_success, mock_subheader):
        column = MagicMock()
        display_transcript("transcript text", "Success message", column, "Title")
        mock_subheader.assert_called_once_with("Title")
        mock_success.assert_called_once_with("Success message")
        mock_text_area.assert_called_once_with("", value="transcript text", height=500)

        display_transcript(None, "Success message", column, "Title")
        mock_error.assert_called_once_with("Transcript not available")

    @patch('utils.st.columns')
    @patch('utils.display_transcript')
    @patch('utils.get_video_transcript')
    @patch('utils.get_video_id')
    @patch('utils.is_valid_youtube_url')
    def test_compare_transcripts(self, mock_is_valid_youtube_url, mock_get_video_id, mock_get_video_transcript, mock_display_transcript, mock_columns):
        mock_is_valid_youtube_url.return_value = True
        mock_get_video_id.side_effect = ["video_id1", "video_id2"]
        mock_get_video_transcript.side_effect = [("transcript1", "message1"), ("transcript2", "message2")]
        mock_columns.return_value = (MagicMock(), MagicMock())

        compare_transcripts("url1", "url2")
        mock_display_transcript.assert_any_call("transcript1", "message1", mock_columns.return_value[0], "Transcript 1")
        mock_display_transcript.assert_any_call("transcript2", "message2", mock_columns.return_value[1], "Transcript 2")

        mock_is_valid_youtube_url.return_value = False
        compare_transcripts("invalid_url1", "invalid_url2")
        mock_display_transcript.assert_not_called()

if __name__ == '__main__':
    unittest.main()