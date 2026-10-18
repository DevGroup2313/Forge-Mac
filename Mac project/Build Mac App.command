#!/usr/bin/env bash
# THE FORGE  |  Copyright (c) 2026 Yannie D. Forest. All rights reserved.
# NO LICENCE IS GRANTED. No copying, adaptation, redistribution, reverse
# engineering or commercial use without the author's written permission.
# See LICENCE.txt. Every distributed copy carries a build marker.
# The Forge — build the standalone macOS app.
# Double-click this file. It needs Python 3 on THIS Mac only; the finished app
# needs nothing at all on the Macs you give it to.

cd "$(dirname "$0")" || exit 1
ORIGIN="$(pwd)"
LOG="$ORIGIN/build_log.txt"
# The round seal at its full size: macOS 26 sets an app's own icon in a grey square when it is not Apple's rounded
# square, and shrinks it, but leaves a custom icon as it is; so each copy is given the seal as its custom icon, as
# Finder's Get Info would. To undo: Get Info on the app, click the small icon at the top, press Delete.
seal_icon(){ [ -f "$1" ] && [ -d "$2" ] || return 0
  osascript -l JavaScript - "$1" "$2" >>"$LOG" 2>&1 <<'JS' || true
ObjC.import('AppKit');
function run(a){var i=$.NSImage.alloc.initWithContentsOfFile(a[0]);if(!i||i.isNil())return 'seal: no picture';return $.NSWorkspace.sharedWorkspace.setIconForFileOptions(i,a[1],0)?'seal: set':'seal: refused';}
JS
}
: > "$LOG"
say(){ printf '%s\n' "$*" | tee -a "$LOG"; }

# Why the tools would not install, said plainly. A path to a log is not an
# answer, and the two causes below account for nearly every failure.
tools_failed(){
  say ""
  say "The build tools could not be installed."
  say ""
  say "The last lines of the log say:"
  tail -n 18 "$LOG"
  say ""
  if grep -qiE "no matching distribution|could not find a version" "$LOG"; then
    say "READ THIS FIRST: no build tool exists yet for this version of Python."
    say "PyInstaller lags a few months behind each new Python release, so a very"
    say "new Python cannot build an app at all."
    say ""
    say "Two ways forward:"
    say "  1. Install Python 3.12 or 3.13 alongside the one you have, then run"
    say "     this again. The installers keep both, and nothing breaks."
    say "  2. Skip the app: double-click the_forge.html. Same app, offline,"
    say "     nothing to install."
  elif grep -qiE "temporary failure in name resolution|failed to establish a new connection|proxyerror|network is unreachable" "$LOG"; then
    say "This step needs the internet once, to download PyInstaller."
    say ""
    say "Three ways forward:"
    say "  1. Connect and run this again. That is all."
    say "  2. Build offline: on any connected Mac run"
    say "       python3 -m pip download pyinstaller pywebview -d wheels"
    say "     then copy the resulting wheels folder next to this file."
    say "  3. Skip the app entirely: double-click the_forge.html."
  elif grep -qi "certificate_verify_failed" "$LOG"; then
    say "The download was refused by a certificate check, which usually means a"
    say "workplace or school network inspecting traffic. On a home connection"
    say "this normally goes away. Or just open the_forge.html."
  else
    say "Full log:  $LOG"
    say "Send that file and the exact cause can be identified."
  fi
  say ""
  read -r -p "Press Return to close. "
  exit 1
}

say "The Forge — building the standalone Mac app"
say "Started $(date)"
say ""
say "You do not have to build anything to use The Forge."
say "the_forge.html in this folder IS the whole app: double-click it and it"
say "runs offline, with nothing installed. This script is optional, and only"
say "wraps that same app as a Mac application."
say ""

if ! command -v python3 >/dev/null 2>&1; then
  say "Python 3 was not found on this Mac."
  say "Install it from https://www.python.org/downloads/ and run this again."
  read -r -p "Press Return to close. "; exit 1
fi
say "Python:      $(python3 --version 2>&1)"

# ---------------------------------------------------------------------------
# 9s21: never build on a removable drive. Measured 22 Sep 2026 on an exFAT USB
# stick: the format holds no symlinks and no macOS permissions, and PyInstaller
# writes thousands of small files through it, so a build that takes minutes on
# the Mac's own disk took most of an hour, and the finished app was then slow
# to verify and slow even to paint its icon, because macOS had to read the
# whole bundle back through the stick. The probe is a feature test, not a
# guess: if a symlink cannot be made here, an app cannot be built here, and the
# work moves to the Mac's own disk. The build log stays beside this file.
STAGED=""
if ! ln -s . .forge_probe 2>/dev/null; then
  STAGED="yes"
  CACHE="$HOME/Library/Caches/TheForgeBuild"
  say ""
  say "NOTE: this folder is on a removable drive (a USB stick or similar), which"
  say "cannot hold a built app. The build will run on the Mac's own disk instead"
  say "($CACHE), and the finished app will be placed on your Desktop."
  mkdir -p "$CACHE" || { say "Could not create $CACHE"; exit 1; }
  WORK="$CACHE/work"
  rm -rf "$WORK"; mkdir -p "$WORK"
  cp "the_forge_app.py" "the_forge.spec" "the_forge.icns" "the_forge.png" "the_forge.html" "$WORK/"
  cp "BUILD_INFO.txt" "$WORK/" 2>/dev/null || true 2>>"$LOG"
  cd "$WORK" || exit 1
  for f in "the_forge_app.py" "the_forge.spec" "the_forge.icns" "the_forge.png" "the_forge.html"; do
    [ -s "$f" ] || { say "Missing piece: $f. The build cannot run. See $LOG"; read -r -p "Press Return to close. "; exit 1; }
  done
else
  rm -f .forge_probe
fi
if [ -n "$STAGED" ]; then VENV="$CACHE/venv"; else VENV=".buildenv"; fi

# A private build environment. Without this, Homebrew and system Python refuse
# pip installs with "error: externally-managed-environment" (PEP 668). When the
# build was staged it lives in the Caches folder and survives between builds.
PY="$VENV/bin/python"
if [ ! -x "$PY" ] || ! "$PY" --version >/dev/null 2>&1; then
  rm -rf "$VENV"
  say "Creating a private build environment (one time)..."
  if ! python3 -m venv "$VENV" >>"$LOG" 2>&1; then
    say ""; say "Could not create the build environment. See $LOG"
    read -r -p "Press Return to close. "; exit 1
  fi
fi

# The tools install only when missing. On the Mac's own disk that means once,
# not once per build, and an interrupted install simply installs again.
if ! "$PY" -m PyInstaller --version >/dev/null 2>&1; then
  if [ -d "$ORIGIN/wheels" ] && ls "$ORIGIN"/wheels/*.whl >/dev/null 2>&1; then
    say "Installing the build tools from the local wheels folder (one time)..."
    if ! "$PY" -m pip install --no-index --find-links "$ORIGIN/wheels" pyinstaller pywebview >>"$LOG" 2>&1; then
      tools_failed
    fi
  else
    say "Installing the build tools (a few minutes, once)..."
    "$PY" -m pip install --upgrade pip >>"$LOG" 2>&1
    if ! "$PY" -m pip install pyinstaller pywebview >>"$LOG" 2>&1; then
      tools_failed
    fi
  fi
fi
say "PyInstaller: $("$PY" -m PyInstaller --version 2>&1)"
say ""

rm -rf build dist
say "Building. This takes a few minutes and the window will look idle..."
T0=$SECONDS
"$PY" -m PyInstaller --noconfirm --clean the_forge.spec >>"$LOG" 2>&1
STATUS=$?
say "Build step took $(( (SECONDS-T0+59)/60 )) minute(s), exit status $STATUS."

APP="dist/The Forge.app"
say ""
if [ "$STATUS" -eq 0 ] && [ -d "$APP" ]; then
  if [ -n "$STAGED" ]; then
    DEST="$HOME/Desktop/The Forge.app"
    rm -rf "$DEST"
    cp -R "$APP" "$DEST" 2>>"$LOG"
    say "SUCCESS."
    say "Your app is on the Desktop:  $DEST"
  else
    DEST="$APP"
    say "SUCCESS."
    say "Your app is:  $(pwd)/$APP"
  fi
  # Clear the download quarantine on the app just built, so it opens on THIS Mac
  # with no Gatekeeper prompt. This copy only: a copy sent to another Mac is
  # quarantined again on arrival, which only Apple notarisation removes for good.
  xattr -dr com.apple.quarantine "$DEST" >/dev/null 2>&1 || true
  seal_icon "$ORIGIN/the_forge.png" "$DEST"
  say ""
  say "The Forge.app is one self-contained bundle. It carries the whole app"
  say "inside, so it opens from anywhere you move it on this Mac, with nothing"
  say "beside it. Drag it to Applications or keep it where you like."
  say ""
  say "On THIS Mac it should now open by double-clicking."
  say "On ANOTHER Mac the first open uses right-click then Open, because the app"
  say "is not notarised by Apple. MACOS_IF_BLOCKED.txt has the other routes."
  if [ -n "$STAGED" ]; then open -R "$DEST" >/dev/null 2>&1; else open dist >/dev/null 2>&1; fi
else
  say "The build did NOT finish, so nothing was produced."
  say "Exit status: $STATUS"
  say ""
  say "What is in dist right now:"
  ls -la dist 2>&1 | tee -a "$LOG"
  say ""
  say "The full build log is:  $LOG"
  say "Send that file and the exact cause can be identified. The last lines of it"
  say "are the ones that matter."
  say ""
  say "Last 15 lines:"
  tail -n 15 "$LOG"
fi
say ""
read -r -p "Press Return to close. "
