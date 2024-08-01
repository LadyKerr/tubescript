import streamlit as st
from utils import get_video_id, get_video_transcript

def main():
    # Inject custom CSS
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fee3e8;
        }
        .st-br {
        background-color: #ffffff;
        color: #000000;
        }
        .st-bc {
        background-color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("TubeScript 📝")
    st.subheader("Get the transcript of any YouTube video")
    youtube_url = st.text_input("Enter a YouTube URL:")
    
    if st.button("Get Transcript"):
        try:
            video_id = get_video_id(youtube_url)
            transcript_text, result_message = get_video_transcript(video_id)
            st.success(result_message)
            if transcript_text:
                st.markdown("### Here's your transcript:")
                st.code(transcript_text, language="text")
        except ValueError as ve:
            st.error(str(ve))

if __name__ == "__main__":
    main()