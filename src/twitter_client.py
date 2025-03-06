"""Twitter API client for posting threads."""
from typing import List, Optional
import tweepy
from .config import settings

class TwitterClient:
    """Client for interacting with Twitter API."""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 api_secret: Optional[str] = None,
                 access_token: Optional[str] = None,
                 access_token_secret: Optional[str] = None):
        """Initialize the Twitter client.
        
        Args:
            api_key: Twitter API key
            api_secret: Twitter API secret
            access_token: Twitter access token
            access_token_secret: Twitter access token secret
        """
        self.api_key = api_key or settings.twitter_api_key
        self.api_secret = api_secret or settings.twitter_api_secret
        self.access_token = access_token or settings.twitter_access_token
        self.access_token_secret = access_token_secret or settings.twitter_access_token_secret
        
        # Initialize API v2 client
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Initialize API v1.1 client for media uploads (still required for v2)
        auth = tweepy.OAuth1UserHandler(
            self.api_key, 
            self.api_secret,
            self.access_token, 
            self.access_token_secret
        )
        self.api = tweepy.API(auth)
        
    def post_thread(self, tweets: List[str]) -> List[str]:
        """Post a thread of tweets.
        
        Args:
            tweets: List of tweet texts to post
            
        Returns:
            List of tweet IDs for the posted thread
        """
        tweet_ids = []
        previous_tweet_id = None
        
        try:
            for tweet in tweets:
                if previous_tweet_id:
                    response = self.client.create_tweet(
                        text=tweet,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                else:
                    response = self.client.create_tweet(text=tweet)
                
                tweet_id = response.data['id']
                tweet_ids.append(str(tweet_id))
                previous_tweet_id = tweet_id
            
            return tweet_ids
        except tweepy.TweepyException as e:
            raise TwitterAPIError(f"Failed to post thread: {str(e)}")
    
    def post_thread_with_media(self, tweets: List[str], media_paths: Optional[List[str]] = None) -> List[str]:
        """Post a thread with media attachments.
        
        Args:
            tweets: List of tweet texts
            media_paths: Optional list of paths to media files
            
        Returns:
            List of tweet IDs for the posted thread
        """
        tweet_ids = []
        previous_tweet_id = None
        
        try:
            for i, tweet in enumerate(tweets):
                media_ids = []
                if media_paths and i < len(media_paths):
                    # Media upload still uses v1.1 API
                    media = self.api.media_upload(filename=media_paths[i])
                    media_ids.append(media.media_id)
                
                if previous_tweet_id:
                    response = self.client.create_tweet(
                        text=tweet,
                        in_reply_to_tweet_id=previous_tweet_id,
                        media_ids=media_ids if media_ids else None
                    )
                else:
                    response = self.client.create_tweet(
                        text=tweet,
                        media_ids=media_ids if media_ids else None
                    )
                
                tweet_id = response.data['id']
                tweet_ids.append(str(tweet_id))
                previous_tweet_id = tweet_id
            
            return tweet_ids
        except tweepy.TweepyException as e:
            raise TwitterAPIError(f"Failed to post thread with media: {str(e)}")

class TwitterAPIError(Exception):
    """Custom exception for Twitter API errors."""
    pass 