# 🎶 Stremtify

A tool for finding FLAC albums on Archive.org and managing Spotify playlists.

## Features

- 🎧 **Spotify Integration**: Parse playlists and extract track information
- 🔍 **Archive.org Scraper**: Search for FLAC albums with verification
- 🌐 **Web Interface**: User-friendly Streamlit interface
- ⚡ **Async Operations**: Fast concurrent searching and verification

## Project Structure

```
stremtify/
├── src/
│   ├── spotify/          # Spotify API integration
│   │   └── playlist_parser.py
│   ├── archive/          # Archive.org scraping
│   │   └── scraper.py
│   └── ui/              # User interfaces
│       └── streamlit_app.py
├── config/
│   └── settings.py      # Configuration management
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md
```

## Installation

### Quick Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/stremtify.git
   cd stremtify
   ```

2. Run the setup script:
   ```bash
   python setup.py
   ```

3. Edit `.env` file with your Spotify API credentials

4. Run the app:
   ```bash
   streamlit run app.py
   ```

### Manual Setup
1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/Mac: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and fill in your Spotify API credentials
6. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

### Web Interface (Recommended)
Choose one of these methods to run the Streamlit app:

**Method 1 - Simple Runner:**
```bash
python run.py
```

**Method 2 - Main App:**
```bash
streamlit run app.py
```

**Method 3 - Direct:**
```bash
streamlit run src/ui/streamlit_app.py
```

### Command Line
#### Spotify Playlist Parser
```bash
python src/spotify/playlist_parser.py
```

#### Archive Scraper
```bash
python src/archive/scraper.py
```

## Configuration

### Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new app
3. Copy Client ID and Client Secret to your `.env` file

### Environment Variables
Copy `.env.example` to `.env` and configure:
```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Development

The project is structured as Python packages with proper imports and configuration management. Each module can be run independently or imported into other projects.

## Legacy Files

The following files are kept for backward compatibility:
- `get_token_and_tracks.py` (use `src/spotify/playlist_parser.py` instead)
- `archive_scraper.py` (use `src/archive/scraper.py` instead)
- `archive_scrapertrack.py` (use `src/ui/streamlit_app.py` instead)

## Contributing

1. Follow the existing code structure
2. Add type hints to new code
3. Include error handling
4. Update this README for new features
