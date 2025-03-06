"""Thread generator combining research and Twitter posting capabilities."""
import json
from datetime import datetime
from typing import Dict, List, Optional
from .research_client import ResearchClient
from .twitter_client import TwitterClient

class Thread:
    """Represents a Twitter thread with its content and metadata."""
    
    def __init__(self, topic: str, tweets: List[str], research_data: Dict):
        """Initialize a thread.
        
        Args:
            topic: The research topic
            tweets: List of tweet texts
            research_data: Original research data from Gemini
        """
        self.topic = topic
        self.tweets = tweets
        self.research_data = research_data
        self.created_at = datetime.now()
        self.tweet_ids: Optional[List[str]] = None
        
    def to_dict(self) -> Dict:
        """Convert thread to dictionary for storage."""
        return {
            "topic": self.topic,
            "tweets": self.tweets,
            "research_data": self.research_data,
            "created_at": self.created_at.isoformat(),
            "tweet_ids": self.tweet_ids
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Thread':
        """Create thread instance from dictionary."""
        thread = cls(
            topic=data["topic"],
            tweets=data["tweets"],
            research_data=data["research_data"]
        )
        thread.created_at = datetime.fromisoformat(data["created_at"])
        thread.tweet_ids = data.get("tweet_ids")
        return thread

class ThreadGenerator:
    """Generates and manages Twitter threads."""
    
    def __init__(self, 
                 google_api_key: Optional[str] = None,
                 twitter_api_key: Optional[str] = None,
                 twitter_api_secret: Optional[str] = None,
                 twitter_access_token: Optional[str] = None,
                 twitter_access_token_secret: Optional[str] = None):
        """Initialize the thread generator.
        
        Args:
            google_api_key: Optional Google API key
            twitter_*: Optional Twitter API credentials
        """
        self.research = ResearchClient(api_key=google_api_key)
        self.twitter = TwitterClient(
            api_key=twitter_api_key,
            api_secret=twitter_api_secret,
            access_token=twitter_access_token,
            access_token_secret=twitter_access_token_secret
        )
        
    def research_and_generate(self, topic: str, depth: str = "comprehensive") -> Thread:
        """Research a topic and generate a thread.
        
        Args:
            topic: Topic to research
            depth: Research depth (quick/comprehensive)
            
        Returns:
            Generated Thread object
        """
        # Get research data with grounded search
        research_data = self.research.research_with_search(topic)
        
        # Generate tweets from research
        tweets = self.research.generate_thread(research_data)
        
        # Create and return thread object
        return Thread(topic, tweets, research_data)
    
    def post_thread(self, thread: Thread, media_paths: Optional[List[str]] = None) -> Thread:
        """Post a thread to Twitter.
        
        Args:
            thread: Thread object to post
            media_paths: Optional list of media file paths
            
        Returns:
            Updated Thread object with tweet IDs
        """
        if media_paths:
            tweet_ids = self.twitter.post_thread_with_media(thread.tweets, media_paths)
        else:
            tweet_ids = self.twitter.post_thread(thread.tweets)
        
        thread.tweet_ids = tweet_ids
        return thread
    
    def save_thread(self, thread: Thread, filepath: str = "data/thread_history.json"):
        """Save thread to history file.
        
        Args:
            thread: Thread to save
            filepath: Path to history file
        """
        try:
            # Load existing threads
            try:
                with open(filepath, 'r') as f:
                    threads = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                threads = []
            
            # Add new thread
            threads.append(thread.to_dict())
            
            # Save updated threads
            with open(filepath, 'w') as f:
                json.dump(threads, f, indent=2)
        except Exception as e:
            raise ThreadStorageError(f"Failed to save thread: {str(e)}")
    
    def load_threads(self, filepath: str = "data/thread_history.json") -> List[Thread]:
        """Load threads from history file.
        
        Args:
            filepath: Path to history file
            
        Returns:
            List of Thread objects
        """
        try:
            with open(filepath, 'r') as f:
                threads_data = json.load(f)
            return [Thread.from_dict(data) for data in threads_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except Exception as e:
            raise ThreadStorageError(f"Failed to load threads: {str(e)}")

class ThreadStorageError(Exception):
    """Custom exception for thread storage operations."""
    pass 