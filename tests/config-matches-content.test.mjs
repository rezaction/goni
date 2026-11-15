// The dashboard form must be able to edit every field in the content files, and nothing it saves may be unknown to the generator.
import { readFileSync, readdirSync } from 'node:fs';
import vm from 'node:vm';
const ctx = { window: { location: { origin: 'https://x.test' } } };
vm.createContext(ctx);
vm.runInContext(readFileSync(new URL('../public/admin/config.js', import.meta.url), 'utf8'), ctx);
const cfg = ctx.window.GONEST_CMS_CONFIG;
let bad = 0;
const fail = (m) => { bad++; console.log('FAIL', m); };

function check(fields, data, where) {
  const names = new Map(fields.map((f) => [f.name, f]));
  for (const k of Object.keys(data)) if (!names.has(k)) fail(`${where}: "${k}" is in the content but not in the dashboard form`);
  for (const f of fields) {
    const v = data[f.name];
    if (v === undefined) { if (f.required !== false && f.widget !== 'boolean') fail(`${where}: required field "${f.name}" missing in content`); continue; }
    if (f.widget === 'object') check(f.fields, v, `${where}.${f.name}`);
    if (f.widget === 'list') {
      if (!Array.isArray(v)) { fail(`${where}.${f.name} should be a list`); continue; }
      v.forEach((item, i) => f.fields ? check(f.fields, item, `${where}.${f.name}[${i}]`) : (typeof item !== 'string' && fail(`${where}.${f.name}[${i}] should be text`)));
    }
  }
}
const root = new URL('../', import.meta.url).pathname;
const names = cfg.collections.map((c) => c.name);
for (const c of cfg.collections) {
  if (c.folder) {
    for (const f of readdirSync(root + c.folder)) {
      if (!f.endsWith('.json')) continue;
      const d = JSON.parse(readFileSync(root + c.folder + '/' + f, 'utf8'));
      check(c.fields, d, `${c.name}/${f}`);
      const idv = d[c.identifier_field];
      if (idv + '.json' !== f) fail(`${c.name}/${f}: file name must equal ${c.identifier_field} ("${idv}")`);
    }
  } else for (const file of c.files) check(file.fields, JSON.parse(readFileSync(root + file.file, 'utf8')), file.file);
  const rels = JSON.stringify(c).match(/"collection":"([a-z]+)"/g) || [];
  for (const r of rels) if (!names.includes(r.split('"')[3])) fail(`relation to missing collection ${r}`);
}
console.log(bad ? `failed ${bad}` : 'dashboard form matches content files');
process.exit(bad ? 1 : 0);
