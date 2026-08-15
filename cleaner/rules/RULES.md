# Usage Rules & Guidelines

**Last Updated:** August 15, 2024

## 1. General Usage Guidelines

### 1.1 System Requirements

Before using Memory Clearer, ensure you have:

**Minimum:**
- Python 3.6 or higher
- 256 MB available RAM
- 50 MB disk space
- Administrator/sudo access (for some operations)

**Recommended:**
- Python 3.8 or higher
- 1 GB+ available RAM
- 500 MB+ disk space
- Latest OS updates installed

### 1.2 Supported Platforms

✅ **Fully Supported:**
- Windows 7, 8, 10, 11
- Ubuntu 18.04+, Debian 10+
- macOS 10.14+

⚠️ **Partial Support:**
- Older Windows versions (pre-Win7)
- Linux distributions without Python
- Windows Server editions

❌ **Not Supported:**
- Mobile devices (Android, iOS)
- Old macOS versions (pre-10.14)
- Custom Linux distributions without standard utilities

## 2. Installation Rules

### 2.1 Before Installation

1. **Backup Important Data**
   ```bash
   # Create a full system backup before first use
   # Windows: Use System Image Backup
   # Linux: Use rsync or tar
   # macOS: Use Time Machine
   ```

2. **Disable Antivirus Scanning (Temporarily)**
   - Some antivirus may block cleanup operations
   - Add exceptions for `Memory Clearer` folder
   - Re-enable after installation

3. **Close Running Applications**
   - Close browsers, editors, and services
   - This improves cleanup effectiveness

### 2.2 Installation Process

```bash
# Windows
run.bat                          # Recommended: automatic setup

# Manual installation
python setup_memory_clearer.py
pip install -r requirements.txt
python memory_clearer.py

# Linux/macOS
python3 setup_memory_clearer.py
pip3 install -r requirements.txt
python3 memory_clearer.py
```

### 2.3 Post-Installation

- ✅ Verify `config.ini` was created
- ✅ Check `clear/logs/` directory exists
- ✅ Test with `python cli.py --status`
- ✅ Review configuration settings

## 3. Operational Rules

### 3.1 Safe Mode (Mandatory)

**Memory Clearer runs in Safe Mode by default.**

Safe Mode:
- ✅ Protects system-critical files
- ✅ Only cleans user directories
- ✅ Requires explicit permission
- ✅ Logs all operations

**Status:** Enabled by default in `config.ini`

```ini
[Cleanup]
safe_mode = true
```

**Rule:** Do NOT disable Safe Mode unless you are advanced user

### 3.2 Running the Application

#### GUI Mode (Recommended)
```bash
python memory_clearer.py        # Start with GUI
# Or simply double-click run.bat (Windows)
```

#### CLI Mode
```bash
python cli.py --status          # Show memory status
python cli.py --clean           # Quick cleanup
python cli.py --monitor         # Monitor memory
```

#### Daemon Mode (Background)
```bash
python monitor_daemon.py        # Run in background
# Press Ctrl+C to stop
```

### 3.3 Cleanup Operations

**Quick Clean** (Safe)
- Removes temporary files
- Clears common cache directories
- Safe for regular use
- ~2-5 minutes per run

**Deep Clean** (Cautious)
- Comprehensive system cleanup
- Removes browser caches
- Clears old log files
- 5-15 minutes per run
- Verify configuration first

**Auto-Clean** (Scheduled)
- Runs at specified intervals
- Triggered by memory threshold
- Respects Safe Mode settings
- Monitor logs for details

### 3.4 Pre-Cleanup Checklist

Before running cleanup:

- [ ] Close all open applications
- [ ] Save all work in progress
- [ ] Back up important files (first run only)
- [ ] Disable active downloads
- [ ] Close browser windows
- [ ] Disable antivirus (optional)
- [ ] Ensure adequate disk space (>100 MB free)

## 4. Configuration Rules

### 4.1 Configuring Memory Threshold

```ini
[Memory]
threshold = 80
```

**Rule:** Set between 50-95
- Too low (50-60): Aggressive cleaning
- Recommended: 75-85
- Too high (90-95): Wait until critical

### 4.2 Configuring Cleanup Paths

```ini
[Paths]
temp_dirs = C:\Windows\Temp,C:\Users\%USERNAME%\AppData\Local\Temp
cache_dirs = ~/.cache
exclude_dirs = /important,/critical
```

**Rule:** Never include system paths
- ✅ Safe: `/tmp`, `~/.cache`, `%TEMP%`
- ❌ Unsafe: `C:\Windows`, `/etc`, `/bin`
- ❌ Unsafe: Program installation directories

### 4.3 Logging Configuration

```ini
[Logging]
level = INFO              # DEBUG, INFO, WARNING, ERROR
directory = clear/logs
max_file_size = 10485760  # 10 MB
```

**Rule:** Use INFO level for normal operation
- DEBUG: Only when troubleshooting
- WARNING: Only for critical issues
- ERROR: Production use not recommended

## 5. Safety Rules

### 5.1 Critical Don'ts

❌ **NEVER:**
- Run without Safe Mode (unless expert)
- Clean system directories
- Delete files from Program Files
- Run as SYSTEM account (Windows)
- Ignore permission errors
- Disable all backup systems

### 5.2 Backup Requirements

**Before major changes:**
```bash
# Windows
Backup-ComputerConfig.ps1

# Linux
tar czf ~/memory_clearer_backup.tar.gz clear/

# macOS
ditto ~/memory_clearer ~/memory_clearer_backup
```

### 5.3 Permission Handling

| Situation | Action |
|-----------|--------|
| Permission Denied | Skip that file, continue |
| Access Forbidden | Check user permissions |
| File Locked | Close application holding file |
| System Protected | Enable Safe Mode, skip |
| Security Blocked | Check antivirus settings |

## 6. Monitoring Guidelines

### 6.1 Real-Time Monitoring

```bash
python monitor_daemon.py
```

**Monitor will:**
- Check memory every 5 seconds (configurable)
- Log usage patterns
- Alert on threshold breaches
- Auto-trigger cleanup if configured

**Rule:** Run monitoring in separate terminal window

### 6.2 Log Review

**Regular Review:**
- Daily: Check for errors
- Weekly: Review cleanup summaries
- Monthly: Archive old logs

**Logs Location:** `clear/logs/memory_clearer.log`

**View logs:**
```bash
# Windows
type clear\logs\memory_clearer.log

# Linux/Mac
cat clear/logs/memory_clearer.log
tail -f clear/logs/memory_clearer.log  # Real-time
```

## 7. Performance Guidelines

### 7.1 System Impact

| Setting | CPU Impact | RAM Impact | Speed |
|---------|-----------|-----------|-------|
| Quick Clean | Low | Low | 2-5 min |
| Deep Clean | Medium | Medium | 5-15 min |
| Auto-Clean | Very Low | Low | N/A |
| Monitoring | Very Low | Very Low | N/A |

### 7.2 Optimization Tips

**For Slow Systems:**
```ini
[Memory]
check_interval = 30       # Check every 30 seconds

[Cleanup]
auto_cleanup_interval = 7200    # Clean every 2 hours
safe_mode = true          # Protect system
```

**For Fast Systems:**
```ini
[Memory]
check_interval = 1        # Check every second

[Cleanup]
auto_cleanup_interval = 1800    # Clean every 30 minutes
```

## 8. Troubleshooting Rules

### 8.1 Common Issues

**Application crashes:**
1. Check log file: `clear/logs/memory_clearer.log`
2. Verify Python version: `python --version`
3. Reinstall dependencies: `pip install -r requirements.txt`
4. Run setup: `python setup_memory_clearer.py`

**GUI not starting:**
1. Try CLI mode: `python cli.py --status`
2. Check display server (Linux)
3. Verify tkinter installed: `python -m tkinter`

**Permission errors:**
1. Run with admin/sudo
2. Check file permissions
3. Adjust config paths
4. Enable Safe Mode

**Memory not decreasing:**
1. Close applications hogging memory
2. Increase cleanup frequency
3. Enable Deep Clean
4. Check available disk space

### 8.2 When to Seek Help

✅ **OK to troubleshoot:**
- Configuration issues
- Log analysis
- Performance tuning

❌ **Seek professional help for:**
- System crashes
- Data loss
- File system corruption
- Security concerns

## 9. Advanced Usage

### 9.1 Command-Line Arguments

```bash
python cli.py --status              # Show memory status
python cli.py --clean              # Perform quick cleanup
python cli.py --deep-clean         # Deep system cleanup
python cli.py --monitor            # Start monitoring
python cli.py --config <file>      # Use custom config
```

### 9.2 Custom Cleanup Scripts

```python
# custom_cleanup.py
from utils import setup_logging, get_memory_info_mb
import gc

logger = setup_logging()
logger.info("Running custom cleanup...")
gc.collect()
logger.info("Custom cleanup complete")
```

### 9.3 Scheduling (Windows Task Scheduler)

```batch
# Create scheduled task
schtasks /create /tn "Memory Clearer" /tr "python C:\path\to\cli.py --clean" /sc HOURLY
```

### 9.4 Scheduling (Linux Cron)

```bash
# Edit crontab
crontab -e

# Add: Run cleanup every hour
0 * * * * /usr/bin/python3 /path/to/cli.py --clean
```

## 10. Compliance & Legal

### 10.1 License Compliance

- ✅ MIT License allows: modification, distribution, commercial use
- ⚠️ Must include: license notice, copyright
- ❌ Prohibited: Hold liable, remove attribution

### 10.2 Terms Acceptance

By using Memory Clearer:
- You accept Terms of Service
- You understand Privacy Policy
- You acknowledge usage rules
- You accept "as-is" warranty disclaimer

### 10.3 Liability

**The Software is provided "AS IS" without warranty.**

Users accept responsibility for:
- Data loss or corruption
- System instability
- Performance issues
- Security breaches

## 11. Support & Reporting

### 11.1 Getting Help

1. **Documentation:** Read README.md and docs/
2. **Troubleshooting:** See TROUBLESHOOTING.md
3. **GitHub Issues:** Search existing issues
4. **Create Issue:** Include logs and configuration

### 11.2 Reporting Bugs

**Include:**
- OS and version
- Python version
- Complete error message
- Steps to reproduce
- Relevant log files
- Configuration (sanitized)

### 11.3 Feature Requests

**Submit via:**
- GitHub Issues with `[FEATURE]` tag
- Include use case and expected behavior
- Provide examples if possible

## 12. End-User License Agreement (EULA)

By installing and using Memory Clearer, you:

✅ **Agree to:**
- Follow these usage guidelines
- Accept safety warnings
- Take responsibility for backups
- Comply with applicable laws

❌ **Prohibited:**
- Illegal use
- System harm
- License violation
- Terms violation

---

## Quick Reference

| Action | Command | Safety |
|--------|---------|--------|
| Check Status | `cli.py --status` | ✅ Safe |
| Quick Clean | `cli.py --clean` | ✅ Safe |
| Deep Clean | `cli.py --deep-clean` | ⚠️ Caution |
| Monitor | `monitor_daemon.py` | ✅ Safe |
| GUI | `memory_clearer.py` | ✅ Safe |

---

**For more information:**
- 📖 See README.md
- 🔒 See PRIVACY.md
- ⚖️ See TERMS.md
- 🛠️ See DEVELOPMENT.md
- 🆘 See TROUBLESHOOTING.md

---

**Memory Clearer © 2024 - All Rights Reserved**

**License:** MIT License
