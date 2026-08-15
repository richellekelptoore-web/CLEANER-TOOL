"""Unit tests for utility functions"""

import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import create_directories


class TestUtilFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_create_directories(self):
        """Test directory creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, 'test_cache')
            
            # Should not raise an exception
            try:
                create_directories()
                self.assertTrue(os.path.exists('clear/cache'))
                self.assertTrue(os.path.exists('clear/logs'))
            except Exception as e:
                self.fail(f"create_directories() raised {type(e).__name__}")


class TestConfigFile(unittest.TestCase):
    """Test configuration handling"""
    
    def test_config_exists(self):
        """Test that config file exists"""
        self.assertTrue(os.path.exists('config.ini'))


if __name__ == '__main__':
    unittest.main()
