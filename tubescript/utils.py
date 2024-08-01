import re
import os
from typing import Tuple, Optional
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def is_valid_youtube_url(url: str) -> bool:
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$'
    return bool(re.match(youtube_regex, url))

def get_video_id(youtube_url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    raise ValueError("Invalid YouTube URL")

def sanitize_filename(filename: str) -> str:
    """Remove or replace characters that are unsafe for filenames."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def save_transcript(transcript: list, file_path: str) -> None:
    """Save the transcript to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for entry in transcript:
            file.write(f"{entry['text']}\n")

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