"""Helper utilities for the Twitter Thread Generator."""
import os
import json
from typing import List, Dict, Any

def ensure_directory_exists(filepath: str):
    """Ensure the directory for a file exists.
    
    Args:
        filepath: Path to file
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def load_json_file(filepath: str, default: Any = None) -> Any:
    """Load JSON data from file with error handling.
    
    Args:
        filepath: Path to JSON file
        default: Default value if file doesn't exist
        
    Returns:
        Loaded JSON data or default value
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json_file(filepath: str, data: Any):
    """Save data to JSON file with error handling.
    
    Args:
        filepath: Path to JSON file
        data: Data to save
    """
    ensure_directory_exists(filepath)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def truncate_text(text: str, max_length: int = 280) -> str:
    """Truncate text to fit Twitter's character limit.
    
    Args:
        text: Text to truncate
        max_length: Maximum length (default: 280 for Twitter)
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def split_into_tweets(text: str, max_length: int = 280) -> List[str]:
    """Split long text into tweet-sized chunks.
    
    Args:
        text: Text to split
        max_length: Maximum tweet length
        
    Returns:
        List of tweet-sized text chunks
    """
    words = text.split()
    tweets = []
    current_tweet = []
    current_length = 0
    
    for word in words:
        # Account for space between words
        word_length = len(word) + (1 if current_tweet else 0)
        
        if current_length + word_length <= max_length:
            current_tweet.append(word)
            current_length += word_length
        else:
            tweets.append(" ".join(current_tweet))
            current_tweet = [word]
            current_length = len(word)
    
    if current_tweet:
        tweets.append(" ".join(current_tweet))
    
    return tweets

def format_tweet_text(text: str, hashtags: List[str] = None) -> str:
    """Format tweet text with hashtags.
    
    Args:
        text: Tweet text
        hashtags: Optional list of hashtags
        
    Returns:
        Formatted tweet text
    """
    if not hashtags:
        return text
    
    # Format hashtags
    hashtag_text = " ".join(f"#{tag.strip('#')}" for tag in hashtags)
    
    # Combine text and hashtags, ensuring we don't exceed limit
    combined = f"{text}\n\n{hashtag_text}"
    return truncate_text(combined)

def validate_tweet_text(text: str) -> bool:
    """Validate tweet text meets Twitter's requirements.
    
    Args:
        text: Tweet text to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Check length
    if len(text) > 280:
        return False
    
    # Add other Twitter-specific validation rules here
    return True 