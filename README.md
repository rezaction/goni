# GONI website

Static website (HTML, CSS, JavaScript) with one small serverless function for the inquiry form. Two languages: English at the root and Indonesian under `/id/`, 35 pages each. No build step for the site itself.

## Folders

    public/                 The website. This folder is what gets published.
    functions/api/inquiry.js  Cloudflare Pages Function that receives the contact form
    wrangler.toml           Cloudflare settings (output folder = public)
    PHOTOS.md               List of photo slots and the file names to use
    SETUP-TRACKING.md       Step-by-step setup for email, GA4 and Search Console
    .dev.vars.example       Example environment variables for local testing

Inside `public/`:

    English (root)                   Indonesian (/id/)
    index.html                       id/                                 Home
    about/                           id/tentang-kami/                    About, plus 4 sub-pages
    services/                        id/layanan/                         Services, plus 5 sub-pages
    how-it-works/                    id/cara-kerja/                      Process, minimum order, FAQ
    products/                        id/produk/                          Categories, plus 4 category pages
    portfolio/                       id/portofolio/                      Project list and 4 sample projects
    insights/                        id/wawasan/                         Knowledge center and 8 sample articles
    contact/                         id/kontak/                          Inquiry form
    privacy-policy/, terms/          id/kebijakan-privasi/, id/syarat-ketentuan/   Legal templates

    assets/css/style.css             Colors and fonts are tokens at the top
    assets/js/main.js                Settings (WhatsApp number, GA ID), consent, tracking, form. Texts for both languages are at the top.
    assets/img/photos/               Photos, shared by both languages
    sitemap.xml                      Lists both languages with hreflang pairs
    robots.txt, 404.html, _headers

Every English page has an Indonesian counterpart. The EN | ID switch in the header links each page to its pair, and each page carries `hreflang` tags so Google shows the right language.

## Put it online as a demo (fastest)

1. Cloudflare dashboard > Workers & Pages > Create > Pages > Upload assets.
2. Name the project (for example `goni-demo`) and drag the whole `public` folder in. Deploy. You get a free `goni-demo.pages.dev` address.
3. Before sharing it, open `public/assets/js/main.js` and set `WHATSAPP_NUMBER` to your own number (format `62812xxxxxxx`). Until you do, the WhatsApp buttons open a chat with a placeholder number.
4. The demo is set to stay out of Google (`noindex` in `public/_headers`, `Disallow: /` in `public/robots.txt`). For the real launch, delete the `X-Robots-Tag` line in `_headers` and restore robots.txt to: `User-agent: *`, `Allow: /`, and `Sitemap: https://yourdomain/sitemap.xml`.
5. The inquiry form works fully only with the Git deployment and the environment variables in `SETUP-TRACKING.md`. With a plain upload, the form shows its WhatsApp fallback, which is fine for a demo.

## Preview locally

Links start with `/`, so use a local server, not a double-click:

    python3 -m http.server 8080 --directory public

Then open http://localhost:8080. The form will show its WhatsApp fallback here, because the function only runs on Cloudflare (or with `npx wrangler pages dev`).

## Deploy to Cloudflare Pages

1. Push this folder to a GitHub repository.
2. Cloudflare Pages > Create project > Connect to Git.
3. Framework preset: None. Build command: leave empty. Build output directory: `public`.
4. Add the custom domain.
5. Follow `SETUP-TRACKING.md` to turn on the form email, analytics and Search Console.

## Replace before launch

- `public/assets/js/main.js`: `WHATSAPP_NUMBER`, `GA_ID`, and set `DEMO_MODE = false` to remove the sample-data banner.
- Domain: replace `https://www.goni.example` in all `.html` files, `sitemap.xml` and `robots.txt`.
- Sample data: prices, minimum orders, statistics, client names, testimonials, projects and machine lists are examples.
- Certification badges and tables (BPOM, Halal, HACCP, ISO 22000) are placeholders. Show only certificates the company holds.
- Photos: add JPG files named as in `PHOTOS.md` to `public/assets/img/photos/`. No code change is needed.
- Contact details (phone, email, address) on both Contact pages (`contact/` and `id/kontak/`) and in the footers.
- Indonesian text was written for this proposal. Have a native reader on the team review wording, especially the legal templates.
- Insights articles are sample drafts. Have the team review them.
- `privacy-policy/` and `terms/` are templates. Have a legal adviser review them and fill the `[brackets]`.

## Editing the site

The pages were generated from content files, so the zip holds finished HTML. To change text, edit the `.html` files directly (search for the words). Sample numbers appear in several pages, so search for a value such as `1.000 kg` or `1,000 kg` to find every place.

## Still to do (optional)

- Real photos, real company data, and client-approved portfolio projects.
- More articles in both languages, and a CMS if the team will publish often.
