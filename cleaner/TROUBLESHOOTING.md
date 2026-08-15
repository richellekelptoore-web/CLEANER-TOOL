# Troubleshooting Guide

## Common Issues & Solutions

### Issue: "Memory info not found" error

**Cause**: `psutil` module not installed or incompatible version

**Solution**:
```bash
pip install --upgrade psutil>=5.8.0
```

### Issue: Permission denied when cleaning cache

**Cause**: Insufficient file permissions

**Solution**:
- **Windows**: Run Command Prompt or PowerShell as Administrator
- **Linux/Mac**: Use `sudo python cli.py --clean`
- **Better**: Configure cleanup paths to user-writable directories in `config.ini`

### Issue: Daemon not staying running

**Cause**: Process terminated or insufficient resources

**Solution**:
1. Check logs in `clear/logs/memory_clearer.log`
2. Verify sufficient disk space available
3. Check system event logs (Windows) or system logs (Linux)
4. Restart the daemon:
   ```bash
   python monitor_daemon.py
   ```

### Issue: GUI not starting

**Cause**: Missing GUI dependencies or display server issues

**Solution**:
- **Windows**: Ensure you have a display server
- **Linux**: Check X11/Wayland configuration
- **Alternative**: Use CLI instead:
  ```bash
  python cli.py --status
  ```

### Issue: High memory usage by Memory Clearer

**Cause**: Monitoring frequency too high, excessive logging

**Solution**:
1. Edit `config.ini` and increase `monitor_interval`
2. Reduce `log_level` from DEBUG to INFO
3. Check `clear/logs/` for excessive log file size

### Issue: Cannot import module errors

**Cause**: Virtual environment not activated

**Solution**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Verify with
python -c "import psutil; print(psutil.__version__)"
```

### Issue: Config file not found

**Cause**: Missing or misconfigured `config.ini`

**Solution**:
```bash
python setup_memory_clearer.py
```

This will regenerate default configuration.

## Performance Tips

1. **Increase monitor interval** in `config.ini` to reduce CPU usage
2. **Disable deep clean** if not needed; use quick clean instead
3. **Limit log retention** by configuring log rotation
4. **Run during off-peak hours** to avoid system slowdown

## Getting Help

1. Check relevant log files in `clear/logs/`
2. Review this troubleshooting guide
3. Search existing GitHub issues
4. Create a new issue with:
   - Your OS and Python version
   - Complete error message
   - Steps to reproduce
   - Relevant log excerpts
