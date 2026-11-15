export async function onRequest({ request, env, next }) {
  const expected = env.INBOX_ADMIN_KEY || '';
  const supplied = request.headers.get('X-Inbox-Key') || '';

  let diff = supplied.length ^ expected.length;
  for (let i = 0; i < Math.max(supplied.length, expected.length); i++) {
    diff |= (supplied.charCodeAt(i) || 0) ^ (expected.charCodeAt(i) || 0);
  }

  if (!expected || diff !== 0) {
    return new Response(JSON.stringify({ ok: false, error: 'unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
    });
  }

  const response = await next();
  const out = new Response(response.body, response);
  out.headers.set('Cache-Control', 'no-store');
  return out;
}
