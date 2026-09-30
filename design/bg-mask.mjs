// Writes a soft subject mask (PNG, alpha channel) for one photo.
//   node design/bg-mask.mjs in.png out.png
// Called by enhance-photo.py --black-bg. Needs `npm install` in design/ once.
import { removeBackground } from '@imgly/background-removal-node';
import fs from 'fs';

const [src, out] = process.argv.slice(2);
const blob = await removeBackground(
  new Blob([fs.readFileSync(src)], { type: 'image/png' }),
  { model: 'medium', output: { format: 'image/png', type: 'mask' } });
fs.writeFileSync(out, Buffer.from(await blob.arrayBuffer()));
