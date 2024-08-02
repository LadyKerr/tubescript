import streamlit as st
import app
import compare

st.set_page_config(page_title="TubeScript", page_icon="📝", layout="wide")

PAGES = {
    "Home": app,
    "Compare Transcripts": compare
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.main()