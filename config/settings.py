"""
Configuration settings for Stremtify.
"""
import os
from typing import Optional


class Config:
    """Configuration class for application settings."""
    
    # Spotify Configuration
    SPOTIFY_CLIENT_ID: Optional[str] = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET: Optional[str] = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI: str = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8888/callback')
    SPOTIFY_SCOPE: str = "playlist-read-private playlist-read-collaborative"
    
    # Archive.org Configuration
    ARCHIVE_BASE_SEARCH_URL: str = "https://archive.org/advancedsearch.php"
    ARCHIVE_BASE_METADATA_URL: str = "https://archive.org/metadata/"
    ARCHIVE_BASE_DOWNLOAD_URL: str = "https://archive.org/download/"
    ARCHIVE_MAX_RESULTS: int = int(os.getenv('ARCHIVE_MAX_RESULTS', '10'))
    ARCHIVE_TIMEOUT: int = int(os.getenv('ARCHIVE_TIMEOUT', '10'))
    
    # File size limits
    MIN_FLAC_SIZE: int = 102400  # 100KB minimum for valid FLAC files
    
    # Selenium Configuration
    FIREFOX_BINARY_PATH: str = os.getenv('FIREFOX_BINARY_PATH', r'C:\Program Files\Mozilla Firefox\firefox.exe')
    GECKODRIVER_PATH: str = os.getenv('GECKODRIVER_PATH', 'geckodriver.exe')
    
    # Google Search
    GOOGLE_SEARCH_URL: str = "https://www.google.com/search?q="
    
    @classmethod
    def validate_spotify_config(cls) -> bool:
        """Validate that required Spotify configuration is present."""
        return bool(cls.SPOTIFY_CLIENT_ID and cls.SPOTIFY_CLIENT_SECRET)
