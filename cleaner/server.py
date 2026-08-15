# server.py - Lightweight local web server for the Memory Clearer web GUI.
# Hosts index.html on http://127.0.0.1:8765 and exposes a small JSON API
# the front-end uses for stats, actions, and process listings.

import os
import sys
import gc
import json
import time
import ctypes
import threading
import webbrowser
import subprocess
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socketserver import ThreadingMixIn

import psutil

# Recent events posted by the toolbar (theme toggle, section toggle, ...).
# The browser subscribes to /api/events (SSE) and consumes them in order.
recent_events = deque(maxlen=64)
events_lock = threading.Lock()

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

# ---- Shared state -----------------------------------------------------
state = {
    "monitoring": False,
    "auto_clean": False,
    "_monitor_thread": None,
    "_auto_thread": None,
}
state_lock = threading.Lock()

# ---- Helpers ----------------------------------------------------------
def _log_path():
    log_dir = os.path.join(ROOT, "clear", "logs")
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, "memory_clearer.log")

def write_log(message, level="info"):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{level.upper()}] {message}\n"
    try:
        with open(_log_path(), "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

def get_stats():
    vm = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=0.3)
    cpu_cores = psutil.cpu_count(logical=True) or 1
    top = []
    for p in psutil.process_iter(["name", "memory_info", "pid"]):
        try:
            mi = p.info.get("memory_info")
            if not mi: continue
            top.append({
                "pid":  p.info["pid"],
                "name": p.info["name"] or "?",
                "mem_mb": mi.rss / (1024 * 1024),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    top.sort(key=lambda x: x["mem_mb"], reverse=True)
    return {
        "ok": True,
        "total_ram_gb":  vm.total     / (1024**3),
        "used_ram_gb":   vm.used      / (1024**3),
        "avail_ram_gb":  vm.available / (1024**3),
        "mem_percent":   vm.percent,
        "cpu_percent":   cpu_percent,
        "cpu_cores":     cpu_cores,
        "top_procs":     top[:8],
    }

def do_clean(deep=False):
    msgs = []
    msgs.append(("Running garbage collection...", "info"))
    gc.collect()
    if sys.platform == "win32":
        try:
            msgs.append(("Trimming process working set...", "info"))
            ctypes.windll.kernel32.SetProcessWorkingSetSize(
                ctypes.windll.kernel32.GetCurrentProcess(), -1, -1
            )
        except Exception:
            pass
    if deep:
        for i in range(5):
            gc.collect()
            msgs.append((f"Deep GC cycle {i+1}/5 complete", "info"))
            time.sleep(0.05)
        try:
            ctypes.windll.kernel32.EmptyWorkingSet(
                ctypes.windll.kernel32.GetCurrentProcess()
            )
            msgs.append(("Working set emptied (deep)", "info"))
        except Exception:
            pass
    gc.collect()
    msgs.append(("Memory cleanup completed successfully!", "good"))
    return msgs

def clean_temp():
    msgs = []
    if sys.platform != "win32":
        msgs.append(("Temp cleanup is Windows-only", "warn"))
        return msgs
    temp = os.environ.get("TEMP", os.environ.get("TMP", r"C:\Windows\Temp"))
    removed = 0
    freed = 0
    for name in os.listdir(temp):
        path = os.path.join(temp, name)
        try:
            if os.path.isfile(path):
                size = os.path.getsize(path)
                os.remove(path)
                removed += 1
                freed += size
            elif os.path.isdir(path):
                # Only remove empty directories for safety.
                if not os.listdir(path):
                    os.rmdir(path)
        except (PermissionError, OSError):
            pass
    msgs.append((f"Cleared {removed} temp files ({freed/1024/1024:.1f} MB)", "good"))
    return msgs

def trim_working_set():
    if sys.platform != "win32":
        return [("Working set trim is Windows-only", "warn")]
    try:
        ctypes.windll.kernel32.SetProcessWorkingSetSize(
            ctypes.windll.kernel32.GetCurrentProcess(), -1, -1
        )
        return [("Working set trimmed for current process", "good")]
    except Exception as e:
        return [(f"Failed: {e}", "bad")]

def empty_standby():
    if sys.platform != "win32":
        return [("Standby list empty is Windows-only", "warn")]
    try:
        # Prefer psutil's helper, fall back to no-op.
        if hasattr(psutil, "windows"):
            psutil.windows.EmptyStandbyList()  # may not exist on all versions
        return [("Standby list empty requested", "good")]
    except AttributeError:
        # No direct binding available; suggest the system command.
        return [(
            "Standby list empty requires elevated privileges; "
            "use 'RAMMap' or 'EmptyStandbyList.exe' as admin.", "warn"
        )]
    except Exception as e:
        return [(f"Failed: {e}", "bad")]

def force_gc():
    before = psutil.Process().memory_info().rss
    gc.collect()
    after = psutil.Process().memory_info().rss
    diff = (before - after) / 1024 / 1024
    return [(f"Forced GC complete ({diff:+.1f} MB this process)", "good")]

# ---- Background workers ----------------------------------------------
def monitor_loop():
    while True:
        with state_lock:
            if not state["monitoring"]:
                break
        try:
            vm = psutil.virtual_memory()
            if vm.percent > 90:
                write_log(f"Warning: memory at {vm.percent}%", "warn")
                if vm.percent > 95:
                    for m in do_clean():
                        write_log(m[0], m[1])
        except Exception as e:
            write_log(f"monitor error: {e}", "error")
        time.sleep(5)

def auto_clean_loop():
    while True:
        with state_lock:
            if not state["auto_clean"]:
                break
        try:
            vm = psutil.virtual_memory()
            if vm.percent > 85:
                write_log(f"Auto-clean at {vm.percent}%", "info")
                for m in do_clean():
                    write_log(m[0], m[1])
        except Exception as e:
            write_log(f"auto-clean error: {e}", "error")
        time.sleep(1800)  # 30 minutes

def start_monitor():
    with state_lock:
        if state["monitoring"]:
            return [("Monitoring already running", "warn")]
        state["monitoring"] = True
        state["_monitor_thread"] = threading.Thread(target=monitor_loop, daemon=True)
        state["_monitor_thread"].start()
    return [("Memory monitoring started", "good")]

def stop_monitor():
    with state_lock:
        if not state["monitoring"]:
            return [("Monitoring was not running", "warn")]
        state["monitoring"] = False
    return [("Memory monitoring stopped", "good")]

def start_auto_clean():
    with state_lock:
        if state["auto_clean"]:
            return [("Auto-clean already enabled", "warn")]
        state["auto_clean"] = True
        state["_auto_thread"] = threading.Thread(target=auto_clean_loop, daemon=True)
        state["_auto_thread"].start()
    return [("Auto-clean enabled (every 30 minutes)", "good")]

def stop_auto_clean():
    with state_lock:
        if not state["auto_clean"]:
            return [("Auto-clean was not enabled", "warn")]
        state["auto_clean"] = False
    return [("Auto-clean disabled", "good")]

def list_procs():
    vm = psutil.virtual_memory()
    out = []
    for p in psutil.process_iter(["name", "memory_info", "pid"]):
        try:
            mi = p.info.get("memory_info")
            if not mi: continue
            out.append((f"{p.info['name']}: {mi.rss/1024/1024:.0f} MB", "info"))
        except Exception:
            pass
    out.sort(key=lambda x: float(x[0].split(": ")[1].split(" MB")[0]), reverse=True)
    return out[:8]

def disk_usage():
    msgs = []
    for part in psutil.disk_partitions(all=False):
        try:
            u = psutil.disk_usage(part.mountpoint)
            msgs.append((
                f"{part.mountpoint} – {u.percent}% used "
                f"({u.used/1024**3:.1f}/{u.total/1024**3:.1f} GB)",
                "info"
            ))
        except (PermissionError, OSError):
            pass
    return msgs or [("No disks accessible", "warn")]

# ---- HTTP server ------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Quiet the default access log; we already write our own.
        pass

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, ctype):
        try:
            with open(path, "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send_file(os.path.join(ROOT, "index.html"), "text/html; charset=utf-8")
        if self.path == "/api/stats":
            return self._send_json(get_stats())
        if self.path == "/api/state":
            with state_lock:
                s = {"monitoring": state["monitoring"], "auto_clean": state["auto_clean"]}
            return self._send_json({"ok": True, "state": s})
        if self.path == "/api/ping":
            return self._send_json({"ok": True})
        if self.path == "/api/events":
            # Server-Sent Events stream for the toolbar's view/more actions.
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            sent_index = len(recent_events)
            try:
                # Send a hello so the browser EventSource knows we're live.
                self.wfile.write(b": connected\n\n")
                self.wfile.flush()
                while True:
                    time.sleep(0.5)
                    with events_lock:
                        while sent_index < len(recent_events):
                            ev = recent_events[sent_index]
                            sent_index += 1
                            payload = json.dumps(ev).encode()
                            self.wfile.write(b"data: " + payload + b"\n\n")
                            self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                return
        self.send_response(404); self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return self._send_json({"ok": False, "error": "invalid json"}, 400)

        if self.path == "/api/action":
            action = data.get("action", "")
            handler = ACTIONS.get(action)
            if not handler:
                return self._send_json({"ok": False, "error": f"unknown action '{action}'"}, 400)
            try:
                msgs = handler()
            except Exception as e:
                return self._send_json({"ok": False, "error": str(e)}, 500)
            with state_lock:
                snap = {"monitoring": state["monitoring"], "auto_clean": state["auto_clean"]}
            for m in msgs:
                write_log(m[0], m[1])
            return self._send_json({"ok": True, "messages": msgs, "state": snap})

        if self.path == "/api/event":
            # Toolbar -> page: forward a UI event the page can react to.
            event = data.get("event", "")
            if not event:
                return self._send_json({"ok": False, "error": "missing event"}, 400)
            with events_lock:
                recent_events.append({"event": event, "ts": time.time()})
            write_log(f"event: {event}", "info")
            return self._send_json({"ok": True})

        return self._send_json({"ok": False, "error": "not found"}, 404)

ACTIONS = {
    "clean":              lambda: do_clean(deep=False),
    "deep":               lambda: do_clean(deep=True),
    "gc":                 force_gc,
    "cleantemp":          clean_temp,
    "winsetsize":         trim_working_set,
    "emptystandby":       empty_standby,
    "monitor-start":      start_monitor,
    "monitor-stop":       stop_monitor,
    "monitor-toggle":     lambda: stop_monitor() if state["monitoring"] else start_monitor(),
    "auto-clean":         start_auto_clean,
    "auto-clean-off":     stop_auto_clean,
    "auto-clean-toggle":  lambda: stop_auto_clean() if state["auto_clean"] else start_auto_clean(),
    "list-procs":         list_procs,
    "disk-usage":         disk_usage,
}

# ---- Entrypoint -------------------------------------------------------
def main():
    port = 8765
    host = "127.0.0.1"
    httpd = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}/"
    print(f"Memory Clearer web GUI ready at {url}")
    write_log(f"Server started on {url}", "info")
    # Open the browser unless we're in silent/headless mode.
    if os.environ.get("MC_SILENT") != "1":
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

if __name__ == "__main__":
    main()
