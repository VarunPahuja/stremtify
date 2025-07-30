"""
Main entry point for Stremtify Streamlit application.
This file should be run with: streamlit run app.py
"""
import sys
import os
from pathlib import Path

# Setup Python path for imports
def setup_python_path():
    """Add necessary directories to Python path for imports."""
    current_dir = Path(__file__).parent.absolute()
    src_dir = current_dir / 'src'
    config_dir = current_dir / 'config'
    
    # Add directories to Python path if they exist
    for directory in [src_dir, config_dir, current_dir]:
        if directory.exists():
            sys.path.insert(0, str(directory))

# Setup path immediately
setup_python_path()

# Now we can import everything
import streamlit as st

try:
    from ui.streamlit_app import main as streamlit_main
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.error("💡 Make sure you've installed dependencies: `pip install -r requirements.txt`")
    st.error("💡 Or run the setup script: `python setup.py`")
    st.stop()

# Check environment
def check_environment():
    """Check if the environment is properly set up."""
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists() and env_example.exists():
        st.warning("⚠️ .env file not found. Please copy .env.example to .env and configure your Spotify API credentials.")
        st.info("💡 Tip: Run `python setup.py` for automated setup.")
        return False
    return True

# Main execution
if __name__ == "__main__":
    # Check environment
    check_environment()
    
    # Run the main Streamlit app
    streamlit_main()
