"""Builds the whole site (English + Indonesian) from content/*.json into public/.
Run: python3 scripts/build.py   (images are processed first by: node scripts/images.mjs)"""
import os, shutil, sys, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content as K

GENERATED_DIRS = ['about', 'services', 'how-it-works', 'products', 'portfolio', 'insights', 'contact', 'privacy-policy', 'terms', 'id']
GENERATED_FILES = ['index.html', '404.html', 'sitemap.xml', 'robots.txt', '_headers']

for d in GENERATED_DIRS:
    shutil.rmtree(K.OUT / d, ignore_errors=True)
for f in GENERATED_FILES:
    try: (K.OUT / f).unlink()
    except FileNotFoundError: pass

runpy.run_path(os.path.join(HERE, 'build_en.py'), run_name='build_en')
runpy.run_path(os.path.join(HERE, 'build_id.py'), run_name='build_id')

# Settings for the browser (WhatsApp number, analytics IDs, demo tape) come from content/settings.json
import json
cfg = dict(whatsapp=K.WA, gaId=K.SETTINGS['analytics'].get('ga_id', ''), clarityId=K.SETTINGS['analytics'].get('clarity_id', ''),
           demoMode=bool(K.DEMO), demoTapeText=K.SETTINGS['demo'].get('tape_text', ''))
os.makedirs(K.OUT / 'assets/js', exist_ok=True)
(K.OUT / 'assets/js/config.js').write_text('/* Generated from content/settings.json. Do not edit by hand. */\nwindow.SITE_CONFIG = ' + json.dumps(cfg, ensure_ascii=False) + ';\n', encoding='utf-8')
print('done')
