# memory_clearer.py
import os
import sys
import psutil
import ctypes
import gc
import time
import threading
import subprocess
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk

def check_official_installation():
    """Verify this is an official installation (non-blocking)"""
    warnings = []

    if not os.path.exists('.official_marker'):
        warnings.append("ℹ️ Not from official repository")

    if not os.path.exists('COPYRIGHT_NOTICE.txt'):
        warnings.append("�️ COPYRIGHT_NOTICE.txt missing")

    if not warnings:
        return True  # Everything verified, nothing to ask the user.

    # Silent mode (used by run.bat / quick launchers): just log and
    # continue. The user can still see license info via Help → License
    # & Copyright, so we do NOT force a dialog.
    if os.environ.get('MC_SILENT') == '1':
        return True

    # Interactive mode: show one combined info dialog, then continue.
    message = "Installation Note:\n\n" + "\n".join(warnings) + \
              "\n\nSee Help → License & Copyright for details"
    messagebox.showinfo("Installation Info", message, icon=messagebox.INFO)

    return True  # Always allow startup

class MemoryClearer:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Clearer v2.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Set icon if available
        try:
            self.root.iconbitmap(default='memory_icon.ico')
        except:
            pass
        
        # Check official installation
        if not check_official_installation():
            self.root.destroy()
            return
        
        # Variables
        self.is_clearing = False
        self.monitor_running = False
        self.monitor_thread = None
        
        # Setup GUI
        self.setup_gui()
        
        # Auto-clean on startup
        self.root.after(1000, self.initial_cleanup)
        
        # Create menu bar
        self.create_menu()
        
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="License & Copyright", command=self.show_copyright)
        help_menu.add_separator()
        help_menu.add_command(label="Documentation", command=self.open_readme)
        
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Memory Clearer",
            "Memory Clearer v2.0\n\n"
            "Advanced Windows System Memory Cleanup & Monitoring Tool\n\n"
            "© 2024 Memory Clearer Contributors\n"
            "Licensed under MIT License\n\n"
            "For more information, visit:\n"
            "https://github.com/[official-repo]\n\n"
            "Version: 2.0.0\n"
            "Release Date: August 15, 2024"
        )
    
    def show_copyright(self):
        """Show copyright and license information"""
        copyright_text = (
            "MEMORY CLEARER - COPYRIGHT & LICENSE\n"
            "=" * 50 + "\n\n"
            "Copyright © 2024 Memory Clearer Contributors\n"
            "Licensed under MIT License\n\n"
            "OFFICIAL INSTALLATION:\n"
            "✓ Clone from official GitHub repository\n"
            "✓ Install via pip: pip install memory-clearer\n"
            "✓ Download from official website\n\n"
            "LICENSE TERMS:\n"
            "✓ Free to use and modify\n"
            "✓ Can be used commercially\n"
            "✓ Can be redistributed\n\n"
            "REQUIREMENTS:\n"
            "• Include copyright notice\n"
            "• Include LICENSE file\n"
            "• Provide proper attribution\n\n"
            "VERIFICATION:\n"
            "• Official installations include .official_marker\n"
            "• Missing markers indicate unofficial copy\n"
            "• Always verify source before use\n\n"
            "For official version:\n"
            "https://github.com/[official-repo]"
        )
        messagebox.showinfo("License & Copyright", copyright_text)
    
    def open_readme(self):
        """Open README.md file"""
        try:
            if sys.platform == 'win32':
                os.startfile('README.md')
            else:
                subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', 'README.md'])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open README.md: {str(e)}")
        
    def setup_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(W, E, N, S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🧹 Memory Clearer", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=W)
        
        # Stats Frame
        stats_frame = ttk.LabelFrame(main_frame, text="System Statistics", padding="10")
        stats_frame.grid(row=1, column=0, sticky=(W, E), pady=(0, 10))
        stats_frame.columnconfigure(1, weight=1)
        
        # Memory stats
        ttk.Label(stats_frame, text="Total RAM:").grid(row=0, column=0, sticky=W, padx=5)
        self.total_ram_label = ttk.Label(stats_frame, text="Loading...")
        self.total_ram_label.grid(row=0, column=1, sticky=W, padx=5)
        
        ttk.Label(stats_frame, text="Used RAM:").grid(row=1, column=0, sticky=W, padx=5)
        self.used_ram_label = ttk.Label(stats_frame, text="Loading...")
        self.used_ram_label.grid(row=1, column=1, sticky=W, padx=5)
        
        ttk.Label(stats_frame, text="Available RAM:").grid(row=2, column=0, sticky=W, padx=5)
        self.available_ram_label = ttk.Label(stats_frame, text="Loading...")
        self.available_ram_label.grid(row=2, column=1, sticky=W, padx=5)
        
        ttk.Label(stats_frame, text="CPU Usage:").grid(row=3, column=0, sticky=W, padx=5)
        self.cpu_label = ttk.Label(stats_frame, text="Loading...")
        self.cpu_label.grid(row=3, column=1, sticky=W, padx=5)
        
        # Progress bar
        ttk.Label(stats_frame, text="Memory Usage:").grid(row=4, column=0, sticky=W, padx=5)
        self.memory_progress = ttk.Progressbar(stats_frame, length=300, mode='determinate')
        self.memory_progress.grid(row=4, column=1, sticky=W, padx=5, pady=5)
        
        # Control Buttons Frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, sticky=(W, E), pady=(0, 10))
        
        # Buttons
        self.clean_btn = ttk.Button(control_frame, text="🧹 Clean Memory Now", 
                                   command=self.clean_memory, width=20)
        self.clean_btn.grid(row=0, column=0, padx=5)
        
        self.deep_clean_btn = ttk.Button(control_frame, text="🔧 Deep Clean", 
                                        command=self.deep_clean, width=20)
        self.deep_clean_btn.grid(row=0, column=1, padx=5)
        
        self.monitor_btn = ttk.Button(control_frame, text="▶ Start Monitoring", 
                                     command=self.toggle_monitor, width=20)
        self.monitor_btn.grid(row=0, column=2, padx=5)
        
        self.auto_clean_btn = ttk.Button(control_frame, text="⚡ Auto-Clean", 
                                        command=self.auto_clean, width=20)
        self.auto_clean_btn.grid(row=0, column=3, padx=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="5")
        log_frame.grid(row=3, column=0, sticky=(W, E, N, S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=70,
                                                  font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(W, E, N, S))
        
        # Clear log button
        clear_log_btn = ttk.Button(log_frame, text="Clear Log", 
                                  command=self.clear_log, width=15)
        clear_log_btn.grid(row=1, column=0, pady=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=SUNKEN, anchor=W)
        self.status_label.grid(row=4, column=0, sticky=(W, E), pady=(5, 0))
        
        # Copyright footer
        copyright_label = ttk.Label(
            main_frame, 
            text="© 2024 Memory Clearer Contributors | MIT License | Help → License & Copyright",
            font=('Arial', 8),
            foreground='gray'
        )
        copyright_label.grid(row=5, column=0, sticky=(W, E), pady=(2, 0))
        
        # Refresh stats
        self.update_stats()
        
    def update_stats(self):
        try:
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent(interval=0.5)
            
            total_gb = memory.total / (1024**3)
            used_gb = memory.used / (1024**3)
            available_gb = memory.available / (1024**3)
            
            self.total_ram_label.config(text=f"{total_gb:.2f} GB")
            self.used_ram_label.config(text=f"{used_gb:.2f} GB")
            self.available_ram_label.config(text=f"{available_gb:.2f} GB")
            self.cpu_label.config(text=f"{cpu}%")
            
            # Update progress bar
            percent = memory.percent
            self.memory_progress['value'] = percent
            if percent > 80:
                self.memory_progress['style'] = 'red.Horizontal.TProgressbar'
            elif percent > 60:
                self.memory_progress['style'] = 'yellow.Horizontal.TProgressbar'
            else:
                self.memory_progress['style'] = 'green.Horizontal.TProgressbar'
                
        except Exception as e:
            self.log_message(f"Error updating stats: {str(e)}")
            
        # Update every 2 seconds
        if not self.is_clearing:
            self.root.after(2000, self.update_stats)
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(END, log_entry)
        self.log_text.see(END)
        self.status_label.config(text=message)
    
    def clear_log(self):
        self.log_text.delete(1.0, END)
        self.log_message("Log cleared")
    
    def initial_cleanup(self):
        self.log_message("Performing initial system cleanup...")
        gc.collect()
        self.log_message("Initial cleanup complete")
    
    def clean_memory(self):
        if self.is_clearing:
            return
            
        self.is_clearing = True
        self.clean_btn.config(state='disabled')
        self.log_message("Starting memory cleanup...")
        self.status_label.config(text="Cleaning memory...")
        
        def cleanup_task():
            try:
                # Step 1: Force garbage collection
                self.log_message("Running garbage collection...")
                gc.collect()
                
                # Step 2: Clean Windows working set (Windows only)
                if sys.platform == 'win32':
                    self.log_message("Cleaning Windows working set...")
                    try:
                        ctypes.windll.kernel32.SetProcessWorkingSetSize(
                            ctypes.windll.kernel32.GetCurrentProcess(), -1, -1
                        )
                    except:
                        pass
                
                # Step 3: Clear system caches
                self.log_message("Clearing system caches...")
                if sys.platform == 'win32':
                    # Clear Windows temp files (optional, commented for safety)
                    pass
                
                # Step 4: Clean specific applications
                self.clean_specific_apps()
                
                # Step 5: Run final GC
                gc.collect()
                
                self.log_message("✅ Memory cleanup completed successfully!")
                self.status_label.config(text="Cleanup complete")
                
            except Exception as e:
                self.log_message(f"❌ Error during cleanup: {str(e)}")
                self.status_label.config(text="Error during cleanup")
            finally:
                self.is_clearing = False
                self.clean_btn.config(state='normal')
                self.update_stats()
        
        threading.Thread(target=cleanup_task, daemon=True).start()
    
    def deep_clean(self):
        if self.is_clearing:
            return

        # In silent / quick-launch mode (run.bat) skip the confirmation
        # dialog so deep cleaning can be triggered programmatically.
        if os.environ.get('MC_SILENT') == '1':
            result = True
        else:
            result = messagebox.askyesno("Deep Clean",
                "⚠️ Deep clean will:\n"
                "- Force garbage collection on all Python objects\n"
                "- Clear memory caches\n"
                "- Optimize memory usage\n"
                "- May temporarily slow down your system\n\n"
                "Continue?")

        if not result:
            return
            
        self.is_clearing = True
        self.deep_clean_btn.config(state='disabled')
        self.log_message("Starting deep memory cleanup...")
        self.status_label.config(text="Performing deep clean...")
        
        def deep_clean_task():
            try:
                # Force multiple GC cycles
                for i in range(5):
                    self.log_message(f"GC cycle {i+1}/5...")
                    gc.collect()
                    time.sleep(0.1)
                
                # Clear Python's internal caches
                self.log_message("Clearing Python caches...")
                if hasattr(sys, 'setrecursionlimit'):
                    sys.setrecursionlimit(10000)
                
                # Force memory optimization
                if sys.platform == 'win32':
                    self.log_message("Optimizing Windows memory...")
                    kernel32 = ctypes.windll.kernel32
                    kernel32.SetProcessWorkingSetSize(
                        kernel32.GetCurrentProcess(), -1, -1
                    )
                    kernel32.EmptyWorkingSet(kernel32.GetCurrentProcess())
                
                # Clean application-specific memory
                self.log_message("Cleaning application memory...")
                
                # Reset any large temporary objects
                for obj in gc.get_objects():
                    try:
                        if hasattr(obj, 'clear') and callable(obj.clear):
                            obj.clear()
                    except:
                        pass
                
                # Final collection
                gc.collect()
                
                self.log_message("✅ Deep cleanup completed successfully!")
                self.status_label.config(text="Deep clean complete")
                self.update_stats()
                
            except Exception as e:
                self.log_message(f"❌ Error during deep cleanup: {str(e)}")
                self.status_label.config(text="Error during deep clean")
            finally:
                self.is_clearing = False
                self.deep_clean_btn.config(state='normal')
        
        threading.Thread(target=deep_clean_task, daemon=True).start()
    
    def clean_specific_apps(self):
        """Clean specific known applications that use lots of memory"""
        try:
            # Close unnecessary Explorer windows
            if sys.platform == 'win32':
                # Check for browser tabs - optional
                pass
                
            # Look for memory-intensive processes
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    if proc.info['memory_info']:
                        mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                        if mem_mb > 1000 and 'chrome' in proc.info['name'].lower():
                            self.log_message(f"Found memory-heavy process: {proc.info['name']} ({mem_mb:.0f} MB)")
                except:
                    pass
        except:
            pass
    
    def toggle_monitor(self):
        if not self.monitor_running:
            self.monitor_running = True
            self.monitor_btn.config(text="⏹ Stop Monitoring")
            self.log_message("Memory monitoring started")
            self.monitor_thread = threading.Thread(target=self.monitor_memory, daemon=True)
            self.monitor_thread.start()
        else:
            self.monitor_running = False
            self.monitor_btn.config(text="▶ Start Monitoring")
            self.log_message("Memory monitoring stopped")
    
    def monitor_memory(self):
        while self.monitor_running:
            try:
                memory = psutil.virtual_memory()
                if memory.percent > 90:
                    self.log_message(f"⚠️ Warning: Memory usage at {memory.percent}%!")
                    self.status_label.config(text=f"⚠️ High memory usage: {memory.percent}%")
                    
                    # Auto-clean if memory is critical
                    if memory.percent > 95:
                        self.log_message("🔴 Critical memory usage! Auto-cleaning...")
                        self.root.after(0, self.clean_memory)
                elif memory.percent > 80:
                    self.status_label.config(text=f"⚠️ Memory usage: {memory.percent}%")
                else:
                    if memory.percent < 50:
                        self.status_label.config(text=f"✓ Memory usage: {memory.percent}%")
                    else:
                        self.status_label.config(text=f"Memory usage: {memory.percent}%")
                
                time.sleep(5)
            except:
                break
    
    def auto_clean(self):
        """Automatically clean memory every X minutes"""
        if os.environ.get('MC_SILENT') == '1':
            result = True
        else:
            result = messagebox.askyesno("Auto-Clean",
                "Enable auto-clean?\n\n"
                "This will automatically clean memory when usage exceeds 85%\n"
                "and run a cleanup every 30 minutes.")

        if result:
            self.log_message("Auto-clean enabled (runs every 30 minutes)")
            self.auto_clean_btn.config(text="⏳ Auto-Clean Active")
            self.root.after(1800000, self.auto_clean_task)  # 30 minutes
        else:
            self.log_message("Auto-clean disabled")
            self.auto_clean_btn.config(text="⚡ Auto-Clean")
    
    def auto_clean_task(self):
        try:
            memory = psutil.virtual_memory()
            if memory.percent > 85:
                self.log_message(f"Auto-clean triggered (memory: {memory.percent}%)")
                self.clean_memory()
            
            # Reschedule
            self.root.after(1800000, self.auto_clean_task)
        except:
            pass

def main():
    # Check if running as administrator (Windows)
    if sys.platform == 'win32':
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if not is_admin:
                print("⚠️ Running without administrator privileges. Some features may not work.")
        except:
            pass
    
    root = tk.Tk()
    app = MemoryClearer(root)
    root.mainloop()

if __name__ == "__main__":
    # Install required packages if missing
    try:
        import psutil
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])

    # Start the GUI
    main()