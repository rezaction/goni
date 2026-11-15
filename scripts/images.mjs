// Photo pipeline. Reads content/photos.json, takes each uploaded original and writes
//   public/assets/img/photos/<slot>.webp      (up to 1600 x 1067, 3:2)
//   public/assets/img/photos/<slot>-800.webp  (800 x 533, for phones)
// Any size or shape of upload is cropped to the 3:2 slot (smart crop around the busiest part)
// and compressed to WebP, so a huge or oddly shaped photo can never break the layout.
import { readFile, writeFile, mkdir, readdir, rm, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'public/assets/img/photos');
const RATIO = 3 / 2;
const MAX_W = 1600;
const SMALL_W = 800;
const QUALITY = 78;

export const slugify = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '-').replace(/^-+|-+$/g, '').replace(/--/g, '-');

export async function processImage(input, outBase) {
  const img = sharp(input, { limitInputPixels: 400e6, failOn: 'none' }).rotate();   // rotate() applies EXIF orientation
  const meta = await sharp(input, { failOn: 'none' }).rotate().metadata();
  const w0 = meta.autoOrient?.width ?? meta.width, h0 = meta.autoOrient?.height ?? meta.height;
  if (!w0 || !h0) throw new Error('not a readable image');
  // largest 3:2 area that fits in the original, never enlarged
  const fitW = Math.min(MAX_W, Math.floor(Math.min(w0, h0 * RATIO)));
  const W = Math.max(2, fitW - (fitW % 2)), H = Math.round(W / RATIO);
  const big = await img.clone().resize(W, H, { fit: 'cover', position: 'attention' }).webp({ quality: QUALITY, effort: 5 }).toBuffer();
  await writeFile(outBase + '.webp', big);
  const sw = Math.min(SMALL_W, W), sh = Math.round(sw / RATIO);
  const small = await sharp(big).resize(sw, sh).webp({ quality: QUALITY - 4, effort: 5 }).toBuffer();
  await writeFile(outBase + '-800.webp', small);
  return { w: W, h: H, bytes: big.length, smallBytes: small.length };
}

async function main() {
  const { slots } = JSON.parse(await readFile(path.join(ROOT, 'content/photos.json'), 'utf8'));
  await mkdir(OUT, { recursive: true });
  const keep = new Set();
  let ok = 0;
  for (const s of slots) {
    if (!s.image) continue;
    const slug = slugify(s.key);
    const src = path.join(ROOT, s.image.replace(/^\/+/, ''));
    try {
      await stat(src);
      const r = await processImage(src, path.join(OUT, slug));
      const orig = (await stat(src)).size;
      keep.add(slug + '.webp'); keep.add(slug + '-800.webp');
      ok++;
      console.log(`photo ${slug}: ${(orig / 1024).toFixed(0)} KB -> ${(r.bytes / 1024).toFixed(0)} KB (${r.w}x${r.h}), phone ${(r.smallBytes / 1024).toFixed(0)} KB`);
    } catch (e) {
      console.warn(`WARNING photo "${s.key}": could not process ${s.image} (${e.message}). The slot keeps its placeholder.`);
    }
  }
  // remove outputs of slots that no longer have a photo
  for (const f of await readdir(OUT)) {
    if (f.endsWith('.webp') && !keep.has(f)) await rm(path.join(OUT, f));
  }
  console.log(`photos processed: ${ok}`);
}
if (process.argv[1] === fileURLToPath(import.meta.url)) await main();
