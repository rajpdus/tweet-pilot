import os
from dotenv import load_dotenv
import tweepy

def test_twitter_auth():
    """Test Twitter API authentication and basic functionality."""
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    print("\nTesting Twitter API Authentication...")
    print("-" * 40)
    
    # Print masked credentials for verification
    print(f"API Key: {api_key[:4]}...{api_key[-4:]}" if api_key else "API Key: Not found")
    print(f"API Secret: {api_secret[:4]}...{api_secret[-4:]}" if api_secret else "API Secret: Not found")
    print(f"Access Token: {access_token[:4]}...{access_token[-4:]}" if access_token else "Access Token: Not found")
    print(f"Access Token Secret: {access_token_secret[:4]}...{access_token_secret[-4:]}" if access_token_secret else "Access Token Secret: Not found")
    
    try:
        # Initialize client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # response = client.create_tweet(text="Hello, world! Posted using the combined OAuth credentials.")

        # Test authentication by getting user info
        user = client.get_me()
        print("\n✅ Authentication successful!")
        print(f"Connected as: @{user.data.username}")
        print(f"User ID: {user.data.id}")
        
        # Test read permissions
        print("\nTesting read permissions...")
        tweets = client.create_tweet(id=user.data.id)
        if tweets.data:
            print("✅ Read permissions working")
        else:
            print("✅ Read permissions working (no tweets found)")
            
        return True
        
    except tweepy.TweepyException as e:
        print("\n❌ Authentication failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_twitter_auth() 