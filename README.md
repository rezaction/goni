# GoNEST website

A bilingual website (English at `/`, Indonesian at `/id/`, 35 pages each) managed from a dashboard. Plain HTML, CSS and JavaScript on the visitor's side, with a small Cloudflare Pages Function for the contact form, the login check and the inquiry inbox.

## How it fits together

    content/        All editable content as JSON (what the dashboard edits)
    uploads/        Original photos uploaded from the dashboard
    scripts/        build.py (pages), images.mjs (photos to WebP), content.py, build_en.py, build_id.py
    public/         The built website. Cloudflare publishes this folder.
    public/admin/   Dashboard (Decap CMS) and the inquiry inbox
    functions/      Form endpoint, inbox API, Cloudflare Access check, GitHub login hand-off
    migrations/     Database table for the inbox
    tests/          Automated tests: npm test
    brand/          Original logo file

Flow: an editor saves in the dashboard, which commits to GitHub. Cloudflare runs `npm install && npm run build`, which converts photos and rebuilds all pages from `content/`, then publishes `public/`.

## Set up

Follow `SETUP-DASHBOARD.md` (login, GitHub, database). Then `SETUP-TRACKING.md` (email delivery, Google Analytics, Search Console). Photos: `SETUP-DASHBOARD.md`, "How photos work".

## Local preview

    npm install
    npm run build
    python3 -m http.server 8080 --directory public

Open http://localhost:8080. The form shows its WhatsApp fallback locally, because Functions only run on Cloudflare (or with `npx wrangler pages dev`).

## Demo mode

While `Settings > Demo mode` is ticked in the dashboard, the site shows the yellow marquee above the header and below the footer ("DESIGN DEMO BY GOLDEN NESTLING ...") and tells Google not to index it (`noindex` header and `Disallow: /`). Untick it to launch.

## Replace before launch (in the dashboard unless noted)

- Settings: domain, WhatsApp number, email, address, office hours, home page numbers, analytics IDs, demo mode.
- Products and prices, portfolio projects, testimonials and articles are sample data. Replace or delete them. Publish only projects and testimonials the brand owner has approved.
- Photos: upload real photos for each slot.
- In code (`scripts/build_en.py`, `scripts/build_id.py`): About, Services, How It Works text; certification badges and tables (BPOM, Halal, HACCP, ISO 22000) are placeholders, show only certificates the company holds; `[brackets]` in the legal templates (have a legal adviser review them).
- Have a native reader review the Indonesian text.

## Tests

    npm test

Covers the form function, the Access token check (forged, expired, wrong audience, missing configuration), the inbox API, the GitHub login hand-off, and that the dashboard form matches every field in `content/`.
