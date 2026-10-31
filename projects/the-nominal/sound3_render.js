// Project 20, session 3, sound check (SESSION3.md, P8), step 1: render the work's own strike() offline in headless Chromium for four
// positions and write the samples. Usage: node sound3_render.js <work index.html> <out.json>
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(process.argv[2]));
  const out = await p.evaluate(async () => {
    const res = {};
    for (const o of [-50, -19.8, 0, 25]) {
      const sr = 44100, ctx = new OfflineAudioContext(1, sr * 1.2, sr);
      const f = 440 * Math.pow(2, o / 1200);
      window.__betweenTheKeys.strike(ctx, ctx.destination, 0, f, 0.5);
      const buf = await ctx.startRendering();
      res[o] = { asked_hz: f, sr: sr, samples: Array.from(buf.getChannelData(0).slice(0, sr * 1.1)) };
    }
    return res;
  });
  fs.writeFileSync(process.argv[3], JSON.stringify(out)); await b.close(); console.log('rendered', Object.keys(out));
})();
