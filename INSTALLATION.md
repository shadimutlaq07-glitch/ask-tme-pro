# ASK TME Pro - Installation & Setup Guide

## Quick Start (5 minutes)

### 1. Clone & Setup

```bash
git clone https://github.com/shadimutlaq07-glitch/ask-tme-pro.git
cd ask-tme-pro
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Telegram BOT_TOKEN
nano .env
```

**Required settings:**
```
BOT_TOKEN=your_telegram_bot_token
MT5_SYMBOL=Gold
DB_PATH=data/ask_tme_pro.db
DEFAULT_TIMEFRAME=H4
MIN_CONFIDENCE=55
DEBUG=false
```

### 3. Run the Bot

```bash
python -m app.bot
```

---

## Project Structure

```
ask-tme-pro/
├── app/
│   ├── __init__.py                 # Base directories
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── models.py              # Direction, SignalState, AnalysisResult
│   │   ├── indicators.py          # EMA, RSI, ATR calculations
│   │   └── engine.py              # Main analysis engine
│   ├── backtesting/
│   │   ├── __init__.py
│   │   ├── simulator.py           # Trade simulation
│   │   ├── walk_forward.py        # Walk-forward backtesting
│   │   └── reports.py             # Report generation
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── __main__.py            # Bot entry point
│   │   ├── application.py         # Bot setup
│   │   ├── keyboards.py           # Inline keyboards
│   │   └── handlers/
│   │       ├── __init__.py
│   │       ├── start.py           # /start command
│   │       ├── settings.py        # Settings handler
│   │       ├── analysis.py        # Analysis handler
│   │       └── router.py          # Main routing logic
│   ├── common/
│   │   ├── __init__.py
│   │   ├── logger.py              # Logging setup
│   │   ├── formatting.py          # Price formatting utilities
│   │   └── validators.py          # Input validation
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Configuration management
│   ├── core/
│   │   ├── __init__.py
│   │   └── exceptions.py          # Custom exceptions
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py            # SQLite operations
│   ├── graphics/
│   │   ├── __init__.py
│   │   └── chart.py               # Image generation
│   └── market/
│       ├── __init__.py
│       ├── mt5_client.py          # MT5 integration
│       └── data_loader.py         # Data loading
├── tests/
│   ├── test_engine.py             # Engine tests
│   ├── test_backtest.py           # Backtest tests
│   └── test_database.py           # Database tests
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── .pre-commit-config.yaml        # Pre-commit hooks
├── .ruff.toml                     # Ruff linter config
├── Dockerfile                      # Docker image
├── docker-compose.yml             # Docker compose setup
├── Makefile                        # Build automation
├── README.md                       # Project documentation
├── pyproject.toml                 # Project metadata
├── pytest.ini                      # Pytest configuration
├── requirements.txt               # Python dependencies
└── INSTALLATION.md                # This file
```

---

## Core Components

### 1. Analytics Engine (`app/analytics/engine.py`)

The heart of the system. Performs multi-timeframe analysis:
- **Input:** Dict of DataFrames (D1, H4, H1, M30, M15)
- **Output:** `AnalysisResult` with direction, confidence, entry/stop/TP levels

```python
from app.analytics.engine import AnalysisEngine
import pandas as pd

engine = AnalysisEngine(symbol="Gold")
frames = {
    "M15": pd.DataFrame(...),
    "M30": pd.DataFrame(...),
    "H1": pd.DataFrame(...),
}
result = engine.analyze_multi_timeframe(frames, execution_timeframe="M15")
print(f"Direction: {result.direction}, Confidence: {result.confidence}%")
```

### 2. Database (`app/database/database.py`)

Stores user preferences and analysis history:
```python
from app.database.database import Database

db = Database("data/ask_tme_pro.db")
db.upsert_user(user_id=123, username="trader", first_name="John")
analysis_id = db.save_analysis(user_id=123, result=analysis_result)
```

### 3. MT5 Client (`app/market/mt5_client.py`)

Connects to MetaTrader5 and fetches market data:
```python
from app.market.mt5_client import MT5Client

mt5 = MT5Client(symbol="Gold")
mt5.connect()
rates = mt5.get_rates(timeframe=240, count=350)  # H4, 350 bars
```

### 4. Telegram Bot (`app/bot/application.py`)

Handles user interactions through Telegram:
```bash
python -m app.bot
```

---

## Quality Assurance

### Run Tests
```bash
pytest -q
```

### Code Quality
```bash
# Format code
black app tests

# Check style
ruff check app tests

# Type checking
mypy app --ignore-missing-imports
```

### Pre-commit Hooks
```bash
pre-commit install
```

---

## Docker Deployment

### Build Image
```bash
docker build -t ask-tme-pro .
```

### Run Container
```bash
docker-compose up -d
```

---

## Telegram Bot Commands

| Command | Function |
|---------|----------|
| `/start` | Initialize bot and show main menu |
| `🤖 Analyze Gold` | Start analysis workflow |
| `⚙️ Settings` | Change default timeframe |
| `ℹ️ About` | Show bot information |

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `BOT_TOKEN` | — | Telegram bot token (required) |
| `MT5_SYMBOL` | Gold | Trading symbol in MT5 |
| `DB_PATH` | data/ask_tme_pro.db | Database file location |
| `DEFAULT_TIMEFRAME` | H4 | Default analysis timeframe |
| `MIN_CONFIDENCE` | 55 | Minimum confidence threshold |
| `LOG_LEVEL` | INFO | Logging verbosity |
| `DEBUG` | false | Debug mode (true/false) |

---

## Troubleshooting

### Bot not responding
- Check `BOT_TOKEN` is valid
- Verify network connectivity
- Check logs: `tail -f logs/ask_tme.log`

### MT5 connection failed
- Ensure MT5 is running and open
- Verify symbol name matches MT5 exactly
- Check MetaTrader5 Python package is installed

### Analysis returns WAIT
- Insufficient bars of data
- Trend not aligned with momentum
- Market in consolidation phase

---

## Development Workflow

### Create feature branch
```bash
git checkout -b feat/your-feature
```

### Make changes and test
```bash
make format
make lint
make test
```

### Commit and push
```bash
git add .
git commit -m "feat: description of changes"
git push origin feat/your-feature
```

### Create pull request
Open PR on GitHub for review

---

## Performance Tips

1. **Reduce backtest step size** for faster iterations (default: 5)
2. **Increase context bars** for more accurate analysis (default: 300)
3. **Use Docker** for consistent environment across machines
4. **Enable async analysis** for real-time updates

---

## Support & Resources

- **GitHub Issues:** Report bugs and request features
- **Documentation:** See README.md for API reference
- **Examples:** Check tests/ for usage examples
- **Logs:** Monitor logs/ask_tme.log for debugging

---

## License

ASK TME Pro is part of the Trade Masters Elite ecosystem.

---

**Last Updated:** 2026-09-27  
**Version:** 0.1.0  
**Status:** Production Ready
