# monitor_daemon.py - Background monitoring daemon
import time
import psutil
import logging
from pathlib import Path
from datetime import datetime
from utils import setup_logging, load_config, get_memory_info_mb, create_directories

class MemoryMonitorDaemon:
    def __init__(self):
        self.config = load_config()
        self.logger = setup_logging()
        self.is_running = False
        
        # Get settings from config
        try:
            self.check_interval = int(self.config.get('Monitoring', 'check_interval', fallback='30'))
            self.alert_threshold = int(self.config.get('Monitoring', 'alert_threshold_mb', fallback='500'))
        except:
            self.check_interval = 30
            self.alert_threshold = 500
        
        self.logger.info("Memory Monitor Daemon initialized")
    
    def check_memory(self):
        """Check current memory usage"""
        try:
            memory_info = get_memory_info_mb()
            if memory_info:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'used_mb': memory_info['used_mb'],
                    'available_mb': memory_info['available_mb'],
                    'percent': memory_info['percent'],
                    'free_mb': memory_info['free_mb']
                }
        except Exception as e:
            self.logger.error(f"Error checking memory: {e}")
        return None
    
    def log_memory_status(self, memory_info):
        """Log memory status"""
        if memory_info:
            msg = (f"Memory: {memory_info['used_mb']:.0f}MB used, "
                   f"{memory_info['available_mb']:.0f}MB available, "
                   f"{memory_info['percent']:.1f}% usage")
            self.logger.info(msg)
            
            # Alert if threshold exceeded
            if memory_info['used_mb'] > self.alert_threshold:
                alert_msg = f"⚠️  ALERT: Memory usage high! {memory_info['used_mb']:.0f}MB"
                self.logger.warning(alert_msg)
                return True
        return False
    
    def cleanup_memory(self):
        """Attempt to free up memory"""
        try:
            import gc
            collected = gc.collect()
            self.logger.info(f"Garbage collection: freed {collected} objects")
            return True
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            return False
    
    def run(self):
        """Main daemon loop"""
        self.is_running = True
        self.logger.info("Memory Monitor Daemon started")
        
        try:
            while self.is_running:
                # Check memory
                memory_info = self.check_memory()
                alert = self.log_memory_status(memory_info)
                
                # Auto-cleanup if threshold exceeded
                if alert:
                    self.logger.info("Attempting automatic cleanup...")
                    self.cleanup_memory()
                
                # Wait for next check
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            self.logger.info("Daemon interrupted by user")
        except Exception as e:
            self.logger.error(f"Daemon error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the daemon"""
        self.is_running = False
        self.logger.info("Memory Monitor Daemon stopped")

if __name__ == "__main__":
    create_directories()
    daemon = MemoryMonitorDaemon()
    daemon.run()
