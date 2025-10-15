<div align="center">
  <h1>🎮 Analyse - League of Legends Data Analysis Suite</h1>
  <p><strong>Comprehensive Riot API toolkit for League of Legends data analysis and research</strong></p>
  
  ![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
  ![Riot API](https://img.shields.io/badge/Riot-API-orange.svg)
  ![License](https://img.shields.io/badge/License-MIT-green.svg)
  ![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
</div>

---

## 🌟 Overview

**Analyse** is a comprehensive data analysis suite designed for League of Legends researchers, analysts, and developers. It provides powerful tools for fetching, processing, and analyzing League of Legends data through the official Riot API.

### ✨ Key Features

- 🔥 **Complete Riot API Coverage** - All major endpoints implemented
- 🌍 **Multi-Server Support** - EUW, KR, NA, EUNE, BR, JP, and more
- 🛠️ **Modular Architecture** - Clean, maintainable, and extensible codebase
- 📊 **Data Analysis Tools** - Jupyter notebooks for in-depth analysis
- 🧪 **Comprehensive Testing** - Unit tests with mocks + live API tests
- 📈 **Performance Optimized** - Rate limiting, retry logic, and error handling
- 🎯 **CLI Interface** - Easy-to-use command-line tools
- 📁 **Organized Output** - Timestamped, categorized data storage

---

## 📁 Project Structure

```
Analyse/
├── 📊 riot_fetcher/           # Riot API CLI Toolkit
│   ├── 🐍 riotkit/           # Core Python modules
│   │   ├── __init__.py       # Package exports
│   │   ├── config.py         # Configuration management
│   │   ├── client.py         # API client with retry logic
│   │   ├── endpoints.py      # All Riot API endpoints
│   │   ├── fetcher.py        # High-level data fetching
│   │   └── io.py             # File I/O utilities
│   ├── 🧪 tests/             # Test suite
│   │   ├── test_unit.py      # Unit tests with mocks
│   │   └── test_live.py      # Live API tests
│   ├── 📄 main.py            # CLI entry point
│   ├── 📚 README.md          # Detailed documentation
│   ├── 📋 riotkits.md        # Technical specifications
│   └── 📁 data/              # Output directory (auto-created)
├── 📓 docs/                  # Documentation and assets
├── 📊 *.ipynb               # Jupyter analysis notebooks
└── 📄 README.md             # This file
```

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** (recommended: Python 3.10+)
- **Riot API Key** (get one at [Riot Developer Portal](https://developer.riotgames.com/))
- **Git** (for cloning the repository)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Analyse.git
cd Analyse

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -U pip
pip install requests python-dotenv jupyter matplotlib pandas numpy
```

### 3. Configuration

```bash
# Navigate to riot_fetcher
cd riot_fetcher

# Copy environment template
copy .env.example .env

# Edit .env file with your API key
# RIOT_API_KEY=RGAPI-your-actual-api-key-here
```

### 4. Test Your Setup

```bash
# Test API connection
python main.py diagnose

# Test with a player profile
python main.py profile --riot-id "Sung Jin woo#SOUL" --count 3

# Run all tests
python -m unittest discover -v
```

---

## 🎮 Riot API Toolkit

The `riot_fetcher/` directory contains a complete CLI toolkit for interacting with the Riot API.

### 🔧 Available Commands

| Category | Commands | Description |
|----------|----------|-------------|
| **Status** | `diagnose` | Check API status and connection |
| **Account** | `by-riot-id`, `by-puuid`, `active-shard` | Player account operations |
| **Summoner** | `by-puuid`, `by-id` | Summoner data and levels |
| **Champion** | `rotation` | Champion rotations and data |
| **Mastery** | `all`, `by-champion`, `top`, `score` | Champion mastery data |
| **Match** | `ids`, `get`, `timeline` | Match history and details |
| **League** | `by-summoner`, `entries`, `challenger`, etc. | Ranked league data |
| **Profile** | `profile` | Complete player profile with matches |

### 🌍 Multi-Server Examples

```bash
# EUW (Europe West) - Default
python main.py profile --riot-id "Sung Jin woo#SOUL" --count 5

# KR (Korea)
python main.py --platform kr --region asia profile --riot-id "Sard#CASS" --count 5

# NA (North America)
python main.py --platform na1 --region americas profile --riot-id "Player#NA1" --count 5
```

### 💾 Output Options

```bash
# Console output (JSON)
python main.py champion rotation --stdout

# File output (default)
python main.py champion rotation
# Saves to: data/champion/20251015T013922Z_rotations.json
```

---

## 📊 Data Analysis Notebooks

The repository includes Jupyter notebooks for various League of Legends data analysis tasks:

- **`Analyse.ipynb`** - Main analysis notebook
- **`Analyse 2.ipynb`** - Secondary analysis
- **`Poids.ipynb`** - Weight/importance analysis
- **`output.ipynb`** - Output processing and visualization

### 🚀 Running Analysis Notebooks

```bash
# Start Jupyter Lab
jupyter lab

# Or start Jupyter Notebook
jupyter notebook

# Open any .ipynb file in your browser
```

---

## 🧪 Testing

### Unit Tests (Fast, No API Calls)
```bash
cd riot_fetcher
python -m unittest tests.test_unit -v
```

### Live Tests (Requires API Key)
```bash
cd riot_fetcher
python -m unittest tests.test_live -v
```

### All Tests
```bash
cd riot_fetcher
python -m unittest discover -v
```

---

## 📈 Features & Capabilities

### 🔥 Riot API Integration
- **Complete Endpoint Coverage** - All major Riot API endpoints
- **Multi-Server Support** - All regions (EUW, KR, NA, EUNE, BR, JP, etc.)
- **Rate Limiting** - Automatic retry with exponential backoff
- **Error Handling** - Comprehensive error management
- **Type Safety** - Full type hints for better IDE support

### 📊 Data Analysis
- **Jupyter Integration** - Ready-to-use analysis notebooks
- **Data Visualization** - Matplotlib and pandas integration
- **Statistical Analysis** - NumPy for numerical computations
- **Export Capabilities** - Multiple output formats (JSON, CSV, etc.)

### 🛠️ Development Tools
- **Modular Architecture** - Clean, maintainable codebase
- **Comprehensive Testing** - Unit tests with mocks + live tests
- **CLI Interface** - Easy-to-use command-line tools
- **Documentation** - Detailed documentation and examples

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
RIOT_API_KEY=RGAPI-your-api-key-here

# Optional (can be overridden via CLI)
PLATFORM_REGION=euw1
REGIONAL_ROUTING=europe
DEFAULT_COUNT=10
LOG_LEVEL=DEBUG
```

### CLI Arguments
```bash
# Global options
--platform euw1          # Platform region
--region europe          # Regional routing
--log-level DEBUG        # Logging level

# Command-specific options
--stdout                 # Print to console
--save                   # Save to file (default)
--count 10              # Number of items
--start 0               # Start index
--page 1                # Page number
```

---

## 🚨 Error Handling

The toolkit handles all common Riot API errors gracefully:

| Error Code | Description | Action |
|------------|-------------|---------|
| **401** | Unauthorized | Invalid API key |
| **403** | Forbidden | Key not authorized for endpoint |
| **404** | Not Found | Player/summoner not found |
| **429** | Rate Limit | Automatic retry with backoff |
| **4xx** | Client Error | Detailed error messages |
| **5xx** | Server Error | Automatic retry with backoff |

---

## 📚 Documentation

- **[Riot API Toolkit](riot_fetcher/README.md)** - Complete CLI documentation
- **[Technical Specs](riot_fetcher/riotkits.md)** - Implementation details
- **[Riot Developer Portal](https://developer.riotgames.com/)** - Official API docs

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Add tests for new functionality**
5. **Ensure all tests pass**
   ```bash
   python -m unittest discover -v
   ```
6. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
7. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 riot_fetcher/

# Run type checking
mypy riot_fetcher/
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Important**: This project is for educational and personal use. Please respect Riot Games' API terms of service and rate limits.

---

## 🙏 Acknowledgments

- **Riot Games** - For providing the comprehensive League of Legends API
- **Python Community** - For excellent libraries and tools
- **Contributors** - For their valuable contributions

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Analyse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Analyse/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/Analyse/wiki)

---

<div align="center">
  <p><strong>Made with ❤️ for the League of Legends community</strong></p>
  <p>⭐ Star this repository if you find it helpful!</p>
</div>