# Dashboard setup (one time, about 30 minutes)

The dashboard has two parts, both under `/admin/` and both behind your Cloudflare Access login:

- **Content dashboard** (`/admin/`): edit articles, portfolio, products and prices, testimonials, settings and photos, in English and Indonesian. Saving commits to your GitHub repository, and Cloudflare rebuilds the site in about 1 to 2 minutes.
- **Inquiry inbox** (`/admin/inbox/`): every form submission is stored, with status, notes, search and CSV export.

Who can sign in needs **both**: an email allowed in Cloudflare Access (step 3) **and** a GitHub account with write access to the repository (step 2). Access protects the pages and the inbox; GitHub decides who may change content.

## 1. Publish from GitHub to Cloudflare Pages

1. Push this folder to a GitHub repository (private is fine). Note its name, like `yourname/gonest-website`.
2. Cloudflare > Workers & Pages > Create > Pages > Connect to Git. Pick the repository.
3. Framework preset: None. **Build command: `npm install && npm run build`**. **Build output directory: `public`**.
4. Open `public/admin/config.js` and change `REPO` to your repository name. Commit.

The build does two things: `node scripts/images.mjs` turns uploaded photos into WebP, then `python3 scripts/build.py` writes every page from `content/`. (The build image ships with Node and Python. If a build ever complains about Python, add the variable `PYTHON_VERSION` = `3.11`.)

## 2. GitHub login for the dashboard

1. GitHub > Settings > Developer settings > OAuth Apps > New OAuth App.
2. Homepage URL: `https://YOUR-DOMAIN`. Authorization callback URL: `https://YOUR-DOMAIN/oauth/callback`.
3. Copy the Client ID, create a Client secret.
4. Cloudflare Pages > your project > Settings > Variables and Secrets: add `GITHUB_CLIENT_ID` (text) and `GITHUB_CLIENT_SECRET` (secret).
5. Add each editor's GitHub account as a collaborator with Write access on the repository.

## 3. Cloudflare Access (the main login)

1. Cloudflare dashboard > Zero Trust > Access > Applications > Add an application > Self-hosted.
2. Add three paths on your domain: `/admin/*`, `/api/admin/*`, `/oauth/*`.
3. Policy: Allow, Include > Emails: the people who may use the dashboard. The default one-time PIN login (a code sent by email) needs no extra setup. The free plan covers up to 50 users.
4. After saving, open the application and copy its **Application Audience (AUD) Tag**. Your **team domain** is shown in Zero Trust > Settings (like `yourteam.cloudflareaccess.com`).
5. Add to Pages variables: `ACCESS_TEAM_DOMAIN` and `ACCESS_AUD`.

Safety net: the site also checks the Access token itself. If these two variables are missing, `/admin/*`, `/api/admin/*` and `/oauth/*` refuse everyone (HTTP 503) rather than opening up.

## 4. Inquiry inbox database

1. Cloudflare > Storage & Databases > D1 > Create database, name `gonest-inquiries`.
2. Open it > Console, paste the contents of `migrations/0001_inquiries.sql`, run it.
3. Pages project > Settings > Bindings > Add > D1 database. Variable name **`DB`**, pick `gonest-inquiries`. Redeploy.
4. Email notifications still work the same way (`SETUP-TRACKING.md`, section 1). The database is stored in addition to email or webhook.

## 5. First check

1. Open `https://YOUR-DOMAIN/admin/`. You should get the Access email-code screen, then the dashboard asking you to log in with GitHub.
2. Edit something small in Settings, press Publish, wait 1 to 2 minutes, reload the site.
3. Send a test inquiry from the Contact page. It should appear in `/admin/inbox/`.

## How photos work

In the dashboard open **Photos**, find the slot (for example "powder blending"), upload any JPG, PNG or WebP, any size, and Publish. During the build each photo is automatically:

- corrected for phone rotation,
- cropped to the 3:2 shape of the slot (the crop follows the most detailed part of the picture),
- never enlarged, limited to 1600 px wide, and saved as WebP (about 100 to 400 KB),
- also saved as an 800 px version that phones download instead.

Slots without a photo keep the dashed placeholder. A broken or unreadable upload is skipped with a warning in the build log, and the site still deploys. To remove a photo, clear the field and publish. Keep each original under about 25 MB (GitHub's limit is 100 MB).

## Day-to-day notes

- **Add an article, project, category or product**: Collections > New. The page appears in English and Indonesian, in menus, lists and the sitemap. The "URL name" becomes part of the address, so choose it carefully; changing it later changes the page address.
- **Delete** removes the page on the next build.
- **Page text that is not in the dashboard** (About, Services, How It Works, legal pages, headings and buttons) lives in `scripts/build_en.py` and `scripts/build_id.py`. Ask a developer to change it, or extend the dashboard (`public/admin/config.js` plus `scripts/content.py`).
- **Go live**: in Settings > Demo mode, untick the demo option. This removes the marquee and lets Google index the site. Also set the real domain, WhatsApp number and contact details there.
- **Brand name**: text inside pages says GoNEST directly. To rename it, search and replace in `content/`, `scripts/` and `public/assets/js/main.js`.
- **Decap version**: `public/admin/index.html` loads Decap CMS 3.x from unpkg. For a fixed version, replace `^3.1.0` with the exact version you tested.
- Local preview: `npm install && npm run build`, then `python3 -m http.server 8080 --directory public`.
