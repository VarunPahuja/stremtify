#!/usr/bin/env python3
"""
Setup script for Stremtify
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None


def main():
    """Main setup function."""
    print("🎶 Setting up Stremtify...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create virtual environment if it doesn't exist
    if not Path(".venv").exists():
        run_command(f"{sys.executable} -m venv .venv", "Creating virtual environment")
    
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = ".venv\\Scripts\\pip.exe"
        python_path = ".venv\\Scripts\\python.exe"
    else:  # Unix/Linux/Mac
        pip_path = ".venv/bin/pip"
        python_path = ".venv/bin/python"
    
    # Install requirements
    if Path("requirements.txt").exists():
        run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies")
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists() and Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
        print("📝 Created .env file from template")
        print("⚠️  Please edit .env file and add your Spotify API credentials")
    
    # Test installation
    print("\n🧪 Testing installation...")
    test_result = run_command(f"{python_path} -c \"import streamlit, spotipy, aiohttp; print('All dependencies imported successfully')\"", "Testing imports")
    
    if test_result:
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit .env file with your Spotify API credentials")
        print("2. Run the app: streamlit run app.py")
        print("3. Or use individual modules:")
        print("   - python src/spotify/playlist_parser.py")
        print("   - python src/archive/scraper.py")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
