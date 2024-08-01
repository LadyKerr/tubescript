import re
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def get_video_id(youtube_url):
    # Extract the video ID from the YouTube URL
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]{11})", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_video_transcript(video_id):
    try:
        # Fetch the transcript using the video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Fetch the video title using pytube
        video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        video_title = video.title
        # Create a valid filename from the video title
        output_file = f"{video_title}.txt".replace(" ", "_").replace("/", "_")
        transcript_text = ""
        with open(output_file, 'w') as file:
            for entry in transcript:
                line = f"{entry['text']}\n"
                file.write(line)
                transcript_text += line
        return transcript_text, f"The transcript is also saved on your machine"
    except NoTranscriptFound:
        return None, "A transcript is not available for this video."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"