"""Unit tests for memory utilities"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import get_memory_info_mb


class TestMemoryUtils(unittest.TestCase):
    """Test memory utility functions"""
    
    def test_get_memory_info_returns_dict(self):
        """Test that get_memory_info returns a dictionary"""
        result = get_memory_info_mb()
        self.assertIsInstance(result, dict)
    
    def test_memory_info_has_required_keys(self):
        """Test that memory info contains required keys"""
        result = get_memory_info_mb()
        required_keys = ['total_mb', 'used_mb', 'available_mb', 'free_mb', 'percent']
        for key in required_keys:
            self.assertIn(key, result)
    
    def test_memory_values_are_positive(self):
        """Test that memory values are positive"""
        result = get_memory_info_mb()
        self.assertGreater(result['total_mb'], 0)
        self.assertGreaterEqual(result['used_mb'], 0)
        self.assertGreaterEqual(result['available_mb'], 0)
        self.assertGreaterEqual(result['free_mb'], 0)
    
    def test_percent_in_valid_range(self):
        """Test that memory percentage is 0-100"""
        result = get_memory_info_mb()
        self.assertGreaterEqual(result['percent'], 0)
        self.assertLessEqual(result['percent'], 100)
    
    def test_used_less_than_total(self):
        """Test that used memory is less than total"""
        result = get_memory_info_mb()
        self.assertLessEqual(result['used_mb'], result['total_mb'])


if __name__ == '__main__':
    unittest.main()
