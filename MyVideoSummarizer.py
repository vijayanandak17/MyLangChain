import streamlit as st
import re
import sys

# Check if the required package is available
def check_dependencies():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        return True, YouTubeTranscriptApi
    except ImportError as e:
        return False, str(e)

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/embed/)([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_transcript(url, api_class):
    """Get transcript from YouTube video"""
    try:
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            return "Error: Invalid YouTube URL"
        
        st.info(f"Extracted video ID: {video_id}")
        
        # Get transcript using the API
        transcript = api_class.get_transcript(video_id)
        
        # Combine all text
        full_text = " ".join([entry['text'] for entry in transcript])
        
        return full_text
        
    except Exception as e:
        return f"Error: {str(e)}"

def summarize_transcript(transcript_text):
    """Simple text summarization"""
    if not transcript_text or transcript_text.startswith("Error:"):
        return "Cannot summarize due to transcript error"
    
    # Basic summarization - extract key sentences
    sentences = transcript_text.split('.')
    
    # Filter out very short sentences and take first meaningful ones
    meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(meaningful_sentences) >= 3:
        summary = '. '.join(meaningful_sentences[:3]) + '.'
    else:
        summary = '. '.join(meaningful_sentences) + '.'
    
    return summary

# Streamlit UI
st.title("🎥 YouTube Video Transcriber & Summarizer")

# Check dependencies first
dependency_ok, api_or_error = check_dependencies()

if not dependency_ok:
    st.error(f"❌ Missing required package: {api_or_error}")
    st.info("Please install the required package by running:")
    st.code("pip install youtube-transcript-api")
    st.stop()

st.success("✅ All dependencies loaded successfully!")

# URL input
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Get Transcript & Summary"):
    if url:
        with st.spinner("Getting transcript..."):
            transcript = get_youtube_transcript(url, api_or_error)
        
        if not transcript.startswith("Error:"):
            st.success("Transcript retrieved successfully!")
            
            # Display transcript
            st.subheader("📝 Full Transcript")
            with st.expander("View Full Transcript"):
                st.text_area("Transcript", transcript, height=300)
            
            # Display summary
            st.subheader("📋 Summary")
            summary = summarize_transcript(transcript)
            st.write(summary)
            
            # Display stats
            st.subheader("📊 Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Characters", len(transcript))
            with col2:
                st.metric("Total Words", len(transcript.split()))
            with col3:
                st.metric("Estimated Reading Time", f"{len(transcript.split()) // 200 + 1} min")
                
        else:
            st.error(transcript)
    else:
        st.warning("Please enter a YouTube URL")

# Debugging information in sidebar
st.sidebar.header("🔧 Debug Info")
st.sidebar.write(f"Python version: {sys.version}")

try:
    import youtube_transcript_api
    st.sidebar.write(f"Package version: {youtube_transcript_api.__version__ if hasattr(youtube_transcript_api, '__version__') else 'Unknown'}")
    st.sidebar.write(f"Package location: {youtube_transcript_api.__file__}")
except:
    st.sidebar.write("Package not properly imported")

# Instructions
st.sidebar.header("📚 How to use")
st.sidebar.write("1. Paste a YouTube URL")
st.sidebar.write("2. Click 'Get Transcript & Summary'")
st.sidebar.write("3. View the results")

st.sidebar.header("⚠️ Note")
st.sidebar.write("- Only works with videos that have transcripts/captions")
st.sidebar.write("- May not work with private or restricted videos")