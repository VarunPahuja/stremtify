"""
Archive.org scraper - consolidated from archive_scraper.py and archive_scrapertrack.py
"""
import aiohttp
import asyncio
import urllib.parse
from typing import List, Tuple, Optional, Dict
import sys
import os

# Add the config directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from config.settings import Config


class ArchiveScraper:
    """Handles Archive.org FLAC album searching and verification."""
    
    def __init__(self):
        """Initialize the scraper with configuration."""
        self.base_search_url = Config.ARCHIVE_BASE_SEARCH_URL
        self.base_metadata_url = Config.ARCHIVE_BASE_METADATA_URL
        self.base_download_url = Config.ARCHIVE_BASE_DOWNLOAD_URL
        self.max_results = Config.ARCHIVE_MAX_RESULTS
        self.timeout = Config.ARCHIVE_TIMEOUT
        self.min_flac_size = Config.MIN_FLAC_SIZE
        self.google_search_url = Config.GOOGLE_SEARCH_URL
    
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> dict:
        """Fetch JSON data from URL with error handling."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                response.raise_for_status()
                return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
            return {}
    
    async def verify_flac_download(self, session: aiohttp.ClientSession, url: str) -> bool:
        """Verify that a FLAC file is accessible and valid."""
        try:
            async with session.head(url, allow_redirects=True, timeout=aiohttp.ClientTimeout(total=self.timeout)) as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '').lower()
                    content_length = int(response.headers.get('Content-Length', '0'))
                    return ('flac' in content_type or url.lower().endswith('.flac')) and content_length > self.min_flac_size
            return False
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
            return False
    
    async def search_album_return_links(self, session: aiohttp.ClientSession, album_name: str, 
                                      artist_name: Optional[str] = None, max_results: Optional[int] = None) -> List[Dict]:
        """Search Archive.org for albums and return metadata."""
        if max_results is None:
            max_results = self.max_results
            
        query_parts = [
            f'title:"{album_name}"',
            'format:"Flac"',
            'mediatype:"audio"'
        ]
        if artist_name:
            query_parts.append(f'creator:"{artist_name}"')

        params = {
            'q': ' AND '.join(query_parts),
            'fl[]': ['identifier', 'title', 'creator', 'year', 'downloads', 'item_size'],
            'rows': max_results,
            'output': 'json',
            'sort[]': 'downloads desc'
        }

        search_url = self.base_search_url + '?' + urllib.parse.urlencode(params, doseq=True)
        data = await self.fetch(session, search_url)
        
        if not data or 'response' not in data:
            return []
        
        results = []
        for doc in data['response']['docs']:
            identifier = doc.get('identifier', '')
            if not identifier:
                continue
            try:
                size = int(doc.get('item_size', '0'))
            except (ValueError, TypeError):
                size = 0
            results.append({
                'identifier': identifier,
                'title': doc.get('title', 'Unknown Album'),
                'artist': doc.get('creator', 'Unknown Artist'),
                'year': doc.get('year', 'Unknown Year'),
                'downloads': int(doc.get('downloads', 0)),
                'size': size,
                'url': f"https://archive.org/details/{identifier}"
            })
        return results
    
    async def get_verified_flac_files(self, session: aiohttp.ClientSession, identifier: str) -> Tuple[Optional[str], List[str]]:
        """Get verified FLAC files and torrent link for an archive."""
        metadata_url = f"{self.base_metadata_url}{identifier}"
        data = await self.fetch(session, metadata_url)
        if not data or 'files' not in data:
            return None, []

        torrent_link = None
        potential_flacs = []

        for file in data.get("files", []):
            name = file.get("name", "")
            format_type = str(file.get("format", "")).lower()
            
            if name.endswith(".torrent"):
                torrent_link = f"{self.base_download_url}{identifier}/{name}"
            elif "flac" in format_type or name.lower().endswith('.flac'):
                file_url = f"{self.base_download_url}{identifier}/{name}"
                try:
                    size = int(file.get('size', 0))
                except (ValueError, TypeError):
                    size = 0
                if size > self.min_flac_size:
                    potential_flacs.append((file_url, size))

        verified_flacs = []
        if potential_flacs:
            verification_tasks = [self.verify_flac_download(session, url) for url, _ in potential_flacs]
            results = await asyncio.gather(*verification_tasks)

            for (url, _), valid in zip(potential_flacs, results):
                if valid:
                    verified_flacs.append(url)
        
        return torrent_link, verified_flacs
    
    async def search_albums(self, album_name: str, artist_name: Optional[str] = None) -> List[Dict]:
        """Basic album search - returns list of albums."""
        async with aiohttp.ClientSession() as session:
            albums = await self.search_album_return_links(session, album_name, artist_name)
            return albums
    
    async def advanced_search(self, album_name: str, artist_name: Optional[str] = None) -> Dict:
        """Advanced search with FLAC verification."""
        async with aiohttp.ClientSession() as session:
            albums = await self.search_album_return_links(session, album_name, artist_name)
            
            for album in albums:
                torrent, flacs = await self.get_verified_flac_files(session, album["identifier"])
                if flacs:
                    return {
                        "verified_album": album,
                        "torrent": torrent,
                        "flacs": flacs
                    }
        
        # Fallback to Google search
        google_query = f'"{album_name}" internet archive flac'
        if artist_name:
            google_query = f'"{album_name}" "{artist_name}" internet archive flac'
        google_url = self.google_search_url + urllib.parse.quote(google_query)
        return {"google_fallback": google_url}
    
    def session_context(self):
        """Create an aiohttp session context manager."""
        return aiohttp.ClientSession()


async def main_scraper(album_name: str, artist_name: Optional[str] = None):
    """Main scraper function for backward compatibility."""
    scraper = ArchiveScraper()
    return await scraper.search_albums(album_name, artist_name)


async def advanced_search(album_name: str, artist_name: Optional[str] = None):
    """Advanced search function for backward compatibility."""
    scraper = ArchiveScraper()
    return await scraper.advanced_search(album_name, artist_name)


def main():
    """Main function for command-line usage."""
    scraper = ArchiveScraper()
    
    artist = input("Enter artist name (or leave blank): ").strip() or None
    album = input("Enter album name: ").strip()
    
    if not album:
        print("❌ Album name is required")
        return
    
    print(f"\n🔍 Searching for album: {album} by {artist or 'any artist'}")
    
    async def run_search():
        results = await scraper.search_albums(album, artist)
        
        if not results:
            print("❌ No results found.")
            return
        
        for i, album_info in enumerate(results, 1):
            print(f"\n#{i} 🗂️ {album_info['title']} by {album_info['artist']} ({album_info['year']})")
            print(f"   📊 Downloads: {album_info['downloads']}")
            print(f"   💾 Size: {album_info['size'] // (1024*1024)} MB")
            print(f"   🔗 Archive Link: {album_info['url']}")
    
    asyncio.run(run_search())


if __name__ == "__main__":
    main()
