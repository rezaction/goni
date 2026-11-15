import { onRequestPost } from '../functions/api/inquiry.js';

const calls = [];
globalThis.fetch = async (url, opts) => {
  calls.push({ url, opts });
  if (String(url).includes('fail')) return new Response('no', { status: 500 });
  return new Response('{}', { status: 200 });
};

const mk = (body, headers = {}) =>
  new Request('https://x.test/api/inquiry', { method: 'POST', headers: { 'Content-Type': 'application/json', ...headers }, body: typeof body === 'string' ? body : JSON.stringify(body) });

const good = { name: 'Rina', whatsapp: '0812-3456-7890', category: 'Coffee', volume: '500 to 1,000 kg', message: 'Hello\nworld', page: '/products/coffee/', utm: { utm_source: 'ig', evil: 'x' } };
const emailEnv = { RESEND_API_KEY: 'k', INQUIRY_TO_EMAIL: 'a@b.c', INQUIRY_FROM_EMAIL: 'GoNEST <i@b.c>' };
let pass = 0, failN = 0;
const t = (name, cond) => { cond ? pass++ : (failN++, console.log('FAIL', name)); };

let r = await onRequestPost({ request: mk(good), env: emailEnv });
t('email ok 200', r.status === 200 && (await r.json()).ok === true);
t('email sent to resend', calls.length === 1 && calls[0].url === 'https://api.resend.com/emails');
const sent = JSON.parse(calls[0].opts.body);
t('email body has name and category', sent.text.includes('Name: Rina') && sent.subject.includes('Coffee'));
t('utm whitelist', sent.text.includes('utm_source') && !sent.text.includes('evil'));

calls.length = 0;
r = await onRequestPost({ request: mk(good), env: { INQUIRY_WEBHOOK_URL: 'https://hook.test/ok' } });
t('webhook only ok', r.status === 200 && calls.length === 1 && JSON.parse(calls[0].opts.body).name === 'Rina');

calls.length = 0;
r = await onRequestPost({ request: mk(good), env: {} });
t('not configured 503', r.status === 503 && calls.length === 0);

r = await onRequestPost({ request: mk(good), env: { INQUIRY_WEBHOOK_URL: 'https://hook.test/fail' } });
t('all fail 502', r.status === 502);

r = await onRequestPost({ request: mk(good), env: { ...emailEnv, INQUIRY_WEBHOOK_URL: 'https://hook.test/fail' } });
t('one of two succeeds 200', r.status === 200);

calls.length = 0;
r = await onRequestPost({ request: mk({ ...good, website: 'spam.example' }), env: emailEnv });
t('honeypot ok but nothing sent', r.status === 200 && calls.length === 0);

r = await onRequestPost({ request: mk({ ...good, name: 'R' }), env: emailEnv });
t('short name 422', r.status === 422);
r = await onRequestPost({ request: mk({ ...good, whatsapp: 'abc' }), env: emailEnv });
t('bad phone 422', r.status === 422);
r = await onRequestPost({ request: mk('not json'), env: emailEnv });
t('bad json 400', r.status === 400);
r = await onRequestPost({ request: mk(good, { Origin: 'https://evil.test' }), env: { ...emailEnv, ALLOWED_ORIGIN: 'https://goni.test' } });
t('wrong origin 403', r.status === 403);
r = await onRequestPost({ request: mk(good, { Origin: 'https://goni.test' }), env: { ...emailEnv, ALLOWED_ORIGIN: 'https://goni.test' } });
t('right origin 200', r.status === 200);

console.log(`passed ${pass}, failed ${failN}`);
process.exit(failN ? 1 : 0);
