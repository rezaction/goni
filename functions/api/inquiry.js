// Cloudflare Pages Function: receives the consultation form and forwards it.
//
// Environment variables (Cloudflare Pages > Settings > Variables and Secrets):
//   RESEND_API_KEY       secret   API key from resend.com (email delivery)
//   INQUIRY_TO_EMAIL     text     where inquiries are sent, e.g. sales@yourdomain.com
//   INQUIRY_FROM_EMAIL   text     verified sender, e.g. "GONI Website <inquiry@yourdomain.com>"
//   INQUIRY_WEBHOOK_URL  secret   optional: a CRM, Google Apps Script or Zapier webhook that receives the JSON
//   ALLOWED_ORIGIN       text     optional: e.g. https://www.yourdomain.com. Requests from other origins are refused.
//
// At least one of the email pair or the webhook must be configured.

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
  });

const clean = (v, max) =>
  String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f]+/g, ' ').trim().slice(0, max);

function buildInquiry(b) {
  const utm = {};
  if (b.utm && typeof b.utm === 'object') {
    for (const k of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']) {
      if (b.utm[k]) utm[k] = clean(b.utm[k], 100);
    }
  }
  return {
    name: clean(b.name, 100),
    whatsapp: clean(b.whatsapp, 30),
    category: clean(b.category, 60),
    volume: clean(b.volume, 40),
    message: String(b.message == null ? '' : b.message).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]+/g, ' ').trim().slice(0, 2000),
    page: clean(b.page, 200),
    lang: b.lang === 'id' ? 'id' : 'en',
    referrer: clean(b.referrer, 100),
    utm,
    receivedAt: new Date().toISOString(),
  };
}

function validate(d) {
  if (d.name.length < 2) return 'Please enter your name.';
  if (!/^[+0-9()\s-]{8,20}$/.test(d.whatsapp)) return 'Please enter a valid WhatsApp number.';
  return null;
}

function emailText(d) {
  const utm = Object.keys(d.utm).length ? JSON.stringify(d.utm) : '-';
  return [
    'New inquiry from the GONI website',
    '',
    `Name: ${d.name}`,
    `WhatsApp: ${d.whatsapp}`,
    `Category: ${d.category}`,
    `Estimated first order: ${d.volume}`,
    '',
    'Message:',
    d.message || '-',
    '',
    `Sent from page: ${d.page || '-'} (${d.lang === 'id' ? 'Indonesian' : 'English'} site)`,
    `Referrer: ${d.referrer || '-'}`,
    `Campaign: ${utm}`,
    `Received: ${d.receivedAt}`,
  ].join('\n');
}

async function sendEmail(env, d) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.INQUIRY_FROM_EMAIL,
      to: [env.INQUIRY_TO_EMAIL],
      subject: `New inquiry: ${d.category || 'General'} - ${d.name}`,
      text: emailText(d),
    }),
  });
  if (!res.ok) throw new Error(`email provider returned ${res.status}`);
}

async function sendWebhook(env, d) {
  const res = await fetch(env.INQUIRY_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(d),
  });
  if (!res.ok) throw new Error(`webhook returned ${res.status}`);
}

export async function onRequestPost({ request, env }) {
  const origin = request.headers.get('Origin');
  if (env.ALLOWED_ORIGIN && origin && origin !== env.ALLOWED_ORIGIN) {
    return json({ ok: false, error: 'forbidden' }, 403);
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ ok: false, error: 'invalid_json' }, 400);
  }
  if (!body || typeof body !== 'object') return json({ ok: false, error: 'invalid_json' }, 400);

  // Honeypot: real visitors never fill this hidden field. Pretend success so bots move on.
  if (body.website) return json({ ok: true });

  const inquiry = buildInquiry(body);
  const problem = validate(inquiry);
  if (problem) return json({ ok: false, error: problem }, 422);

  const tasks = [];
  if (env.RESEND_API_KEY && env.INQUIRY_TO_EMAIL && env.INQUIRY_FROM_EMAIL) tasks.push(sendEmail(env, inquiry));
  if (env.INQUIRY_WEBHOOK_URL) tasks.push(sendWebhook(env, inquiry));
  if (!tasks.length) return json({ ok: false, error: 'not_configured' }, 503);

  const results = await Promise.allSettled(tasks);
  if (!results.some((r) => r.status === 'fulfilled')) {
    return json({ ok: false, error: 'delivery_failed' }, 502);
  }
  return json({ ok: true });
}

export async function onRequest() {
  return json({ ok: false, error: 'method_not_allowed' }, 405);
}
