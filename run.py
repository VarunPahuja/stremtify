#!/usr/bin/env python3
"""
Simple runner for Stremtify Streamlit app.
Alternative to app.py with direct path to streamlit app.
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Run the Streamlit app directly."""
    # Get the path to the streamlit app
    current_dir = Path(__file__).parent
    streamlit_app_path = current_dir / 'src' / 'ui' / 'streamlit_app.py'
    
    if not streamlit_app_path.exists():
        print(f"❌ Streamlit app not found at: {streamlit_app_path}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    
    # Run streamlit directly on the file
    try:
        print(f"🚀 Starting Streamlit app: {streamlit_app_path}")
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', str(streamlit_app_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped.")

if __name__ == "__main__":
    main()
