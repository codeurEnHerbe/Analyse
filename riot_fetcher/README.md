# Riot API CLI - Complete League of Legends Data Fetcher

A comprehensive, modular CLI tool for fetching League of Legends data from the Riot API. Supports all major endpoints with proper error handling, rate limiting, and multi-server support.

## 🚀 Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -U pip
pip install requests python-dotenv
```

### 2. Get Your Riot API Key

1. Go to [Riot Developer Portal](https://developer.riotgames.com/)
2. Sign in with your Riot account
3. Go to "API Keys" section
4. Create a new API key or regenerate existing one
5. Copy your API key (starts with `RGAPI-`)

### 3. Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env
```

Edit `.env` file:
```dotenv
RIOT_API_KEY=RGAPI-your-actual-api-key-here
```

**Note**: Only the API key goes in `.env`. All other settings (platform, region, etc.) are configured via CLI arguments.

### 4. Test Your Setup

```bash
# Test API connection
python main.py diagnose

# Test with a player profile
python main.py profile --riot-id "Sung Jin woo#SOUL" --count 3
```

## 📋 Available Commands

### Status & Diagnostics
```bash
# Check API status and connection
python main.py diagnose
```

### Account Operations
```bash
# Get account by Riot ID
python main.py account by-riot-id --riot-id "Player#TAG"

# Get account by PUUID
python main.py account by-puuid --puuid "player-puuid-here"

# Get active shard for a game
python main.py account active-shard --game lol --puuid "player-puuid-here"
```

### Summoner Operations
```bash
# Get summoner by PUUID
python main.py summoner by-puuid --puuid "player-puuid-here"

# Get summoner by ID
python main.py summoner by-id --summoner-id "summoner-id-here"
```

### Champion Operations
```bash
# Get champion rotations
python main.py champion rotation
```

### Champion Mastery
```bash
# Get all champion masteries for a player
python main.py cm all --puuid "player-puuid-here"

# Get mastery for specific champion
python main.py cm by-champion --puuid "player-puuid-here" --champion-id 1

# Get top champion masteries
python main.py cm top --puuid "player-puuid-here" --count 5

# Get total mastery score
python main.py cm score --puuid "player-puuid-here"
```

### Match Operations
```bash
# Get match IDs for a player
python main.py match ids --puuid "player-puuid-here" --start 0 --count 20

# Get match details
python main.py match get --match-id "match-id-here"

# Get match timeline
python main.py match timeline --match-id "match-id-here"
```

### League Operations
```bash
# Get league entries by summoner
python main.py league by-summoner --summoner-id "summoner-id-here"

# Get league entries by queue/tier/division
python main.py league entries --queue RANKED_SOLO_5x5 --tier DIAMOND --division I --page 1

# Get league by ID
python main.py league by-league-id --league-id "league-id-here"

# Get challenger league
python main.py league challenger --queue RANKED_SOLO_5x5

# Get grandmaster league
python main.py league grandmaster --queue RANKED_SOLO_5x5

# Get master league
python main.py league master --queue RANKED_SOLO_5x5
```

### League EXP Operations
```bash
# Get league EXP entries
python main.py league-exp entries --queue RANKED_SOLO_5x5 --tier DIAMOND --division I --page 1
```

### Legacy Profile (Complete Data)
```bash
# Get complete profile with matches
python main.py profile --riot-id "Player#TAG" --count 10
```

## 🌍 Multi-Server Support

### EUW (Europe West) - Default
```bash
python main.py profile --riot-id "Sung Jin woo#SOUL" --count 5
```

### KR (Korea)
```bash
python main.py --platform kr --region asia profile --riot-id "Sard#CASS" --count 5
```

### NA (North America)
```bash
python main.py --platform na1 --region americas profile --riot-id "Player#NA1" --count 5
```

### Other Regions
```bash
# EUNE (Europe Nordic & East)
python main.py --platform eun1 --region europe profile --riot-id "Player#EUNE"

# BR (Brazil)
python main.py --platform br1 --region americas profile --riot-id "Player#BR1"

# JP (Japan)
python main.py --platform jp1 --region asia profile --riot-id "Player#JP1"
```

## 💾 Output Options

### Console Output (--stdout)
```bash
# Print JSON to console
python main.py champion rotation --stdout
```

### File Output (Default)
```bash
# Save to data/champion/20251015T013922Z_rotations.json
python main.py champion rotation

# Save to data/account/20251015T013929Z_by-riot-id_Player_TAG.json
python main.py account by-riot-id --riot-id "Player#TAG"
```

**File Structure:**
```
data/
├── account/
│   └── 20251015T013929Z_by-riot-id_Player_TAG.json
├── champion/
│   └── 20251015T013922Z_rotations.json
├── match/
├── league/
├── profile/
└── ...
```

## 🧪 Testing

### Run All Tests
```bash
python -m unittest discover -v
```

### Run Specific Tests
```bash
# Unit tests only (with mocks)
python -m unittest tests.test_unit -v

# Live tests only (requires API key)
python -m unittest tests.test_live -v
```

## ⚙️ Configuration Options

### Global Arguments
- `--platform`: Platform region (euw1, na1, kr, br1, jp1, etc.)
- `--region`: Regional routing (europe, americas, asia)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Command-Specific Arguments
- `--stdout`: Print output to console instead of saving to file
- `--save`: Save output to file (default behavior)
- `--count`: Number of matches/items to fetch
- `--start`: Start index for pagination
- `--page`: Page number for pagination

## 🚨 Error Handling

The CLI handles all common Riot API errors:

- **401 Unauthorized**: Invalid or expired API key
- **403 Forbidden**: API key not authorized for endpoint
- **404 Not Found**: Player/summoner not found
- **429 Rate Limit**: Automatic retry with exponential backoff
- **4xx Client Errors**: Detailed error messages
- **5xx Server Errors**: Automatic retry with backoff

## 📁 Project Structure

```
riot_fetcher/
├── riotkit/                 # Core modules
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── client.py           # API client with retry logic
│   ├── endpoints.py        # All API endpoints
│   ├── fetcher.py          # High-level data fetching
│   └── io.py               # File I/O utilities
├── tests/                  # Test suite
│   ├── test_unit.py        # Unit tests with mocks
│   └── test_live.py        # Live API tests
├── data/                   # Output directory (auto-created)
├── main.py                 # CLI entry point
├── .env.example           # Environment template
└── README.md              # This file
```

## 🔧 Development

### Adding New Endpoints
1. Add endpoint function to `riotkit/endpoints.py`
2. Add CLI command to `main.py`
3. Add tests to `tests/test_unit.py`
4. Update `riotkit/__init__.py` exports

### Running in Development
```bash
# Enable debug logging
python main.py --log-level DEBUG diagnose

# Test specific functionality
python main.py --log-level DEBUG champion rotation --stdout
```

## 📚 API Documentation

This tool implements all major Riot API endpoints:

- **Account API**: Player account resolution
- **Summoner API**: Summoner data and levels
- **Champion API**: Champion rotations and data
- **Champion Mastery API**: Player champion mastery
- **Match API**: Match history and details
- **League API**: Ranked league data
- **Status API**: Server status and health

For detailed API documentation, visit [Riot Developer Portal](https://developer.riotgames.com/docs).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is for educational and personal use. Please respect Riot Games' API terms of service.