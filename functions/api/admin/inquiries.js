// Dashboard inbox API. Protected by functions/api/admin/_middleware.js (Cloudflare Access login).
//   GET    /api/admin/inquiries?status=new&q=text&limit=50&before=ID   list (newest first)
//   GET    /api/admin/inquiries?format=csv                             export everything as CSV
//   PATCH  /api/admin/inquiries   { id, status?, note? }               update one inquiry
//   DELETE /api/admin/inquiries?id=ID                                  delete one inquiry
const STATUSES = ['new', 'contacted', 'quoted', 'won', 'lost', 'spam'];
const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });

const csvCell = (v) => {
  let s = String(v ?? '');
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s;            // stop spreadsheet formula injection
  return '"' + s.replace(/"/g, '""') + '"';
};

function needDb(env) {
  return env.DB ? null : json({ ok: false, error: 'database_not_configured' }, 503);
}

export async function onRequestGet({ request, env }) {
  const noDb = needDb(env); if (noDb) return noDb;
  const url = new URL(request.url);

  if (url.searchParams.get('format') === 'csv') {
    const { results } = await env.DB.prepare('SELECT * FROM inquiries ORDER BY id DESC LIMIT 5000').all();
    const cols = ['id', 'created_at', 'status', 'name', 'whatsapp', 'category', 'volume', 'message', 'page', 'lang', 'referrer', 'utm', 'note'];
    const csv = [cols.join(',')].concat(results.map((r) => cols.map((c) => csvCell(r[c])).join(','))).join('\r\n');
    return new Response('﻿' + csv, { headers: { 'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': 'attachment; filename="inquiries.csv"', 'Cache-Control': 'no-store' } });
  }

  const status = url.searchParams.get('status') || '';
  const q = (url.searchParams.get('q') || '').trim().slice(0, 80);
  const limit = Math.min(Math.max(parseInt(url.searchParams.get('limit') || '50', 10) || 50, 1), 200);
  const before = parseInt(url.searchParams.get('before') || '0', 10) || 0;

  const where = [], args = [];
  if (STATUSES.includes(status)) { where.push('status = ?'); args.push(status); }
  if (q) {
    where.push('(name LIKE ? ESCAPE \'\\\' OR whatsapp LIKE ? ESCAPE \'\\\' OR message LIKE ? ESCAPE \'\\\' OR category LIKE ? ESCAPE \'\\\')');
    const like = '%' + q.replace(/[\\%_]/g, (m) => '\\' + m) + '%';
    args.push(like, like, like, like);
  }
  if (before) { where.push('id < ?'); args.push(before); }
  const sql = 'SELECT * FROM inquiries' + (where.length ? ' WHERE ' + where.join(' AND ') : '') + ' ORDER BY id DESC LIMIT ?';
  const { results } = await env.DB.prepare(sql).bind(...args, limit).all();
  const counts = await env.DB.prepare('SELECT status, COUNT(*) AS n FROM inquiries GROUP BY status').all();
  return json({
    ok: true,
    items: results.map((r) => ({ ...r, utm: safeJson(r.utm) })),
    counts: Object.fromEntries(counts.results.map((c) => [c.status, c.n])),
    next: results.length === limit ? results[results.length - 1].id : null,
  });
}

function safeJson(s) { try { return JSON.parse(s || '{}'); } catch (e) { return {}; } }

export async function onRequestPatch({ request, env }) {
  const noDb = needDb(env); if (noDb) return noDb;
  let b; try { b = await request.json(); } catch (e) { return json({ ok: false, error: 'invalid_json' }, 400); }
  const id = parseInt(b && b.id, 10);
  if (!id) return json({ ok: false, error: 'id_required' }, 400);
  const sets = [], args = [];
  if (b.status !== undefined) {
    if (!STATUSES.includes(b.status)) return json({ ok: false, error: 'bad_status' }, 422);
    sets.push('status = ?'); args.push(b.status);
  }
  if (b.note !== undefined) { sets.push('note = ?'); args.push(String(b.note).slice(0, 2000)); }
  if (!sets.length) return json({ ok: false, error: 'nothing_to_update' }, 400);
  const r = await env.DB.prepare(`UPDATE inquiries SET ${sets.join(', ')} WHERE id = ?`).bind(...args, id).run();
  if (!r.meta || r.meta.changes === 0) return json({ ok: false, error: 'not_found' }, 404);
  return json({ ok: true });
}

export async function onRequestDelete({ request, env }) {
  const noDb = needDb(env); if (noDb) return noDb;
  const id = parseInt(new URL(request.url).searchParams.get('id'), 10);
  if (!id) return json({ ok: false, error: 'id_required' }, 400);
  const r = await env.DB.prepare('DELETE FROM inquiries WHERE id = ?').bind(id).run();
  if (!r.meta || r.meta.changes === 0) return json({ ok: false, error: 'not_found' }, 404);
  return json({ ok: true });
}

export async function onRequest() {
  return json({ ok: false, error: 'method_not_allowed' }, 405);
}
