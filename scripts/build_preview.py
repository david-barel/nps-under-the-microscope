"""Build an offline, single-file interactive preview from the Quarto source.

Run from the repository root: python scripts/build_preview.py
The lesson markup is taken from index.qmd so editorial changes have one source of truth.
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = (root / 'index.qmd').read_text(encoding='utf-8')
match = re.search(r'```\{=html\}\n(.*?)\n```', source, re.S)
if not match or 'id="nps-lessons"' not in match.group(1):
    raise RuntimeError('Could not find HTML lesson block in index.qmd')
markup = match.group(1)
css = (root / 'assets/lessons.css').read_text(encoding='utf-8')
model_js = (root / 'assets/model_results.js').read_text(encoding='utf-8')
lessons_js = (root / 'assets/lessons.js').read_text(encoding='utf-8')
# Standard inline scripts don't embed tag terminators in the present sources.
for name, js in [('model', model_js), ('lessons', lessons_js)]:
    if '</script' in js.lower():
        raise RuntimeError(f'Unsafe closing script tag in {name} JavaScript')
html = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="An interactive R and Quarto research case study on measuring and interpreting Net Promoter Score.">
<title>NPS Under the Microscope — Five interactive lessons</title>
<style>body{{background:#f5f8fa;margin:0}}{css}</style>
</head><body>{markup}
<script>{model_js}</script>
<script>{lessons_js}</script>
</body></html>'''
(root / 'preview.html').write_text(html, encoding='utf-8')
(root / 'assets/playground.html').write_text(html, encoding='utf-8')
print(f'Updated preview.html and assets/playground.html ({len(html):,} characters each)')
