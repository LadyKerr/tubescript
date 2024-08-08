import re
import os
import difflib
import streamlit as st
from typing import Tuple, Optional
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

# Load custom CSS for the Streamlit app
def load_css():
    """Load custom CSS for the Streamlit app."""
    st.markdown("""
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

# Highlight differences between two texts
def highlight_diff(text1: str, text2: str) -> tuple:
    """Highlight differences between two texts."""
    d = difflib.Differ()
    diff = list(d.compare(text1.splitlines(), text2.splitlines()))
    
    highlighted1 = []
    highlighted2 = []
    
    for line in diff:
        if line.startswith('  '):  # unchanged
            highlighted1.append(line[2:])
            highlighted2.append(line[2:])
        elif line.startswith('- '):  # in text1 but not text2
            highlighted1.append(f"<span style='background-color: #ffcccc'>{line[2:]}</span>")
        elif line.startswith('+ '):  # in text2 but not text1
            highlighted2.append(f"<span style='background-color: #ffcccc'>{line[2:]}</span>")
    
    return '\n'.join(highlighted1), '\n'.join(highlighted2)

# Check if a URL is a valid YouTube URL
def is_valid_youtube_url(url: str) -> bool:
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    return bool(re.match(youtube_regex, url))

# Extract the video ID from a YouTube URL
def get_video_id(youtube_url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    raise ValueError("Invalid YouTube URL")

# Sanitize a filename to make it safe for file systems
def sanitize_filename(filename: str) -> str:
    """Remove or replace characters that are unsafe for filenames."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# Save the transcript to a file
def save_transcript(transcript: list, file_path: str) -> None:
    """Save the transcript to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in transcript:
            file.write(f"{entry['text']}\n")

# Fetch and save the transcript for a given YouTube video ID
def get_video_transcript(video_id: str) -> Tuple[Optional[str], str]:
    """Fetch and save the transcript for a given YouTube video ID."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        safe_title = sanitize_filename(video.title)
        output_file = f"{safe_title}.txt"
        
        output_dir = os.path.join(os.path.expanduser("~"), "Documents", "Projects", "TubeScript_Transcripts")
        os.makedirs(output_dir, exist_ok=True)
        
        file_path = os.path.join(output_dir, output_file)
        save_transcript(transcript, file_path)
        
        transcript_text = "\n".join(entry['text'] for entry in transcript)
        return transcript_text, f"The transcript is saved at: {file_path}"
    except NoTranscriptFound:
        return None, "A transcript is not available for this video."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# Display the transcript in the given column
def display_transcript(transcript: str, message: str, column, title: str):
    """Display the transcript in the given column."""
    with column:
        st.subheader(title)
        st.success(message)
        if transcript:
            st.text_area("", value=transcript, height=500)
        else:
            st.error("Transcript not available")

# Compare two transcripts
def compare_transcripts(url1: str, url2: str):
    if url1 == url2:
        st.error("The URLs are identical. Please enter two different YouTube URLs for comparison.")
        return
    
    if not is_valid_youtube_url(url1) or not is_valid_youtube_url(url2):
        st.error("One or both URLs are invalid. Please enter valid YouTube URLs.")
        return
    
    try:
        video_id1 = get_video_id(url1)
        video_id2 = get_video_id(url2)
        
        transcript1, message1 = get_video_transcript(video_id1)
        transcript2, message2 = get_video_transcript(video_id2)
        
        col1, col2 = st.columns(2)
        
        display_transcript(transcript1, message1, col1, "Transcript 1")
        display_transcript(transcript2, message2, col2, "Transcript 2")
        
        if transcript1 and transcript2:
            highlighted1, highlighted2 = highlight_diff(transcript1, transcript2)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Highlighted Transcript 1")
                st.markdown(highlighted1, unsafe_allow_html=True)
            
            with col2:
                st.subheader("Highlighted Transcript 2")
                st.markdown(highlighted2, unsafe_allow_html=True)
    
    except ValueError as ve:
        st.error(f"Value Error: {str(ve)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
