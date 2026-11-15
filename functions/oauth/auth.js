// Step 1 of the GitHub login used by the dashboard (Decap CMS). Sends the editor to GitHub.
// Environment: GITHUB_CLIENT_ID (text), GITHUB_CLIENT_SECRET (secret). Created at github.com > Settings > Developer settings > OAuth Apps.
// The Authorization callback URL of that OAuth app must be https://YOUR-DOMAIN/oauth/callback
export async function onRequestGet({ request, env }) {
  if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) {
    return new Response('GitHub login is not configured (GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET).', { status: 503 });
  }
  const url = new URL(request.url);
  const state = crypto.randomUUID();
  const gh = new URL('https://github.com/login/oauth/authorize');
  gh.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
  gh.searchParams.set('redirect_uri', `${url.origin}/oauth/callback`);
  gh.searchParams.set('scope', url.searchParams.get('scope') || 'repo,user');
  gh.searchParams.set('state', state);
  return new Response(null, {
    status: 302,
    headers: { Location: gh.toString(), 'Set-Cookie': `oauth_state=${state}; HttpOnly; Secure; SameSite=Lax; Path=/oauth; Max-Age=600`, 'Cache-Control': 'no-store' },
  });
}
