# Development Guide

Guide for developers working on Memory Clearer.

## Project Structure

```
cleaner/
├── cli.py                  # Command-line interface
├── memory_clearer.py       # GUI application
├── monitor_daemon.py       # Background monitoring service
├── utils.py               # Utility functions
├── setup_memory_clearer.py # Setup/initialization script
├── config.ini             # Configuration file
├── requirements.txt       # Python dependencies
├── clear/
│   ├── cache/            # Cache files (generated)
│   └── logs/             # Log files (generated)
├── docs/                 # Documentation
├── tests/                # Unit tests
├── README.md             # Main documentation
├── CHANGELOG.md          # Version history
├── CONTRIBUTING.md       # Contribution guidelines
├── TROUBLESHOOTING.md    # Troubleshooting guide
└── QUICK_START.md        # Quick start guide
```

## Setting Up Development Environment

1. **Clone and navigate**:
   ```bash
   cd cleaner
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate it**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest  # For running tests
   ```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest -v tests/

# Run specific test file
pytest tests/test_memory.py

# Run with coverage
pytest --cov=. tests/
```

## Code Style

Follow PEP 8:

```bash
pip install flake8
flake8 *.py
```

## Key Modules

### `cli.py`
- Entry point for command-line usage
- Functions: `show_status()`, `clean_memory()`, `monitor()`
- Handles argument parsing

### `memory_clearer.py`
- GUI application
- Uses tkinter for cross-platform compatibility
- Real-time dashboard display

### `monitor_daemon.py`
- Background service
- Continuous memory monitoring
- Auto-cleanup trigger logic

### `utils.py`
- `get_memory_info_mb()` - Get system memory stats
- `setup_logging()` - Configure logging
- `create_directories()` - Create necessary dirs

## Adding New Features

### Feature: Custom Cleanup Paths

1. **Edit config.ini**:
   ```ini
   [Cleanup]
   custom_paths = C:\MyTemp,D:\Cache
   ```

2. **Add function in utils.py**:
   ```python
   def clean_custom_paths():
       """Clean custom paths defined in config"""
       # Implementation
   ```

3. **Add CLI argument in cli.py**:
   ```python
   parser.add_argument('--custom', help='Clean custom paths')
   ```

4. **Add tests in tests/**:
   ```python
   def test_clean_custom_paths(self):
       # Test implementation
   ```

5. **Update README.md** with new feature

## Debugging

### Enable Debug Logging

Edit `config.ini`:
```ini
[Logging]
level = DEBUG
```

### View Logs

```bash
# Windows
type clear\logs\memory_clearer.log

# Linux/Mac
cat clear/logs/memory_clearer.log

# Follow in real-time (Linux/Mac)
tail -f clear/logs/memory_clearer.log
```

### Use Python Debugger

```python
import pdb; pdb.set_trace()  # Add breakpoint
```

## Building Distribution

```bash
# Create standalone exe (Windows)
pip install pyinstaller
pyinstaller --onefile cli.py

# Result in dist/cli.exe
```

## Continuous Integration

Set up GitHub Actions by creating `.github/workflows/tests.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt pytest
      - run: pytest tests/
```

## Common Development Tasks

### Add new dependency
```bash
pip install package-name
pip freeze > requirements.txt
```

### Update version
1. Edit version string in relevant files
2. Update CHANGELOG.md
3. Tag in git: `git tag v2.0.0`

### Format code
```bash
pip install black
black *.py
```

### Check for issues
```bash
pip install pylint
pylint *.py
```

## Performance Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile here

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

## Useful Resources

- [Python Documentation](https://docs.python.org/3/)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [PEP 8 Style Guide](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
