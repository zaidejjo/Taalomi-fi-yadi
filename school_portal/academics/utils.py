import re
import logging
import traceback
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

def validate_youtube_urls(video_urls):
    """
    Validate and clean YouTube video URLs.
    
    Args:
        video_urls (list): List of YouTube video URLs to validate
        
    Returns:
        tuple: (cleaned_urls, errors)
            - cleaned_urls: List of valid, embedded YouTube URLs
            - errors: Dictionary mapping original URLs to their error messages
    """
    cleaned_urls = []
    errors = {}
    
    for url in video_urls:
        try:
            # Check if URL is empty or None
            if not url:
                raise ValueError("Empty URL provided")
                
            # Parse the URL
            parsed_url = urlparse(url)
            
            # Validate HTTPS
            if parsed_url.scheme != 'https':
                raise ValueError("URL must use HTTPS protocol")
                
            # Validate YouTube domain
            if not parsed_url.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']:
                raise ValueError("Not a valid YouTube URL")
                
            # Handle different YouTube URL formats
            if 'embed' in parsed_url.path:
                # Already in embed format, just validate the video ID
                video_id = parsed_url.path.split('/')[-1]
                if not re.match(r'^[\w-]{11}$', video_id):
                    raise ValueError("Invalid YouTube video ID")
                cleaned_urls.append(f'https://www.youtube.com/embed/{video_id}')
                
            elif 'watch' in parsed_url.path:
                # Convert watch URL to embed format
                params = parse_qs(parsed_url.query)
                if 'v' not in params:
                    raise ValueError("Missing video ID parameter")
                    
                video_id = params['v'][0]
                if not re.match(r'^[\w-]{11}$', video_id):
                    raise ValueError("Invalid YouTube video ID")
                    
                cleaned_urls.append(f'https://www.youtube.com/embed/{video_id}')
                
            elif 'youtu.be' in parsed_url.netloc:
                # Handle shortened URLs
                video_id = parsed_url.path.lstrip('/')
                if not re.match(r'^[\w-]{11}$', video_id):
                    raise ValueError("Invalid YouTube video ID")
                    
                cleaned_urls.append(f'https://www.youtube.com/embed/{video_id}')
                
            else:
                raise ValueError("Unsupported YouTube URL format")
                
        except Exception as e:
            # Log the full error with traceback
            logger.error(f"Error processing URL '{url}': {str(e)}")
            logger.error(traceback.format_exc())
            errors[url] = str(e)
            
    return cleaned_urls, errors