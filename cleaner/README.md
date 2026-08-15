# Memory Clearer v2.0

A comprehensive Windows system memory cleanup and monitoring tool with a GUI interface.

## Features

- 🧹 **Quick Memory Cleanup** - Remove unused memory and cache files
- 📊 **Real-time Monitoring** - Track memory usage with live updates
- 🔧 **Deep Clean** - Thorough system cleanup including temporary files
- ⚙️ **Configurable** - Adjust cleanup parameters via config.ini
- 📝 **Logging** - Detailed activity logs for troubleshooting
- 🎯 **Auto-Cleanup** - Automatic memory management at intervals

## Installation

### Requirements
- Windows/Linux/Mac
- Python 3.6+
- pip (Python package manager)

### Setup

1. **Quick Setup** (Windows):
```bash
run.bat
```

2. **Manual Setup**:
```bash
python setup_memory_clearer.py
pip install -r requirements.txt
```

## Usage

### GUI Mode
```bash
python memory_clearer.py
```

### Monitor Daemon (Background)
```bash
python monitor_daemon.py
```

### Command Line
```bash
python cli.py --clean
python cli.py --monitor
python cli.py --status
```

## Configuration

Edit `config.ini` to customize:
- Auto-cleanup interval
- Memory alert thresholds
- Logging level
- Backup settings

```ini
[Cleanup]
auto_cleanup_interval = 300  # seconds
cache_cleanup_enabled = true

[Monitoring]
alert_threshold_mb = 500
check_interval = 30
```

## Project Structure

```
cleaner/
├── memory_clearer.py      # Main GUI application
├── setup_memory_clearer.py # Initial setup script
├── utils.py               # Utility functions
├── config.ini             # Configuration file
├── requirements.txt       # Python dependencies
├── run.bat               # Quick launcher (Windows)
├── README.md             # This file
└── clear/                # Working directory
    ├── logs/             # Activity logs
    ├── cache/            # Cache files
    ├── backups/          # Backup files
    └── config/           # Config backups
```

## Troubleshooting

### Python not found
Install Python from [python.org](https://www.python.org)

### Permission denied
Run as Administrator or use `run.bat`

### psutil not found
```bash
pip install psutil
```

### High memory usage
Enable monitoring for continuous management

## Logs

Activity logs are saved in `clear/logs/` with timestamps.

## Support

For issues or feature requests, check the log files first.

## License

Free to use and modify.
