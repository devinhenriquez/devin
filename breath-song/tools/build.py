"""Builds ../index.html from src/app.html.
The page no longer embeds any audio (the flute is synthesized in the browser), so this is a straight copy,
kept so the edit -> build -> publish routine stays the same.
Run from anywhere:  python3 tools/build.py
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'src', 'app.html')).read()
open(os.path.join(ROOT, 'index.html'), 'w').write(src)
print(f'Wrote index.html ({len(src) // 1024} KB)')
