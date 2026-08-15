# toolbar.py - Native always-on-top toolbar window with the six dropdowns.
# Renders as a small borderless Tk window that lives "outside" the browser
# (the web GUI itself opens in the user's default browser via server.py).
#
# Communication with the running web GUI is done via a tiny local HTTP
# control endpoint (http://127.0.0.1:8766) that proxies actions to the
# main server. The toolbar owns no state of its own.

import os
import sys
import json
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk, font
from urllib import request as urlrequest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MAIN_URL    = os.environ.get("MC_MAIN_URL",    "http://127.0.0.1:8765")
TOOLBAR_URL = os.environ.get("MC_TOOLBAR_URL", "http://127.0.0.1:8766")

# ----- Menu structure (mirrors index.html) -----------------------------
MENUS = [
    ("Help", [
        ("📖 Documentation",        "help-docs"),
        ("⌨️  Keyboard Shortcuts",  "help-shortcuts"),
        ("❓ FAQ",                  "help-faq"),
        ("�️  Troubleshooting",    "help-troubleshoot"),
    ]),
    ("About", [
        ("�️  About App",           "about-app"),
        ("🏷️  Version Info",        "about-version"),
        ("©️  License & Copyright", "about-copyright"),
        ("🙏 Credits",             "about-credits"),
    ]),
    ("View", [
        ("🌙 Dark Theme",           "view-dark"),
        ("☀️  Light Theme",         "view-light"),
        ("� Toggle Stats",         "view-toggle-stats"),
        ("📝 Toggle Logs",          "view-toggle-logs"),
        ("🧽 Clear Log View",       "view-clear-log"),
    ]),
    ("Run", [
        ("🧹 Clean Memory Now",     "clean"),
        ("🔧 Deep Clean",           "deep"),
        ("♻️  Force GC",             "gc"),
        ("🗑️  Clear Temp Files",    "cleantemp"),
        ("🪟 Trim Working Set",     "winsetsize"),
        ("💤 Empty Standby List",   "emptystandby"),
    ]),
    ("Task", [
        ("▶️  Start Monitoring",    "monitor-start"),
        ("⏹️  Stop Monitoring",     "monitor-stop"),
        ("⚡ Enable Auto-Clean",    "auto-clean"),
        ("🚫 Disable Auto-Clean",   "auto-clean-off"),
    ]),
    ("More", [
        ("🧬 Top Processes",        "list-procs"),
        ("💽 Disk Usage",           "disk-usage"),
        ("⚙️  Settings",            "more-settings"),
        ("📤 Export Logs",          "more-export"),
        ("♻️  Reset App",           "more-reset"),
    ]),
]

# ----- Bridge HTTP server: turns menu clicks into actions --------------
class BridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, *a, **kw): pass

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/ping":
            return self._send_json({"ok": True})
        self.send_response(404); self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length).decode() if length else "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return self._send_json({"ok": False, "error": "invalid json"}, 400)

        action = data.get("action", "")

        # "view-*" actions are local UI toggles inside the web page. We
        # forward them via a custom event the page listens for.
        if action.startswith("view-") or (action.startswith("more-") and action != "more-reset"):
            # Send a message via the main server's /api/event endpoint
            # (added below) so the page can react instantly.
            try:
                urlrequest.urlopen(urlrequest.Request(
                    MAIN_URL + "/api/event",
                    data=json.dumps({"event": action}).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                ), timeout=2)
                return self._send_json({"ok": True, "forwarded": True})
            except Exception as e:
                return self._send_json({"ok": False, "error": str(e)}, 502)

        # Everything else is a real backend action.
        try:
            resp = urlrequest.urlopen(urlrequest.Request(
                MAIN_URL + "/api/action",
                data=json.dumps({"action": action}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            ), timeout=10)
            payload = json.loads(resp.read().decode())
            return self._send_json(payload)
        except Exception as e:
            return self._send_json({"ok": False, "error": str(e)}, 502)

def start_bridge():
    """Run the toolbar's bridge server in a background thread."""
    port = int(TOOLBAR_URL.rsplit(":", 1)[1].rsplit("/", 1)[0])
    httpd = ThreadingHTTPServer(("127.0.0.1", port), BridgeHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

# ----- Toolbar UI ------------------------------------------------------
class Toolbar:
    BG       = "#0f172a"
    BG_HOVER = "#334155"
    FG       = "#e2e8f0"
    ACCENT   = "#22d3ee"
    BORDER   = "#475569"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Memory Clearer")
        self.root.configure(bg=self.BG)
        self.root.overrideredirect(True)            # borderless
        self.root.attributes("-topmost", True)      # always on top
        try:
            self.root.attributes("-alpha", 0.96)
        except tk.TclError:
            pass

        # Position at top-center of primary screen.
        sw = self.root.winfo_screenwidth()
        self.W = max(720, int(sw * 0.55))
        self.H = 40
        x = (sw - self.W) // 2
        self.root.geometry(f"{self.W}x{self.H}+{x}+6")

        bar = tk.Frame(self.root, bg=self.BG, height=self.H)
        bar.pack(fill="x")
        # Border line at the bottom for definition.
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill="x")

        # Drag handle / brand on the left.
        self._drag = {"x": 0, "y": 0}
        brand = tk.Label(
            bar, text="🧹 Memory Clearer", fg=self.ACCENT, bg=self.BG,
            font=("Segoe UI", 10, "bold"), padx=12, pady=8
        )
        brand.pack(side="left")
        brand.bind("<Button-1>", self._drag_start)
        brand.bind("<B1-Motion>", self._drag_move)

        # Right-side controls.
        right = tk.Frame(bar, bg=self.BG)
        right.pack(side="right", padx=8)
        tk.Button(
            right, text="Open GUI", command=self.open_gui,
            bg=self.ACCENT, fg="#052e16", activebackground="#67e8f9",
            relief="flat", font=("Segoe UI", 9, "bold"), padx=10, pady=3,
            bd=0, cursor="hand2"
        ).pack(side="right", padx=4)

        self.live_lbl = tk.Label(
            right, text="● Live", fg="#052e16", bg="#22c55e",
            font=("Segoe UI", 8, "bold"), padx=8, pady=3
        )
        self.live_lbl.pack(side="right", padx=4)

        # Menu buttons in the middle.
        menus = tk.Frame(bar, bg=self.BG)
        menus.pack(side="left", padx=8)
        self.menus = {}
        for name, items in MENUS:
            b = tk.Label(
                menus, text=f"{name}  ▾", fg=self.FG, bg=self.BG,
                font=("Segoe UI", 10), padx=12, pady=8, cursor="hand2"
            )
            b.pack(side="left")
            b.bind("<Enter>", lambda e, n=name: self._hover(n, True))
            b.bind("<Leave>", lambda e, n=name: self._hover(n, False))
            b.bind("<Button-1>", lambda e, n=name: self._toggle(n))
            self.menus[name] = {"btn": b, "items": items, "open": False, "popup": None}

        # Close on Escape / right-click anywhere on the title bar.
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Heartbeat that pings the bridge to keep the live pill honest.
        self.root.after(2000, self._heartbeat)
        self.root.after(100, self._post_init)

    # ---- window dragging ----
    def _drag_start(self, e):
        self._drag["x"] = e.x_root
        self._drag["y"] = e.y_root
    def _drag_move(self, e):
        dx = e.x_root - self._drag["x"]
        dy = e.y_root - self._drag["y"]
        x = self.root.winfo_x() + dx
        y = self.root.winfo_y() + dy
        self.root.geometry(f"+{x}+{y}")
        self._drag["x"] = e.x_root
        self._drag["y"] = e.y_root

    # ---- menu hover + dropdowns ----
    def _hover(self, name, on):
        m = self.menus[name]
        m["btn"].configure(bg=self.BG_HOVER if on else self.BG)

    def _toggle(self, name):
        m = self.menus[name]
        if m["open"]:
            self._close(name)
        else:
            # close any other open menu
            for n, other in self.menus.items():
                if other["open"]:
                    self._close(n)
            self._open(name)

    def _open(self, name):
        m = self.menus[name]
        m["open"] = True
        m["btn"].configure(bg=self.BG_HOVER)

        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.configure(bg=self.BG)

        # Position under the button.
        bx = m["btn"].winfo_rootx()
        by = m["btn"].winfo_rooty() + m["btn"].winfo_height() + 2
        popup.geometry(f"+{bx}+{by}")

        for label, action in m["items"]:
            row = tk.Label(
                popup, text="  " + label + "  ", fg=self.FG, bg=self.BG,
                font=("Segoe UI", 10), anchor="w", padx=14, pady=6,
                cursor="hand2", width=24
            )
            row.pack(fill="x")
            row.bind("<Enter>", lambda e, r=row: r.configure(bg=self.BG_HOVER))
            row.bind("<Leave>", lambda e, r=row: r.configure(bg=self.BG))
            row.bind("<Button-1>", lambda e, a=action, n=name: self._click(n, a))

        # Auto-close when the mouse leaves the popup.
        popup.bind("<Leave>", lambda e, n=name: self.root.after(180, lambda: self._maybe_close(n)))
        m["popup"] = popup

    def _maybe_close(self, name):
        m = self.menus[name]
        if not m["popup"]: return
        # If pointer is outside both the popup and the trigger button, close.
        try:
            x, y = self.root.winfo_pointerxy()
            px = m["popup"].winfo_rootx()
            py = m["popup"].winfo_rooty()
            pw = m["popup"].winfo_width()
            ph = m["popup"].winfo_height()
            bx = m["btn"].winfo_rootx()
            bh = m["btn"].winfo_height()
            inside_popup = (px <= x <= px+pw and py <= y <= py+ph)
            inside_btn    = (bx <= x <= bx+m["btn"].winfo_width() and
                             m["btn"].winfo_rooty() <= y <= m["btn"].winfo_rooty()+bh)
            if not (inside_popup or inside_btn):
                self._close(name)
        except tk.TclError:
            pass

    def _close(self, name):
        m = self.menus[name]
        m["open"] = False
        m["btn"].configure(bg=self.BG)
        if m["popup"]:
            try: m["popup"].destroy()
            except tk.TclError: pass
            m["popup"] = None

    def _click(self, name, action):
        self._close(name)
        self._dispatch(action)

    # ---- action dispatch ----
    def _dispatch(self, action):
        # View/more items are page-local UI events.
        if action.startswith("view-") or action.startswith("more-"):
            self._post_event(action)
            return
        try:
            port = TOOLBAR_URL.rsplit(":", 1)[1].rsplit("/", 1)[0]
            req = urlrequest.Request(
                f"http://127.0.0.1:{port}/api/action",
                data=json.dumps({"action": action}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlrequest.urlopen(req, timeout=10) as r:
                payload = json.loads(r.read().decode())
            if payload.get("ok"):
                # If the main window isn't open yet, open it.
                if action in {"clean","deep","gc","cleantemp","winsetsize",
                              "emptystandby","monitor-start","monitor-stop",
                              "auto-clean","auto-clean-off","list-procs",
                              "disk-usage","more-reset"}:
                    webbrowser.open(MAIN_URL)
        except Exception as e:
            print(f"[toolbar] action '{action}' failed: {e}")

    def _post_event(self, event_name):
        try:
            urlrequest.urlopen(urlrequest.Request(
                MAIN_URL + "/api/event",
                data=json.dumps({"event": event_name}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            ), timeout=2)
        except Exception:
            pass
        webbrowser.open(MAIN_URL)

    def open_gui(self):
        webbrowser.open(MAIN_URL)

    def _heartbeat(self):
        try:
            with urlrequest.urlopen(TOOLBAR_URL + "/api/ping", timeout=2) as r:
                ok = json.loads(r.read().decode()).get("ok", False)
        except Exception:
            ok = False
        if ok:
            self.live_lbl.configure(text="● Live",  bg="#22c55e", fg="#052e16")
        else:
            self.live_lbl.configure(text="● Offline", bg="#ef4444", fg="#ffffff")
        self.root.after(4000, self._heartbeat)

    def _post_init(self):
        # Auto-open the GUI the first time so the user sees results.
        if os.environ.get("MC_SILENT") != "1":
            webbrowser.open(MAIN_URL)

    def run(self):
        self.root.mainloop()


def main():
    start_bridge()
    Toolbar().run()

if __name__ == "__main__":
    main()
