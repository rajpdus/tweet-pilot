# Twitter Thread Generator with Perplexity Research

## Overview
This application will help generate and post Twitter threads by leveraging Perplexity's DeepResearch for content generation and Tweepy for Twitter integration. The application will:
1. Use Perplexity API to research trending topics and generate thread content
2. Allow user selection and customization of threads
3. Post threads directly to Twitter using Tweepy
4. Maintain a history of posted threads

## Technical Requirements

### Dependencies
- Python 3.8+
- Tweepy (latest version)
- Perplexity API client
- Python-dotenv (for environment variables)
- Rich (for terminal UI)

### API Keys Required
1. Twitter API (Elevated Access)
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   
2. Perplexity API
   - API Key

## Project Structure
```
/
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── perplexity_client.py  # Perplexity API integration
│   ├── twitter_client.py  # Twitter API integration
│   ├── thread_generator.py # Thread generation logic
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── cli.py        # Command-line interface
│   │   └── prompts.py    # User interaction prompts
│   └── utils/
│       ├── __init__.py
│       └── helpers.py     # Helper functions
└── data/
    └── thread_history.json # Store generated threads
```

## Core Features

### 1. Topic Research & Thread Generation
- Integration with Perplexity DeepResearch API
- Topic suggestion based on trending subjects
- Customizable research parameters
- Thread structure templates
- Content optimization for Twitter

### 2. Thread Management
- Preview generated threads
- Edit thread content
- Save drafts
- Thread history tracking
- Thread performance analytics

### 3. Twitter Integration
- OAuth authentication
- Thread posting with proper formatting
- Media attachment support
- Scheduling capabilities
- Error handling and rate limit management

### 4. User Interface
- Interactive CLI using Rich
- Thread preview formatting
- Color-coded status messages
- Progress indicators
- Easy navigation between features

## Implementation Plan

### Phase 1: Setup & Basic Infrastructure
1. Project structure setup
2. Environment configuration
3. API client implementations
4. Basic CLI interface

### Phase 2: Core Functionality
1. Perplexity research integration
2. Thread generation logic
3. Twitter posting capability
4. Basic thread management

### Phase 3: Enhanced Features
1. Thread templates
2. Media support
3. Scheduling
4. Analytics

### Phase 4: UI & UX
1. Rich CLI implementation
2. Interactive thread editing
3. Preview formatting
4. Status notifications

## Usage Example

```python
# Example usage of the application
from thread_generator import ThreadGenerator
from twitter_client import TwitterClient

# Initialize clients
generator = ThreadGenerator(perplexity_api_key="your_key")
twitter = TwitterClient(auth_credentials)

# Generate thread
topic = "AI in Healthcare"
thread = generator.research_and_generate(topic)

# Preview and edit
thread.preview()
thread.edit()

# Post to Twitter
twitter.post_thread(thread)
```

## Security Considerations
1. Secure API key storage using environment variables
2. Rate limiting implementation
3. Error handling for API failures
4. Data persistence security
5. User authentication for sensitive operations

## Future Enhancements
1. GUI interface
2. Multiple Twitter account support
3. Advanced scheduling features
4. AI-powered content optimization
5. Integration with other social platforms
6. Analytics dashboard
7. Custom template creation

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the application: `python -m src.ui.cli`

## Notes
- Ensure Twitter API has Elevated access for full functionality
- Keep API keys secure and never commit them to version control
- Regular updates to maintain compatibility with API changes
- Monitor API usage to stay within rate limits 