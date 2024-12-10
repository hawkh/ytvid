import streamlit as st
import os
from pytube import YouTube
from downloader import get_stream_info, download_video

def main():
    st.set_page_config(
        page_title="YouTube Video Downloader", 
        page_icon="📥", 
        layout="centered"
    )
    
    st.title("🎥 YouTube Video Downloader")
    
    # URL Input
    url = st.text_input("Enter YouTube Video URL", placeholder="https://youtu.be/...")
    
    # Download directory selection
    download_path = st.text_input(
        "Download Path", 
        value=os.path.expanduser("~/Downloads"),
        help="Select the directory where the video will be saved"
    )
    
    # Fetch and display stream information
    if url:
        try:
            # Disable error messages
            st.spinner("Fetching video streams...")
            
            # Get YouTube object
            yt = YouTube(url)
            
            # Display basic video info
            col1, col2 = st.columns(2)
            with col1:
                st.image(yt.thumbnail_url, caption="Video Thumbnail", width=300)
            with col2:
                st.write(f"**Title:** {yt.title}")
                st.write(f"**Author:** {yt.author}")
                st.write(f"**Length:** {yt.length} seconds")
            
            # Get stream information
            streams_info = get_stream_info(yt)
            
            # Create a dataframe for stream selection
            import pandas as pd
            df = pd.DataFrame(streams_info)
            st.dataframe(df, hide_index=True)
            
            # Stream selection
            selected_stream = st.selectbox(
                "Select Download Stream", 
                range(len(streams_info)), 
                format_func=lambda x: f"{streams_info[x]['res']} | {streams_info[x]['type']} | {streams_info[x]['filesize']}"
            )
            
            # Download button
            if st.button("Download Video", type="primary"):
                with st.spinner("Downloading Video..."):
                    final_path = download_video(url, download_path, selected_stream)
                    st.success(f"Video downloaded successfully to {final_path}")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
