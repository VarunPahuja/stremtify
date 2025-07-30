"""
Streamlit UI for Stremtify - moved from archive_scrapertrack.py
"""
import streamlit as st
import asyncio
import sys
import os
from pathlib import Path

# Setup path for imports
def setup_imports():
    """Setup Python path for proper imports."""
    current_file = Path(__file__).resolve()
    src_dir = current_file.parent.parent  # Go up from ui/ to src/
    project_root = src_dir.parent  # Go up from src/ to project root
    config_dir = project_root / 'config'
    
    for path in [str(src_dir), str(config_dir), str(project_root)]:
        if path not in sys.path:
            sys.path.insert(0, path)

# Setup imports
setup_imports()

try:
    from archive.scraper import ArchiveScraper
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.error("Please make sure the project structure is correct and dependencies are installed.")
    st.stop()


def main():
    """Main Streamlit application."""
    st.title("🎶 Stremtify FLAC Album Scraper")

    # Initialize session state
    if "search_results" not in st.session_state:
        st.session_state.search_results = []
    if "verified_search" not in st.session_state:
        st.session_state.verified_search = {}

    # UI Elements
    mode = st.radio("Select Mode:", ["Search", "Advanced Search"])
    artist = st.text_input("Artist Name (optional):")
    album = st.text_input("Album Name:")

    # Search button
    if st.button("Go"):
        if not album:
            st.warning("Please enter at least the album name.")
        else:
            st.session_state.search_results = []
            st.session_state.verified_search = {}
            
            scraper = ArchiveScraper()
            
            if mode == "Search":
                with st.spinner("Searching Archive.org..."):
                    st.session_state.search_results = asyncio.run(
                        scraper.search_albums(album, artist or None)
                    )
            else:
                with st.spinner("Searching and verifying..."):
                    result = asyncio.run(
                        scraper.advanced_search(album, artist or None)
                    )
                
                if "verified_album" in result:
                    album_info = result["verified_album"]
                    st.success(f"✅ Verified FLAC Album Found: {album_info['title']} by {album_info['artist']} ({album_info['year']})")
                    st.write(f"**Downloads:** {album_info['downloads']}")
                    st.write(f"**Size:** {album_info['size']//(1024*1024)} MB")
                    st.write(f"[Archive Link]({album_info['url']})")

                    if result["torrent"]:
                        st.info(f"[🧲 Torrent Link]({result['torrent']})")

                    st.write(f"**FLAC Files:**")
                    for flac_url in result["flacs"][:5]:
                        st.write(f"[{flac_url.split('/')[-1]}]({flac_url})")
                    if len(result["flacs"]) > 5:
                        st.write(f"...and {len(result['flacs']) - 5} more.")

                elif "google_fallback" in result:
                    st.warning("No verified FLAC albums found. Try this Google search (results not verified):")
                    st.write(f"[🔎 Google Search]({result['google_fallback']})")

    # Show Search Results if available
    if mode == "Search" and st.session_state.search_results:
        st.success(f"Found {len(st.session_state.search_results)} album(s):")
        for idx, album_info in enumerate(st.session_state.search_results, 1):
            with st.expander(f"{idx}. {album_info['title']} by {album_info['artist']} ({album_info['year']})"):
                st.write(f"**Downloads:** {album_info['downloads']}")
                st.write(f"**Size:** {album_info['size']//(1024*1024)} MB")
                st.write(f"[Archive Link]({album_info['url']})")

                verify_key = f"verify_{album_info['identifier']}"
                if st.button(f"🔎 Verify FLACs", key=verify_key):
                    with st.spinner("Verifying FLAC files..."):
                        scraper = ArchiveScraper()
                        
                        async def verify_and_store():
                            async with scraper.session_context() as session:
                                torrent, flacs = await scraper.get_verified_flac_files(session, album_info['identifier'])
                                return {"torrent": torrent, "flacs": flacs}
                        
                        result = asyncio.run(verify_and_store())
                        st.session_state.verified_search[album_info['identifier']] = result

                if album_info['identifier'] in st.session_state.verified_search:
                    result = st.session_state.verified_search[album_info['identifier']]
                    if result["torrent"]:
                        st.info(f"[🧲 Torrent Link]({result['torrent']})")
                    
                    if result["flacs"]:
                        st.success(f"Found {len(result['flacs'])} valid FLAC files:")
                        for flac_url in result["flacs"][:5]:
                            st.write(f"[{flac_url.split('/')[-1]}]({flac_url})")
                        if len(result["flacs"]) > 5:
                            st.write(f"...and {len(result['flacs']) - 5} more.")
                    else:
                        st.error("No valid FLAC files found.")


if __name__ == "__main__":
    main()
