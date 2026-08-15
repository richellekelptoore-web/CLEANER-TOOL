# Contributing to Memory Clearer

Thank you for your interest in contributing! Here's how you can help.

## Getting Started

1. **Fork the repository** and clone your fork locally
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test thoroughly

3. **Run tests** (before committing):
   ```bash
   python -m pytest tests/
   ```

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: description of what you added"
   git commit -m "Fix: description of what you fixed"
   ```

5. **Push and create a Pull Request**

## Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation as needed
- Test on Windows, Linux, and macOS if possible

## Reporting Issues

- Check if the issue already exists
- Provide clear reproduction steps
- Include your Python version and OS
- Attach relevant error logs from `clear/logs/`

## Areas for Contribution

- Bug fixes and stability improvements
- Performance optimizations
- New cleanup features
- Documentation improvements
- Cross-platform testing
- Code quality enhancements
