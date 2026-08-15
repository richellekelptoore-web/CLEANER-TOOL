# Configuration Guide

## Overview

Memory Clearer is configured via `config.ini` file located in the project root directory.

## Configuration Sections

### [Memory]

Controls memory monitoring and thresholds.

```ini
[Memory]
threshold = 80              # Alert when memory usage exceeds this percentage
check_interval = 5          # Check memory every N seconds
```

### [Cleanup]

Controls cleanup behavior and targets.

```ini
[Cleanup]
enable_auto_cleanup = true  # Enable automatic cleanup
auto_cleanup_interval = 3600    # Auto-cleanup every N seconds (1 hour)
cleanup_temp = true         # Remove temporary files
cleanup_cache = true        # Clear cache directories
cleanup_logs = false        # Remove old log files (use with caution)
max_cleanup_size = 500      # Max cleanup size in MB
safe_mode = true            # Don't delete system files
```

### [Logging]

Controls logging behavior.

```ini
[Logging]
level = INFO                # Log level: DEBUG, INFO, WARNING, ERROR
directory = clear/logs      # Log file directory
filename = memory_clearer.log   # Log filename
max_file_size = 10485760    # Max log file size in bytes (10 MB)
backup_count = 3            # Number of backup log files to keep
```

### [Paths]

Custom paths for monitoring and cleanup.

```ini
[Paths]
temp_dirs = /tmp,/var/tmp   # Directories to clean
cache_dirs = ~/.cache       # Cache directories (platform-specific)
exclude_dirs = /important   # Paths to never clean
```

## Default Configuration

Run this command to generate default `config.ini`:

```bash
python setup_memory_clearer.py
```

## Environment Variables

You can override config settings with environment variables:

```bash
set MEMORY_THRESHOLD=85
set AUTO_CLEANUP_INTERVAL=7200
python cli.py --clean
```

## Platform-Specific Settings

### Windows

```ini
[Paths]
temp_dirs = C:\Windows\Temp,C:\Users\%USERNAME%\AppData\Local\Temp
cache_dirs = C:\Users\%USERNAME%\AppData\Local\Cache
```

### Linux

```ini
[Paths]
temp_dirs = /tmp,/var/tmp
cache_dirs = ~/.cache,~/.local/share
```

### macOS

```ini
[Paths]
temp_dirs = /tmp,/var/tmp
cache_dirs = ~/Library/Caches
```

## Advanced Tuning

### For High-Performance Systems

```ini
[Memory]
check_interval = 1          # Check every second

[Cleanup]
auto_cleanup_interval = 1800    # Clean every 30 minutes
```

### For Low-Resource Systems

```ini
[Memory]
check_interval = 30         # Check every 30 seconds

[Cleanup]
auto_cleanup_interval = 7200    # Clean every 2 hours
safe_mode = true            # Extra safety
```

### For Maximum Privacy

```ini
[Cleanup]
cleanup_temp = true
cleanup_cache = true
cleanup_logs = true         # Also clean logs
max_cleanup_size = 1000     # More aggressive cleanup
```

## Troubleshooting Configuration

**Issue**: Settings not taking effect

**Solution**: 
1. Restart the application
2. Verify config file syntax (check for missing `=` or brackets)
3. Check file permissions

**Issue**: Application crashes on startup

**Solution**:
1. Delete `config.ini`
2. Run `python setup_memory_clearer.py` to regenerate
3. Start application again
