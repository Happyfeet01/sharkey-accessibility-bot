# Sharkey Accessibility Bot

This bot improves image accessibility on Sharkey/Misskey instances by reminding users to add alt text to their images and generating descriptions if necessary.

## Features
- Reacts only to posts by users who follow the bot
- Ignores private, followers-only, or sensitive posts
- Ignores renotes and replies
- Reminds users to add alt text to images
- Generates image descriptions using Ollama vision model if no alt text is added after 5 minutes
- Stops reacting if a user unfollows the bot

## Setup

### Prerequisites
- Python 3.12
- pip

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Happyfeet01/sharkey-accessibility-bot.git
   cd sharkey-accessibility-bot
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your actual data.

5. **Run the bot**:
   ```bash
   python3 main.py
   ```

### Configuration

Create a `.env` file in the root directory with the following variables:

```ini
MISSKEY_INSTANCE=https://example.social
MISSKEY_TOKEN=xxxxxxxx
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llava-phi3
CHECK_INTERVAL_SECONDS=300
```

Replace the values with your actual data.

### Running the Bot

Start the bot by running:
```bash
python3 main.py
```

### Stopping the Bot

To stop the bot, use `Ctrl+C` in the terminal where it is running.

## License

This project is licensed under the MIT License.