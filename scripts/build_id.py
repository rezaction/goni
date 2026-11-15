import json, os, html, sys
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathmap import PATHMAP, REVERSE
import id_content as C

OUT = str(C.K.OUT)
DOMAIN = C.K.DOMAIN
PUB_DATE = '2026-11-10'
E = html.escape
CURRENT = ['']
WRITTEN = []

NAV = [('Beranda', '/id/'), ('Tentang', '/id/tentang-kami/'), ('Layanan', '/id/layanan/'), ('Produk', '/id/produk/'),
       ('Portofolio', '/id/portofolio/'), ('Wawasan', '/id/wawasan/'), ('Kontak', '/id/kontak/')]
CATS = C.CATS
CAT_BY_EN = {c['en']: c for c in CATS}

def slugify(s):
    return ''.join(ch if ch.isalnum() else '-' for ch in s.lower()).strip('-').replace('--', '-')

def write(path, content):
    full = os.path.join(OUT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)
    WRITTEN.append(path)

# ---------------- layout ----------------
def head(title, desc, path, extra=''):
    CURRENT[0] = path
    full = title if title.startswith('GoNEST') else title + ' | GoNEST'
    url = DOMAIN + path
    en = REVERSE.get(path)
    alt = ''
    if en:
        alt = (f'<link rel="alternate" hreflang="en" href="{DOMAIN}{en}">\n'
               f'<link rel="alternate" hreflang="id" href="{url}">\n'
               f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{en}">\n')
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
{alt}<meta property="og:type" content="website">
<meta property="og:title" content="{E(full)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="GoNEST">
<meta property="og:locale" content="id_ID">
<meta name="theme-color" content="#123B67">
<link rel="icon" href="/assets/img/favicon.png" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Source+Sans+3:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Langsung ke konten</a>
'''

def lang_switch(path):
    en = REVERSE.get(path)
    if not en: return ''
    return (f'<div class="lang-switch" role="group" aria-label="Bahasa">'
            f'<a href="{en}" hreflang="en" lang="en">EN</a>'
            f'<a href="{path}" hreflang="id" lang="id" aria-current="true">ID</a></div>\n')

def header(nav_path):
    links = ''
    for label, href in NAV:
        cur = ' aria-current="page"' if (href == nav_path or (href != '/id/' and nav_path.startswith(href))) else ''
        links += f'<a href="{href}"{cur}>{label}</a>\n'
    return f'''<header class="site-header">
<div class="container">
<a class="brand" href="/id/"><img src="/assets/img/logo.png" alt="" width="36" height="36">GoNEST</a>
<button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" type="button">Menu</button>
<nav class="nav" id="site-nav" aria-label="Navigasi utama">
{links}</nav>
{lang_switch(CURRENT[0])}<a class="btn btn-primary" href="/id/kontak/">Hubungi Kami</a>
</div>
</header>
<main id="main">
'''

def footer():
    cat_links = ''.join(f'<a href="/id/produk/{c["slug"]}/">{E(c["name"])}</a>' for c in CATS)
    return f'''</main>
<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div><div class="footer-brand">GoNEST</div><p style="font-size:15px;max-width:320px">Pengembangan produk dan jasa maklon makanan dan minuman.</p></div>
<div><strong>Layanan</strong><a href="/id/layanan/pengembangan-produk/">Pengembangan Produk</a><a href="/id/layanan/jasa-maklon/">Jasa Maklon</a><a href="/id/layanan/private-label/">Private Label</a><a href="/id/layanan/oem-odm/">OEM dan ODM</a><a href="/id/layanan/kemasan/">Solusi Kemasan</a></div>
<div><strong>Produk</strong>{cat_links}</div>
<div><strong>Perusahaan</strong><a href="/id/tentang-kami/">Tentang Kami</a><a href="/id/tentang-kami/fasilitas/">Fasilitas</a><a href="/id/tentang-kami/jaminan-mutu/">Jaminan Mutu</a><a href="/id/tentang-kami/sertifikasi/">Sertifikasi</a><a href="/id/cara-kerja/">Cara Kerja</a><a href="/id/portofolio/">Portofolio</a><a href="/id/wawasan/">Wawasan</a><a href="/id/kontak/">Kontak</a></div>
</div>
<div class="footer-bottom"><span>&copy; <span id="year">2026</span> GoNEST. Hak cipta dilindungi.</span><span><a href="/id/kebijakan-privasi/" style="display:inline">Kebijakan Privasi</a> &nbsp;|&nbsp; <a href="/id/syarat-ketentuan/" style="display:inline">Syarat dan Ketentuan</a> <a href="#" data-consent-reset hidden style="display:inline">&nbsp;|&nbsp; Pengaturan cookie</a></span></div>
</div>
</footer>
<a class="wa-float" data-wa="Halo GoNEST, saya ingin berdiskusi tentang proyek produk." href="#">WhatsApp</a>
<script src="/assets/js/config.js"></script>
<script src="/assets/js/main.js"></script>
</body>
</html>
'''

# ---------------- components ----------------
def ph(key, cls=''):
    label = C.PH.get(key, key)
    return C.K.photo_slot(key, cls, 'FOTO: ' + label, label.capitalize(), 'Unggah di dashboard: Photos')

def section_head(eyebrow, title, sub=''):
    p = f'<p>{sub}</p>' if sub else ''
    return f'<div class="section-head"><div class="eyebrow">{E(eyebrow)}</div><h2>{title}</h2>{p}</div>'

def sec(inner_html, cls=''):
    return f'<section class="section {cls}"><div class="container">{inner_html}</div></section>\n'

def lst(items):
    return '<ul class="list">' + ''.join(f'<li>{E(i)}</li>' for i in items) + '</ul>'

def table(headers, rows, minw=520):
    th = ''.join(f'<th>{E(h)}</th>' for h in headers)
    tr = ''.join('<tr>' + ''.join(f'<td>{E(x)}</td>' for x in r) + '</tr>' for r in rows)
    return f'<div class="table-wrap"><table style="min-width:{minw}px"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def faq_html(fq):
    return '<div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in fq) + '</div>'

def faq_ld(fq):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "id",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fq]}, ensure_ascii=False) + '</script>\n'

def steps_html():
    return '<div class="steps">' + ''.join(f'<div class="step"><small>Langkah {n}</small><h3>{t}</h3><p>{d}</p><em>{w}</em></div>' for n, t, d, w in C.STEPS) + '</div>'

def price_table(note=True):
    n = '<p class="note" style="margin-top:12px">Harga belum termasuk PPN dan ongkos kirim.</p>' if note else ''
    return table(['Kategori', 'Contoh produk', 'Format', 'Pesanan minimum', 'Harga indikatif', 'Waktu produksi'], C.ROWS, 720) + n

def stats_html():
    return '\n'.join(f'<div class="stat"><b>{E(x["id_value"])}</b><span>{E(x["id_label"])}</span></div>' for x in C.K.STATS)

def testimonials_html():
    return '\n'.join(f'<div class="card plain"><p style="font-size:19px">{E(t["id"]["quote"])}</p><div><b style="color:var(--primary)">{E(t["id"]["name"])}</b><br><span class="note">{E(t["id"]["role"])}</span></div></div>' for t in C.K.TESTIMONIALS)

def cat_cards():
    out = ''
    for c in CATS:
        out += f'''<div class="card">
{ph(c["photo"])}
<h3>{E(c["name"])}</h3>
<p>{E(c["desc"])}</p>
<div class="meta"><span>Pesanan minimum: <b>{c["moq"]}</b></span><span>Format: <b>{c["formats"]}</b></span></div>
<a class="link-arrow" href="/id/produk/{c["slug"]}/">Lihat {E(c["name"])} &rarr;</a>
</div>
'''
    return out

def project_cards(items=None):
    return ''.join(f'''<a class="card plain" href="/id/portofolio/{p["slug"]}/" style="text-decoration:none">
{ph(p["photo"])}
<div class="eyebrow">{E(p["cat"])}</div>
<h3>{E(p["name"])}</h3>
<p>{E(p["note"])}</p>
<span class="link-arrow">Lihat proyek &rarr;</span>
</a>
''' for p in (items or C.PROJECTS))

def article_cards(items=None, limit=None):
    items = items or C.ARTICLES
    if limit: items = items[:limit]
    return ''.join(f'''<a class="card plain" href="/id/wawasan/{a["slug"]}/" style="text-decoration:none">
<div class="eyebrow">{E(a["cat"])}</div><h3>{E(a["title"])}</h3><p>{E(a["desc"])}</p><span class="note">{E(a["read"])}</span>
</a>
''' for a in items)

def cta_band(title='Mari Kembangkan Produk Anda Berikutnya', cat_en=None):
    qs = f'?category={quote(cat_en)}' if cat_en else ''
    return f'''<section class="section mid">
<div class="container stack" style="align-items:flex-start">
<h2>{E(title)}</h2>
<p class="lead" style="font-size:19px;color:#E1EAF5;max-width:640px">Punya ide produk, atau sedang mencari mitra produksi? Ceritakan kebutuhan Anda dan tim kami akan membalas dalam satu hari kerja.</p>
<a class="btn btn-accent" href="/id/kontak/{qs}">Mulai Konsultasi</a>
</div>
</section>
'''

def inner(path, title, desc, crumbs, h1, lead, body, ld='', nav=None, cta=None):
    parts = [f'<a href="{h}">{E(l)}</a>' if h else E(l) for l, h in crumbs]
    hero = f'''
<section class="page-hero"><div class="container">
<div class="crumbs">{" / ".join(parts)}</div>
<h1>{E(h1)}</h1>
<p class="lead">{E(lead)}</p>
</div></section>
'''
    page = head(title, desc, path, ld) + header(nav or path) + hero + body + (cta if cta is not None else cta_band()) + footer()
    write(path, page)

# ================= Home =================
org = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "GoNEST", "url": DOMAIN + '/id/',
                  "description": "Mitra pengembangan produk dan jasa maklon makanan dan minuman."}, ensure_ascii=False)
home = head('GoNEST | Mitra Jasa Maklon Makanan & Minuman',
            'Pengembangan produk dan jasa maklon minuman serbuk, kopi, bumbu, dan produk herbal dengan merek Anda sendiri.',
            '/id/', f'<script type="application/ld+json">{org}</script>\n') + header('/id/') + f'''
<section class="hero">
<div class="container hero-grid">
<div class="stack" style="gap:24px">
<div class="eyebrow">Jasa Maklon Makanan &amp; Minuman</div>
<h1>Membangun Produk Lebih Baik. Memproduksi Visi Brand Anda.</h1>
<p class="lead">GoNEST adalah mitra Anda untuk pengembangan produk dan jasa maklon makanan dan minuman. Kami membawa ide Anda dari formula sampai produk jadi yang siap dipasarkan.</p>
<div class="hero-actions"><a class="btn btn-accent" href="/id/kontak/">Diskusikan Proyek Anda</a><a class="btn btn-ghost" href="/id/produk/">Lihat Kemampuan Kami</a></div>
<div class="hero-tags"><span>Minuman Serbuk</span><span>Kopi</span><span>Bumbu &amp; Rempah</span><span>Herbal</span></div>
</div>
<div class="brief">
<div class="brief-head"><strong>Contoh brief proyek</strong><span class="chip">Contoh</span></div>
<dl>
<div><dt>Produk</dt><dd>Premix Latte Matcha</dd></div>
<div><dt>Kategori</dt><dd>Minuman Serbuk</dd></div>
<div><dt>Format</dt><dd>Sachet, 25 g neto</dd></div>
<div><dt>Batch pertama</dt><dd>1.000 kg</dd></div>
<div><dt>Sampel siap</dt><dd>7 sampai 10 hari kerja</dd></div>
<div><dt>Harga indikatif</dt><dd>mulai Rp 2.900 / sachet</dd></div>
</dl>
<a class="btn btn-primary" href="/id/kontak/?category=Powdered%20Beverage">Minta penawaran serupa</a>
</div>
</div>
</section>

<section class="stats"><div class="container grid-4">
{stats_html()}
</div></section>

<section class="section">
<div class="container split">
<div class="stack">
<div class="eyebrow">Tentang perusahaan</div>
<h2>Lebih dari Sekadar Pabrik. Mitra Pengembangan Produk Anda.</h2>
<p>Kebanyakan pabrik maklon menjual kapasitas. GoNEST juga membawa formulasi, sampel, kontrol mutu, dan dukungan kemasan, sehingga Anda bisa meluncurkan produk dengan merek sendiri tanpa membangun pabrik.</p>
<p>Kami bekerja dengan pengusaha yang memulai brand pertamanya, pemilik brand yang menambah lini produk, dan distributor yang membutuhkan mitra produksi yang andal.</p>
<a class="link-arrow" href="/id/tentang-kami/">Tentang GoNEST &rarr;</a>
</div>
{ph('production floor', 'tall')}
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Kemampuan manufaktur', 'Keahlian Manufaktur Kami', 'Empat kategori produk, masing-masing dengan halaman sendiri tentang formula, pilihan kemasan, pesanan minimum, dan sampel.')}
<div class="grid-4">{cat_cards()}</div>
</div>
</section>

<section class="section dark">
<div class="container">
{section_head('Mengapa GoNEST', 'Mitra yang Tepat untuk Produk Anda Berikutnya')}
<div class="grid-4">
<div class="card"><h3>Pengembangan produk</h3><p>Formulasi, penyesuaian rasa, dan putaran sampel ditangani tim R&amp;D kami.</p></div>
<div class="card"><h3>Manufaktur</h3><p>Lini pencampuran, pengisian, dan penyegelan yang ukurannya pas untuk startup dan brand yang bertumbuh.</p></div>
<div class="card"><h3>Kontrol mutu</h3><p>Pemeriksaan batch terhadap spesifikasi yang Anda setujui, dengan catatan untuk setiap produksi.</p></div>
<div class="card"><h3>Solusi kemasan</h3><p>Bantuan memilih pouch, sachet, atau jar, plus panduan label dan desain.</p></div>
</div>
</div>
</section>

<section class="section">
<div class="container">
{section_head('Proses manufaktur', 'Dari Ide Anda sampai Produk Jadi', 'Enam tahap dengan urutan yang sama di setiap proyek. Waktu umum dari konsultasi pertama sampai pengiriman adalah 5 sampai 8 minggu.')}
{steps_html()}
<p style="margin-top:24px"><a class="link-arrow" href="/id/cara-kerja/">Lihat proses lengkap &rarr;</a></p>
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Pesanan minimum dan harga indikatif', 'Ketahui Angkanya Sebelum Menghubungi Kami', 'Titik awal yang jelas membantu pembeli serius mengambil keputusan lebih cepat. Harga akhir tergantung formula, bahan baku, kemasan, dan volume.')}
{price_table()}
</div>
</section>

<section class="section">
<div class="container split">
{ph('qc laboratory', 'tall')}
<div class="stack">
<div class="eyebrow">Fasilitas dan jaminan mutu</div>
<h2>Mutu Dimulai di Balik Layar</h2>
<p>Setiap batch diperiksa terhadap spesifikasi yang Anda setujui: kadar air, ukuran partikel, rasa, berat neto, dan segel kemasan sebelum meninggalkan pabrik.</p>
<div class="badges"><span class="badge">BPOM</span><span class="badge">Halal</span><span class="badge">HACCP</span><span class="badge">ISO 22000</span></div>
<p class="note">Lencana ini hanya placeholder. Tampilkan hanya sertifikat yang benar-benar dimiliki perusahaan, lengkap dengan masa berlakunya.</p>
</div>
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Portofolio pilihan', 'Produk yang Sudah Kami Bawa ke Pasar')}
<div class="grid-4">{project_cards()}</div>
<p style="margin-top:24px"><a class="link-arrow" href="/id/portofolio/">Lihat semua proyek &rarr;</a></p>
</div>
</section>

<section class="section">
<div class="container">
{section_head('Mitra bisnis kami', 'Membangun Produk yang Sukses Bersama')}
<div class="grid-2">
{testimonials_html()}
</div>
</div>
</section>

<section class="section white">
<div class="container">
{section_head('Wawasan dan pengetahuan', 'Pengetahuan untuk Produk yang Lebih Baik', 'Panduan tentang jasa maklon, pengembangan produk, dan kemasan.')}
<div class="grid-3">{article_cards(limit=3)}</div>
<p style="margin-top:24px"><a class="link-arrow" href="/id/wawasan/">Semua artikel &rarr;</a></p>
</div>
</section>
''' + cta_band() + footer()
write('/id/', home)

# ================= About =================
def about_trust_badges():
    return '<div class="badges"><span class="badge">BPOM</span><span class="badge">Halal</span><span class="badge">HACCP</span><span class="badge">ISO 22000</span></div>'

inner('/id/tentang-kami/', 'Tentang GoNEST', 'GoNEST adalah mitra pengembangan produk dan jasa maklon makanan dan minuman untuk pemilik brand, pengusaha, dan distributor.',
      [('Beranda', '/id/'), ('Tentang Kami', None)], 'Tentang GoNEST', 'Mitra pengembangan produk dan manufaktur untuk brand makanan dan minuman.',
      sec('<div class="split"><div class="stack"><div class="eyebrow">Gambaran perusahaan</div><h2>Siapa Kami</h2>'
          '<p>GoNEST mengembangkan dan memproduksi minuman serbuk, kopi, bumbu, dan produk herbal untuk brand lain. Kami memadukan lantai produksi dengan meja R&amp;D, sehingga klien bisa datang dengan ide dan pulang dengan produk.</p>'
          '<p>[Ganti dengan sejarah perusahaan yang sebenarnya: tahun berdiri, lokasi, perkembangan, dan tonggak penting.]</p></div>' + ph('company building', 'tall') + '</div>')
      + sec(section_head('Visi dan misi', 'Yang Menuntun Pekerjaan Kami')
            + '<div class="grid-2"><div class="card"><h3>Visi</h3><p>Menjadi mitra manufaktur makanan dan minuman yang paling dipercaya bagi brand Indonesia yang bertumbuh.</p></div>'
            + '<div class="card"><h3>Misi</h3>' + lst(['Mengembangkan produk yang sesuai dengan brief setiap klien.', 'Memproduksi dengan mutu konsisten, batch demi batch.', 'Jelas soal minimum order, jadwal, dan biaya.']) + '</div></div>', 'white')
      + sec(section_head('Keahlian kami', 'Di Mana Kami Kuat')
            + '<div class="grid-4"><div class="card plain"><h3>Formulasi</h3><p>Pengembangan rasa dan tekstur dengan putaran sampel yang bisa diulang.</p></div>'
            + '<div class="card plain"><h3>Pencampuran dan pengisian</h3><p>Pencampuran kering dan lini pengisian sachet, pouch, dan jar.</p></div>'
            + '<div class="card plain"><h3>Kontrol mutu</h3><p>Pemeriksaan bahan masuk, selama proses, dan pelepasan batch.</p></div>'
            + '<div class="card plain"><h3>Dukungan kemasan</h3><p>Panduan bahan, ukuran, dan label sebelum Anda mencetak.</p></div></div>')
      + sec('<div class="split">' + ph('qc laboratory', 'tall') + '<div class="stack"><div class="eyebrow">Fasilitas dan sertifikasi</div><h2>Siap Diaudit</h2>'
            '<p>Klien dipersilakan mengunjungi pabrik dan meninjau proses kami. Foto fasilitas, daftar mesin, dan sertifikat akan ditampilkan di bawah setelah dikonfirmasi perusahaan.</p>'
            + about_trust_badges() + '<p class="note">Lencana placeholder. Ganti dengan sertifikat asli dan masa berlakunya.</p></div></div>', 'white')
      + sec(section_head('Nilai kami', 'Cara Kami Bekerja dengan Klien')
            + '<div class="grid-3"><div class="card plain"><h3>Kejelasan</h3><p>Anda melihat pesanan minimum, kisaran harga, dan jadwal sejak awal.</p></div>'
            + '<div class="card plain"><h3>Konsistensi</h3><p>Sampel yang disetujui menjadi tolok ukur setiap batch yang kami lepas.</p></div>'
            + '<div class="card plain"><h3>Kerahasiaan</h3><p>Formula dan merek Anda adalah milik Anda.</p></div></div>'))

inner('/id/tentang-kami/profil-perusahaan/', 'Profil Perusahaan', 'Profil perusahaan GoNEST: fokus bisnis, kategori produk, layanan, dan kapasitas produksi.',
      [('Beranda', '/id/'), ('Tentang Kami', '/id/tentang-kami/'), ('Profil Perusahaan', None)], 'Profil Perusahaan', 'Fakta tentang GoNEST dalam satu halaman.',
      sec(section_head('Sekilas', 'GoNEST Singkatnya', 'Isian dalam kurung siku adalah placeholder yang harus diganti dengan data perusahaan yang sebenarnya.')
          + table(['Hal', 'Keterangan'], [
              ('Nama perusahaan', '[Nama badan hukum]'), ('Merek', 'GoNEST'), ('Tahun berdiri', '[Tahun]'), ('Lokasi', '[Kota, provinsi]'),
              ('Fokus bisnis', 'Pengembangan produk dan jasa maklon makanan dan minuman'),
              ('Kategori produk', 'Minuman serbuk, kopi, bumbu dan rempah, produk herbal'),
              ('Layanan', 'Pengembangan produk, jasa maklon, private label, OEM dan ODM, dukungan kemasan'),
              ('Kapasitas pencampuran', '4 ton per hari'), ('Tim', '[Jumlah] orang'), ('Pasar', 'Indonesia [konfirmasi pasar ekspor]')], 520))
      + sec(section_head('Tonggak perusahaan', 'Perjalanan Perusahaan', 'Ganti dengan sejarah yang sebenarnya.')
            + table(['Tahun', 'Tonggak'], [('[Tahun]', 'Perusahaan didirikan'), ('[Tahun]', 'Lini minuman serbuk pertama dipasang'), ('[Tahun]', 'Penyangraian kopi ditambahkan'), ('[Tahun]', 'Laboratorium mutu dibuka')], 480), 'white'))

fac_cards = ''.join(f'<div class="card plain">{ph(k)}<h3>{E(n)}</h3><p>{E(d)}</p></div>' for n, k, d in C.FAC_AREAS)
mach = table(['Peralatan', 'Fungsi', 'Kapasitas'], [
    ('Ribbon blender', 'Pencampuran kering serbuk', '500 kg per batch'), ('Mesin pengisi sachet', 'Mengisi dan menyegel sachet', '[Unit per menit]'),
    ('Mesin pengisi pouch', 'Mengisi dan menyegel stand-up pouch', '[Unit per menit]'), ('Mesin sangrai kopi', 'Menyangrai green bean', '30 kg per batch'),
    ('Grinder / pulverizer', 'Menggiling rempah dan kopi', '[kg per jam]'), ('Metal detector', 'Memeriksa barang jadi', 'Inline'),
    ('Moisture analyzer', 'Uji kadar air di laboratorium', 'Setiap batch')], 560)
inner('/id/tentang-kami/fasilitas/', 'Fasilitas Kami', 'Area produksi, mesin, dan laboratorium GoNEST untuk minuman serbuk, kopi, bumbu, dan produk herbal.',
      [('Beranda', '/id/'), ('Tentang Kami', '/id/tentang-kami/'), ('Fasilitas', None)], 'Fasilitas Kami', 'Tempat produk Anda dibuat.',
      sec(section_head('Area produksi', 'Menyusuri Pabrik', 'Foto-foto ini masih placeholder. Pakai foto asli pabrik.') + f'<div class="grid-3">{fac_cards}</div>')
      + sec(section_head('Mesin', 'Daftar Peralatan') + mach, 'white'))

inner('/id/tentang-kami/jaminan-mutu/', 'Jaminan Mutu', 'Cara GoNEST memeriksa bahan baku, produksi, dan barang jadi, serta bagaimana batch dilacak.',
      [('Beranda', '/id/'), ('Tentang Kami', '/id/tentang-kami/'), ('Jaminan Mutu', None)], 'Jaminan Mutu', 'Setiap batch dibandingkan dengan sampel yang Anda setujui.',
      sec(section_head('Tiga titik pemeriksaan', 'Cara Kami Mengendalikan Mutu')
          + '<div class="grid-3"><div class="card plain"><h3>Bahan baku masuk</h3><p>Setiap kiriman diperiksa tampilan, berat, dan dokumennya sebelum masuk gudang.</p></div>'
          + '<div class="card plain"><h3>Selama produksi</h3><p>Campuran ditimbang sesuai formula dan diperiksa berkala untuk berat dan segel.</p></div>'
          + '<div class="card plain"><h3>Barang jadi</h3><p>Sampel diuji dan dicicipi terhadap acuan yang disetujui sebelum dilepas.</p></div></div>')
      + sec(section_head('Pengujian', 'Yang Kami Periksa')
            + table(['Pengujian', 'Kapan', 'Tujuan'], [('Kadar air', 'Setiap batch', 'Menjaga serbuk tetap mengalir dan memperpanjang masa simpan'), ('Berat neto', 'Saat pengisian', 'Memastikan setiap kemasan sesuai label'),
                                                       ('Keutuhan segel', 'Saat pengisian', 'Mencegah kelembapan dan kontaminasi'), ('Rasa dan aroma', 'Setiap batch', 'Sesuai dengan sampel yang disetujui'),
                                                       ('Deteksi logam', 'Barang jadi', 'Melindungi konsumen'), ('Uji mikrobiologi', 'Sesuai peraturan, di laboratorium pihak ketiga', 'Memastikan batas keamanan terpenuhi')], 560), 'white')
      + sec('<div class="split"><div class="stack"><div class="eyebrow">Ketertelusuran</div><h2>Setiap Batch Bisa Dilacak</h2><p>Setiap batch mendapat kode lot. Lot bahan baku, tanggal produksi, dan hasil QC dicatat dan dihubungkan, dan sampel simpan disimpan.</p><p>Jika ada pertanyaan setelah pengiriman, kami bisa menelusurinya sampai lot bahan baku.</p></div>' + ph('quality inspection', 'tall') + '</div>'))

inner('/id/tentang-kami/sertifikasi/', 'Sertifikasi', 'Sertifikasi dan perizinan yang dimiliki GoNEST, lengkap dengan ruang lingkup dan masa berlaku.',
      [('Beranda', '/id/'), ('Tentang Kami', '/id/tentang-kami/'), ('Sertifikasi', None)], 'Sertifikasi', 'Kepatuhan yang bisa Anda verifikasi.',
      sec(section_head('Izin dan sertifikat', 'Yang Kami Miliki', 'Tabel placeholder. Cantumkan hanya sertifikat yang saat ini dimiliki perusahaan, dengan nomor dan masa berlaku yang sebenarnya, dan tambahkan pindaian dokumennya.')
          + table(['Sertifikasi', 'Ruang lingkup', 'Nomor', 'Berlaku sampai'], [
              ('BPOM', '[Ruang lingkup]', '[Nomor]', '[Tanggal]'), ('Halal', '[Ruang lingkup]', '[Nomor]', '[Tanggal]'), ('HACCP', '[Ruang lingkup]', '[Nomor]', '[Tanggal]'),
              ('ISO 22000', '[Ruang lingkup]', '[Nomor]', '[Tanggal]'), ('Izin usaha (NIB)', '[Ruang lingkup]', '[Nomor]', '[Tanggal]')], 600)
          + '<p class="note" style="margin-top:12px">Jangan tampilkan sertifikasi sebelum dokumennya ada di tangan dan masih berlaku.</p>'))

# ================= Services =================
cmp_rows = [('Pemilik formula', 'Klien', 'GoNEST atau dibagi', 'GoNEST'),
            ('Pekerjaan pengembangan', 'Klien menyediakan formula', 'GoNEST mengembangkan', 'Formula GoNEST yang sudah ada'),
            ('Pesanan minimum', 'Standar', 'Standar', 'Lebih rendah'),
            ('Waktu sampai meluncur', '5 sampai 8 minggu', '6 sampai 10 minggu', '3 sampai 5 minggu'),
            ('Cocok untuk', 'Brand yang sudah punya resep', 'Brand baru yang punya ide', 'Peluncuran cepat dan berisiko rendah')]
cmp_html = table(['', 'OEM', 'ODM', 'Private label'], cmp_rows, 640)
svc_cards = ''.join(f'''<div class="card plain" id="{s["slug"]}"><h3>{E(s["name"])}</h3><p>{E(s["lead"])}</p>{lst(s["inc"][:3])}<a class="link-arrow" href="/id/layanan/{s["slug"]}/">Selengkapnya &rarr;</a></div>
''' for s in C.SERVICES)
faqs_svc = [('Bagaimana cara memulai?', 'Kirim brief singkat lewat formulir kontak atau WhatsApp. Kami membalas dalam satu hari kerja dengan pertanyaan dan langkah berikutnya.'),
            ('Apakah sampel dikenai biaya?', 'Ketentuan sampel disepakati saat konsultasi. (Jawaban contoh: putaran sampel pertama sudah termasuk setelah proyek dikonfirmasi.)'),
            ('Bolehkah saya mengunjungi fasilitas?', 'Boleh, dengan perjanjian terlebih dahulu pada jam kerja.')]
inner('/id/layanan/', 'Layanan Manufaktur', 'Pengembangan produk, jasa maklon, private label, OEM dan ODM, serta dukungan kemasan untuk brand makanan dan minuman.',
      [('Beranda', '/id/'), ('Layanan', None)], 'Layanan Manufaktur', 'Semua yang ada di antara ide Anda dan produk jadi, dalam satu tempat.',
      sec(section_head('Apa yang kami kerjakan', 'Lima Cara Bekerja Sama', 'Setiap layanan berlaku untuk keempat kategori produk: minuman serbuk, kopi, bumbu, dan herbal.') + f'<div class="grid-3">{svc_cards}</div>')
      + sec(section_head('Memilih model', 'OEM, ODM, atau Private Label?') + cmp_html, 'white')
      + sec(section_head('Cara kerja', 'Dari Konsultasi sampai Pengiriman', 'Enam tahap yang sama di setiap proyek, sehingga Anda selalu tahu apa yang berikutnya.') + steps_html()
            + '<p style="margin-top:24px"><a class="link-arrow" href="/id/cara-kerja/">Baca proses lengkapnya &rarr;</a></p>')
      + sec(section_head('Pesanan minimum dan persyaratan', 'Yang Perlu Disiapkan Sebelum Menghubungi Kami')
            + '<div class="grid-2"><div class="card"><h3>Sebaiknya dibawa</h3>' + lst(['Produk acuan atau gambaran rasa', 'Target harga per unit', 'Perkiraan pesanan pertama dan volume bulanan', 'Format kemasan yang diinginkan']) + '</div>'
            + '<div class="card"><h3>Pesanan minimum per kategori</h3>' + lst(['Minuman Serbuk: 1.000 kg', 'Kopi: 300 kg sangrai, 1.000 kg instan', 'Bumbu dan Rempah: 500 kg', 'Produk Herbal: 500 kg']) + '</div></div>', 'white')
      + sec(section_head('Pertanyaan', 'Pertanyaan yang Sering Diajukan') + faq_html(faqs_svc)),
      faq_ld(faqs_svc))

for s in C.SERVICES:
    path = f'/id/layanan/{s["slug"]}/'
    apply_cards = ''.join(f'<a class="card plain" href="/id/produk/{c["slug"]}/" style="text-decoration:none"><h3>{E(c["name"])}</h3><p>{E(c["desc"])}</p><span class="link-arrow">Lihat kategori &rarr;</span></a>' for c in CATS)
    body = (sec('<div class="split"><div class="stack"><div class="eyebrow">Gambaran umum</div><h2>' + E(s['name']) + '</h2><p>' + E(s['over']) + '</p></div>' + ph(s['photo'], 'tall') + '</div>')
            + sec(section_head('Cakupan', 'Yang Termasuk dan Untuk Siapa') + '<div class="grid-2"><div class="card"><h3>Termasuk</h3>' + lst(s['inc']) + '</div><div class="card"><h3>Cocok untuk</h3>' + lst(s['who']) + '</div></div>', 'white')
            + sec(section_head('Cara kerja', 'Empat Langkah') + '<div class="steps">' + ''.join(f'<div class="step"><small>Langkah {i+1}</small><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(s['steps'])) + '</div>'
                  + '<p style="margin-top:24px"><a class="link-arrow" href="/id/cara-kerja/">Lihat proses lengkap &rarr;</a></p>')
            + sec(section_head('Berlaku untuk', 'Tersedia untuk Keempat Kategori') + f'<div class="grid-4">{apply_cards}</div>', 'white')
            + sec(section_head('Pertanyaan', 'Pertanyaan yang Sering Diajukan') + faq_html(s['faqs'])))
    inner(path, s['name'], s['lead'], [('Beranda', '/id/'), ('Layanan', '/id/layanan/'), (s['name'], None)], s['name'], s['lead'], body, faq_ld(s['faqs']), nav='/id/layanan/')

# ================= How it works =================
stage_cards = ''.join(f'''<div class="card plain"><div class="eyebrow">Langkah {i+1} &middot; {E(w)}</div><h3>{E(t)}</h3>
<div><b>Yang kami lakukan</b>{lst(we)}</div><div><b>Yang Anda lakukan</b>{lst(you)}</div>
<div class="meta"><span>Anda menerima: <b>{E(out)}</b></span></div></div>
''' for i, (t, w, we, you, out) in enumerate(C.STAGES))
faqs_how = [('Berapa lama satu proyek berlangsung?', 'Waktu umumnya 5 sampai 8 minggu dari konsultasi pertama sampai pengiriman. Produk private label sederhana bisa lebih cepat.'),
            ('Berapa putaran sampel yang termasuk?', 'Ketentuan sampel ditetapkan saat konsultasi. Proyek umumnya membutuhkan dua sampai empat putaran.'),
            ('Bisakah formula diubah setelah disetujui?', 'Perubahan kecil bisa dilakukan sebelum produksi dimulai. Perubahan setelah batch pertama dihitung sebagai putaran pengembangan baru.'),
            ('Siapa pemilik formula?', 'Tergantung model kerja sama. Lihat OEM, ODM, dan Private Label di halaman Layanan.'),
            ('Bagaimana jika saya belum yakin soal kemasan?', 'Ceritakan produk dan pasarnya. Kami menyarankan format dan ukuran, lalu Anda memilih.')]
moq_tbl = table(['Kategori', 'Pesanan minimum', 'Setara kira-kira'], [
    ('Minuman Serbuk', '1.000 kg per formula', 'sekitar 40.000 sachet 25 g'),
    ('Kopi', '300 kg sangrai; 1.000 kg instan', 'sekitar 1.500 pouch 200 g'),
    ('Bumbu dan Rempah', '500 kg per formula', 'sekitar 5.000 pouch 100 g'),
    ('Produk Herbal', '500 kg per formula', 'sekitar 25.000 sachet 20 g')])
inner('/id/cara-kerja/', 'Cara Kerja', 'Enam tahap bekerja sama dengan GoNEST, dari konsultasi pertama sampai pengiriman, lengkap dengan pesanan minimum dan persyaratan proyek.',
      [('Beranda', '/id/'), ('Cara Kerja', None)], 'Cara Kerja', 'Enam tahap, urutannya sama di setiap proyek.',
      sec(section_head('Gambaran proses', 'Dari Pesan Pertama sampai Produk Jadi', 'Setiap tahap punya hasil yang jelas, sehingga Anda selalu tahu apa yang sudah disepakati dan apa yang berikutnya.') + steps_html())
      + sec(section_head('Tahapan secara rinci', 'Apa yang Terjadi di Setiap Langkah') + f'<div class="grid-2">{stage_cards}</div>', 'white')
      + sec(section_head('Pesanan minimum dan persyaratan', 'Yang Perlu Disiapkan') + moq_tbl
            + '<div class="grid-2" style="margin-top:20px"><div class="card plain"><h3>Sebaiknya dibawa</h3>' + lst(['Produk acuan atau gambaran rasa', 'Target harga per unit', 'Perkiraan pesanan pertama dan volume bulanan', 'Format kemasan yang diinginkan']) + '</div>'
            + '<div class="card plain"><h3>Perlu diketahui</h3>' + lst(['Beberapa rasa dengan satu dasar bisa berbagi satu kali produksi', 'Desain kemasan biasanya yang paling lama ditunggu, jadi mulai lebih awal', 'Pendaftaran produk adalah tanggung jawab pemilik brand']) + '</div></div>')
      + sec(section_head('Pertanyaan', 'Pertanyaan yang Sering Diajukan') + faq_html(faqs_how), 'white'),
      faq_ld(faqs_how))

# ================= Products =================
inner('/id/produk/', 'Kategori Produk', 'Jasa maklon minuman serbuk, kopi, bumbu dan rempah, serta produk herbal.',
      [('Beranda', '/id/'), ('Produk', None)], 'Kategori Produk', 'Pilih kategori untuk melihat jenis produk, pilihan formula, kemasan, pesanan minimum, dan sampel.',
      sec(f'<div class="grid-4">{cat_cards()}</div>')
      + sec(section_head('Pesanan minimum dan harga indikatif', 'Titik Awal per Kategori') + price_table(), 'white'))

STEP_TITLE = 'Cara Proyek {n} Berjalan'
for c in CATS:
    path = f'/id/produk/{c["slug"]}/'
    spec_rows = ''.join(f'<tr><td>{E(k)}</td><td>{E(v)}</td></tr>' for k, v in c['specs'])
    msg = f'Halo GoNEST, saya ingin berdiskusi tentang jasa maklon {c["name"]}.'
    page = head(c['hero'], c['lead'], path, faq_ld(c['faqs'])) + header('/id/produk/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/id/">Beranda</a> / <a href="/id/produk/">Produk</a> / {E(c["name"])}</div>
<h1>{E(c["hero"])}</h1>
<p class="lead">{E(c["lead"])}</p>
<div class="hero-actions" style="margin-top:24px"><a class="btn btn-accent" href="/id/kontak/?category={quote(c["en"])}">Minta Penawaran</a><a class="btn btn-ghost" data-wa="{E(msg)}" href="#">Chat WhatsApp</a></div>
</div></section>

<section class="section"><div class="container split">
<div class="stack"><div class="eyebrow">Gambaran kategori</div><h2>{E(c["name"])} Sesuai Brief Anda</h2><p>{E(c["intro"][0])}</p><p>{E(c["intro"][1])}</p></div>
{ph(c["photo"], "tall")}
</div></section>

<section class="section white"><div class="container">
{section_head('Yang bisa kami buat', 'Jenis Produk, Formula, dan Kemasan')}
<div class="grid-3">
<div class="card"><h3>Jenis produk</h3>{lst(c["types"])}</div>
<div class="card"><h3>Pilihan formula dan bahan</h3>{lst(c["formula"])}</div>
<div class="card"><h3>Pilihan kemasan</h3>{lst(c["pack"])}</div>
</div>
</div></section>

<section class="section"><div class="container">
{section_head('Pesanan minimum dan spesifikasi', 'Angka Penting untuk ' + E(c["name"]))}
<div class="table-wrap"><table style="min-width:520px"><thead><tr><th>Hal</th><th>Keterangan</th></tr></thead><tbody>{spec_rows}</tbody></table></div>
</div></section>

<section class="section white"><div class="container">
{section_head('Sampel dan produksi', 'Cara Proyek ' + E(c["name"]) + ' Berjalan')}
{steps_html()}
</div></section>

<section class="section"><div class="container split">
<div class="stack"><div class="eyebrow">Manufaktur dan kontrol mutu</div><h2>Diperiksa Sebelum Dikirim</h2><p>Setiap batch ditimbang sesuai formula, diperiksa selama proses, dan dibandingkan dengan sampel yang Anda setujui sebelum dilepas. Catatan batch disimpan agar setiap lot dapat dilacak.</p></div>
{ph("quality inspection", "tall")}
</div></section>

<section class="section white"><div class="container">
{section_head('Pertanyaan', 'FAQ ' + E(c["name"]))}
{faq_html(c["faqs"])}
</div></section>
''' + cta_band(f'Mari Kembangkan Produk {c["name"]} Anda', c['en']) + footer()
    write(path, page)

# ================= Portfolio =================
inner('/id/portofolio/', 'Portofolio', 'Produk pilihan yang dikembangkan dan diproduksi GoNEST untuk mitra brand.',
      [('Beranda', '/id/'), ('Portofolio', None)], 'Portofolio', 'Produk yang sudah kami bawa ke pasar bersama mitra kami.',
      sec(section_head('Proyek pilihan', 'Hasil Kerja Kami') + f'<div class="grid-4">{project_cards()}</div>'))
for p in C.PROJECTS:
    path = f'/id/portofolio/{p["slug"]}/'
    cat = CAT_BY_EN[p['cat_en']]
    body = (sec('<div class="split"><div class="stack"><div class="eyebrow">' + E(p['cat']) + '</div><h2>' + E(p['name']) + '</h2><p><b>Kebutuhan klien.</b> ' + E(p['need']) + '</p><p class="note">Proyek contoh untuk proposal.</p></div>' + ph(p['photo'], 'tall') + '</div>')
            + sec(section_head('Proyeknya', 'Konsep, Tantangan, Solusi, dan Hasil')
                  + '<div class="grid-2"><div class="card plain"><h3>Konsep</h3><p>' + E(p['concept']) + '</p></div><div class="card plain"><h3>Tantangan</h3><p>' + E(p['challenge']) + '</p></div>'
                  + '<div class="card plain"><h3>Solusi</h3><p>' + E(p['solution']) + '</p></div><div class="card plain"><h3>Hasil</h3><p>' + E(p['result']) + '</p></div></div>', 'white')
            + sec(section_head('Fakta proyek', 'Sekilas') + table(['Hal', 'Keterangan'], [('Klien', p['client']), ('Kategori', p['cat']), ('Format', p['fmt']), ('Batch pertama', p['batch']), ('Waktu sampai meluncur', p['time'])], 480)
                  + f'<p style="margin-top:24px"><a class="link-arrow" href="/id/produk/{cat["slug"]}/">Selengkapnya tentang {E(p["cat"])} &rarr;</a> &nbsp; <a class="link-arrow" href="/id/portofolio/">Semua proyek &rarr;</a></p>'))
    inner(path, p['name'], p['concept'], [('Beranda', '/id/'), ('Portofolio', '/id/portofolio/'), (p['name'], None)], p['name'], p['note'], body, nav='/id/portofolio/', cta=cta_band('Mari Kembangkan Produk Anda Berikutnya', p['cat_en']))

# ================= Insights =================
cats_seen = []
for a in C.ARTICLES:
    if a['cat'] not in cats_seen: cats_seen.append(a['cat'])
chips = ''.join(f'<span class="badge">{E(c)}</span>' for c in cats_seen)
featured = C.ARTICLES[0]
inner('/id/wawasan/', 'Wawasan', 'Panduan tentang jasa maklon, pengembangan produk, produksi makanan dan minuman, dan kemasan dari GoNEST.',
      [('Beranda', '/id/'), ('Wawasan', None)], 'Wawasan', 'Pengetahuan untuk produk yang lebih baik.',
      sec(section_head('Pusat pengetahuan', 'Panduan untuk Pemilik Brand')
          + f'<div class="badges" style="margin-bottom:28px">{chips}</div><div class="grid-3">{article_cards()}</div>')
      + sec(section_head('Mulai dari sini', 'Baru Mengenal Jasa Maklon?')
            + f'<div class="callout"><p>Mulailah dengan <a href="/id/wawasan/{featured["slug"]}/" style="color:var(--secondary);font-weight:700">{E(featured["title"])}</a>, lalu baca panduan tentang OEM, ODM, dan private label untuk memilih cara bekerja sama dengan pabrik.</p></div>', 'white'))
for a in C.ARTICLES:
    path = f'/id/wawasan/{a["slug"]}/'
    body_html = ''
    for h, paras in a['body']:
        body_html += f'<h2>{E(h)}</h2>'
        if len(paras) > 1 and all(len(p) < 110 for p in paras):
            body_html += '<ul>' + ''.join(f'<li>{E(p)}</li>' for p in paras) + '</ul>'
        else:
            body_html += ''.join(f'<p>{E(p)}</p>' for p in paras)
    rel = ''.join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in a['related'])
    others = [x for x in C.ARTICLES if x['slug'] != a['slug']][:3]
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "Article", "inLanguage": "id", "headline": a['title'], "description": a['desc'],
        "datePublished": a["date"] or PUB_DATE, "dateModified": a["date"] or PUB_DATE, "author": {"@type": "Organization", "name": "GoNEST"},
        "publisher": {"@type": "Organization", "name": "GoNEST"}, "mainEntityOfPage": DOMAIN + path}, ensure_ascii=False) + '</script>\n'
    body = (sec(f'<article class="prose"><p class="note">{E(a["cat"])} &middot; {E(a["read"])}</p>{body_html}'
                f'<div class="callout"><b>Terkait di situs ini</b><ul style="margin-top:8px">{rel}</ul></div></article>')
            + sec(section_head('Lanjut membaca', 'Panduan Lainnya') + f'<div class="grid-3">{article_cards(others)}</div>', 'white'))
    inner(path, a['title'], a['desc'], [('Beranda', '/id/'), ('Wawasan', '/id/wawasan/'), (a['cat'], None)], a['title'], a['desc'], body, ld, nav='/id/wawasan/')

# ================= Contact =================
opts = ''.join(f'<option value="{E(c["en"])}">{E(c["name"])}</option>' for c in CATS)
contact = head('Kontak', 'Bicara dengan GoNEST tentang produk makanan atau minuman Anda. Kirim brief lewat formulir atau WhatsApp dan dapatkan balasan dalam satu hari kerja.', '/id/kontak/') + header('/id/kontak/') + f'''
<section class="page-hero"><div class="container">
<div class="crumbs"><a href="/id/">Beranda</a> / Kontak</div>
<h1>Mari Diskusikan Produk Anda</h1>
<p class="lead">Ceritakan apa yang ingin Anda buat. Brief singkat sudah cukup untuk memulai.</p>
</div></section>

<section class="section mid"><div class="container cta-grid">
<div class="stack">
<h2>Mulai Konsultasi</h2>
<p class="lead">Tim kami membalas dalam satu hari kerja dengan pertanyaan dan langkah berikutnya.</p>
<div class="contact-lines"><span>WhatsApp: {E(C.K.SETTINGS["whatsapp_display"])}</span><span>Email: {E(C.K.SETTINGS["email"])}</span><span>{E(C.K.SETTINGS["hours"]["id"])}</span><span>Alamat: {E(C.K.SETTINGS["address"]["id"])}</span></div>
</div>
<form class="consult" id="consult-form">
<div class="row">
<div class="field"><label for="f-name">Nama lengkap</label><input id="f-name" type="text" required placeholder="Nama Anda"></div>
<div class="field"><label for="f-wa">Nomor WhatsApp</label><input id="f-wa" type="tel" required placeholder="08xx xxxx xxxx"></div>
</div>
<div class="row">
<div class="field"><label for="f-cat">Kategori produk</label><select id="f-cat">{opts}</select></div>
<div class="field"><label for="f-vol">Perkiraan pesanan pertama</label><select id="f-vol"><option>Di bawah 500 kg</option><option>500 sampai 1.000 kg</option><option>1.000 sampai 5.000 kg</option><option>Di atas 5.000 kg</option></select></div>
</div>
<div class="field"><label for="f-msg">Ceritakan tentang produk Anda</label><textarea id="f-msg" rows="4" placeholder="Rasa, target pasar, ide kemasan"></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-website">Kosongkan kolom ini</label><input id="f-website" type="text" tabindex="-1" autocomplete="off"></div>
<div class="form-actions"><button class="btn btn-accent" type="submit" id="send-form">Kirim Permintaan</button><button class="btn btn-outline" type="button" id="send-wa">Kirim lewat WhatsApp</button></div>
<div id="form-status" class="form-status" role="status" aria-live="polite" hidden></div>
<p class="form-note">Kami memakai data Anda hanya untuk membalas permintaan Anda. Lihat <a href="/id/kebijakan-privasi/">Kebijakan Privasi</a> kami.</p>
</form>
</div></section>

<section class="section"><div class="container">
{section_head('Pertanyaan', 'Sebelum Anda Menulis')}
{faq_html([("Secepat apa kalian membalas?", "Dalam satu hari kerja."), ("Apakah ada pesanan minimum?", "Ada. Besarnya tergantung kategori. Lihat halaman Produk untuk angkanya."), ("Bolehkah saya mengunjungi pabrik?", "Boleh, dengan perjanjian terlebih dahulu.")])}
</div></section>
''' + footer()
write('/id/kontak/', contact)

# ================= Legal =================
def legal(path, title, desc, lead, blocks):
    h = ('<article class="prose"><div class="callout"><b>Templat.</b> Teks ini adalah titik awal dan belum ditinjau oleh ahli hukum. '
         'Minta perusahaan atau penasihat hukumnya meninjau dan menyesuaikannya sebelum situs dipublikasikan.</div>'
         '<p class="note">Terakhir diperbarui: [tanggal]</p>')
    for hd, paras in blocks:
        h += f'<h2>{E(hd)}</h2>' + ''.join(f'<p>{E(p)}</p>' for p in paras)
    h += '</article>'
    inner(path, title, desc, [('Beranda', '/id/'), (title, None)], title, lead, sec(h))

legal('/id/kebijakan-privasi/', 'Kebijakan Privasi', 'Cara situs GoNEST menangani informasi pribadi.', 'Cara situs ini menangani informasi dan bagaimana informasi itu dipakai.', [
    ('Siapa kami', ['Situs ini dioperasikan oleh [nama badan hukum], dengan merek GoNEST, berlokasi di [alamat].']),
    ('Informasi yang kami terima', ['Saat Anda mengirim formulir konsultasi, kami menerima data yang Anda ketik: nama, nomor WhatsApp, kategori produk, perkiraan pesanan, dan pesan. Kami juga menerima halaman asal pengiriman dan, jika Anda datang lewat tautan kampanye, nama kampanyenya.',
                                    'Jika Anda memilih "Kirim lewat WhatsApp" atau menghubungi kami lewat WhatsApp atau email, kami menerima informasi yang Anda kirim di sana.']),
    ('Cara kami menggunakannya', ['Kami memakai data Anda untuk membalas permintaan, menyiapkan penawaran, dan menindaklanjuti proyek Anda. Kami tidak menjual informasi Anda.']),
    ('Analitik dan cookie', ['Dengan izin Anda, kami memakai Google Analytics (dan, jika diaktifkan, Microsoft Clarity) untuk memahami halaman mana yang dikunjungi dan tombol mana yang dipakai. Alat ini memasang cookie dan menerima data teknis seperti halaman yang dilihat, jenis perangkat, dan perkiraan lokasi. Tidak ada analitik yang dimuat kecuali Anda menyetujui.',
                              'Anda dapat mengubah pilihan kapan saja lewat "Pengaturan cookie" di footer. [Konfirmasi alat yang dipakai dan masa penyimpanan data sebelum peluncuran.]']),
    ('Berapa lama kami menyimpannya', ['Kami menyimpan data permintaan selama diperlukan untuk menangani permintaan dan proyek yang menyertainya, selama [jangka waktu], kecuali hukum mengharuskan lebih lama.']),
    ('Berbagi informasi', ['Kami hanya membagikan informasi kepada pihak yang membantu melayani permintaan Anda, seperti tim kami dan penyedia layanan, atau bila diwajibkan hukum.']),
    ('Pilihan Anda', ['Anda dapat meminta kami memperbaiki atau menghapus informasi tentang Anda dengan menghubungi [email].']),
    ('Perubahan', ['Kami dapat memperbarui kebijakan ini. Tanggal di bagian atas menunjukkan versi terbaru.']),
])
legal('/id/syarat-ketentuan/', 'Syarat dan Ketentuan', 'Syarat penggunaan situs GoNEST.', 'Ketentuan untuk menggunakan situs ini.', [
    ('Penggunaan situs', ['Situs ini memberikan informasi umum tentang produk dan layanan [nama badan hukum], dengan merek GoNEST. Dengan menggunakannya, Anda menyetujui syarat ini.']),
    ('Informasi dan harga', ['Harga, pesanan minimum, waktu produksi, dan angka lain di situs ini bersifat indikatif dan dapat berubah. Penawaran atau perjanjian tertulis diperlukan untuk setiap pesanan.']),
    ('Ketersediaan tidak dijamin', ['Produk dan layanan yang ditampilkan mungkin tidak tersedia untuk setiap proyek. Kami mengonfirmasi kelayakannya saat konsultasi.']),
    ('Kekayaan intelektual', ['Teks, desain, dan gambar di situs ini dimiliki [nama badan hukum] atau pemberi lisensinya. Jangan menyalinnya tanpa izin. Formula dan materi merek Anda tetap menjadi milik Anda dan ditangani dengan perjanjian kerahasiaan terpisah ketika proyek dimulai.']),
    ('Tautan ke situs lain', ['Situs ini dapat menautkan ke situs lain. Kami tidak bertanggung jawab atas isinya.']),
    ('Batasan tanggung jawab', ['Kami berupaya menjaga situs ini akurat, tetapi kami tidak menerima tanggung jawab atas kerugian yang timbul karena hanya mengandalkan informasi di sini.']),
    ('Hukum yang berlaku', ['Syarat ini diatur oleh hukum Republik Indonesia. [Konfirmasi dengan penasihat hukum.]']),
    ('Kontak', ['Pertanyaan tentang syarat ini dapat dikirim ke [email].']),
])

assert set(WRITTEN) == set(PATHMAP.values()), (set(WRITTEN) ^ set(PATHMAP.values()))
print('indonesian pages written:', len(WRITTEN))
