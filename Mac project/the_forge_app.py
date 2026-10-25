#!/usr/bin/env python3
# THE FORGE  |  Copyright (c) 2026 Yannie D. Forest. All rights reserved.
# NO LICENCE IS GRANTED. No copying, adaptation, redistribution, reverse
# engineering or commercial use without the author's written permission.
# See LICENCE.txt. Every distributed copy carries a build marker.
"""
The Forge — desktop launcher.

This is a thin native-window shell around the app. All of the
app's behaviour lives in the bundled HTML/JavaScript file (the_forge.html);
this script only opens it in a proper desktop window using the system's native
web view. The app still runs entirely offline: nothing is sent anywhere.

Run it with:   python the_forge_app.py
"""

import os
import sys

# The window title and starting size. The app itself is responsive, so these are
# just sensible defaults; the window can be resized and maximised freely.
WINDOW_TITLE = "The Forge"
DEFAULT_WIDTH = 1180
DEFAULT_HEIGHT = 820
MIN_WIDTH = 380      # the app works down to a narrow width
MIN_HEIGHT = 560
ACCENT_BLUE = "#1B6B93"   # the seal blue


def tell_user(text, title="The Forge"):
    """Say something the person will actually see.

    The packaged exe is built windowed, with no console attached, so anything
    written to stderr disappears. Every message below therefore goes to a native
    dialog on Windows, and to the terminal when one exists (running the script
    directly, or on macOS and Linux).
    """
    try:
        sys.stderr.write(text if text.endswith("\n") else text + "\n")
    except Exception:
        pass
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0x40)
            return
        except Exception:
            pass
    if sys.platform == "darwin":
        # An app opened from the Dock or Finder has no terminal either, so the
        # message goes to a real dialog. osascript is present on every Mac.
        try:
            import subprocess
            body = str(text).replace("\\", "\\\\").replace('"', '\\"')
            head = str(title).replace('"', '\\"')
            subprocess.run(
                ["osascript", "-e",
                 'display dialog "%s" with title "%s" buttons {"OK"} default button "OK"'
                 % (body, head)],
                check=False, timeout=120)
            return
        except Exception:
            pass


def open_in_browser(app_html):
    """Last resort: the page itself is the whole application.

    If a native window cannot be created, opening the same file in the default
    browser still gives the entire app, offline. It is better than an exe that
    appears to do nothing.
    """
    try:
        import webbrowser
        from pathlib import Path
        webbrowser.open(Path(app_html).as_uri())
        return True
    except Exception:
        return False


def resource_path(filename):
    """Return an absolute path to a file that sits next to this script.

    This also works when the app has been frozen into a single executable with
    PyInstaller, where bundled files live in a temporary folder exposed as
    sys._MEIPASS.
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


def find_app_html():
    """Locate the bundled app HTML, with several sensible fallbacks.

    A frozen single-file build carries the page inside itself and finds it
    through resource_path first, so it needs no folder at all. The extra
    candidates cover running from source, and a build started from a different
    working folder.
    """
    here_script = os.path.dirname(os.path.abspath(__file__))
    try:
        here_exe = os.path.dirname(os.path.abspath(sys.executable))
    except Exception:
        here_exe = here_script
    candidates = [
        resource_path("the_forge.html"),
        resource_path("the_forge_offline.html"),
        # PyInstaller 6 places bundled data files in Contents/Resources on macOS,
        # while sys._MEIPASS points at Contents/Frameworks and the executable sits
        # in Contents/MacOS. Check every home the file could plausibly have.
        os.path.normpath(resource_path(os.path.join("..", "Resources", "the_forge.html"))),
        os.path.join(here_exe, "the_forge.html"),
        os.path.normpath(os.path.join(here_exe, "..", "Resources", "the_forge.html")),
        os.path.join(here_script, "the_forge.html"),
        os.path.normpath(os.path.join(here_script, "..", "Resources", "the_forge.html")),
        os.path.join(os.getcwd(), "the_forge.html"),
    ]
    seen = set()
    for path in candidates:
        if path and path not in seen:
            seen.add(path)
            if os.path.isfile(path):
                return path
    return None


def friendly_missing_dependency_message():
    """A clear, non-technical message shown if pywebview is not installed."""
    return (
        "\n"
        "The Forge needs one small free component to open its window.\n"
        "\n"
        "Please install it once by running this in a terminal or command prompt:\n"
        "\n"
        "    pip install pywebview\n"
        "\n"
        "On Windows you may instead need:   py -m pip install pywebview\n"
        "On some Linux systems you may also need a web view backend, e.g.:\n"
        "    sudo apt install python3-webview   (or)   pip install pywebview[qt]\n"
        "\n"
        "Then run this program again.\n"
    )


def storage_dir():
    """A persistent place for the web view's own storage.

    pywebview runs in PRIVATE MODE by default, which discards localStorage when
    the window closes. Everything written in the desktop app was therefore lost
    on exit, not only a sticky note: curriculum progress, documents, reminders,
    all of it. A onefile build also unpacks into a temporary directory that is
    deleted afterwards, so the storage must live in the user's own profile and
    not beside the executable.
    """
    import os
    home = os.path.expanduser("~")
    if sys.platform.startswith("win"):
        base = os.environ.get("LOCALAPPDATA") or os.path.join(home, "AppData", "Local")
    elif sys.platform == "darwin":
        base = os.path.join(home, "Library", "Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")
    path = os.path.join(base, "TheForge", "storage")
    try:
        os.makedirs(path, exist_ok=True)
        return path
    except Exception:
        log_problem("storage_dir: could not create %r" % path)
        return None


def crash_log_path():
    """Beside the program if that is writable, otherwise the home folder."""
    import os
    try:
        base = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
        probe = os.path.join(base, ".the_forge_write_test")
        with open(probe, "w") as fh:
            fh.write("")
        os.remove(probe)
        return os.path.join(base, "the_forge_crash.log")
    except Exception:
        return os.path.join(os.path.expanduser("~"), "the_forge_crash.log")


def log_problem(tag, exc_info=None):
    """Record a fault so a crash leaves evidence instead of vanishing."""
    import datetime, traceback
    try:
        with open(crash_log_path(), "a", encoding="utf-8") as fh:
            fh.write("\n=== %s  %s ===\n" % (datetime.datetime.now().isoformat(timespec="seconds"), tag))
            if exc_info:
                traceback.print_exception(exc_info[0], exc_info[1], exc_info[2], file=fh)
            else:
                traceback.print_exc(file=fh)
    except Exception:
        pass


def print_document(win, name, mime, data_b64):
    """Hand a document to the operating system so it can be printed.

    WKWebView, which is what this wrapper draws through on macOS, does not implement
    window.print(). A print request made inside the web view therefore reaches nothing,
    which is the fault this answers. Rather than write a Cocoa print path, the bytes are
    written to a temporary file and opened with the system's own application: a PDF opens
    in Preview and an HTML page in the default browser, and in both the print dialog is
    the machine's own.

    Returns the path opened, or False so the page can fall back to saving the file.
    """
    import base64, os, subprocess, sys, tempfile
    try:
        raw = base64.b64decode(data_b64 or "")
    except Exception:
        log_problem("print_document: undecodable payload")
        return False
    if not raw:
        return False
    # 647 (forge_shell_647.py): opened only as what it says it is, with the Forge's own extension
    kind = {"application/pdf": ".pdf", "text/html": ".html", "text/plain": ".txt", "image/png": ".png", "image/jpeg": ".jpg",
            "image/gif": ".gif", "image/webp": ".webp"}.get(str(mime or "").split(";")[0].strip().lower())
    if not kind:
        log_note("print_document: a document of type %r was not opened (a PDF, a web page, plain text or a picture is)" % str(mime)[:60])
        return False
    base = os.path.splitext(os.path.basename(str(name or "document").replace("\\", "/")))[0]
    safe = "".join(c for c in base if c.isalnum() or c in " _-").strip()[:80] or "document"
    try:
        folder = os.path.join(tempfile.gettempdir(), "TheForgePrint")
        os.makedirs(folder, exist_ok=True)
        fd, path = tempfile.mkstemp(prefix=safe + "-", suffix=kind, dir=folder)
        with os.fdopen(fd, "wb") as fh:
            fh.write(raw)
    except Exception as exc:
        log_problem("print_document: could not write %s (%s)" % (safe, exc))
        return False
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["/usr/bin/open", path])
        elif sys.platform.startswith("win"):
            os.startfile(path)          # noqa: S606
        else:
            subprocess.Popen(["xdg-open", path])
        log_problem("print_document: opened %s for printing" % safe)
        return path
    except Exception as exc:
        log_problem("print_document: could not open %s (%s)" % (safe, exc))
        return False

def save_bytes(win, name, mime, data_b64):
    """Write an exported file from Python.

    A synthetic <a download> click inside a native web view is handed to the
    platform's download machinery. That is the path the Windows crash was
    reported on, and writing the bytes here avoids it entirely. Returns the path
    written, or False so the page can fall back to the anchor.
    """
    import base64, os
    try:
        raw = base64.b64decode(data_b64 or "")
    except Exception:
        log_problem("save_bytes: undecodable payload")
        return False
    keep = " ._-()[]"
    safe = "".join(c for c in str(name or "download") if c.isalnum() or c in keep).strip() or "download"
    target = None
    shown = False
    try:
        import webview
        # THE EXPORT CRASH (mac/windows): "Export to file" hands the webview a blob
        # download; without download support pywebview can bring the window down.
        # Recent pywebview honours this switch; older ones ignore the unknown key.
        try:
            webview.settings['ALLOW_DOWNLOADS'] = True
        except Exception:
            pass
        w = win
        if w is None:
            ws = [x for x in (getattr(webview, "windows", None) or []) if x is not None]
            w = ws[0] if ws else None
        if w is not None:
            shown = True
            res = w.create_file_dialog(webview.SAVE_DIALOG, save_filename=safe)
            if res:
                target = res if isinstance(res, str) else res[0]
    except Exception:
        # a missing dialog is not a cancellation: fall through to the folder
        log_problem("save_bytes: file dialog unavailable")
        shown = False
        target = None
    if shown and not target:
        # the person chose Cancel, so nothing is written and nothing falls back
        return "cancelled"
    if not target:
        try:
            d = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.isdir(d):
                d = os.path.expanduser("~")
            target = os.path.join(d, safe.lstrip(".") or "download")
            # 647 (forge_shell_647.py): never over a file already there
            stem, ext = os.path.splitext(target)
            n = 2
            while os.path.exists(target) and n < 1000:
                target = "%s (%d)%s" % (stem, n, ext)
                n += 1
        except Exception:
            log_problem("save_bytes: no writable folder")
            return False
    try:
        with open(target, "wb") as fh:
            fh.write(raw)
        return target
    except Exception:
        log_problem("save_bytes: write failed")
        return False


def log_note(tag):
    """One line in the same record, with nothing under it.

    log_problem() writes the exception being handled beneath its line (or
    "NoneType: None" when there is none), and a traceback in the record
    stops the GitHub build's open test. A plain note needs neither.
    """
    import datetime
    try:
        with open(crash_log_path(), "a", encoding="utf-8") as fh:
            fh.write("\n=== %s  %s ===\n" % (datetime.datetime.now().isoformat(timespec="seconds"), tag))
    except Exception:
        pass


# ---------------------------------------------------------------- clipboard
# 9s58: THE CLIPBOARD, for the page's own right-click menu. Its Paste, Paste
# as plain text, Copy and Cut reach the Mac's clipboard through
#   window.pywebview.api.read_clipboard()        -> {"text": ..., "html": ...}
#   window.pywebview.api.write_clipboard(text, html)  -> true or false
# so a link copied in any other app pastes from the menu, and nothing asks
# for keys to be pressed. (A page inside a web view may read the clipboard
# by itself only while a person presses the keys; a Mac app may read it,
# so the page asks this one.)
#
# The Mac's clipboard is NSPasteboard, reached through AppKit, the part of
# pyobjc that pywebview draws its Mac window with: pywebview's
# webview.platforms.cocoa imports it, and the_forge.spec names 'AppKit'
# in its hiddenimports, so it is inside the app already. Nothing new.
#
# ON THE MAIN THREAD. pywebview runs every js_api call on a new thread of
# its own (webview.util.js_bridge_call). Apple does not list NSPasteboard
# among AppKit's thread-safe classes, so the pasteboard is used on the
# app's main thread, the one AppKit runs on, the way pywebview does its own
# window work (PyObjCTools.AppHelper.callAfter), and the calling thread
# waits for the answer. The wait has a limit (CLIPBOARD_WAIT_S), so a main
# thread that is busy can never hold the page's Promise for ever: the page
# then tries its next way. The limit is generous because macOS may first ask
# whether this app may paste from another, and a person needs time to answer.

CLIPBOARD_WAIT_S = 30
PB_TEXT = "public.utf8-plain-text"   # NSPasteboardTypeString
PB_HTML = "public.html"              # NSPasteboardTypeHTML
PB_URL = "public.url"                # NSPasteboardTypeURL: a link copied on its own


class ClipboardUnavailable(Exception):
    """The clipboard could not be read just now; the page tries its next way."""


def _plain_newlines(text):
    """Some programs write a new line as CR or CR LF; the page wants LF alone."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _on_main_thread(work):
    """Run work() on the main thread and return what it returns."""
    import threading
    if threading.current_thread() is threading.main_thread():
        return work()
    from PyObjCTools import AppHelper
    box = {}
    done = threading.Event()

    def run():
        try:
            box["value"] = work()
        except Exception as exc:
            box["error"] = exc
        finally:
            done.set()

    AppHelper.callAfter(run)
    if not done.wait(CLIPBOARD_WAIT_S):
        raise ClipboardUnavailable("the clipboard did not answer in time")
    if "error" in box:
        raise ClipboardUnavailable("the clipboard could not be used (%s)" % (box["error"],))
    return box.get("value")


def clipboard_read():
    """What the clipboard holds: {"text": ..., "html": ...}.

    Each is "" when the clipboard holds none; an empty clipboard is not a
    failure. A link copied on its own (public.url, with no text beside it)
    comes back as its text. When the clipboard cannot be read, this raises
    ClipboardUnavailable: pywebview then rejects the page's Promise, and the
    page tries its next way.
    """
    if sys.platform != "darwin":
        raise ClipboardUnavailable("this clipboard bridge is for the Mac")

    def read():
        import AppKit
        board = AppKit.NSPasteboard.generalPasteboard()
        text = board.stringForType_(PB_TEXT)
        if text is None:
            text = board.stringForType_(PB_URL)
        html = board.stringForType_(PB_HTML)
        return {"text": _plain_newlines(str(text or "")), "html": str(html or "")}

    try:
        return _on_main_thread(read)
    except ClipboardUnavailable as exc:
        log_note("clipboard: %s; the page tries its next way" % (exc,))
        raise


def clipboard_write(text, html=""):
    """Put text on the clipboard, with its formatted copy when html is given.

    clearContents, then setString_forType_ for each kind (since macOS 10.6
    no types need declaring first). True when the text is on the clipboard.
    """
    if sys.platform != "darwin":
        return False
    text = "" if text is None else str(text)
    html = "" if html is None else str(html)

    def write():
        import AppKit
        board = AppKit.NSPasteboard.generalPasteboard()
        board.clearContents()
        done = bool(board.setString_forType_(text, PB_TEXT))
        if done and html and not board.setString_forType_(html, PB_HTML):
            log_note("clipboard: the text was copied, its formatting was not")
        return done

    try:
        return bool(_on_main_thread(write))
    except Exception as exc:
        log_note("clipboard: nothing was copied (%s)" % (exc,))
        return False


class TabulaWindowApi:
    """JS API for a floating app window: close, save, and open a sibling window.

    open_app delegates to the main window's API. Without it, pressing Imago
    inside the Tabula window had no way to ask for a window of its own, so the
    page fell back to tearing Tabula down and building Imago in its place, which
    is the heaviest thing a secondary web view can be asked to do.
    """

    def __init__(self, host=None):
        self._win = None
        self._host = host

    def open_app(self, which):
        try:
            if self._host is not None:
                return self._host.open_app(which)
        except Exception:
            log_problem("TabulaWindowApi.open_app(%r)" % (which,))
        return False

    def save_file(self, name, mime, data_b64):
        """The floating window previously had no way to write a file at all."""
        return save_bytes(self._win, name, mime, data_b64)

    def read_clipboard(self):
        """9s58: the clipboard, for the page's own Paste (see clipboard_read)."""
        return clipboard_read()

    def write_clipboard(self, text, html=""):
        """9s58: the page's own Copy and Cut (see clipboard_write)."""
        return clipboard_write(text, html)

    def close_self(self):
        try:
            if self._win is not None:
                self._win.destroy()
                return True
        except Exception:
            pass
        return False


class CarpeApi:
    """JS API exposed to the main window as window.pywebview.api.

    Opens Tabula, Abacus, or Imago in its own native window (the in-app floating
    button calls open_app). The windows share the same on-disk localStorage where
    the platform web view allows it; each app re-reads its saved work on load.
    """

    APP_TITLES = {"tabula": "Tabula", "abacus": "Abacus", "slides": "Imago", "scriba": "Scriba", "fontes": "Fontes"}
    APP_COLORS = {"tabula": "#2A2622", "abacus": "#1E3D2C", "slides": "#7A2530", "scriba": "#22304A", "fontes": "#F1EBE1"}

    def __init__(self, app_url):
        import threading
        self._app_url = app_url
        # Every window reference on an API object starts with an underscore.
        # pywebview walks each public attribute of the API on every page load,
        # and a public window led it through the whole native window and web
        # view (on Windows: errors, a slower start, and native controls offered
        # to the page). It skips names that start with an underscore.
        self._main_window = None
        self._wins = {}
        # Creating two native windows at once, or twice for the same studio
        # because the float button was pressed again while the first was still
        # opening, is a real way to destabilise the platform web view. One
        # creation at a time, and never a duplicate.
        self._lock = threading.RLock()
        self._creating = set()

    def _alive(self, which):
        w = self._wins.get(which)
        if w is None:
            return False
        try:
            _ = w.title
            return True
        except Exception:
            self._wins.pop(which, None)
            return False

    def print_document(self, name, mime, data_b64):
        """Printing has to leave the web view.

        WKWebView does not implement window.print(), so a print request made inside
        the page reaches nothing at all. The document is written to a file and opened
        with the system's own application, where the print dialog is the machine's.
        """
        return print_document(self._main_window, name, mime, data_b64)

    def save_file(self, name, mime, data_b64):
        return save_bytes(None, name, mime, data_b64)

    def read_clipboard(self):
        """9s58: the clipboard, for the page's own Paste (see clipboard_read)."""
        return clipboard_read()

    def write_clipboard(self, text, html=""):
        """9s58: the page's own Copy and Cut (see clipboard_write)."""
        return clipboard_write(text, html)

    def close_app(self, which):
        """Close a native studio window, so the desk bar's cross can reach it.
        Without this the cross could only ever close a desk frame, which is why it
        looked ornamental on the desktop builds."""
        if which not in self.APP_TITLES:
            return False
        with self._lock:
            w = self._wins.get(which)
        if w is None:
            return False
        try:
            w.destroy()
        except Exception:
            log_problem("close_app(%r): destroy failed" % (which,), sys.exc_info())
        finally:
            with self._lock:
                self._wins.pop(which, None)
        return True

    def focus_app(self, which):
        """Return True if that app window is open (and try to bring it forward)."""
        if which not in self.APP_TITLES or not self._alive(which):
            return False
        w = self._wins[which]
        try:
            w.restore()
        except Exception:
            pass
        try:
            w.show()
        except Exception:
            pass
        return True

    def open_app(self, which):
        """Open (or focus) a separate native window for the app. True on success."""
        if which not in self.APP_TITLES:
            return False
        with self._lock:
            if self._alive(which):
                return self.focus_app(which)
            if which in self._creating:
                log_problem("open_app(%r): already opening, ignored" % (which,))
                return False
            self._creating.add(which)
        try:
            import webview
            win_api = TabulaWindowApi(host=self)
            win = webview.create_window(
                self.APP_TITLES[which],
                url=self._app_url + "#cd=" + which,
                width=1050,
                height=760,
                min_size=(MIN_WIDTH, MIN_HEIGHT),
                background_color=self.APP_COLORS[which],
                confirm_close=False,
                text_select=True,
                js_api=win_api,
            )
            win_api._win = win
            self._wins[which] = win
            try:
                win.events.closed += (lambda *a, w=which: self._wins.pop(w, None))
            except Exception:
                pass
            return True
        except Exception:
            log_problem("open_app(%r)" % (which,))
            self._wins.pop(which, None)
            return False
        finally:
            with self._lock:
                self._creating.discard(which)

    # Backward compatible names kept for older builds of the app HTML.
    def broadcast_theme(self, dark):
        """Carry a theme change to every other native window of this app.

        Separate webviews do not reliably observe one another's localStorage
        writes, so the main window asks Python to relay the change directly.
        """
        js = "try{window.cdApplyThemeExternal&&window.cdApplyThemeExternal(%s);}catch(e){}" % (
            "true" if dark else "false",
        )
        targets = []
        try:
            targets.append(self._main_window)
        except Exception:
            pass
        with self._lock:
            targets.extend(list(self._wins.values()))
        for w in targets:
            if w is None:
                continue
            try:
                w.evaluate_js(js)
            except Exception:
                pass
        return True

    def open_tabula(self):
        return self.open_app("tabula")

    def focus_tabula(self):
        return self.focus_app("tabula")


# 644 (forge_guard_644.py): the Forge's own address answers the Forge's own window only. pywebview serves the page from
# 127.0.0.1; a request that names any other host (a page that has pointed its own name at 127.0.0.1) is refused before any
# file is read.
def _guard_local_server():
    try:
        import webview.http as _wh
    except Exception:
        return False
    b = getattr(_wh, "bottle", None)
    if b is None or getattr(b.run, "_forge_guard", False):
        return bool(b)
    orig = b.run

    def run(app=None, *a, **kw):
        # the port as pywebview gives it (by name), or in its place (bottle.run(app, server, host, port))
        port, inner = kw.get("port") or (a[2] if len(a) > 2 else None), app

        def guarded(environ, start_response):
            host = (environ.get("HTTP_HOST") or "").strip().lower()
            name = host if host.endswith("]") else host.rsplit(":", 1)[0]
            # with the port known, the window's own address exactly; were a later pywebview to start its server some
            # other way, the computer's own name alone (a page that rebinds a name always names its own), never a blank window
            if (port and host in ("127.0.0.1:%s" % port, "localhost:%s" % port, "[::1]:%s" % port)) or                     (not port and name in ("127.0.0.1", "localhost", "[::1]")):
                return inner(environ, _forge_no_store(start_response))  # 647 (forge_shell_647b.py)
            body = b"This address answers only the Forge's own window."
            start_response("421 Misdirected Request", [("Content-Type", "text/plain; charset=utf-8"),
                                                       ("Content-Length", str(len(body)))])
            return [body]
        return orig(guarded, *a, **kw)   # the app first, in its place, however the rest is given
    run._forge_guard = True
    b.run = run
    return True


def _make_window(webview, api, app_html):
    """The main window, in one place so its creation can be guarded."""
    _guard_local_server()
    return webview.create_window(
        WINDOW_TITLE,
        url=app_html,
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        min_size=(MIN_WIDTH, MIN_HEIGHT),
        background_color=ACCENT_BLUE,
        confirm_close=False,
        text_select=True,
        js_api=api,
    )



class CarpeApiSingle:
    """The API offered on macOS by default: no second native window.

    A second web view in the same process is the most likely cause of the Mac
    crash, by the same reasoning that explained the Intel Windows machine. The
    page asks Python for a native window only because open_app exists; with it
    absent the app uses its own floating windows, drawn inside the page. Since
    pass 299 those resize from every edge, remember their place, fold into the
    dock and answer the desk tabs, so nothing is lost except the risk.

    CARPE_DIEM_NATIVE_WINDOWS=1 restores the old behaviour.
    """

    def __init__(self, app_url):
        self._app_url = app_url
        self._main_window = None

    def print_document(self, name, mime, data_b64):
        """Printing has to leave the web view.

        WKWebView does not implement window.print(), so a print request made inside
        the page reaches nothing at all. The document is written to a file and opened
        with the system's own application, where the print dialog is the machine's.
        """
        return print_document(self._main_window, name, mime, data_b64)

    def save_file(self, name, mime, data_b64):
        return save_bytes(None, name, mime, data_b64)

    def read_clipboard(self):
        """9s58: the clipboard, for the page's own Paste (see clipboard_read)."""
        return clipboard_read()

    def write_clipboard(self, text, html=""):
        """9s58: the page's own Copy and Cut (see clipboard_write)."""
        return clipboard_write(text, html)

    def broadcast_theme(self, dark):
        js = "try{window.cdApplyThemeExternal&&window.cdApplyThemeExternal(%s);}catch(e){}" % (
            "true" if dark else "false",)
        try:
            if self._main_window is not None:
                self._main_window.evaluate_js(js)
        except Exception:
            pass
        return True


def _session_flag():
    """Where the breadcrumb lives. Beside the log, so one folder holds both."""
    try:
        base = pathlib.Path.home() / "Library" / "Application Support" / "TheForge"
        base.mkdir(parents=True, exist_ok=True)
        return base / "the_forge_session.flag"
    except Exception:
        try:
            return pathlib.Path.home() / ".the_forge_session.flag"
        except Exception:
            return None


def _begin_session():
    """Return how many previous runs ended without cleaning up after themselves."""
    f = _session_flag()
    if f is None:
        return 0
    prior = 0
    try:
        if f.exists():
            prior = int((f.read_text().strip() or "1"))
    except Exception:
        prior = 1
    try:
        f.write_text(str(prior + 1))
    except Exception:
        pass
    return prior


def _end_session():
    """A clean exit removes the breadcrumb, so only bad endings accumulate."""
    f = _session_flag()
    try:
        if f is not None and f.exists():
            f.unlink()
    except Exception:
        pass


def _closing_is_clean():
    """The window is closing on purpose: its close button, Quit, or Command+Q.

    Quit ends the app from macOS itself, so webview.start() never returns and
    the clean exit below never runs. Every ordinary Quit was therefore counted
    as a bad ending, and after two of them the next start opened the app in
    the browser instead of its own window. The window's closing event runs for
    a close and for a Quit alike, before the app goes, so the mark is cleared
    here. A crash still leaves it, which is what the safeguard is for. Returns
    nothing, so the closing goes ahead.
    """
    _end_session()


_loaded_once = []


def _page_loaded():
    """Recorded once, so a slow first start can be measured from the log."""
    if not _loaded_once:
        _loaded_once.append(1)
        log_problem("start: the page has loaded")


import pathlib

def skip_server_name_lookup():
    """Start the app's local page server without asking the network who it is.

    pywebview serves the_forge.html from a small server on this Mac only
    (127.0.0.1). Python's server, as it starts, looks up the computer's full
    network name before it begins accepting connections. On macOS Sequoia that
    lookup can go out to the local network: macOS then asks "Allow The Forge
    to find devices on local networks?", and while the lookup waits the server
    refuses the window's first request, so the window stays blank. Seen on
    GitHub's Mac in build 1042, Apple silicon and Intel alike.

    The name is only ever used for a header nobody reads, so the server is
    given its own address instead. Same address, same port: the storage that
    holds your work is untouched.
    """
    try:
        import http.server
        import socketserver

        def server_bind(self):
            socketserver.TCPServer.server_bind(self)
            host, port = self.server_address[:2]
            self.server_name = host
            self.server_port = port

        http.server.HTTPServer.server_bind = server_bind
    except Exception:
        log_problem("could not skip the page server's name lookup")



def show_seal_in_dock(picture):
    """macOS 26 sets an app's own icon in a grey square when it is not Apple's rounded square, and shrinks it.
    While the app runs, the Dock shows the picture the app gives it, so the round seal is given here, at its full size.
    Anywhere else (Windows, an older Mac) nothing changes."""
    if sys.platform != "darwin":
        return
    try:
        pic = resource_path(picture)
        if not os.path.isfile(pic):
            return
        from AppKit import NSApplication, NSImage
        img = NSImage.alloc().initWithContentsOfFile_(pic)
        if img is not None:
            NSApplication.sharedApplication().setApplicationIconImage_(img)
    except Exception:
        try:
            log_problem("dock seal", sys.exc_info())
        except Exception:
            pass


def give_bundle_its_seal(picture="the_forge.icns"):
    """642 (as Ingenium 6.1): macOS 26 puts the icon an app ships with in a grey rounded square and shrinks it, unless
    that icon is Apple's rounded square; a custom icon (what Finder's Get Info sets) it leaves as it is, round. The
    owner's words (20 October 2026): "For the Forge its even worse, the icon only looks like the circle seal on the
    Dock when the app is open, other than that its shrunk inside of the square". So on macOS 26 and later the app gives
    its own bundle the round seal as its custom icon, once for each copy of the app (a new build arrives without one),
    and gives it to its shortcuts and copies on the Desktop. The Desktop, the Applications folder and the Dock then
    show the seal at its full size, open or closed. Nothing changes on an older Mac."""
    if sys.platform != "darwin":
        return
    try:
        if int(os.uname().release.split(".")[0]) < 25:   # Darwin 25 is macOS 26
            return
        bundle = os.path.abspath(sys.executable)
        while bundle and bundle != os.path.dirname(bundle) and not bundle.endswith(".app"):
            bundle = os.path.dirname(bundle)
        if not bundle.endswith(".app") or not os.path.isdir(bundle):
            return
        pic = resource_path(picture)
        if not os.path.isfile(pic):
            pic = resource_path("the_forge.png")
        if not os.path.isfile(pic):
            return
        from AppKit import NSImage, NSWorkspace
        img = NSImage.alloc().initWithContentsOfFile_(pic)
        if img is None:
            return
        if os.access(bundle, os.W_OK) and not os.path.exists(os.path.join(bundle, "Icon\r")):
            ok = NSWorkspace.sharedWorkspace().setIcon_forFile_options_(img, bundle, 0)
            log_problem("mac: the seal was %s as this copy's own icon (%s)" % ("given" if ok else "refused", bundle))
        _seal_shortcuts(bundle, img)
    except Exception:
        try:
            log_problem("mac: custom icon", sys.exc_info())
        except Exception:
            pass


def _seal_shortcuts(bundle, img):
    """642: the shortcuts to this app on the Desktop (Finder aliases, symbolic links) and copies of it there get the round
    seal as their own icon too. The owner's words (20 October 2026): "It looks fine on the applications list on the mac
    and on the Dock but the shortcut on the desktop has the grey look." A shortcut is a file of its own, which macOS 26
    draws with the app's shipped icon in its grey square; a custom icon on the shortcut itself is left as it is, round.
    Each one is given the seal once (seal_shortcuts.json, beside the stored session, remembers which)."""
    import json
    from AppKit import NSWorkspace
    from Foundation import NSURL, NSBundle
    ws = NSWorkspace.sharedWorkspace()
    real = os.path.realpath(bundle)
    try:
        mine = NSBundle.bundleWithPath_(bundle).bundleIdentifier()
    except Exception:
        mine = None
    rec_path = None
    try:
        d = storage_dir()
        rec_path = os.path.join(os.path.dirname(d), "seal_shortcuts.json") if d else None
    except Exception:
        rec_path = None
    rec = {}
    try:
        if rec_path and os.path.isfile(rec_path):
            with open(rec_path, encoding="utf-8") as fh:
                rec = json.load(fh) or {}
    except Exception:
        rec = {}
    desk = os.path.expanduser("~/Desktop")
    if not os.path.isdir(desk):
        return
    changed = False
    for name in sorted(os.listdir(desk)):
        p = os.path.join(desk, name)
        try:
            ours = False
            if os.path.islink(p):
                ours = os.path.realpath(p) == real
            elif name.endswith(".app") and os.path.isdir(p):
                ours = os.path.realpath(p) == real
                if not ours and mine:
                    b = NSBundle.bundleWithPath_(p)
                    ours = bool(b is not None and b.bundleIdentifier() == mine)
                if ours and os.path.exists(os.path.join(p, "Icon\r")):
                    continue
            elif os.path.isfile(p):
                url = NSURL.fileURLWithPath_(p)
                res = NSURL.URLByResolvingAliasFileAtURL_options_error_(url, 1 << 8, None)
                to = res[0] if isinstance(res, tuple) else res
                if to is not None and to.path() and os.path.realpath(str(to.path())) != os.path.realpath(p):
                    ours = os.path.realpath(str(to.path())) == real
            if not ours:
                continue
            st = os.lstat(p)
            if rec.get(p) == [st.st_ino, int(st.st_mtime)]:
                continue
            if ws.setIcon_forFile_options_(img, p, 0):
                st = os.lstat(p)
                rec[p] = [st.st_ino, int(st.st_mtime)]
                changed = True
                try:
                    ws.noteFileSystemChanged_(p)
                except Exception:
                    pass
                log_problem("mac: the seal was given to the shortcut " + p)
        except Exception:
            log_problem("mac: shortcut icon " + p, sys.exc_info())
    if changed and rec_path:
        try:
            with open(rec_path, "w", encoding="utf-8") as fh:
                json.dump(rec, fh)
        except Exception:
            pass


# ---- PASS 643 (20 October 2026): Refresh from the Mac's own menu and keys ----------------------------------------
# The owner's words: "I want a refresh button added to Ingenium and the Forge, that refreshed the app if it glitches
# or freezes." The page has its own Refresh key, which saves first, but a frozen page cannot answer a key of its own.
# So the app menu holds "Refresh The Forge", and Command+R reaches the app before the page: the page is asked to
# refresh itself (saving first); when it gives no answer within two seconds, the window loads the page again by itself.
_REFRESH = {"monitor": None, "url": None, "lock": None}


def _refresh_window(window):
    """Runs on its own thread (a menu action or the key monitor starts it)."""
    import threading
    if _REFRESH["lock"] is None:
        _REFRESH["lock"] = threading.Lock()
    if not _REFRESH["lock"].acquire(False):
        return
    try:
        answer = {}

        def _ask():
            try:
                answer["v"] = window.evaluate_js(
                    "(function(){try{var f=window.forgeRefresh||window.ingRefresh;if(typeof f==='function'){f('menu');return 'page';}}"
                    "catch(e){}return 'none';})()")
            except BaseException:
                answer["v"] = "!" + repr(sys.exc_info()[1])

        t = threading.Thread(target=_ask, daemon=True)
        t.start()
        t.join(2.0)
        if answer.get("v") == "page":
            log_problem("refresh: the page refreshes itself")
            return
        log_problem("refresh: no answer from the page (%r); the window loads it again" % (answer.get("v"),))
        try:
            url = window.get_current_url()
        except BaseException:
            url = None
        url = url or _REFRESH["url"]
        if url:
            window.load_url(url)
    except BaseException:
        log_problem("refresh failed", sys.exc_info())
    finally:
        _REFRESH["lock"].release()


def _refresh_menu(webview, window):
    """The app menu's "Refresh The Forge", or None where this pywebview cannot add to the app menu (6.2 and later can)."""
    if sys.platform != "darwin":
        return None
    try:
        import re
        ver = tuple(int(x) for x in re.findall(r"\d+", str(getattr(webview, "__version__", "0")))[:2])
        if ver < (6, 2):
            return None
        from webview.menu import Menu, MenuAction

        def refresh_the_forge():
            _refresh_window(window)

        return [Menu("__app__", [MenuAction("Refresh The Forge", refresh_the_forge)])]
    except Exception:
        log_problem("refresh menu: not available", sys.exc_info())
        return None


def _install_refresh_key_monitor(window):
    """macOS only: Command+R (with Shift too) in the main window refreshes, even while the page is frozen."""
    if _REFRESH["monitor"] is not None or sys.platform != "darwin":
        return
    try:
        import threading
        import AppKit
        mask = getattr(AppKit, "NSEventMaskKeyDown", getattr(AppKit, "NSKeyDownMask", 1 << 10))
        flag_cmd = getattr(AppKit, "NSEventModifierFlagCommand", getattr(AppKit, "NSCommandKeyMask", 1 << 20))
        flag_alt = getattr(AppKit, "NSEventModifierFlagOption", getattr(AppKit, "NSAlternateKeyMask", 1 << 19))
        flag_ctrl = getattr(AppKit, "NSEventModifierFlagControl", getattr(AppKit, "NSControlKeyMask", 1 << 18))

        def _handler(ev):
            try:
                f = ev.modifierFlags()
                if not (f & flag_cmd) or (f & flag_alt) or (f & flag_ctrl):
                    return ev
                if str(ev.charactersIgnoringModifiers() or "").lower() != "r":
                    return ev
                win = ev.window()
                if win is None or str(win.title() or "") != WINDOW_TITLE:
                    return ev
                threading.Thread(target=_refresh_window, args=(window,), daemon=True).start()
                return None  # the app has it; the page does not see it as well
            except BaseException:
                return ev

        _REFRESH["monitor"] = AppKit.NSEvent.addLocalMonitorForEventsMatchingMask_handler_(mask, _handler)
        log_problem("refresh key monitor installed" if _REFRESH["monitor"] is not None else "refresh key monitor: AppKit refused it")
    except Exception:
        log_problem("refresh key monitor failed", sys.exc_info())


def _start_refresh_keys(window):
    """The key monitor installs on the main thread once the window has settled (PyObjCTools' AppHelper, which
    pywebview itself carries)."""
    if sys.platform != "darwin":
        return
    import threading
    import time

    def _boot():
        time.sleep(1.2)
        try:
            from PyObjCTools import AppHelper
            AppHelper.callAfter(_install_refresh_key_monitor, window)
        except Exception:
            _install_refresh_key_monitor(window)

    threading.Thread(target=_boot, daemon=True).start()


def _guard_bridge_frames():
    """647 (forge_shell_647.py): on a Mac, answer a call from the page only when it comes from the main frame of the Forge's
    own page, never from a frame inside it (pywebview's message handler is defined in every frame and does not check)."""
    if sys.platform != "darwin":
        return
    try:
        import objc
        from webview.platforms import cocoa as _pc
        base = _pc.BrowserView.JSBridge
        if getattr(base, "_forge_guarded", False):
            return

        class ForgeFrameGuardedJSBridge(base):
            def userContentController_didReceiveScriptMessage_(self, controller, message):
                try:
                    info = message.frameInfo()
                    if info is None or not info.isMainFrame():
                        return
                    origin = info.securityOrigin()
                    host = str(origin.host() or "") if origin is not None else ""
                    proto = str(origin.protocol() or "").lower() if origin is not None else ""
                    # the Forge's own page: from its file, or from pywebview's own address; never a website
                    if not (host in ("127.0.0.1", "localhost") or proto in ("file", "about") or (proto == "" and host == "")):
                        return
                except Exception:
                    return
                objc.super(ForgeFrameGuardedJSBridge, self).userContentController_didReceiveScriptMessage_(controller, message)

        ForgeFrameGuardedJSBridge._forge_guarded = True
        _pc.BrowserView.JSBridge = ForgeFrameGuardedJSBridge
    except Exception:
        log_problem("guard of the page's calls to the program could not be set", sys.exc_info())


_CARE = {"attached": False, "reloads": [], "told": False, "gpu": 0, "refs": []}


def _care_say(text):
    if not _CARE["told"]:
        _CARE["told"] = True
        import threading as _th
        _th.Thread(target=tell_user, args=(text,), daemon=True).start()


def _forge_care_attach(window):
    """647 (forge_shell_647.py), Windows: listen for the web view's processes stopping. Once, from the first page load (the web
    view exists by then); the listening itself is set up on the window's own thread."""
    if _CARE["attached"] or not sys.platform.startswith("win"):
        return
    _CARE["attached"] = True
    try:
        import time as _t
        import clr  # noqa: F401  (pythonnet, already loaded by the window)
        from System import Func, Type
        from Microsoft.Web.WebView2.Core import CoreWebView2ProcessFailedKind as K
        form = getattr(window, "native", None)
        wv = getattr(form, "webview", None) if form is not None else None
        if wv is None:
            log_problem("care: the web view could not be reached; a page whose process stops will not come back by itself")
            return

        def failed(_sender, args):
            try:
                kind = args.ProcessFailedKind
                more = ""
                try:
                    more = " (%s, exit code %s)" % (args.Reason, args.ExitCode)
                except Exception:
                    pass
                now = _t.time()
                if kind == K.RenderProcessExited:
                    recent = [x for x in _CARE["reloads"] if now - x < 120]
                    if len(recent) >= 3:
                        log_note("page: its process stopped again%s, after three new starts in two minutes; left as it is" % more)
                        _care_say("The Forge's page stopped working several times in a row.\n\nYour work is saved as you go. "
                                  "Please close The Forge and open it again.\n\nDetails were written to:\n  %s" % crash_log_path())
                        return
                    recent.append(now)
                    _CARE["reloads"] = recent
                    log_note("page: its process stopped%s; the page is loaded again" % more)
                    wv.CoreWebView2.Reload()
                elif kind == K.RenderProcessUnresponsive:
                    log_note("page: its process is not answering%s; left to finish what it is doing" % more)
                elif kind == K.GpuProcessExited:
                    _CARE["gpu"] += 1
                    log_note("graphics: the graphics process stopped%s (%d this run)" % (more, _CARE["gpu"]))
                    path = _safe_graphics_file()
                    if _CARE["gpu"] >= 2 and not os.path.isfile(path) and _remember_safe_graphics(path, 1):
                        log_note("graphics: safe graphics kept for the next start (%s)" % path)
                elif kind == K.BrowserProcessExited:
                    log_note("web view: its own process stopped%s; the window cannot show the page until The Forge is opened again" % more)
                    _care_say("The Forge's window stopped working (its web view closed).\n\nYour work is saved as you go. "
                              "Please close The Forge and open it again.")
                else:
                    log_note("web view: a helper process stopped (%s)%s" % (kind, more))
            except BaseException:
                log_problem("care: a stopped process could not be handled", sys.exc_info())

        def attach():
            core = wv.CoreWebView2
            if core is None:
                log_problem("care: the web view is not ready; a page whose process stops will not come back by itself")
                return None
            core.ProcessFailed += failed
            _CARE["refs"].append(failed)
            ver = ""
            try:
                ver = str(core.Environment.BrowserVersionString)
            except Exception:
                pass
            log_note("care: listening for the page's processes stopping (web view %s)" % (ver or "version unknown"))
            return None
        form.Invoke(Func[Type](attach))
    except BaseException:
        log_problem("care: could not listen to the web view", sys.exc_info())


def _forge_no_store(start_response):
    """647 (forge_shell_647b.py): every answer from the Forge's own address says it is not to be kept."""
    def sr(status, headers, exc_info=None):
        keep = [(k, v) for (k, v) in headers if k.lower() not in ("cache-control", "expires", "pragma", "etag", "last-modified")]
        keep += [("Cache-Control", "no-store, max-age=0"), ("Pragma", "no-cache"), ("Expires", "0")]
        if exc_info is not None:
            return start_response(status, keep, exc_info)
        return start_response(status, keep)
    return sr


def _page_build(path):
    """The build the Forge's page names (window.CD_BUILD's pass and stamp), read from the file, or ''."""
    import re as _re
    try:
        with open(path, "rb") as fh:
            data = fh.read()
        m = _re.search(rb'window\.CD_BUILD=\{date:"[^"]*",pass:"(\d+)",stamp:"([^"]*)"', data)
        return (m.group(1) + b" " + m.group(2)).decode("ascii", "replace") if m else ""
    except Exception:
        return ""


def _forget_old_pages(app_html):
    """647 (forge_shell_647b.py): the first time a build starts, the web view's cache of pages is emptied, so the window shows
    this build's page and not one kept from an earlier build at the same address. The work (local storage, the databases) is
    never touched."""
    build = _page_build(app_html)
    store = storage_dir()
    if not build or not store:
        return
    note = os.path.join(os.path.dirname(store), "page_build.txt")
    try:
        with open(note, encoding="utf-8") as fh:
            before = fh.read().strip()
    except Exception:
        before = ""
    if before == build:
        return
    emptied = False
    try:
        if sys.platform == "darwin":
            import time as _t
            import WebKit
            from Foundation import NSDate, NSRunLoop, NSSet
            kinds = NSSet.setWithArray_([WebKit.WKWebsiteDataTypeDiskCache, WebKit.WKWebsiteDataTypeMemoryCache])
            done = {"ok": False}

            def _done():
                done["ok"] = True
            WebKit.WKWebsiteDataStore.defaultDataStore().removeDataOfTypes_modifiedSince_completionHandler_(
                kinds, NSDate.dateWithTimeIntervalSince1970_(0), _done)
            end = _t.time() + 5
            while not done["ok"] and _t.time() < end:
                NSRunLoop.currentRunLoop().runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.05))
            emptied = done["ok"]
        elif sys.platform.startswith("win"):
            import shutil as _sh
            for rel in (("EBWebView", "Default", "Cache"), ("EBWebView", "Default", "Code Cache")):
                p = os.path.join(store, *rel)
                if os.path.isdir(p):
                    _sh.rmtree(p, ignore_errors=True)
            emptied = True
    except Exception:
        log_problem("page cache: could not be emptied", sys.exc_info())
    log_note("page: build %s starts (the build before: %s); the web view's cache of pages %s"
             % (build, before or "none noted", "emptied" if emptied else "NOT emptied"))
    if emptied:
        try:
            with open(note, "w", encoding="utf-8") as fh:
                fh.write(build)
        except Exception:
            pass


def main():
    skip_server_name_lookup()
    app_html = find_app_html()
    if not app_html:
        tell_user(
            "Could not find the app file, the_forge.html.\n\n"
            "If you are running from the source folder, keep the_forge.html\n"
            "beside this program. The portable version that needs no folder is\n"
            "the single file made by the Build step (The Forge.exe on Windows,\n"
            "The Forge.app on Mac). It carries the whole app inside and opens\n"
            "from anywhere you move it.\n\n"
            "You can also open the_forge.html on its own. That file is the\n"
            "whole app, offline."
        )
        sys.exit(1)

    try:
        _forget_old_pages(app_html)  # 647 (forge_shell_647b.py)
    except Exception:
        log_problem("page cache: the check failed", sys.exc_info())
    log_problem("start: locating the window component")
    try:
        import webview  # pywebview
    except BaseException:
        # Not ImportError alone. On Windows pywebview loads pythonnet, and a
        # runtime that will not start raises RuntimeError, OSError or worse.
        # This was a crash before the window ever appeared.
        log_problem("import webview failed", sys.exc_info())
        _missing = isinstance(sys.exc_info()[1], ImportError)
        if open_in_browser(app_html):
            if _missing:
                tell_user(
                    "The Forge has opened in your browser, because the component\n"
                    "that draws its own window is not installed.\n\n"
                    "Everything works exactly the same there, and nothing is sent\n"
                    "anywhere."
                )
            else:
                tell_user(
                    "The Forge has opened in your browser, because the component\n"
                    "that draws its own window would not start on this PC.\n\n"
                    "Everything works exactly the same there, and nothing is sent\n"
                    "anywhere.\n\n"
                    "Details were written to:\n  %s" % crash_log_path()
                )
            return
        tell_user(friendly_missing_dependency_message())
        sys.exit(1)

    # Create the native window pointing at the local HTML file. Because the file
    # is loaded from disk, everything runs offline with no server involved.
    # background_color tints the native window behind the page. It is what shows
    # during load and around the content, so the window reads as The Forge blue
    # rather than default grey. Note: this is NOT the same as the blue title bar
    # you get from installing as a web app, which comes from the manifest's
    # theme_color and is applied by the browser. See README (Blue title bar).
    # File URI form so a query flag can be appended for the Tabula window.
    try:
        from pathlib import Path
        app_url = Path(app_html).as_uri()
    except Exception:
        app_url = app_html

    # Recorded once at startup so a crash report says what it was running on.
    try:
        import platform
        log_problem("start: python %s on %s %s | pywebview %s" % (
            platform.python_version(), platform.system(), platform.release(),
            getattr(webview, "__version__", "unknown")))
    except Exception:
        pass

    _prior_bad = _begin_session()
    if _prior_bad >= 2:
        # Two runs in a row ended badly. The file is the whole application,
        # so hand it to the browser rather than fail a third time.
        log_problem("mac: two bad endings, opening in the browser instead")
        try:
            import webbrowser
            webbrowser.open(pathlib.Path(app_html).as_uri())
        except Exception:
            pass
        _end_session()
        # Never silently: the browser keeps its own copy of the work.
        tell_user(
            "The Forge did not close properly the last two times it ran, so this\n"
            "once it has opened in your browser instead of its own window.\n\n"
            "Your work in the app's own window is kept there, and the next start\n"
            "opens that window again. Work done in the browser is kept by the\n"
            "browser, separately.\n\n"
            "Details were written to:\n  %s" % crash_log_path())
        return 0
    if not os.environ.get("CARPE_DIEM_NATIVE_WINDOWS"):
        api = CarpeApiSingle(app_url)
        log_problem("mac: one window, the app draws its own floating windows")
    else:
        api = CarpeApi(app_url)
    try:
        window = _make_window(webview, api, app_html)
    except BaseException:
        # Creating the window can fail on its own, before start() is reached.
        log_problem("create_window failed", sys.exc_info())
        if open_in_browser(app_html):
            tell_user(
                "The Forge could not open a native window on this PC, so it has\n"
                "opened in your browser instead. Everything works the same there.\n\n"
                "On Windows the usual cause is a missing Edge WebView2 runtime; on a Mac\n"
                "it is a Python built without the frameworks a window needs.\n\n"
                "Details were written to:\n  %s" % crash_log_path())
            return
        tell_user(
            "The Forge could not open a window on this PC.\n\n"
            "Open the_forge.html by hand: that file IS the whole app.\n\n"
            "Details were written to:\n  %s" % crash_log_path())
        sys.exit(1)
    try:
        api._main_window = window
    except Exception:
        pass
    # A Quit is a clean ending (see _closing_is_clean); a crash still is not.
    try:
        window.events.closing += _closing_is_clean
    except Exception:
        log_problem("could not watch the window closing")
    try:
        window.events.loaded += _page_loaded
        window.events.loaded += lambda *_a, **_k: _forge_care_attach(window)  # 647 (forge_shell_647.py)
    except Exception:
        pass

    # gui=None lets pywebview pick the best native backend for the platform
    # (Edge WebView2 on Windows, WKWebView on macOS, WebKitGTK/Qt on Linux).
    # debug=False keeps developer tools hidden for a clean, app-like feel.
    def _hook(exc_type, exc, tb):
        log_problem("uncaught", (exc_type, exc, tb))
        sys.__excepthook__(exc_type, exc, tb)
    sys.excepthook = _hook
    try:
        import threading
        if hasattr(threading, "excepthook"):
            threading.excepthook = lambda a: log_problem(
                "uncaught in thread", (a.exc_type, a.exc_value, a.exc_traceback))
    except Exception:
        pass

    # private_mode=False is what makes the work survive closing the app.
    # storage_path keeps it in the user's profile rather than in a temporary
    # unpack directory. An older pywebview may not accept either, so the failure
    # is caught and RECORDED rather than passing silently, because passing
    # silently is exactly how the data loss went unnoticed.
    _guard_bridge_frames()  # 647 (forge_shell_647.py)
    show_seal_in_dock('the_forge.png')
    give_bundle_its_seal()
    _store = storage_dir()
    _REFRESH["url"] = app_url
    _menu = _refresh_menu(webview, window)  # PASS 643: "Refresh The Forge" in the app menu, and Command+R
    _start_refresh_keys(window)
    try:
        if _store and _menu:
            try:
                webview.start(gui=None, debug=False, private_mode=False, storage_path=_store, menu=_menu)
            except TypeError:
                log_problem("webview.start refused the menu; starting without it")
                webview.start(gui=None, debug=False, private_mode=False, storage_path=_store)
            _end_session()
        elif _store:
            webview.start(gui=None, debug=False, private_mode=False, storage_path=_store)
            _end_session()
        else:
            webview.start(gui=None, debug=False, private_mode=False)
    except TypeError:
        log_problem("webview.start refused private_mode or storage_path; "
                    "this pywebview is too old and YOUR WORK WILL NOT PERSIST")
        webview.start(gui=None, debug=False)
    except Exception:
        # No native window could be created at all: a missing WebView2 runtime
        # on Windows is the usual reason. The page still is the application, so
        # it opens in the browser rather than the program dying in silence.
        log_problem("webview.start failed", sys.exc_info())
        if open_in_browser(app_html):
            tell_user(
                "The Forge could not open a native window on this PC, so it has\n"
                "opened in your browser instead. Everything works the same there.\n\n"
                "On Windows that usually means a missing Edge WebView2 runtime; on a Mac,\n"
                "a Python built without the frameworks a window needs.\n"
                "Details were written to:\n  %s" % crash_log_path()
            )
        else:
            tell_user(
                "The Forge could not open a window, and could not reach a browser\n"
                "either. Open the_forge.html by hand: that file IS the whole app.\n\n"
                "Details were written to:\n  %s" % crash_log_path()
            )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        # A crash now leaves a file to read instead of a window that vanishes.
        log_problem("fatal")
        tell_user(
            "The Forge stopped unexpectedly.\n\n"
            "Details were written to:\n  %s\n\n"
            "the_forge.html in the same folder still opens the whole app." % crash_log_path())
        sys.exit(1)
