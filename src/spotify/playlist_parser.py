"""
Spotify playlist parser - moved from get_token_and_tracks.py
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict, Optional
import sys
import os

# Add the config directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.settings import Config


class SpotifyPlaylistParser:
    """Handles Spotify playlist parsing and track extraction."""
    
    def __init__(self):
        """Initialize the Spotify client."""
        if not Config.validate_spotify_config():
            raise ValueError(
                "Spotify credentials not configured. Please set SPOTIFY_CLIENT_ID and "
                "SPOTIFY_CLIENT_SECRET in your .env file. See .env.example for template."
            )
        
        self.client_id = Config.SPOTIFY_CLIENT_ID
        self.client_secret = Config.SPOTIFY_CLIENT_SECRET
        
        self.redirect_uri = Config.SPOTIFY_REDIRECT_URI
        self.scope = Config.SPOTIFY_SCOPE
        
        # Initialize Spotify client
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            show_dialog=True
        ))
    
    def extract_playlist_id(self, url: str) -> Optional[str]:
        """Extract playlist ID from Spotify URL."""
        parts = url.strip().split("/")
        if "playlist" in parts:
            return parts[parts.index("playlist") + 1].split("?")[0]
        elif "spotify:playlist:" in url:
            return url.split(":")[-1]
        return None
    
    def get_playlist_tracks(self, playlist_url: str) -> List[Dict[str, str]]:
        """Get all tracks from a Spotify playlist."""
        playlist_id = self.extract_playlist_id(playlist_url)
        
        if not playlist_id:
            raise ValueError("Invalid playlist URL")
        
        tracks = []
        results = self.sp.playlist_items(playlist_id)
        
        # Get all tracks (handle pagination)
        while results:
            for item in results['items']:
                track = item['track']
                if track:
                    tracks.append({
                        'title': track['name'],
                        'artist': ", ".join([a['name'] for a in track['artists']]),
                        'album': track['album']['name']
                    })
            
            # Check for more tracks (pagination)
            if results['next']:
                results = self.sp.next(results)
            else:
                break
        
        return tracks
    
    def print_tracklist(self, tracks: List[Dict[str, str]]) -> None:
        """Print formatted tracklist."""
        print("\n🎶 TRACKLIST:\n")
        for track in tracks:
            print(f"{track['artist']} - {track['title']} ({track['album']})")


def main():
    """Main function for backward compatibility."""
    parser = SpotifyPlaylistParser()
    
    playlist_url = input("🎧 Paste your Spotify playlist URL: ").strip()
    
    try:
        tracks = parser.get_playlist_tracks(playlist_url)
        parser.print_tracklist(tracks)
    except ValueError as e:
        print(f"❌ {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
