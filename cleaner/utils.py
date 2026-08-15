# utils.py - Utility functions for Memory Clearer
import os
import sys
import psutil
import logging
from datetime import datetime
from pathlib import Path
import configparser

def setup_logging(log_path="clear/logs"):
    """Setup logging configuration"""
    Path(log_path).mkdir(parents=True, exist_ok=True)
    
    log_file = Path(log_path) / f"memory_clearer_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_config(config_file="config.ini"):
    """Load configuration from ini file"""
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
    return config

def get_memory_info():
    """Get current system memory information"""
    try:
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'used': memory.used,
            'available': memory.available,
            'percent': memory.percent,
            'free': memory.free
        }
    except Exception as e:
        logging.error(f"Error getting memory info: {e}")
        return None

def get_memory_info_mb():
    """Get memory info in MB"""
    info = get_memory_info()
    if info:
        return {
            'total_mb': info['total'] / (1024 * 1024),
            'used_mb': info['used'] / (1024 * 1024),
            'available_mb': info['available'] / (1024 * 1024),
            'free_mb': info['free'] / (1024 * 1024),
            'percent': info['percent']
        }
    return None

def create_directories():
    """Create necessary directory structure"""
    dirs = [
        'clear',
        'clear/logs',
        'clear/cache',
        'clear/backups',
        'clear/temp_cleanup',
        'clear/config'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def cleanup_old_logs(log_path="clear/logs", days=7):
    """Clean up log files older than specified days"""
    import time
    now = time.time()
    for file in Path(log_path).glob("*.log"):
        if os.stat(file).st_mtime < now - days * 86400:
            try:
                file.unlink()
                logging.info(f"Deleted old log: {file}")
            except Exception as e:
                logging.error(f"Failed to delete log {file}: {e}")

def format_bytes(bytes_value):
    """Format bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} TB"

def is_admin():
    """Check if running with admin privileges"""
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    logger = setup_logging()
    info = get_memory_info_mb()
    print(f"Memory Info: {info}")
