import re
import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




def file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Fayl 5 MB dan katta bo\'lishi mumkin emas.')

def file_size_50(value):
    limit = 50 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Fayl 50 MB dan katta bo\'lishi mumkin emas.') 

def validate_youtube_link(value):
    """
    Validates YouTube URLs and checks if the video exists.
    Supports various YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/embed/VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    """
    if not value:
        raise ValidationError("YouTube havolasi talab etiladi.")
    
    # Regex pattern to match various YouTube URL formats
    youtube_regex = re.compile(
        r'^(?:https?://)?'  # Optional protocol
        r'(?:(?:www|m)\.)?'  # Optional www or m subdomain
        r'(?:youtu\.be/|youtube\.com/'  # Domain variations
        r'(?:embed/|v/|watch\?v=|watch\?.+&v=))'  # Path variations
        r'([\w\-]{11})'  # Video ID (11 characters)
        r'(?:\S+)?$'  # Optional additional parameters
    )
    
    match = youtube_regex.match(value)
    if not match:
        raise ValidationError(
            "YouTube havolasi noto'g'ri formatda. Iltimos, to'g'ri YouTube havolasini kiriting."
        )
    
    video_id = match.group(1)
    
    # Additional validation: Check if video exists by testing thumbnail
    if not _youtube_video_exists(video_id):
        raise ValidationError(
            "YouTube videosi mavjud emas yoki foydalanishga yaroqsiz."
        )


def _youtube_video_exists(video_id):
    """
    Check if YouTube video exists by requesting its thumbnail.
    Returns True if video exists, False otherwise.
    """
    try:
        # Try to get the medium quality thumbnail
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
        response = requests.head(thumbnail_url, timeout=5)
        
        # If we get a 200 response, try to verify it's not the default thumbnail
        if response.status_code == 200:
            # Get the actual image to check dimensions
            img_response = requests.get(thumbnail_url, timeout=5)
            if img_response.status_code == 200:
                # Check content length as a proxy for image size
                # Default thumbnails are typically smaller
                content_length = len(img_response.content)
                return content_length > 2000  # Arbitrary threshold
        
        return False
        
    except (requests.RequestException, Exception):
        # If we can't verify, assume it's valid to avoid false negatives
        # due to network issues
        return True