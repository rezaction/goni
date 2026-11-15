import json, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathmap import PATHMAP
import content as K
from urllib.parse import quote

ROOT_DIR = str(K.ROOT)
OUT = str(K.OUT)
DOMAIN = K.DOMAIN
WA = K.WA
BRAND = K.BRAND

CATS = K.CATS_EN

ROWS = K.ROWS_EN

STEPS = [
    ('1', 'Consultation', 'We review your concept, target market and budget.', 'Week 1'),
    ('2', 'Development', 'Formula draft and ingredient selection.', 'Week 1 to 2'),
    ('3', 'Sampling', 'You taste, we adjust, you approve.', 'Week 2 to 4'),
    ('4', 'Production', 'Full batch run on the approved formula.', 'Week 4 to 6'),
    ('5', 'Quality control', 'Lab checks and release of the batch.', 'Week 6'),
    ('6', 'Delivery', 'Packed, palletized and shipped to you.', 'Week 6 to 8'),
]

E = html.escape

def wa_link(msg):
    return 'https://wa.me/%s?text=%s' % (WA, quote(msg))

NAV = [('Home', '/'), ('About', '/about/'), ('Services', '/services/'), ('Products', '/products/'), ('Portfolio', '/portfolio/'), ('Insights', '/insights/'), ('Contact', '/contact/')]

PROJECTS = K.PROJECTS_EN
CAT_SLUG = {c['name']: c['slug'] for c in CATS}

ARTICLES = K.ARTICLES_EN

def article_cards(items=None, limit=None):
    items = (items or ARTICLES)[:limit] if limit else (items or ARTICLES)
    return ''.join(f'''<a class="card plain" href="/insights/{a["slug"]}/" style="text-decoration:none">
<div class="eyebrow">{E(a["cat"])}</div><h3>{E(a["title"])}</h3><p>{E(a["desc"])}</p><span class="note">{E(a["read"])}</span>
</a>
''' for a in items)

def alt_links(path):
    idp = PATHMAP.get(path)
    if not idp: return ''
    return (f'<link rel="alternate" hreflang="en" href="{DOMAIN}{path}">\n'
            f'<link rel="alternate" hreflang="id" href="{DOMAIN}{idp}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{path}">\n')

def lang_switch(path):
    idp = PATHMAP.get(path)
    if not idp: return ''
    return (f'<div class="lang-switch" role="group" aria-label="Language">'
            f'<a href="{path}" hreflang="en" lang="en" aria-current="true">EN</a>'
            f'<a href="{idp}" hreflang="id" lang="id">ID</a></div>\n')

CURRENT = ['']

def head(title, desc, path, extra=''):
    CURRENT[0] = path
    full = title if title.startswith('GoNEST') else title + ' | GoNEST'
    url = DOMAIN + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
{alt_links(path)}<meta property="og:type" content="website">
<meta property="og:title" content="{E(full)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="GoNEST">
<meta name="theme-color" content="#123B67">
<link rel="icon" href="/assets/img/favicon.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Source+Sans+3:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def header(path):
    links = ''
    for label, href in NAV:
        cur = ' aria-current="page"' if (href == path or (href != '/' and path.startswith(href))) else ''
        links += f'<a href="{href}"{cur}>{label}</a>\n'
    return f'''<header class="site-header">
<div class="container">
<a class="brand" href="/"><img src="/assets/img/logo.png" alt="" width="36" height="36">GoNEST</a>
<button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" type="button">Menu</button>
<nav class="nav" id="site-nav" aria-label="Main">
{links}</nav>
{lang_switch(CURRENT[0])}<a class="btn btn-primary" href="/contact/">Let's Talk</a>
</div>
</header>
<main id="main">
'''

def footer():
    cat_links = ''.join(f'<a href="/products/{c["slug"]}/">{E(c["name"])}</a>' for c in CATS)
    return f'''</main>
<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div><div class="footer-brand">GoNEST</div><p style="font-size:15px;max-width:320px">Food and beverage product development and contract manufacturing.</p></div>
<div><strong>Services</strong><a href="/services/product-development/">Product Development</a><a href="/services/contract-manufacturing/">Contract Manufacturing</a><a href="/services/private-label/">Private Label</a><a href="/services/oem-odm/">OEM and ODM</a><a href="/services/packaging/">Packaging Solutions</a></div>
<div><strong>Products</strong>{cat_links}</div>
<div><strong>Company</strong><a href="/about/">About</a><a href="/about/facilities/">Facilities</a><a href="/about/quality-assurance/">Quality Assurance</a><a href="/about/certifications/">Certifications</a><a href="/how-it-works/">How It Works</a><a href="/portfolio/">Portfolio</a><a href="/insights/">Insights</a><a href="/contact/">Contact</a></div>
</div>
<div class="footer-bottom"><span>&copy; <span id="year">2026</span> GoNEST. All rights reserved.</span><span><a href="/privacy-policy/" style="display:inline">Privacy Policy</a> &nbsp;|&nbsp; <a href="/terms/" style="display:inline">Terms and Conditions</a> <a href="#" data-consent-reset hidden style="display:inline">&nbsp;|&nbsp; Cookie settings</a></span></div>
</div>
</footer>
<a class="wa-float" data-wa="Hello GoNEST, I would like to discuss a product project." href="#">WhatsApp</a>
<script src="/assets/js/config.js"></script>
<script src="/assets/js/main.js"></script>
</body>
</html>
'''

PHOTOS = {}
def slugify(s):
    return ''.join(ch if ch.isalnum() else '-' for ch in s.lower()).strip('-').replace('--', '-')
def ph(label, cls=''):
    slug = slugify(label)
    PHOTOS.setdefault(slug, label)
    return K.photo_slot(label, cls, 'PHOTO: ' + label, label.capitalize(), 'Upload in the dashboard: Photos')

def section_head(eyebrow, title, sub=''):
    p = f'<p>{sub}</p>' if sub else ''
    return f'<div class="section-head"><div class="eyebrow">{E(eyebrow)}</div><h2>{title}</h2>{p}</div>'

def stats_html():
    return '\n'.join(f'<div class="stat"><b>{E(x["en_value"])}</b><span>{E(x["en_label"])}</span></div>' for x in K.STATS)

def testimonials_html():
    return '\n'.join(f'<div class="card plain"><p style="font-size:19px">{E(t["en"]["quote"])}</p><div><b style="color:var(--primary)">{E(t["en"]["name"])}</b><br><span class="note">{E(t["en"]["role"])}</span></div></div>' for t in K.TESTIMONIALS)

def cat_cards():
    out = ''
    for c in CATS:
        out += f'''<div class="card">
{ph(c["photo"])}
<h3>{E(c["name"])}</h3>
<p>{E(c["desc"])}</p>
<div class="meta"><span>Min. order: <b>{c["moq"]}</b></span><span>Formats: <b>{c["formats"]}</b></span></div>
<a class="link-arrow" href="/products/{c["slug"]}/">View {E(c["name"])} &rarr;</a>
</div>
'''
    return out

def project_cards(items=None):
    out = ''
    for p in (items or PROJECTS):
        out += f'''<a class="card plain" href="/portfolio/{p["slug"]}/" style="text-decoration:none">
{ph(p["photo"])}
<div class="eyebrow">{E(p["cat"])}</div>
<h3>{E(p["name"])}</h3>
<p>{E(p["note"])}</p>
<span class="link-arrow">View project &rarr;</span>
</a>
'''
    return out

def price_table(extra_note=True):
    rows = ''.join('<tr>' + ''.join(f'<td>{E(x)}</td>' for x in r) + '</tr>' for r in ROWS)
    note = '<p class="note" style="margin-top:12px">Prices exclude VAT and shipping.</p>' if extra_note else ''
    return f'''<div class="table-wrap"><table>
<thead><tr><th>Category</th><th>Example product</th><th>Format</th><th>Min. order</th><th>Indicative price</th><th>Lead time</th></tr></thead>
<tbody>{rows}</tbody></table></div>{note}'''

def steps_html():
    return '<div class="steps">' + ''.join(f'<div class="step"><small>Step {n}</small><h3>{t}</h3><p>{d}</p><em>{w}</em></div>' for n, t, d, w in STEPS) + '</div>'

def cta_band(title='Let\'s Develop Your Next Product', cat=None):
    qs = f'?category={quote(cat)}' if cat else ''
    return f'''<section class="section mid">
<div class="container stack" style="align-items:flex-start">
<h2>{E(title)}</h2>
<p class="lead" style="font-size:19px;color:#E1EAF5;max-width:640px">Have a product idea, or looking for a manufacturing partner? Tell us what you need and our team will reply within one business day.</p>
<a class="btn btn-accent" href="/contact/{qs}">Start Your Consultation</a>
</div>
</section>
'''

def write(path, content):
    full = os.path.join(OUT, path.strip('/'), 'index.html') if path != '/' else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)

pages = ['/']

# ---------------- Home ----------------
org = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "GoNEST", "url": DOMAIN,
                  "description": "Food and beverage product development and contract manufacturing partner."}, ensure_ascii=False)
home = head('GoNEST | Food & Beverage Contract Manufacturing Partner',
            'Product development and contract manufacturing for powdered beverages, coffee, seasoning and herbal products under your own brand.',
            '/', f'<script type="application/ld+json">{org}</script>\n') + header('/') + f'''
<section class="hero">
<div class="container hero-grid">
<div class="stack" style="gap:24px">
<div class="eyebrow">Food &amp; Beverage Contract Manufacturing</div>
<h1>Building Better Products. Manufacturing Your Brand's Vision.</h1>
<p class="lead">GoNEST is your partner for food and beverage product development and contract manufacturing. We take your idea from formula to a finished product that is ready for the shelf.</p>
<div class="hero-actions"><a class="btn btn-accent" href="/contact/">Discuss Your Project</a><a class="btn btn-ghost" href="/products/">Explore Capabilities</a></div>
<div class="hero-tags"><span>Powdered Beverage</span><span>Coffee</span><span>Seasoning &amp; Spices</span><span>Herbal</span></div>
</div>
<div class="brief">
<div class="brief-head"><strong>Sample project brief</strong><span class="chip">Example</span></div>
<dl>
<div><dt>Product</dt><dd>Matcha Latte Premix</dd></div>
<div><dt>Category</dt><dd>Powdered Beverage</dd></div>
<div><dt>Format</dt><dd>Sachet, 25 g net</dd></div>
<div><dt>First batch</dt><dd>1,000 kg</dd></div>
<div><dt>Sample ready</dt><dd>7 to 10 working days</dd></div>
<div><dt>Indicative price</dt><dd>from Rp 2.900 / sachet</dd></div>
</dl>
<a class="btn btn-primary" href="/contact/?category=Powdered%20Beverage">Request a similar quote</a>
</div>
</div>
</section>

<section class="stats"><div class="container grid-4">
{stats_html()}
</div></section>

<section class="section">
<div class="container split">
<div class="stack">
<div class="eyebrow">Company introduction</div>
<h2>More Than a Manufacturer. Your Product Development Partner.</h2>
<p>Most contract manufacturers sell capacity. GoNEST also brings formulation, sampling, quality control and packaging support, so you can launch a product with your own brand without building a factory.</p>
<p>We work with entrepreneurs starting their first brand, owners extending a product line, and distributors who need a reliable production partner.</p>
<a class="link-arrow" href="/about/">About GoNEST &rarr;</a>
</div>
{ph('production floor', 'tall')}
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Manufacturing capabilities', 'Our Manufacturing Expertise', 'Four product categories, each with its own page covering formulas, packaging options, minimum order and sampling.')}
<div class="grid-4">{cat_cards()}</div>
</div>
</section>

<section class="section dark">
<div class="container">
{section_head('Why GoNEST', 'The Right Partner for Your Next Product')}
<div class="grid-4">
<div class="card"><h3>Product development</h3><p>Formulation, flavor tuning and sample rounds handled by our R&amp;D team.</p></div>
<div class="card"><h3>Manufacturing</h3><p>Blending, filling and sealing lines sized for startups and growing brands.</p></div>
<div class="card"><h3>Quality control</h3><p>Batch checks against your approved spec, with records kept for every run.</p></div>
<div class="card"><h3>Packaging solutions</h3><p>Help choosing pouch, sachet or jar, plus label and artwork guidance.</p></div>
</div>
</div>
</section>

<section class="section">
<div class="container">
{section_head('Manufacturing process', 'From Your Idea to a Finished Product', 'Six stages, the same order on every project. Typical time from first consultation to delivery is 5 to 8 weeks.')}
{steps_html()}
<p style="margin-top:24px"><a class="link-arrow" href="/how-it-works/">See the full process &rarr;</a></p>
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Minimum order and indicative pricing', 'Know the Numbers Before You Call', 'Clear starting points help serious buyers decide faster. Final price depends on formula, ingredients, packaging and volume.')}
{price_table()}
</div>
</section>

<section class="section">
<div class="container split">
{ph('QC laboratory', 'tall')}
<div class="stack">
<div class="eyebrow">Facilities and quality assurance</div>
<h2>Quality Starts Behind the Scenes</h2>
<p>Every batch is checked against your approved specification: moisture, particle size, taste, net weight and packaging seal before it leaves the plant.</p>
<div class="badges"><span class="badge">BPOM</span><span class="badge">Halal</span><span class="badge">HACCP</span><span class="badge">ISO 22000</span></div>
<p class="note">Placeholder badges. Show only certificates the company actually holds, with valid dates.</p>
</div>
</div>
</section>

<section class="section">
<div class="container">
{section_head('Selected product portfolio', 'Products We Have Brought to Market')}
<div class="grid-4">{project_cards()}</div>
<p style="margin-top:24px"><a class="link-arrow" href="/portfolio/">View all projects &rarr;</a></p>
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Our business partners', 'Building Successful Products Together')}
<div class="grid-2">
{testimonials_html()}
</div>
</div>
</section>
<section class="section">
<div class="container">
{section_head('Insights and knowledge', 'Knowledge for Better Products', 'Guides on contract manufacturing, product development and packaging.')}
<div class="grid-3">{article_cards(limit=3)}</div>
<p style="margin-top:24px"><a class="link-arrow" href="/insights/">All articles &rarr;</a></p>
</div>
</section>
''' + cta_band() + footer()
write('/', home)

# ---------------- About ----------------
about = head('About GoNEST', 'GoNEST is a food and beverage product development and contract manufacturing partner for brand owners, entrepreneurs and distributors.', '/about/') + header('/about/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/">Home</a> / About</div>
<h1>About GoNEST</h1>
<p class="lead">A product development and manufacturing partner for food and beverage brands.</p>
</div></section>

<section class="section"><div class="container split">
<div class="stack">
<div class="eyebrow">Company overview</div>
<h2>Who We Are</h2>
<p>GoNEST develops and manufactures powdered beverages, coffee, seasoning and herbal products for other brands. We combine a production floor with an R&amp;D desk, so a client can bring an idea and leave with a product.</p>
<p>[Replace with the real company history: founding year, location, growth, key milestones.]</p>
</div>
{ph('company building', 'tall')}
</div></section>

<section class="section white"><div class="container">
{section_head('Vision and mission', 'What Guides Our Work')}
<div class="grid-2">
<div class="card"><h3>Vision</h3><p>To be the most trusted food and beverage manufacturing partner for growing Indonesian brands.</p></div>
<div class="card"><h3>Mission</h3><ul class="list"><li>Develop products that match each client's brief.</li><li>Produce with consistent quality, batch after batch.</li><li>Be clear about minimums, timelines and costs.</li></ul></div>
</div>
</div></section>

<section class="section"><div class="container">
{section_head('Our expertise', 'Where We Are Strong')}
<div class="grid-4">
<div class="card plain"><h3>Formulation</h3><p>Taste and texture development with repeatable sample rounds.</p></div>
<div class="card plain"><h3>Blending and filling</h3><p>Dry blending and sachet, pouch and jar filling lines.</p></div>
<div class="card plain"><h3>Quality control</h3><p>Incoming inspection, in-process checks and batch release.</p></div>
<div class="card plain"><h3>Packaging support</h3><p>Material, size and label guidance before you print.</p></div>
</div>
</div></section>

<section class="section white"><div class="container split">
{ph('QC laboratory', 'tall')}
<div class="stack">
<div class="eyebrow">Facilities and certifications</div>
<h2>Built to Be Audited</h2>
<p>Clients are welcome to visit the plant and review our process. Facility photos, machine list and certificates are listed below once confirmed by the company.</p>
<div class="badges"><span class="badge">BPOM</span><span class="badge">Halal</span><span class="badge">HACCP</span><span class="badge">ISO 22000</span></div>
<p class="note">Placeholder badges. Replace with real certificates and expiry dates.</p>
</div>
</div></section>

<section class="section"><div class="container">
{section_head('Our values', 'How We Work With Clients')}
<div class="grid-3">
<div class="card plain"><h3>Clarity</h3><p>You see the minimum order, price range and timeline at the start.</p></div>
<div class="card plain"><h3>Consistency</h3><p>The approved sample is the benchmark for every batch we release.</p></div>
<div class="card plain"><h3>Confidentiality</h3><p>Your formula and your brand belong to you.</p></div>
</div>
</div></section>
''' + cta_band() + footer()
write('/about/', about)

# ---------------- Services ----------------
svc = [
    ('product-development', 'Product Development', 'Concept, formula, ingredient selection and sample rounds until you approve the product.', ['Taste and texture targets', 'Ingredient and cost options', 'Up to three sample rounds included']),
    ('contract-manufacturing', 'Contract Manufacturing', 'Production to your specification and your approved formula.', ['Batch production in agreed volumes', 'Batch records and retained samples', 'Scheduled delivery']),
    ('private-label', 'Private Label Manufacturing', 'Ready formulas from our range, packed under your brand for a faster, lower-cost launch.', ['Choose from existing base formulas', 'Lower minimum order', 'Your label and your packaging']),
    ('oem-odm', 'OEM and ODM', 'OEM: we produce your formula. ODM: we develop the formula and you own the brand.', ['Clear ownership of the formula', 'Flexible cooperation models', 'Suitable for distributors and B2B buyers']),
    ('packaging', 'Packaging Solutions', 'Advice on sachet, pouch, jar and box formats, plus label requirements.', ['Material and size guidance', 'Filling and sealing in-house', 'Artwork checks before printing']),
]
svc_cards = ''.join(f'''<div class="card plain" id="{s}"><h3>{n}</h3><p>{d}</p><ul class="list">{"".join(f"<li>{E(i)}</li>" for i in items)}</ul><a class="link-arrow" href="/services/{s}/">Learn more &rarr;</a></div>
''' for s, n, d, items in svc)
cmp_rows = [('Who owns the formula', 'Client', 'GoNEST or shared', 'GoNEST'),
            ('Development work', 'Client supplies formula', 'GoNEST develops', 'Existing GoNEST formula'),
            ('Minimum order', 'Standard', 'Standard', 'Lower'),
            ('Time to launch', '5 to 8 weeks', '6 to 10 weeks', '3 to 5 weeks'),
            ('Best for', 'Brands with a recipe', 'New brands with an idea', 'Fast, low-risk starts')]
cmp_html = '<div class="table-wrap"><table><thead><tr><th></th><th>OEM</th><th>ODM</th><th>Private label</th></tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{E(x)}</td>' for x in r) + '</tr>' for r in cmp_rows) + '</tbody></table></div>'
faqs_svc = [('How do I start?', 'Send a short brief through the contact form or WhatsApp. We reply within one business day with questions and next steps.'),
            ('Is there a fee for samples?', 'Sample terms are agreed during consultation. (Sample answer: first sample round is included once a project is confirmed.)'),
            ('Can I visit the facility?', 'Yes, by appointment during business hours.')]
faq_ld = lambda fq: '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}, ensure_ascii=False) + '</script>\n'
faq_html = lambda fq: '<div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in fq) + '</div>'
services = head('Manufacturing Services', 'Product development, contract manufacturing, private label, OEM and ODM, and packaging support for food and beverage brands.', '/services/', faq_ld(faqs_svc)) + header('/services/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/">Home</a> / Services</div>
<h1>Manufacturing Services</h1>
<p class="lead">Everything between your idea and a finished product, in one place.</p>
</div></section>

<section class="section"><div class="container">
{section_head('What we do', 'Five Ways We Can Work Together', 'Each service applies to all four product categories: powdered beverage, coffee, seasoning and herbal.')}
<div class="grid-3">{svc_cards}</div>
</div></section>

<section class="section white"><div class="container">
{section_head('Choosing a model', 'OEM, ODM or Private Label?')}
{cmp_html}
</div></section>

<section class="section" id="process"><div class="container">
{section_head('How it works', 'From Consultation to Delivery', 'The same six stages on every project, so you always know what comes next.')}
{steps_html()}
<p style="margin-top:24px"><a class="link-arrow" href="/how-it-works/">Read the detailed process &rarr;</a></p>
</div></section>

<section class="section white"><div class="container">
{section_head('Minimum order and requirements', 'What to Prepare Before You Call')}
<div class="grid-2">
<div class="card"><h3>Helpful to bring</h3><ul class="list"><li>A reference product or taste description</li><li>Target price per unit</li><li>Expected first order and monthly volume</li><li>Preferred packaging format</li></ul></div>
<div class="card"><h3>Minimum order by category</h3><ul class="list"><li>Powdered Beverage: 1,000 kg</li><li>Coffee: 300 kg roasted, 1,000 kg instant</li><li>Seasoning and Spices: 500 kg</li><li>Herbal Products: 500 kg</li></ul></div>
</div>
</div></section>

<section class="section"><div class="container">
{section_head('Questions', 'Frequently Asked Questions')}
{faq_html(faqs_svc)}
</div></section>
''' + cta_band() + footer()
write('/services/', services)

# ---------------- Products index ----------------
products = head('Product Categories', 'Contract manufacturing for powdered beverages, coffee, seasoning and spices, and herbal products.', '/products/') + header('/products/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/">Home</a> / Products</div>
<h1>Product Categories</h1>
<p class="lead">Choose a category to see product types, formula options, packaging, minimum order and sampling.</p>
</div></section>

<section class="section"><div class="container"><div class="grid-4">{cat_cards()}</div></div></section>

<section class="section white"><div class="container">
{section_head('Minimum order and indicative pricing', 'Starting Points by Category')}
{price_table()}
</div></section>
''' + cta_band() + footer()
write('/products/', products)

# ---------------- Category pages ----------------
for c in CATS:
    path = f'/products/{c["slug"]}/'
    lst = lambda items: '<ul class="list">' + ''.join(f'<li>{E(i)}</li>' for i in items) + '</ul>'
    spec_rows = ''.join(f'<tr><td>{E(k)}</td><td>{E(v)}</td></tr>' for k, v in c['specs'])
    msg = f'Hello GoNEST, I would like to discuss {c["name"]} contract manufacturing.'
    page = head(c['hero'], c['lead'], path, faq_ld(c['faqs'])) + header('/products/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/">Home</a> / <a href="/products/">Products</a> / {E(c["name"])}</div>
<h1>{E(c["hero"])}</h1>
<p class="lead">{E(c["lead"])}</p>
<div class="hero-actions" style="margin-top:24px"><a class="btn btn-accent" href="/contact/?category={quote(c["name"])}">Request a Quote</a><a class="btn btn-ghost" data-wa="{E(msg)}" href="#">Chat on WhatsApp</a></div>
</div></section>

<section class="section"><div class="container split">
<div class="stack"><div class="eyebrow">Category overview</div><h2>{E(c["name"])} Made to Your Brief</h2><p>{E(c["intro"][0])}</p><p>{E(c["intro"][1])}</p></div>
{ph(c["photo"], "tall")}
</div></section>

<section class="section white"><div class="container">
{section_head('What we can make', 'Product Types, Formulas and Packaging')}
<div class="grid-3">
<div class="card"><h3>Product types</h3>{lst(c["types"])}</div>
<div class="card"><h3>Formula and ingredient options</h3>{lst(c["formula"])}</div>
<div class="card"><h3>Packaging options</h3>{lst(c["pack"])}</div>
</div>
</div></section>

<section class="section"><div class="container">
{section_head('Minimum order and specifications', 'Key Numbers for {name}'.format(name=E(c["name"])))}
<div class="table-wrap"><table style="min-width:520px"><thead><tr><th>Item</th><th>Detail</th></tr></thead><tbody>{spec_rows}</tbody></table></div>
</div></section>

<section class="section white"><div class="container">
{section_head('Sampling and production', 'How a {name} Project Runs'.format(name=E(c["name"])))}
{steps_html()}
</div></section>

<section class="section"><div class="container split">
<div class="stack"><div class="eyebrow">Manufacturing and quality control</div><h2>Checked Before It Ships</h2><p>Each batch is weighed by formula, checked in process and compared with your approved sample before release. Batch records are kept so any lot can be traced.</p></div>
{ph("quality inspection", "tall")}
</div></section>

<section class="section white"><div class="container">
{section_head('Questions', '{name} FAQ'.format(name=E(c["name"])))}
{faq_html(c["faqs"])}
</div></section>
''' + cta_band(f'Let\'s Develop Your {c["name"]} Product', c['name']) + footer()
    write(path, page)
    pages.append(path)

# ---------------- Contact ----------------
opts = ''.join(f'<option>{E(c["name"])}</option>' for c in CATS)
contact = head('Contact', 'Talk to GoNEST about your food or beverage product. Send a brief by form or WhatsApp and get a reply within one business day.', '/contact/') + header('/contact/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/">Home</a> / Contact</div>
<h1>Let's Discuss Your Product</h1>
<p class="lead">Tell us what you want to make. A short brief is enough to start.</p>
</div></section>

<section class="section mid"><div class="container cta-grid">
<div class="stack">
<h2>Start Your Consultation</h2>
<p class="lead">Our team replies within one business day with questions and next steps.</p>
<div class="contact-lines"><span>WhatsApp: {E(K.SETTINGS["whatsapp_display"])}</span><span>Email: {E(K.SETTINGS["email"])}</span><span>{E(K.SETTINGS["hours"]["en"])}</span><span>Address: {E(K.SETTINGS["address"]["en"])}</span></div>
</div>
<form class="consult" id="consult-form">
<div class="row">
<div class="field"><label for="f-name">Full name</label><input id="f-name" type="text" required placeholder="Your name"></div>
<div class="field"><label for="f-wa">WhatsApp number</label><input id="f-wa" type="tel" required placeholder="08xx xxxx xxxx"></div>
</div>
<div class="row">
<div class="field"><label for="f-cat">Product category</label><select id="f-cat">{opts}</select></div>
<div class="field"><label for="f-vol">Estimated first order</label><select id="f-vol"><option>Under 500 kg</option><option>500 to 1,000 kg</option><option>1,000 to 5,000 kg</option><option>Above 5,000 kg</option></select></div>
</div>
<div class="field"><label for="f-msg">Tell us about your product</label><textarea id="f-msg" rows="4" placeholder="Flavor, target market, packaging idea"></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-website">Leave this field empty</label><input id="f-website" type="text" tabindex="-1" autocomplete="off"></div>
<div class="form-actions"><button class="btn btn-accent" type="submit" id="send-form">Send Inquiry</button><button class="btn btn-outline" type="button" id="send-wa">Send via WhatsApp</button></div>
<div id="form-status" class="form-status" role="status" aria-live="polite" hidden></div>
<p class="form-note">We use your details only to reply to your inquiry. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
</form>
</div></section>

<section class="section"><div class="container">
{section_head('Questions', 'Before You Write')}
{faq_html([("How fast will you reply?", "Within one business day."), ("Do you have a minimum order?", "Yes. It depends on the category. See the Products pages for figures."), ("Can I visit the factory?", "Yes, by appointment.")])}
</div></section>
''' + footer()
write('/contact/', contact)

# ================= Stage 1: remaining Phase 2 pages =================
NEW_PATHS = []

def sec(inner_html, cls=''):
    return f'<section class="section {cls}"><div class="container">{inner_html}</div></section>\n'

def lst(items):
    return '<ul class="list">' + ''.join(f'<li>{E(i)}</li>' for i in items) + '</ul>'

def inner(path, title, desc, crumbs, h1, lead, body, ld='', nav=None, cta=None):
    parts = []
    for label, href in crumbs:
        parts.append(f'<a href="{href}">{E(label)}</a>' if href else E(label))
    hero = f'''
<section class="page-hero"><div class="container">
<div class="crumbs">{" / ".join(parts)}</div>
<h1>{E(h1)}</h1>
<p class="lead">{E(lead)}</p>
</div></section>
'''
    page = head(title, desc, path, ld) + header(nav or path) + hero + body + (cta if cta is not None else cta_band()) + footer()
    write(path, page)
    NEW_PATHS.append(path)

def table(headers, rows, minw=520):
    th = ''.join(f'<th>{E(h)}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{E(x)}</td>' for x in r) + '</tr>' for r in rows)
    return f'<div class="table-wrap"><table style="min-width:{minw}px"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

# ---------- How It Works ----------
STAGES = [
    ('Initial Consultation', 'Week 1', ['Review your concept, target market and budget', 'Explain minimum order, timeline and cost range'], ['Share a short brief and a reference product if you have one', 'Tell us your target price and first order size'], 'Project brief and rough quote'),
    ('Product Development', 'Week 1 to 2', ['Draft the formula and choose ingredients', 'Estimate cost per unit'], ['Confirm taste direction and budget'], 'Formula proposal'),
    ('Sampling and Approval', 'Week 2 to 4', ['Make the sample and adjust it after each round', 'Record the approved formula'], ['Taste and give clear feedback', 'Approve the final sample in writing'], 'Approved sample, kept as the reference for production'),
    ('Production', 'Week 4 to 6', ['Buy ingredients and packaging', 'Schedule and run the batch to the approved formula'], ['Approve packaging artwork', 'Confirm order quantity and payment terms'], 'Finished batch, packed'),
    ('Quality Control', 'Week 6', ['Check moisture, weight, seal and taste against the reference', 'Release the batch and keep a retained sample'], ['Review the batch report if requested'], 'Batch release report'),
    ('Packaging and Delivery', 'Week 6 to 8', ['Pack in cartons, palletize and label', 'Arrange delivery or hand over for pickup'], ['Receive and inspect the goods'], 'Delivery note and batch documents'),
]
stage_cards = ''.join(f'''<div class="card plain"><div class="eyebrow">Step {i+1} &middot; {E(w)}</div><h3>{E(t)}</h3>
<div><b>What we do</b>{lst(we)}</div><div><b>What you do</b>{lst(you)}</div>
<div class="meta"><span>You receive: <b>{E(out)}</b></span></div></div>
''' for i, (t, w, we, you, out) in enumerate(STAGES) for _ in [0] for we, you, out in [(we, you, out)])
faqs_how = [('How long does a project take?', 'The typical timeline is 5 to 8 weeks from the first consultation to delivery. Simple private-label products can be faster.'),
            ('How many sample rounds are included?', 'Sample terms are set during consultation. A typical project needs two to four rounds.'),
            ('Can I change the formula after approval?', 'Small changes are possible before production starts. A change after the first batch is treated as a new development round.'),
            ('Who owns the formula?', 'It depends on the cooperation model. See OEM, ODM and Private Label on the Services page.'),
            ('What if I am not sure about packaging?', 'Tell us the product and the market. We suggest formats and sizes, then you choose.')]
moq_tbl = table(['Category', 'Minimum order', 'About how many units'], [
    ('Powdered Beverage', '1,000 kg per formula', 'about 40,000 sachets of 25 g'),
    ('Coffee', '300 kg roasted; 1,000 kg instant', 'about 1,500 pouches of 200 g'),
    ('Seasoning and Spices', '500 kg per formula', 'about 5,000 pouches of 100 g'),
    ('Herbal Products', '500 kg per formula', 'about 25,000 sachets of 20 g')])
inner('/how-it-works/', 'How It Works', 'The six stages of working with GoNEST, from first consultation to delivery, with minimum order and project requirements.',
      [('Home', '/'), ('How It Works', None)], 'How It Works', 'Six stages, the same order on every project.',
      sec(section_head('Process overview', 'From First Message to Finished Product', 'Each stage has a clear output, so you always know what has been agreed and what comes next.') + steps_html())
      + sec(section_head('The stages in detail', 'What Happens at Each Step') + f'<div class="grid-2">{stage_cards}</div>', 'white')
      + sec(section_head('Minimum order and requirements', 'What to Prepare') + moq_tbl
            + '<div class="grid-2" style="margin-top:20px"><div class="card plain"><h3>Helpful to bring</h3>' + lst(['A reference product or a taste description', 'Target price per unit', 'Expected first order and monthly volume', 'Preferred packaging format']) + '</div>'
            + '<div class="card plain"><h3>Good to know</h3>' + lst(['Several flavors on one base can share a production run', 'Packaging artwork is usually the longest wait, so start it early', 'Product registration is the brand owner\'s responsibility']) + '</div></div>')
      + sec(section_head('Questions', 'Frequently Asked Questions') + faq_html(faqs_how), 'white'),
      faq_ld(faqs_how))

# ---------- About sub-pages ----------
inner('/about/company-profile/', 'Company Profile', 'Company profile of GoNEST: business focus, product categories, services and production capacity.',
      [('Home', '/'), ('About', '/about/'), ('Company Profile', None)], 'Company Profile', 'The facts about GoNEST in one place.',
      sec(section_head('At a glance', 'GoNEST in Brief', 'Items in square brackets are placeholders to fill with real company data.')
          + table(['Item', 'Detail'], [
              ('Company name', '[Legal company name]'), ('Brand', 'GoNEST'), ('Established', '[Year]'), ('Location', '[City, province]'),
              ('Business focus', 'Food and beverage product development and contract manufacturing'),
              ('Product categories', 'Powdered beverage, coffee, seasoning and spices, herbal products'),
              ('Services', 'Product development, contract manufacturing, private label, OEM and ODM, packaging support'),
              ('Blending capacity', '4 tons per day'), ('Team', '[Number] people'), ('Markets', 'Indonesia [confirm export markets]')], 520))
      + sec(section_head('Milestones', 'How the Company Grew', 'Replace with the real history.')
            + table(['Year', 'Milestone'], [('[Year]', 'Company founded'), ('[Year]', 'First powdered beverage line installed'), ('[Year]', 'Coffee roasting added'), ('[Year]', 'Quality laboratory opened')], 480), 'white'))

fac_areas = [('Receiving and storage', 'Ingredients are checked, labeled and stored by type.'), ('Dry blending room', 'Powder is blended by weight to the approved formula.'),
             ('Filling and sealing line', 'Sachet and pouch lines fill to a set net weight.'), ('Packing area', 'Finished goods are cartoned and labeled by batch.'),
             ('QC laboratory', 'Moisture, weight and sensory checks happen here.'), ('Finished goods warehouse', 'Batches wait for release and pickup.')]
fac_cards = ''.join(f'<div class="card plain">{ph(n.lower())}<h3>{E(n)}</h3><p>{E(d)}</p></div>' for n, d in fac_areas)
mach = table(['Equipment', 'Function', 'Capacity'], [
    ('Ribbon blender', 'Dry blending of powders', '500 kg per batch'), ('Sachet filling machine', 'Fills and seals sachets', '[Units per minute]'),
    ('Pouch filling machine', 'Fills and seals stand-up pouches', '[Units per minute]'), ('Coffee roaster', 'Roasting green beans', '30 kg per batch'),
    ('Grinder / pulverizer', 'Grinding spices and coffee', '[kg per hour]'), ('Metal detector', 'Checks finished goods', 'Inline'),
    ('Moisture analyzer', 'Moisture testing in the lab', 'Per batch')], 560)
inner('/about/facilities/', 'Our Facilities', 'Production areas, machines and laboratory at GoNEST for powdered beverages, coffee, seasoning and herbal products.',
      [('Home', '/'), ('About', '/about/'), ('Facilities', None)], 'Our Facilities', 'Where your product is made.',
      sec(section_head('Production areas', 'A Walk Through the Plant', 'Photos are placeholders. Use real photos of the plant.') + f'<div class="grid-3">{fac_cards}</div>')
      + sec(section_head('Machines', 'Equipment List') + mach, 'white'))

inner('/about/quality-assurance/', 'Quality Assurance', 'How GoNEST checks ingredients, production and finished goods, and how batches are traced.',
      [('Home', '/'), ('About', '/about/'), ('Quality Assurance', None)], 'Quality Assurance', 'Every batch is compared with the sample you approved.',
      sec(section_head('Three checkpoints', 'How We Control Quality')
          + '<div class="grid-3"><div class="card plain"><h3>Incoming ingredients</h3><p>Each delivery is checked for appearance, weight and documents before it enters storage.</p></div>'
          + '<div class="card plain"><h3>During production</h3><p>Blends are weighed by formula and checked at set intervals for weight and seal.</p></div>'
          + '<div class="card plain"><h3>Finished goods</h3><p>Samples are tested and tasted against the approved reference before release.</p></div></div>')
      + sec(section_head('Tests', 'What We Check')
            + table(['Test', 'When', 'Purpose'], [('Moisture content', 'Each batch', 'Keeps powder free-flowing and extends shelf life'), ('Net weight', 'During filling', 'Confirms every pack meets the label'),
                                                  ('Seal integrity', 'During filling', 'Prevents moisture and contamination'), ('Taste and aroma', 'Each batch', 'Matches the approved sample'),
                                                  ('Metal detection', 'Finished goods', 'Protects consumers'), ('Microbiological test', 'Per regulation, third-party lab', 'Confirms safety limits')], 560), 'white')
      + sec('<div class="split"><div class="stack"><div class="eyebrow">Traceability</div><h2>Every Batch Can Be Traced</h2><p>Each batch gets a lot code. Ingredient lots, production date and QC results are recorded and linked, and a retained sample is kept.</p><p>If a question comes up after delivery, we can trace it back to the ingredient lot.</p></div>' + ph('quality inspection', 'tall') + '</div>'))

certs_tbl = table(['Certification', 'Scope', 'Number', 'Valid until'], [
    ('BPOM', '[Scope]', '[Number]', '[Date]'), ('Halal', '[Scope]', '[Number]', '[Date]'), ('HACCP', '[Scope]', '[Number]', '[Date]'),
    ('ISO 22000', '[Scope]', '[Number]', '[Date]'), ('Business license (NIB)', '[Scope]', '[Number]', '[Date]')], 600)
inner('/about/certifications/', 'Certifications', 'Certifications and licenses held by GoNEST, with scope and validity.',
      [('Home', '/'), ('About', '/about/'), ('Certifications', None)], 'Certifications', 'Compliance you can verify.',
      sec(section_head('Licenses and certificates', 'What We Hold', 'Placeholder table. List only certificates the company holds today, with their real numbers and expiry dates, and add scans of the documents.') + certs_tbl
          + '<p class="note" style="margin-top:12px">Do not publish a certification until the document is in hand and valid.</p>'))
TaskNote = None

# ---------- Services sub-pages ----------
SERVICES = [
    dict(slug='product-development', name='Product Development', lead='Concept, formula, ingredient selection and sample rounds until you approve the product.',
         over='We turn a product idea into a working formula. You tell us the taste, texture, price level and target market, and we develop samples until the product matches your brief.',
         inc=['Formula development and ingredient selection', 'Cost per unit estimate', 'Sample rounds with written feedback', 'Approved sample kept as the production reference'],
         who=['New brands with an idea but no formula', 'Owners extending an existing product line', 'Distributors adding their own brand'],
         steps=[('Brief', 'You describe the product and share a reference.'), ('Draft', 'We propose a formula and cost.'), ('Samples', 'We make samples and adjust after your feedback.'), ('Approval', 'You approve one sample as the standard.')],
         photo='sample development',
         faqs=[('How many sample rounds do I get?', 'Sample terms are agreed in consultation. Two to four rounds is typical.'), ('Can you copy a competitor?', 'We match a taste and texture target, but we create our own formula and do not copy another brand.'), ('Do I own the formula I pay to develop?', 'This depends on the cooperation model. We agree it in writing before development starts.')]),
    dict(slug='contract-manufacturing', name='Contract Manufacturing', lead='Production to your specification and your approved formula.',
         over='You bring the formula, or approve one we developed, and we produce it in the volume you need with the same result every time.',
         inc=['Batch production to the approved formula', 'Batch records and retained samples', 'Quality checks before release', 'Scheduled delivery'],
         who=['Brands that already have a formula', 'Companies outsourcing part of their production', 'Brands scaling up from home or small-scale production'],
         steps=[('Order', 'Confirm quantity, packaging and delivery date.'), ('Prepare', 'We buy ingredients and packaging.'), ('Produce', 'We run the batch to formula.'), ('Release', 'QC checks, then delivery.')],
         photo='filling and sealing line',
         faqs=[('What is the minimum order?', 'It depends on the category. See Products for figures.'), ('Can you produce on a regular schedule?', 'Yes. Repeat orders can be planned monthly or quarterly.'), ('How do you keep batches consistent?', 'Batches are weighed by formula and compared with the approved reference sample.')]),
    dict(slug='private-label', name='Private Label Manufacturing', lead='Ready formulas from our range, packed under your brand for a faster, lower-cost launch.',
         over='Choose a base formula from our range, adjust the flavor or packaging, and launch under your own brand without paying for full development.',
         inc=['A choice of existing base formulas', 'Light flavor and packaging adjustments', 'Your label and your brand', 'Lower minimum order'],
         who=['First-time entrepreneurs testing a market', 'Shops and distributors adding a house brand', 'Brands that need to launch quickly'],
         steps=[('Choose', 'Pick a base formula and taste it.'), ('Adjust', 'Select flavor and pack size.'), ('Brand', 'Send your label artwork.'), ('Produce', 'We produce and deliver.')],
         photo='packaging options',
         faqs=[('Will other brands sell the same product?', 'A base formula may be shared. Flavor adjustments and packaging make your product distinct, and exclusivity can be discussed.'), ('Is the minimum lower?', 'Usually yes, because the formula is already developed.'), ('How fast can I launch?', 'The typical timeline is 3 to 5 weeks, mostly waiting for packaging.')]),
    dict(slug='oem-odm', name='OEM and ODM', lead='OEM: we produce your formula. ODM: we develop the formula and you own the brand.',
         over='OEM and ODM describe who creates the product. In OEM you supply the specification and we manufacture it. In ODM we design and develop the product, and you sell it under your brand.',
         inc=['OEM: production to your specification', 'ODM: development plus production', 'Written agreement on formula ownership', 'Confidentiality for your formula and brand'],
         who=['Distributors and B2B buyers', 'Companies with their own product specifications', 'Brands who want development and production from one partner'],
         steps=[('Choose model', 'OEM, ODM or private label.'), ('Agree terms', 'Ownership, volume and price.'), ('Develop or confirm', 'Formula approved by you.'), ('Produce', 'Batches delivered on schedule.')],
         photo='client meeting',
         faqs=[('What is the difference between OEM and ODM?', 'OEM produces your design. ODM designs and produces the product for you.'), ('Who owns the formula in ODM?', 'We agree it in writing. It can be exclusive to you or shared.'), ('Can I move to another factory later?', 'In OEM you own the specification, so yes. In ODM it depends on the agreement.')]),
    dict(slug='packaging', name='Packaging Solutions', lead='Advice on sachet, pouch, jar and box formats, plus label requirements.',
         over='Packaging affects shelf life, cost and shelf appeal. We help you choose the right material and size, and we fill and seal in-house.',
         inc=['Guidance on material and barrier level', 'Net weight and size recommendations', 'In-house filling and sealing', 'Label content checks before printing'],
         who=['Brands unsure which pack suits their product', 'Owners changing pack size or format', 'Brands preparing artwork for the first time'],
         steps=[('Review', 'We look at the product and market.'), ('Recommend', 'We suggest formats and materials.'), ('Artwork', 'Your designer prepares the label.'), ('Check', 'We check content and fit before printing.')],
         photo='packaging options',
         faqs=[('Do you supply packaging?', 'We can source packaging from our suppliers, or you can supply your own.'), ('What label information is required?', 'Requirements depend on the product and regulation. We list what must appear and you confirm with the regulator.'), ('What is the minimum print run?', 'It depends on the supplier. We share options during consultation.')]),
]
for s in SERVICES:
    path = f'/services/{s["slug"]}/'
    apply_cards = ''.join(f'<a class="card plain" href="/products/{c["slug"]}/" style="text-decoration:none"><h3>{E(c["name"])}</h3><p>{E(c["desc"])}</p><span class="link-arrow">See category &rarr;</span></a>' for c in CATS)
    body = (sec('<div class="split"><div class="stack"><div class="eyebrow">Overview</div><h2>' + E(s['name']) + '</h2><p>' + E(s['over']) + '</p></div>' + ph(s['photo'], 'tall') + '</div>')
            + sec(section_head('Scope', 'What Is Included and Who It Is For') + '<div class="grid-2"><div class="card"><h3>Included</h3>' + lst(s['inc']) + '</div><div class="card"><h3>Best for</h3>' + lst(s['who']) + '</div></div>', 'white')
            + sec(section_head('How it works', 'Four Steps') + '<div class="steps">' + ''.join(f'<div class="step"><small>Step {i+1}</small><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(s['steps'])) + '</div>'
                  + '<p style="margin-top:24px"><a class="link-arrow" href="/how-it-works/">See the full process &rarr;</a></p>')
            + sec(section_head('Applies to', 'Available for All Four Categories') + f'<div class="grid-4">{apply_cards}</div>', 'white')
            + sec(section_head('Questions', 'Frequently Asked Questions') + faq_html(s['faqs'])))
    inner(path, s['name'], s['lead'], [('Home', '/'), ('Services', '/services/'), (s['name'], None)], s['name'], s['lead'], body, faq_ld(s['faqs']), nav='/services/')

# ---------- Portfolio ----------
inner('/portfolio/', 'Portfolio', 'Selected products GoNEST has developed and manufactured for brand partners.',
      [('Home', '/'), ('Portfolio', None)], 'Portfolio', 'Products we have brought to market with our partners.',
      sec(section_head('Selected projects', 'Our Work')
          + f'<div class="grid-4">{project_cards()}</div>'))
for p in PROJECTS:
    path = f'/portfolio/{p["slug"]}/'
    slug = CAT_SLUG[p['cat']]
    body = (sec('<div class="split"><div class="stack"><div class="eyebrow">' + E(p['cat']) + '</div><h2>' + E(p['name']) + '</h2><p><b>Client need.</b> ' + E(p['need']) + '</p><p class="note">Sample project for the proposal.</p></div>' + ph(p['photo'], 'tall') + '</div>')
            + sec(section_head('The project', 'Concept, Challenge, Solution and Result')
                  + '<div class="grid-2"><div class="card plain"><h3>Concept</h3><p>' + E(p['concept']) + '</p></div><div class="card plain"><h3>Challenge</h3><p>' + E(p['challenge']) + '</p></div>'
                  + '<div class="card plain"><h3>Solution</h3><p>' + E(p['solution']) + '</p></div><div class="card plain"><h3>Result</h3><p>' + E(p['result']) + '</p></div></div>', 'white')
            + sec(section_head('Project facts', 'At a Glance') + table(['Item', 'Detail'], [('Client', p['client']), ('Category', p['cat']), ('Format', p['fmt']), ('First batch', p['batch']), ('Time to launch', p['time'])], 480)
                  + f'<p style="margin-top:24px"><a class="link-arrow" href="/products/{slug}/">More about {E(p["cat"])} &rarr;</a> &nbsp; <a class="link-arrow" href="/portfolio/">All projects &rarr;</a></p>'))
    inner(path, p['name'], p['concept'], [('Home', '/'), ('Portfolio', '/portfolio/'), (p['name'], None)], p['name'], p['note'], body, nav='/portfolio/', cta=cta_band('Let\'s Develop Your Next Product', p['cat']))

# ================= Phase 3: Insights and legal =================
PUB_DATE = '2026-11-10'
CATEGORIES = []
for a in ARTICLES:
    if a['cat'] not in CATEGORIES: CATEGORIES.append(a['cat'])

chips = ''.join(f'<span class="badge">{E(c)}</span>' for c in CATEGORIES)
featured = ARTICLES[0]
inner('/insights/', 'Insights', 'Guides on contract manufacturing, product development, food and beverage production and packaging from GoNEST.',
      [('Home', '/'), ('Insights', None)], 'Insights', 'Knowledge for better products.',
      sec(section_head('Knowledge center', 'Guides for Brand Owners')
          + f'<div class="badges" style="margin-bottom:28px">{chips}</div>'
          + f'<div class="grid-3">{article_cards()}</div>')
      + sec(section_head('Start here', 'New to Contract Manufacturing?')
            + f'<div class="callout"><p>Begin with <a href="/insights/{featured["slug"]}/" style="color:var(--secondary);font-weight:700">{E(featured["title"])}</a>, then read the guide on OEM, ODM and private label to choose how to work with a factory.</p></div>', 'white'))

for a in ARTICLES:
    path = f'/insights/{a["slug"]}/'
    body_html = ''
    for h, paras in a['body']:
        body_html += f'<h2>{E(h)}</h2>'
        if len(paras) > 1 and all(len(p) < 110 for p in paras):
            body_html += '<ul>' + ''.join(f'<li>{E(p)}</li>' for p in paras) + '</ul>'
        else:
            body_html += ''.join(f'<p>{E(p)}</p>' for p in paras)
    rel = ''.join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in a['related'])
    others = [x for x in ARTICLES if x['slug'] != a['slug']][:3]
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'],
        "datePublished": a["date"] or PUB_DATE, "dateModified": a["date"] or PUB_DATE, "author": {"@type": "Organization", "name": "GoNEST"},
        "publisher": {"@type": "Organization", "name": "GoNEST"}, "mainEntityOfPage": DOMAIN + path}, ensure_ascii=False) + '</script>\n'
    body = (sec(f'<article class="prose"><p class="note">{E(a["cat"])} &middot; {E(a["read"])}</p>{body_html}'
                f'<div class="callout"><b>Related on this site</b><ul style="margin-top:8px">{rel}</ul></div></article>')
            + sec(section_head('Keep reading', 'More Guides') + f'<div class="grid-3">{article_cards(others)}</div>', 'white'))
    inner(path, a['title'], a['desc'], [('Home', '/'), ('Insights', '/insights/'), (a['cat'], None)], a['title'], a['desc'], body, ld, nav='/insights/')

# ---------- Legal ----------
def legal(path, title, desc, blocks):
    inner_html = '<article class="prose"><div class="callout"><b>Template.</b> This text is a starting point and has not been reviewed by a lawyer. Have the company or its legal adviser review and adjust it before the site goes live.</div>'
    inner_html += '<p class="note">Last updated: [date]</p>'
    for h, paras in blocks:
        inner_html += f'<h2>{E(h)}</h2>' + ''.join(f'<p>{E(p)}</p>' for p in paras)
    inner_html += '</article>'
    inner(path, title, desc, [('Home', '/'), (title, None)], title, 'How this website handles information and how it may be used.' if 'privacy' in path else 'The terms for using this website.', sec(inner_html), cta=cta_band())

legal('/privacy-policy/', 'Privacy Policy', 'How the GoNEST website handles personal information.', [
    ('Who we are', ['This website is operated by [legal company name], trading as GoNEST, located at [address].']),
    ('Information we receive', ['When you send the consultation form, we receive the details you type: name, WhatsApp number, product category, estimated order and message. We also receive the page you sent it from and, if you arrived through a campaign link, the campaign name.',
                                'If you choose "Send via WhatsApp" or contact us by WhatsApp or email, we receive the information you send there.']),
    ('How we use it', ['We use your details to reply to your inquiry, prepare quotes and follow up on your project. We do not sell your information.']),
    ('Analytics and cookies', ['With your permission, we use Google Analytics (and, if enabled, Microsoft Clarity) to understand which pages are visited and which buttons are used. These tools set cookies and receive technical data such as pages viewed, device type and approximate location. No analytics are loaded unless you accept.',
                               'You can change your choice at any time with "Cookie settings" in the footer. [Confirm the tools in use and the data retention period before launch.]']),
    ('How long we keep it', ['We keep inquiry details for as long as needed to handle your inquiry and any resulting project, for [period], unless the law requires longer.']),
    ('Sharing', ['We share information only with people who help us serve your inquiry, such as our team and service providers, or when the law requires it.']),
    ('Your choices', ['You may ask us to correct or delete the information we hold about you by contacting [email].']),
    ('Changes', ['We may update this policy. The date at the top shows the latest version.']),
])
legal('/terms/', 'Terms and Conditions', 'Terms for using the GoNEST website.', [
    ('Use of this website', ['This website provides general information about the products and services of [legal company name], trading as GoNEST. By using it you agree to these terms.']),
    ('Information and prices', ['Prices, minimum orders, lead times and other figures on this website are indicative and may change. A quote or written agreement is required for any order.']),
    ('No guarantee of availability', ['Products and services shown may not be available for every project. We confirm feasibility during consultation.']),
    ('Intellectual property', ['The text, design and images on this website belong to [legal company name] or its licensors. Do not copy them without permission. Your formulas and brand materials remain yours and are handled under a separate confidentiality agreement when a project starts.']),
    ('Links to other sites', ['This website may link to other sites. We are not responsible for their content.']),
    ('Limitation of liability', ['We take care to keep this website accurate, but we do not accept liability for loss caused by relying only on the information shown here.']),
    ('Governing law', ['These terms are governed by the laws of the Republic of Indonesia. [Confirm with legal adviser.]']),
    ('Contact', ['Questions about these terms can be sent to [email].']),
])

# ---------------- Static assets ----------------
os.makedirs(os.path.join(OUT, 'assets/img'), exist_ok=True)
all_paths = ['/', '/about/', '/services/', '/products/'] + [f'/products/{c["slug"]}/' for c in CATS] + ['/contact/'] + NEW_PATHS
assert set(all_paths) == set(PATHMAP), (set(all_paths) ^ set(PATHMAP))
def sm_entry(loc, en, idp):
    return (f'  <url><loc>{DOMAIN}{loc}</loc>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{DOMAIN}{en}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="id" href="{DOMAIN}{idp}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}{en}"/>\n  </url>\n')
sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
      + ''.join(sm_entry(en, en, idp) + sm_entry(idp, en, idp) for en, idp in sorted(PATHMAP.items())) + '</urlset>\n')
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
if K.DEMO:
    open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
else:
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /api/\n\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(OUT, '404.html'), 'w').write(head('Page not found', 'This page could not be found.', '/404') + header('/404') + '<section class="section"><div class="container stack"><h1>Page not found</h1><p>The page you are looking for does not exist or has moved.</p><a class="btn btn-primary" href="/" style="align-self:flex-start">Back to home</a></div></section>\n' + footer())
_robots = '  X-Robots-Tag: noindex, nofollow\n' if K.DEMO else ''
open(os.path.join(OUT, '_headers'), 'w').write('/*\n' + _robots + '  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n\n/assets/*\n  Cache-Control: public, max-age=604800\n\n/admin/*\n  X-Robots-Tag: noindex, nofollow\n  Cache-Control: no-store\n')
print('pages written:', len(all_paths))

print('photo slots used:', len(PHOTOS))
