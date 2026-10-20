// P16 (SESSION3.md): chess.js writes the same SAN as python-chess for every ply of 1,000 January games (seed 20261020).
// The sample is read from scratch (argv[2]); the result is written to p16.json.
import { readFileSync, writeFileSync } from 'node:fs';
import { Chess } from './vendor/chess.js';
const games = JSON.parse(readFileSync(process.argv[2], 'utf8'));
let plies = 0, equal = 0, firstDiff = null;
for (const g of games) {
  const c = new Chess();
  for (const san of g) {
    plies++;
    let m;
    try { m = c.move(san); } catch (e) { m = null; }
    if (m && m.san === san) equal++;
    else { if (!firstDiff) firstDiff = { ply: plies, kind: m ? 'written otherwise' : 'not accepted' }; break; }
  }
}
const out = { games: games.length, plies, equal, held: plies === equal, first_difference: firstDiff };
writeFileSync('p16.json', JSON.stringify(out, null, 1));
console.log(out);
