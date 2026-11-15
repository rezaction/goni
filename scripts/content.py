"""Loads the content files (content/*.json) that the dashboard edits and exposes them
in the shapes the page generators use. Everything editable lives in content/."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'content'
OUT = ROOT / 'public'

def _read(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def _folder(name):
    items = [_read(p) for p in sorted((CONTENT / name).glob('*.json'))]
    return items

SETTINGS = _read(CONTENT / 'settings.json')
DOMAIN = SETTINGS['domain'].rstrip('/')
BRAND = SETTINGS.get('brand', 'GoNEST')
WA = re.sub(r'\D', '', SETTINGS['whatsapp'])
DEMO = SETTINGS.get('demo', {}).get('enabled', True)

PHOTO_SLOTS = _read(CONTENT / 'photos.json')['slots']
PHOTO_LABEL_ID = {s['key']: s.get('label_id') or s['key'] for s in PHOTO_SLOTS}

def slugify(s):
    return ''.join(ch if ch.isalnum() else '-' for ch in s.lower()).strip('-').replace('--', '-')

def _cat(c, lang, extra):
    b = dict(c[lang])
    b['specs'] = [(s['label'], s['value']) for s in b['specs']]
    b['faqs'] = [(f['q'], f['a']) for f in b['faqs']]
    b['photo'] = c['photo']
    b.update(extra)
    return b

_cats = sorted(_folder('categories'), key=lambda c: (c.get('order', 99), c['slug_en']))
CATS_EN = [_cat(c, 'en', dict(slug=c['slug_en'])) for c in _cats]
CATS_ID = [_cat(c, 'id', dict(slug=c['slug_id'], en_slug=c['slug_en'], en=c['en']['name'])) for c in _cats]
_name_en = {c['slug_en']: c['en']['name'] for c in _cats}
_name_id = {c['slug_en']: c['id']['name'] for c in _cats}

_prods = sorted(_folder('products'), key=lambda p: (p.get('order', 99), p['en']['name']))
def _row(p, lang, names):
    b = p[lang]
    return (names[p['category']], b['name'], b['format'], b['moq'], b['price'], b['lead_time'])
ROWS_EN = [_row(p, 'en', _name_en) for p in _prods]
ROWS_ID = [_row(p, 'id', _name_id) for p in _prods]

_projs = sorted(_folder('projects'), key=lambda p: (p.get('date', ''), p['slug']), reverse=True)
PROJECTS_EN = [dict(p['en'], slug=p['slug'], cat=_name_en[p['category']], photo=p['photo']) for p in _projs]
PROJECTS_ID = [dict(p['id'], slug=p['slug'], cat=_name_id[p['category']], cat_en=_name_en[p['category']], photo=p['photo']) for p in _projs]

_arts = sorted(_folder('articles'), key=lambda a: (-int(a.get('date', '0').replace('-', '') or 0), a.get('order', 99)))
def _art(a, lang, slug):
    b = a[lang]
    return dict(slug=slug, cat=b['category'], read=b['read'], title=b['title'], desc=b['description'], date=a.get('date', ''),
                related=[(r['path'], r['label']) for r in b.get('related', [])],
                body=[(s['heading'], s['paragraphs']) for s in b['sections']])
ARTICLES_EN = [_art(a, 'en', a['slug_en']) for a in _arts]
ARTICLES_ID = [_art(a, 'id', a['slug_id']) for a in _arts]
ARTICLE_SLUGS = {a['slug_en']: a['slug_id'] for a in _arts}

TESTIMONIALS = sorted(_folder('testimonials'), key=lambda t: t.get('order', 99))
STATS = SETTINGS['stats']

# ---------- photos ----------
PHOTO_W, PHOTO_H = 1600, 1067   # 3:2 master size written by images.mjs
def photo_slot(key, cls, label, alt, hint):
    """A photo slot. Shows the processed WebP when one exists, else a dashed placeholder."""
    from html import escape as e
    slug = slugify(key)
    base = f'/assets/img/photos/{slug}'
    if (OUT / 'assets/img/photos' / f'{slug}.webp').exists():
        return (f'<div class="ph has-img {cls}"><img src="{base}.webp" srcset="{base}-800.webp 800w, {base}.webp {PHOTO_W}w" '
                f'sizes="(max-width: 800px) 100vw, 600px" width="{PHOTO_W}" height="{PHOTO_H}" alt="{e(alt)}" loading="lazy" decoding="async" '
                f'onerror="this.remove()"></div>')
    return f'<div class="ph {cls}"><span>{e(label)}<br>{e(hint)}</span></div>'
