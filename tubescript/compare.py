import streamlit as st
from utils import get_video_id, get_video_transcript, is_valid_youtube_url, load_css, compare_transcripts

def main():
    load_css()
    st.title("TubeScript Comparison 📝")
    st.subheader("Compare transcripts of two YouTube videos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        youtube_url1 = st.text_input("Enter first YouTube URL:")
    
    with col2:
        youtube_url2 = st.text_input("Enter second YouTube URL:")
    
    if st.button("Compare Transcripts"):
        if youtube_url1 and youtube_url2:
            compare_transcripts(youtube_url1, youtube_url2)
        else:
            st.error("Please enter both YouTube URLs.")

if __name__ == "__main__":
    main()