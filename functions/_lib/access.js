// Verifies the Cloudflare Access login (the Cf-Access-Jwt-Assertion header) so that the dashboard
// and its API stay closed even if the Access policy is misconfigured. Fails closed.
//
// Environment variables:
//   ACCESS_TEAM_DOMAIN   e.g. yourteam.cloudflareaccess.com
//   ACCESS_AUD           the Application Audience (AUD) tag of the Access application
//   ALLOW_INSECURE_ADMIN set to "1" ONLY in .dev.vars for local testing. Never in production.

let certCache = { at: 0, keys: null, team: '' };

const b64uToBytes = (s) => {
  const pad = '='.repeat((4 - (s.length % 4)) % 4);
  const bin = atob(s.replace(/-/g, '+').replace(/_/g, '/') + pad);
  return Uint8Array.from(bin, (c) => c.charCodeAt(0));
};
const b64uToJson = (s) => JSON.parse(new TextDecoder().decode(b64uToBytes(s)));

async function getKeys(team, fetchImpl) {
  const now = Date.now();
  if (certCache.keys && certCache.team === team && now - certCache.at < 10 * 60 * 1000) return certCache.keys;
  const res = await fetchImpl(`https://${team}/cdn-cgi/access/certs`);
  if (!res.ok) throw new Error('certs_unavailable');
  const { keys } = await res.json();
  certCache = { at: now, keys, team };
  return keys;
}

export function resetCertCache() { certCache = { at: 0, keys: null, team: '' }; }

/** Returns { ok: true, email } or { ok: false, status, error }. */
export async function verifyAccess(request, env, fetchImpl = fetch) {
  if (env.ALLOW_INSECURE_ADMIN === '1') return { ok: true, email: 'local-dev' };
  const team = (env.ACCESS_TEAM_DOMAIN || '').replace(/^https?:\/\//, '').replace(/\/$/, '');
  const aud = env.ACCESS_AUD || '';
  if (!team || !aud) return { ok: false, status: 503, error: 'access_not_configured' };

  const token = request.headers.get('Cf-Access-Jwt-Assertion');
  if (!token) return { ok: false, status: 403, error: 'login_required' };
  const parts = token.split('.');
  if (parts.length !== 3) return { ok: false, status: 403, error: 'bad_token' };

  try {
    const header = b64uToJson(parts[0]);
    const payload = b64uToJson(parts[1]);
    if (header.alg !== 'RS256') return { ok: false, status: 403, error: 'bad_token' };

    let keys = await getKeys(team, fetchImpl);
    let jwk = keys.find((k) => k.kid === header.kid);
    if (!jwk) { resetCertCache(); keys = await getKeys(team, fetchImpl); jwk = keys.find((k) => k.kid === header.kid); }
    if (!jwk) return { ok: false, status: 403, error: 'unknown_key' };

    const key = await crypto.subtle.importKey('jwk', jwk, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
    const valid = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64uToBytes(parts[2]), new TextEncoder().encode(parts[0] + '.' + parts[1]));
    if (!valid) return { ok: false, status: 403, error: 'bad_signature' };

    const now = Math.floor(Date.now() / 1000);
    const auds = Array.isArray(payload.aud) ? payload.aud : [payload.aud];
    if (payload.iss !== `https://${team}`) return { ok: false, status: 403, error: 'bad_issuer' };
    if (!auds.includes(aud)) return { ok: false, status: 403, error: 'bad_audience' };
    if (typeof payload.exp !== 'number' || payload.exp <= now) return { ok: false, status: 403, error: 'expired' };
    if (typeof payload.nbf === 'number' && payload.nbf > now + 30) return { ok: false, status: 403, error: 'not_yet_valid' };
    return { ok: true, email: payload.email || payload.sub || '' };
  } catch (e) {
    return { ok: false, status: 403, error: 'bad_token' };
  }
}

export async function guard({ request, env, next }) {
  const r = await verifyAccess(request, env);
  if (!r.ok) {
    return new Response(JSON.stringify({ ok: false, error: r.error }), {
      status: r.status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    });
  }
  const res = await next();
  const out = new Response(res.body, res);
  out.headers.set('Cache-Control', 'no-store');
  return out;
}
