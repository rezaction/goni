// Step 2 of the GitHub login: swaps the code for a token and hands it to the dashboard window.
const page = (status, content) => `<!doctype html><meta charset="utf-8"><body><script>
(function () {
  var msg = ${JSON.stringify(status)}, data = ${JSON.stringify(content)};
  function receive(e) {
    if (e.origin !== window.location.origin) return;
    window.opener.postMessage('authorization:github:' + msg + ':' + JSON.stringify(data), e.origin);
    window.removeEventListener('message', receive, false);
    window.close();
  }
  window.addEventListener('message', receive, false);
  window.opener && window.opener.postMessage('authorizing:github', window.location.origin);
})();
</script><p>Signing in...</p></body>`;

const html = (body, status = 200) => new Response(body, {
  status, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'Set-Cookie': 'oauth_state=; HttpOnly; Secure; SameSite=Lax; Path=/oauth; Max-Age=0' },
});

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const cookie = (request.headers.get('Cookie') || '').match(/(?:^|;\s*)oauth_state=([^;]+)/);
  if (!code || !state || !cookie || cookie[1] !== state) {
    return html(page('error', { message: 'Login could not be verified. Please try again.' }), 400);
  }
  try {
    const res = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json', 'User-Agent': 'gonest-dashboard' },
      body: JSON.stringify({ client_id: env.GITHUB_CLIENT_ID, client_secret: env.GITHUB_CLIENT_SECRET, code }),
    });
    const out = await res.json();
    if (!out.access_token) return html(page('error', { message: out.error_description || 'GitHub did not return a token.' }), 400);
    return html(page('success', { token: out.access_token, provider: 'github' }));
  } catch (e) {
    return html(page('error', { message: 'Could not reach GitHub.' }), 502);
  }
}
