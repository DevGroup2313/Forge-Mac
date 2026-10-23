# THE FORGE  |  Copyright (c) 2026 Yannie D. Forest. All rights reserved.
# NO LICENCE IS GRANTED. No copying, adaptation, redistribution, reverse
# engineering or commercial use without the author's written permission.
# See LICENCE.txt. Every distributed copy carries a build marker.
# -*- mode: python ; coding: utf-8 -*-
#
# The Forge — standalone macOS app.
#
#   Built on GitHub by .github/workflows/build-mac-app.yml, or on a Mac by
#   "Build Mac App.command". You do not run this file yourself.
#
# Compatibility note, and the reason this file was rewritten on 28 July 2026:
# the previous version was the PyInstaller 5 template. PyInstaller 6.0 removed
# `cipher`, `Analysis(win_no_prefer_redirects=...)`,
# `Analysis(win_private_assemblies=...)`, the `a.zipped_data` argument to PYZ and
# the `a.zipfiles` argument to COLLECT. Since `pip install pyinstaller` installs
# version 6, the old spec raised the moment it was read, after PyInstaller had
# already created an empty `dist` folder. This version uses only arguments that
# exist in both 5 and 6.

import os
import re
import sys

from PyInstaller.utils.hooks import collect_all

# The build number shown by macOS (Finder, Get Info) is read from
# BUILD_INFO.txt, so the app's version always matches the build inside it.
try:
    _pass = re.search(r'^Pass:\s*(\d+)', open('BUILD_INFO.txt', encoding='utf-8').read(), re.M).group(1)
except Exception:
    _pass = '1'

# On GitHub the app is built for Intel and Apple silicon at once
# (CD_TARGET_ARCH=universal2). Built on your own Mac it matches that Mac.
_target_arch = os.environ.get('CD_TARGET_ARCH') or None

extra_datas = []
extra_binaries = []
extra_hidden = []

# pywebview loads its own JavaScript from disk while a window opens, so those
# files must travel inside the bundle. collect_all takes a package's modules,
# data and binaries together, and a package that is absent is simply skipped.
for _pkg in ('webview', 'proxy_tools', 'objc', 'Foundation', 'WebKit'):
    try:
        _d, _b, _h = collect_all(_pkg)
        extra_datas += _d
        extra_binaries += _b
        extra_hidden += _h
    except Exception as _e:
        print('the_forge: nothing collected for %s (%s)' % (_pkg, _e))

a = Analysis(
    ['the_forge_app.py'],
    pathex=[],
    binaries=extra_binaries,
    # the app itself travels inside the bundle
    # 644: the apps the Forge carries, in files beside the page (the Mac app opens the quick page)
    datas=extra_datas + ([('the_forge_parts', 'the_forge_parts')] if os.path.isdir('the_forge_parts') else []) + [('the_forge.html', '.'), ('the_forge.icns', '.'), ('the_forge.png', '.')],
    # Named outright because PyInstaller cannot see them: pywebview chooses its
    # backend while running, so nothing in the source imports these by name.
    # Left out, the app builds cleanly and then cannot draw a window. Any that
    # are not installed are merely reported, which does not stop the build.
    hiddenimports=[
        'webview.platforms.cocoa',
        'objc',
        'Foundation',
        'AppKit',
        'WebKit',
    ] + extra_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='The Forge',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=_target_arch,
    codesign_identity=None,
    entitlements_file=None,
    icon='the_forge.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='The Forge',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='The Forge.app',
        icon='the_forge.icns',
        bundle_identifier='com.yannieforest.theforge',
        info_plist={
            'CFBundleName': 'The Forge',
            'CFBundleDisplayName': 'The Forge',
            'CFBundleShortVersionString': _pass,
            'CFBundleVersion': _pass,
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '11.0',

            # REQUIRED, not optional. macOS terminates an app the instant it
            # asks for the microphone without a reason string present, and it
            # dies with no message a person could read. Scriba's dictation asks
            # for exactly that, so without these two lines the app would appear
            # to crash the first time dictation was used.
            'NSMicrophoneUsageDescription':
                'The Forge uses the microphone only while you ask it to '
                'listen, for dictation or a recording. Nothing is sent anywhere '
                'by the app itself.',
            'NSSpeechRecognitionUsageDescription':
                'Dictation turns your speech into text inside The Forge.',
        },
    )
