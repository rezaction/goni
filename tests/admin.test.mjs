import { DatabaseSync } from 'node:sqlite';
import { readFileSync } from 'node:fs';
import { verifyAccess, guard, resetCertCache } from '../functions/_lib/access.js';
import * as inquiries from '../functions/api/admin/inquiries.js';
import { onRequestPost as submit } from '../functions/api/inquiry.js';
import * as oauthCb from '../functions/oauth/callback.js';
import * as oauthAuth from '../functions/oauth/auth.js';

let pass = 0, failN = 0;
const t = (name, cond) => { cond ? pass++ : (failN++, console.log('FAIL', name)); };

// ---- a fake Cloudflare Access: real RSA keys, JWTs signed like Access does ----
const TEAM = 'acme.cloudflareaccess.com', AUD = 'aud123';
const kp = await crypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
const other = await crypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
const pub = { ...(await crypto.subtle.exportKey('jwk', kp.publicKey)), kid: 'k1', alg: 'RS256' };
const b64u = (buf) => Buffer.from(buf).toString('base64url');
async function jwt(payload, key = kp.privateKey, header = { alg: 'RS256', kid: 'k1' }) {
  const h = b64u(JSON.stringify(header)), p = b64u(JSON.stringify(payload));
  const sig = await crypto.subtle.sign('RSASSA-PKCS1-v1_5', key, new TextEncoder().encode(h + '.' + p));
  return `${h}.${p}.${b64u(sig)}`;
}
const now = Math.floor(Date.now() / 1000);
const good = { iss: `https://${TEAM}`, aud: [AUD], exp: now + 600, email: 'boss@acme.test' };
let certHits = 0;
const fetchStub = async (url) => { certHits++; return String(url) === `https://${TEAM}/cdn-cgi/access/certs` ? new Response(JSON.stringify({ keys: [pub] })) : new Response('no', { status: 404 }); };
const env = { ACCESS_TEAM_DOMAIN: TEAM, ACCESS_AUD: AUD };
const req = (token, url = 'https://x.test/api/admin/inquiries', init = {}) => new Request(url, { ...init, headers: { ...(token ? { 'Cf-Access-Jwt-Assertion': token } : {}), ...(init.headers || {}) } });

let r = await verifyAccess(req(await jwt(good)), env, fetchStub);
t('valid token accepted', r.ok && r.email === 'boss@acme.test');
const hits = certHits; await verifyAccess(req(await jwt(good)), env, fetchStub);
t('certs cached', certHits === hits);
t('no header refused', (await verifyAccess(req(null), env, fetchStub)).status === 403);
t('not configured is 503 (fails closed)', (await verifyAccess(req(await jwt(good)), {}, fetchStub)).status === 503);
t('expired refused', (await verifyAccess(req(await jwt({ ...good, exp: now - 5 })), env, fetchStub)).error === 'expired');
t('wrong audience refused', (await verifyAccess(req(await jwt({ ...good, aud: ['nope'] })), env, fetchStub)).error === 'bad_audience');
t('wrong issuer refused', (await verifyAccess(req(await jwt({ ...good, iss: 'https://evil.test' })), env, fetchStub)).error === 'bad_issuer');
t('forged signature refused', (await verifyAccess(req(await jwt(good, other.privateKey)), env, fetchStub)).error === 'bad_signature');
t('alg none refused', !(await verifyAccess(req(await jwt(good, kp.privateKey, { alg: 'none', kid: 'k1' })), env, fetchStub)).ok);
t('garbage token refused', !(await verifyAccess(req('a.b.c'), env, fetchStub)).ok);
t('tampered payload refused', !(await verifyAccess(req((await jwt(good)).split('.').map((x, i) => i === 1 ? b64u(JSON.stringify({ ...good, email: 'x@y.z', exp: now + 99999 })) : x).join('.')), env, fetchStub)).ok);
t('insecure dev flag works', (await verifyAccess(req(null), { ALLOW_INSECURE_ADMIN: '1' }, fetchStub)).ok);

// guard uses global fetch for certs
globalThis.fetch = fetchStub; resetCertCache();
let nextCalled = 0;
const next = async () => { nextCalled++; return new Response('secret page'); };
let res = await guard({ request: req(null), env, next });
t('guard blocks without login', res.status === 403 && nextCalled === 0);
res = await guard({ request: req(await jwt(good)), env, next });
t('guard passes with login + no-store', res.status === 200 && nextCalled === 1 && res.headers.get('Cache-Control') === 'no-store');
res = await guard({ request: req(null), env: {}, next });
t('guard blocks when Access not configured', res.status === 503);

// ---- D1 stand-in on node:sqlite ----
const sql = new DatabaseSync(':memory:');
sql.exec(readFileSync(new URL('../migrations/0001_inquiries.sql', import.meta.url), 'utf8'));
const DB = { prepare(q) { let args = []; const o = {
  bind(...a) { args = a; return o; },
  async all() { return { results: sql.prepare(q).all(...args) }; },
  async run() { const x = sql.prepare(q).run(...args); return { meta: { changes: Number(x.changes) } }; } }; return o; } };
const dbEnv = { DB };

const mk = (body) => new Request('https://x.test/api/inquiry', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
const lead = { name: 'Rina', whatsapp: '0812-3456-7890', category: 'Coffee', volume: '1,000 kg', message: '<script>alert(1)</script>', page: '/contact/', lang: 'id', utm: { utm_source: 'ig' } };
r = await submit({ request: mk(lead), env: dbEnv });
t('form saves to the database only (no email set)', r.status === 200 && sql.prepare('SELECT COUNT(*) n FROM inquiries').get().n === 1);
await submit({ request: mk({ ...lead, name: 'Budi "=cmd"', whatsapp: '0811 000 0000' }), env: dbEnv });
r = await submit({ request: mk(lead), env: { DB: { prepare() { throw new Error('db down'); } } } });
t('db failure alone is a 502, not silent', r.status === 502);

// ---- inbox API ----
const g = (qs = '') => inquiries.onRequestGet({ request: new Request('https://x.test/api/admin/inquiries' + qs), env: dbEnv });
let j = await (await g()).json();
t('list newest first with counts', j.ok && j.items.length === 3 || j.items.length === 2);
t('utm parsed', j.items.some((i) => i.utm.utm_source === 'ig'));
t('message stored raw (the page shows it as text)', j.items.some((i) => i.message.includes('<script>')));
const firstId = j.items[j.items.length - 1].id;
r = await inquiries.onRequestPatch({ request: new Request('https://x', { method: 'PATCH', body: JSON.stringify({ id: firstId, status: 'contacted', note: 'called' }) }), env: dbEnv });
t('patch ok', r.status === 200);
j = await (await g('?status=contacted')).json();
t('filter by status', j.items.length === 1 && j.items[0].note === 'called');
r = await inquiries.onRequestPatch({ request: new Request('https://x', { method: 'PATCH', body: JSON.stringify({ id: firstId, status: 'bogus' }) }), env: dbEnv });
t('bad status 422', r.status === 422);
r = await inquiries.onRequestPatch({ request: new Request('https://x', { method: 'PATCH', body: JSON.stringify({ id: 9999, status: 'won' }) }), env: dbEnv });
t('unknown id 404', r.status === 404);
j = await (await g("?q=" + encodeURIComponent('%'))).json();
t('search treats % literally', j.items.length === 0);
j = await (await g('?q=Rina')).json();
t('search finds by name', j.items.length >= 1);
const csv = await (await g('?format=csv')).text();
t('csv neutralises formulas', csv.includes(`"'Budi ""=cmd"""`) || csv.includes(`"Budi ""=cmd"""`));
const bytes = new Uint8Array(await (await g('?format=csv')).arrayBuffer());
t('csv starts with BOM + header', bytes[0] === 0xEF && bytes[1] === 0xBB && bytes[2] === 0xBF && csv.startsWith('id,created_at'));
r = await inquiries.onRequestDelete({ request: new Request('https://x.test/api/admin/inquiries?id=' + firstId, { method: 'DELETE' }), env: dbEnv });
t('delete ok', r.status === 200 && sql.prepare('SELECT COUNT(*) n FROM inquiries').get().n === 1);
r = await inquiries.onRequestGet({ request: new Request('https://x.test/api/admin/inquiries'), env: {} });
t('no database 503', r.status === 503);

// ---- GitHub login hand-off ----
r = await oauthAuth.onRequestGet({ request: new Request('https://site.test/oauth/auth'), env: { GITHUB_CLIENT_ID: 'cid', GITHUB_CLIENT_SECRET: 's' } });
const loc = new URL(r.headers.get('Location'));
const state = loc.searchParams.get('state');
t('auth redirects to github with state + callback', loc.host === 'github.com' && loc.searchParams.get('redirect_uri') === 'https://site.test/oauth/callback' && state && r.headers.get('Set-Cookie').includes('HttpOnly'));
t('auth unconfigured 503', (await oauthAuth.onRequestGet({ request: new Request('https://site.test/oauth/auth'), env: {} })).status === 503);
globalThis.fetch = async (u, o) => new Response(JSON.stringify({ access_token: 'gho_token' }));
const cbReq = (st, cookie) => new Request(`https://site.test/oauth/callback?code=abc&state=${st}`, { headers: cookie ? { Cookie: `oauth_state=${cookie}` } : {} });
r = await oauthCb.onRequestGet({ request: cbReq(state, state), env: { GITHUB_CLIENT_ID: 'c', GITHUB_CLIENT_SECRET: 's' } });
let body = await r.text();
t('callback hands token to dashboard', r.status === 200 && body.includes('authorization:github:') && body.includes('gho_token'));
r = await oauthCb.onRequestGet({ request: cbReq(state, 'different'), env: {} });
t('callback rejects bad state (CSRF)', r.status === 400 && !(await r.text()).includes('gho_token'));
r = await oauthCb.onRequestGet({ request: cbReq(state, null), env: {} });
t('callback rejects missing cookie', r.status === 400);

console.log(`passed ${pass}, failed ${failN}`);
process.exit(failN ? 1 : 0);
