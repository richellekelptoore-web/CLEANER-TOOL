# cli.py - Command-line interface for Memory Clearer
import sys
import os
import argparse
import time
from utils import setup_logging, get_memory_info_mb, create_directories
from monitor_daemon import MemoryMonitorDaemon

def check_official_installation():
    """Check if this is an official installation"""
    if not os.path.exists('.official_marker'):
        print("\n" + "="*60)
        print("⚠️  WARNING: UNOFFICIAL INSTALLATION DETECTED")
        print("="*60)
        print("\nThis folder does not appear to be from the official source.\n")
        print("RECOMMENDED:")
        print("  • Clone from: https://github.com/[official-repo]")
        print("  • Install via pip: pip install memory-clearer")
        print("\nLEGAL NOTICE:")
        print("  • Ensure COPYRIGHT_NOTICE.txt is included")
        print("  • MIT License requires proper attribution\n")
        print("="*60 + "\n")
    
    if not os.path.exists('COPYRIGHT_NOTICE.txt'):
        print("⚠️  WARNING: COPYRIGHT_NOTICE.txt is missing")
        print("   This file is required by MIT License.\n")

def show_copyright():
    """Show copyright and license information"""
    print("\n" + "="*60)
    print("MEMORY CLEARER - COPYRIGHT & LICENSE")
    print("="*60)
    print("\nCopyright © 2024 Memory Clearer Contributors")
    print("Licensed under MIT License\n")
    print("OFFICIAL INSTALLATION:")
    print("  ✓ Clone from official GitHub repository")
    print("  ✓ Install via pip: pip install memory-clearer")
    print("  ✓ Download from official website\n")
    print("LICENSE TERMS:")
    print("  ✓ Free to use and modify")
    print("  ✓ Can be used commercially")
    print("  ✓ Can be redistributed\n")
    print("REQUIREMENTS:")
    print("  • Include copyright notice")
    print("  • Include LICENSE file")
    print("  • Provide proper attribution\n")
    print("VERIFICATION:")
    print("  • Official installations include .official_marker")
    print("  • Missing markers indicate unofficial copy")
    print("  • Always verify source before use\n")
    print("For official version:")
    print("https://github.com/[official-repo]")
    print("="*60 + "\n")

def show_status():
    """Show current system status"""
    memory_info = get_memory_info_mb()
    if memory_info:
        print("\n" + "="*50)
        print("  Memory Clearer - System Status")
        print("="*50)
        print(f"Total Memory:     {memory_info['total_mb']:.0f} MB")
        print(f"Used Memory:      {memory_info['used_mb']:.0f} MB")
        print(f"Available Memory: {memory_info['available_mb']:.0f} MB")
        print(f"Free Memory:      {memory_info['free_mb']:.0f} MB")
        print(f"Memory Usage:     {memory_info['percent']:.1f}%")
        print("="*50 + "\n")
    else:
        print("Error: Could not retrieve memory info")

def clean_memory():
    """Quick memory cleanup"""
    logger = setup_logging()
    import gc
    
    print("Starting memory cleanup...")
    show_status()
    
    try:
        collected = gc.collect()
        print(f"✓ Garbage collection completed: freed {collected} objects")
        
        time.sleep(1)
        print("\nAfter cleanup:")
        show_status()
        logger.info("Manual cleanup completed successfully")
        
    except Exception as e:
        print(f"✗ Error during cleanup: {e}")
        logger.error(f"Cleanup failed: {e}")
        sys.exit(1)

def start_monitor():
    """Start monitoring daemon"""
    print("Starting Memory Monitor Daemon...")
    print("Press Ctrl+C to stop\n")
    
    try:
        daemon = MemoryMonitorDaemon()
        daemon.run()
    except KeyboardInterrupt:
        print("\n\nMonitor stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    # Check official installation
    check_official_installation()
    
    parser = argparse.ArgumentParser(
        description="Memory Clearer - System memory management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --status      Show current memory status
  python cli.py --clean       Perform quick memory cleanup
  python cli.py --monitor     Start background monitoring daemon
  python cli.py --copyright   Show copyright and license information
        """
    )
    
    parser.add_argument('--status', action='store_true', 
                        help='Show current memory status')
    parser.add_argument('--clean', action='store_true',
                        help='Perform quick memory cleanup')
    parser.add_argument('--monitor', action='store_true',
                        help='Start monitoring daemon')
    parser.add_argument('--copyright', action='store_true',
                        help='Show copyright and license information')
    parser.add_argument('--version', action='version', version='Memory Clearer v2.0')
    
    args = parser.parse_args()
    
    # Create directories if they don't exist
    create_directories()
    
    # Handle copyright flag
    if args.copyright:
        show_copyright()
        return
    
    # Default to status if no args
    if not any(vars(args).values()):
        show_status()
        return
    
    # Execute requested action
    if args.status:
        show_status()
    elif args.clean:
        clean_memory()
    elif args.monitor:
        start_monitor()

if __name__ == "__main__":
    main()
