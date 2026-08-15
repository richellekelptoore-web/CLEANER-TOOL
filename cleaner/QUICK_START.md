# Quick Start Guide

Get Memory Clearer up and running in 2 minutes!

## Installation

### Windows (Fastest)
```bash
run.bat
```

### Manual (All Platforms)
```bash
python setup_memory_clearer.py
pip install -r requirements.txt
```

## Basic Usage

### Check Memory Status
```bash
python cli.py --status
```

Output:
```
==================================================
  Memory Clearer - System Status
==================================================
Total Memory:     16384 MB
Used Memory:      8192 MB
Available Memory: 8192 MB
Free Memory:      6000 MB
Memory Usage:     50.0%
==================================================
```

### Clean Memory
```bash
python cli.py --clean
```

### Start Monitoring
```bash
python monitor_daemon.py
```

Press `Ctrl+C` to stop monitoring.

### Open GUI (Windows)
```bash
python memory_clearer.py
```

## What Gets Cleaned?

- Temporary files
- Cache directories
- Browser caches
- System temp folders
- Unnecessary memory allocations

**Note**: System-critical files are never deleted in Safe Mode (default).

## Configuration

Edit `config.ini` to customize behavior:

```ini
[Memory]
threshold = 80              # Alert at 80% usage

[Cleanup]
auto_cleanup_interval = 3600   # Auto-clean every hour
safe_mode = true            # Protect system files
```

See [Configuration Guide](docs/CONFIGURATION.md) for full details.

## Next Steps

- ✅ Run the application
- ✅ Check memory status
- ✅ Perform a quick clean
- ✅ Review logs in `clear/logs/`
- ✅ Customize settings in `config.ini`

## Troubleshooting

**Problem**: Permission denied error
- **Solution**: Run as Administrator (Windows) or with `sudo` (Linux/Mac)

**Problem**: Module not found error
- **Solution**: Reinstall dependencies: `pip install -r requirements.txt`

**Problem**: GUI won't start
- **Solution**: Use CLI instead: `python cli.py --status`

## Getting Help

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review logs in `clear/logs/memory_clearer.log`
- Read [CONFIGURATION.md](docs/CONFIGURATION.md)

Enjoy! 🧹
