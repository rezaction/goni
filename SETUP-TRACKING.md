# Phase 4 setup: tracking and inquiry form

Everything below is optional until launch. The site works without it: with no GA ID there is no analytics and no cookie banner, and with no email or webhook configured the form shows a message with a WhatsApp button instead.

## 1. Inquiry form (email and CRM)

The form posts to `functions/api/inquiry.js`, a Cloudflare Pages Function. It checks the fields, ignores bots (hidden honeypot field), and forwards the inquiry by email, to a webhook, or both.

1. Create a free account at resend.com and verify your sending domain. Create an API key.
2. In Cloudflare Pages open your project > Settings > Variables and Secrets, and add:
   - `RESEND_API_KEY` (secret)
   - `INQUIRY_TO_EMAIL`: the sales inbox that should receive inquiries
   - `INQUIRY_FROM_EMAIL`: for example `GONI Website <inquiry@yourdomain.com>` (must be on the verified domain)
   - `ALLOWED_ORIGIN` (optional): `https://www.yourdomain.com`
3. Optional CRM or spreadsheet: set `INQUIRY_WEBHOOK_URL` to a webhook (Google Apps Script web app, Zapier, Make, or a CRM form endpoint). It receives a JSON body with name, whatsapp, category, volume, message, page, referrer, utm and receivedAt.
4. Redeploy, then send a test inquiry from the Contact page.

If delivery fails, the visitor sees a message with a button that opens WhatsApp with the same details, so no inquiry is lost.

Local test: copy `.dev.vars.example` to `.dev.vars`, then run `npx wrangler pages dev`.

## 2. Google Analytics 4

1. Create a GA4 property and a Web data stream. Copy the Measurement ID (`G-XXXXXXXXXX`).
2. Put it in `public/assets/js/main.js` as `GA_ID`. Redeploy.
3. A cookie banner then appears. Analytics load only after a visitor clicks Accept. "Cookie settings" appears in the footer so visitors can change their choice.

Events the site sends (after consent):

| Event | When | Useful parameters |
|---|---|---|
| `generate_lead` | A visitor sends the form, or uses Send via WhatsApp | `method` (form or whatsapp), `product_category`, `estimated_order` |
| `whatsapp_click` | Any WhatsApp link or button is clicked | `link_location` (floating_button, page, form, form_fallback) |
| `cta_click` | A button that leads to the Contact page is clicked | `cta_text` |

In GA4: Admin > Events, then mark `generate_lead` as a key event. In Admin > Custom definitions, add `product_category` and `link_location` as event-scoped dimensions to report on them.

Campaign links: add `?utm_source=...&utm_medium=...&utm_campaign=...` to links you share. The site remembers them for the visit and includes them in the inquiry email, so sales can see where each lead came from.

## 3. Google Search Console

1. Add your domain as a property in Search Console and verify it. For a domain on Cloudflare, the DNS TXT record method is easiest and needs no code change.
2. In the sitemaps section, submit `https://yourdomain.com/sitemap.xml`.
3. After a few days, open Pages and Performance to see which searches reach which pages.
4. Replace `https://www.goni.example` with the real domain in all pages (English and `id/`), `sitemap.xml` and `robots.txt` first, so canonical links, hreflang tags and the sitemap are correct.
5. In Performance, filter by page path (`/id/`) to see Indonesian-language traffic separately.

The inquiry email also says whether the visitor used the English or the Indonesian site.

## 4. Visitor behavior (optional)

Create a free Microsoft Clarity project and put its ID in `CLARITY_ID` in `main.js`. It loads only after consent and provides heatmaps and session recordings.

## 5. What to review monthly

- Inquiries by category (`generate_lead` with `product_category`), and by campaign source.
- Which pages bring visitors who then click WhatsApp or send the form.
- Search Console: queries with many impressions but few clicks. Improve the title and description of those pages.
- Pages with traffic but no inquiries. Check the call to action and the answers to common questions.
