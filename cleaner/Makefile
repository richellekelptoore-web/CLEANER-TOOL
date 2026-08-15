.PHONY: help install clean test run monitor status setup lint format

help:
	@echo "Memory Clearer - Available commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make setup      - Run initial setup"
	@echo "  make status     - Show memory status"
	@echo "  make clean      - Perform memory cleanup"
	@echo "  make monitor    - Start monitoring daemon"
	@echo "  make test       - Run unit tests"
	@echo "  make lint       - Check code style"
	@echo "  make format     - Format code (autopep8)"
	@echo "  make dev-setup  - Setup development environment"
	@echo "  make clean-all  - Remove all build artifacts"
	@echo ""

install:
	pip install -r requirements.txt

setup:
	python setup_memory_clearer.py

status:
	python cli.py --status

clean:
	python cli.py --clean

monitor:
	python monitor_daemon.py

test:
	python -m pytest tests/ -v

lint:
	python -m flake8 *.py tests/

format:
	python -m autopep8 --in-place --aggressive *.py

dev-setup: install
	pip install pytest flake8 autopep8 black pylint

clean-all:
	rm -rf __pycache__ .pytest_cache .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
