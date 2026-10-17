"""Patch helpers for the Forge's single file. Every anchor must match exactly once, or the build stops.
   Usage: a build script imports this, reads the base, applies named patches in order, writes the output."""
import re, sys

class Patcher:
    def __init__(self, text):
        self.t = text
        self.log = []
    def count(self, s):
        return self.t.count(s)
    def must_once(self, s, what=''):
        n = self.t.count(s)
        if n != 1:
            raise SystemExit('PATCH FAILED (%s): anchor found %d times, expected 1:\n  %r' % (what, n, s[:160]))
    def replace_once(self, old, new, what=''):
        self.must_once(old, what)
        self.t = self.t.replace(old, new, 1)
        self.log.append('replace: ' + (what or old[:60]))
    def replace_all(self, old, new, what='', expect=None):
        n = self.t.count(old)
        if n == 0 or (expect is not None and n != expect):
            raise SystemExit('PATCH FAILED (%s): anchor found %d times, expected %s' % (what, n, expect))
        self.t = self.t.replace(old, new)
        self.log.append('replace all x%d: %s' % (n, what or old[:60]))
    def insert_before(self, anchor, text, what=''):
        self.must_once(anchor, what)
        i = self.t.index(anchor)
        self.t = self.t[:i] + text + self.t[i:]
        self.log.append('insert before: ' + (what or anchor[:60]))
    def insert_after(self, anchor, text, what=''):
        self.must_once(anchor, what)
        i = self.t.index(anchor) + len(anchor)
        self.t = self.t[:i] + text + self.t[i:]
        self.log.append('insert after: ' + (what or anchor[:60]))
    def insert_before_last(self, anchor, text, what=''):
        i = self.t.rindex(anchor)
        self.t = self.t[:i] + text + self.t[i:]
        self.log.append('insert before last: ' + (what or anchor[:60]))

def js_string(s):
    """a JS double-quoted string literal of s, safe inside a <script> (no </script> can appear)"""
    import json
    return json.dumps(s, ensure_ascii=False).replace('</', '<\\/')
