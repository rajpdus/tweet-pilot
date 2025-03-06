# Twitter Thread Generator

An AI-powered tool that generates and posts Twitter threads using Google's Gemini API for research and the Twitter API for posting.

## Features

- AI-powered research on any topic using Google's Gemini API
- Automatic thread generation and formatting
- Direct posting to Twitter
- Media handling support
- Rate limit handling
- Configurable thread length and style

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/twitter-thread-generator.git
cd twitter-thread-generator

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Add your API keys to `.env`:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
GOOGLE_API_KEY=your_gemini_api_key
```

## Usage

```bash
# Run the CLI
python -m src.ui.cli
```

Example:
```bash
# Generate and post a thread about space exploration
python -m src.ui.cli "Latest developments in space exploration"
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed information about the system design and component interaction.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini API for research capabilities
- Twitter API for thread posting
- All contributors and users of this project 