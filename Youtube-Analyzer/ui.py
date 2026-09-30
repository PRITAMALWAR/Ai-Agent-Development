import streamlit as st

from youtube_analyzer import analyze_video


st.set_page_config(
    page_title="YouTube Analyzer",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube Video Analyzer")

youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

if st.button("Analyze Video"):

    if not youtube_url:
        st.warning("Please enter a YouTube URL.")

    else:
        with st.spinner("Analyzing video..."):

            try:
                result = analyze_video(youtube_url)

                st.markdown("## 📊 Video Analysis")
                st.markdown(result)

            except Exception as e:
                st.error(f"Something went wrong: {e}")