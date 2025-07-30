"""
Backward compatibility wrapper for archive_scrapertrack.py
This file ensures your existing Streamlit app continues to work.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import and run the new streamlit app
from ui.streamlit_app import main

if __name__ == "__main__":
    main()
