#!/usr/bin/env node
/* Render verification of the practice's surfaces — the standing procedure of
 * REGISTER.md (form revision 2026-08-20), as committed code.
 *
 * First committed night 18 (record 43, 2026-09-01), after the in-session
 * verification script mis-queried the pages' class names on two consecutive
 * nights (nights 17 and 18, both caught before commit, both logged under T4):
 * a procedure that recurs nightly and errs twice the same way becomes code,
 * per the case law of the scan (night 16) and the asking script (nights 16-18).
 *
 * Checks, at 1440x900 and 390x844, for each surface: zero page errors, zero
 * console errors, no horizontal overflow — plus per-page structural counts
 * against the pages' real markup. Exits nonzero on any failure.
 *
 * Run: a static server on the repository root (e.g. python3 -m http.server
 * 8471), then `node render-check.js` [BASE=http://127.0.0.1:8471]. Needs the
 * browser-automation library (playwright) resolvable from the working
 * directory — installed per session into the scratchpad, never committed
 * (REGISTER.md, procedures).
 */
const BASE = process.env.BASE || 'http://127.0.0.1:8471';
// resolve the automation library from the working directory (the session's
// scratchpad install), not from this script's own directory in the repository
const { createRequire } = require('module');
const requireFromCwd = createRequire(require('path').join(process.cwd(), 'noop.js'));
const { chromium } = requireFromCwd('playwright');

const PAGES = [
  { path: 'index.html', probe: () => ({}) },
  { path: 'record.html', probe: () => ({}) },
  {
    path: 'works/below-the-threshold/index.html',
    probe: () => ({
      asking_entries: document.querySelectorAll('ul.askings li').length,
      ledger_error_shown: !!document.querySelector('ul.askings .err'),
    }),
    ok: (r) => r.asking_entries > 0 && !r.ledger_error_shown,
  },
  {
    path: 'works/two-nights-deep/index.html',
    probe: () => ({
      glyphs: document.querySelectorAll('ul.nights .glyph').length,
      seam_lines: document.querySelectorAll('li.seam').length,
      unwritten: document.querySelectorAll('ul.nights li.unwritten').length,
      resaid_lines: document.querySelectorAll('ul.nights .retold').length,
      legend_shown: !!document.querySelector('.legend'),
      // the readings replay (form addendum night 20): drawn and captioned
      readings_shown: !!document.getElementById('readings') &&
        !document.getElementById('readings').hidden,
      reading_marks: document.querySelectorAll('#rd-svg circle').length,
      reading_captioned:
        (document.getElementById('rd-caption') || { textContent: '' })
          .textContent.length > 0,
    }),
    ok: (r) => r.glyphs > 0 && r.seam_lines === 1 && r.legend_shown &&
      r.readings_shown && r.reading_marks > 0 && r.reading_captioned,
  },
  {
    // project 1, session 3 (night 37): the first study, built by
    // projects/earth-rotation/study-1/build.py
    path: 'projects/earth-rotation/study-1/index.html',
    probe: () => ({
      bars: document.querySelectorAll('svg.strip rect').length,
      leaps: document.querySelectorAll('svg.strip line.leap').length,
      nos: document.querySelectorAll('svg.strip line.no').length,
      play_shown: !!document.getElementById('play') &&
        getComputedStyle(document.querySelector('.controls')).display !== 'none',
    }),
    ok: (r) => r.bars > 0 && r.leaps === 26 && r.nos === 40 && r.play_shown,
  },
  {
    // project 1, session 4 (night 38): the study promoted to a work, built by
    // works/the-days-end-to-end/build.py; the same strips as the study
    path: 'works/the-days-end-to-end/index.html',
    probe: () => ({
      bars: document.querySelectorAll('svg.strip rect').length,
      leaps: document.querySelectorAll('svg.strip line.leap').length,
      nos: document.querySelectorAll('svg.strip line.no').length,
      play_shown: !!document.getElementById('play') &&
        getComputedStyle(document.querySelector('.controls')).display !== 'none',
    }),
    ok: (r) => r.bars > 0 && r.leaps === 26 && r.nos === 40 && r.play_shown,
  },
  {
    // project 7, session 3 (night 58): the work Corrected Silently, built by
    // projects/transcribers-notes/build_work.py; one square per book, and the
    // readout must answer a click
    path: 'projects/transcribers-notes/silently/index.html',
    probe: () => {
      const t = document.querySelectorAll('.field .t');
      const before = document.getElementById('r').textContent;
      if (t.length) t[t.length - 1].click();
      return {
        squares: t.length,
        listed: document.querySelectorAll('.field .t.l').length,
        hover: document.querySelectorAll('.field .t.h').length,
        none: document.querySelectorAll('.field .t.s').length,
        readout_changed: document.getElementById('r').textContent !== before,
      };
    },
    ok: (r) => r.squares === 384 && r.listed === 126 && r.hover === 17 && r.none === 241 && r.readout_changed,
  },
  {
    // project 8, session 1 (night 59): I will write, built by
    // projects/will-write/build.py; one mark per promise, twenty lanes, and
    // the sentence panel must answer a click; session 2 (night 60) adds the
    // 179 marks with a letter on their bill filed within sixty days; session 3
    // (night 61) adds the 'Outside the bills' section, no marks
    path: 'projects/will-write/index.html',
    probe: () => {
      const m = document.querySelectorAll('.ms .m');
      const before = document.getElementById('say').textContent;
      if (m.length) m[m.length - 1].click();
      return {
        marks: m.length,
        library: document.querySelectorAll('.ms .m.l').length,
        back: document.querySelectorAll('.ms .m.b').length,
        lanes: document.querySelectorAll('.lane').length,
        panel_changed: document.getElementById('say').textContent !== before,
        outside: !!document.getElementById('outside'),
      };
    },
    ok: (r) => r.outside && r.marks === 2645 && r.library === 113 && r.back === 179 && r.lanes === 20 && r.panel_changed,
  },
  {
    // project 9, session 1 (night 62): Named into the sky, built by
    // projects/minor-planet-names/build.py; one dot per honouree, living and
    // dead; the panel must answer a click; no link on any under-18 dot
    path: 'projects/minor-planet-names/index.html',
    probe: () => {
      const d = document.querySelectorAll('.d');
      const before = document.getElementById('say').textContent;
      if (d.length) d[d.length - 1].click();
      const liv = document.querySelectorAll('#liv .d');
      return {
        dots: d.length,
        living: liv.length,
        dead: document.querySelectorAll('#dead .d').length,
        year_bars: document.querySelectorAll('#yrs .yb').length,
        panel_changed: document.getElementById('say').textContent !== before,
        redated_lines: (document.querySelectorAll('svg.sl')[0] || document).querySelectorAll('.ln').length,
        lag_lines: (document.querySelectorAll('svg.sl')[1] || document).querySelectorAll('.ln').length,
      };
    },
    // session 2 (night 63): dots placed by the year of naming (12 living and 4 dead whose naming year is unknown set
    // aside, so 34 years of naming carry a citation, not 30); two line charts, 156 re-dated citations and the
    // competition-to-naming pairs
    ok: (r) => r.dots === 1719 && r.living === 1340 && r.dead === 379 && r.year_bars === 34 && r.panel_changed
      && r.redated_lines === 156 && r.lag_lines > 20,
  },
  {
    // project 9, session 3 (night 64): the work Named into the Sky, built by
    // projects/minor-planet-names/work_build.py; the age distribution alone; the panel must answer a click
    path: 'projects/minor-planet-names/named-into-the-sky/index.html',
    probe: () => {
      const d = document.querySelectorAll('.d');
      const before = document.getElementById('say').textContent;
      if (d.length) d[0].click();
      return {
        living: document.querySelectorAll('#liv .d').length,
        dead: document.querySelectorAll('#dead .d').length,
        panel_changed: document.getElementById('say').textContent !== before,
      };
    },
    ok: (r) => r.living === 1340 && r.dead === 379 && r.panel_changed,
  },
  {
    // project 10, sessions 1-3: Within sight of itself (the study), built by projects/light-characters/build.py;
    // the map is a canvas; the panel must name a pair and change when "Another pair" is pressed
    path: 'projects/light-characters/index.html',
    probe: () => {
      const before = document.getElementById('who').textContent;
      document.getElementById('next').click();
      return {
        canvas: !!document.querySelector('canvas#map'),
        lamps: document.querySelectorAll('.lamp').length,
        named: /every .* s, \d+ km apart/.test(before),
        panel_changed: document.getElementById('who').textContent !== before,
        not_for_navigation: /not for navigation/i.test(document.body.textContent),
        // session 2: the field inset and the arcs sentence
        field: !!document.querySelector('canvas#field'),
        arcs_said: /(seen together over \d+ %|never meet)/.test(document.getElementById('who').textContent),
      };
    },
    ok: (r) => r.canvas && r.lamps === 2 && r.named && r.panel_changed && r.not_for_navigation && r.field && r.arcs_said,
  },
  {
    // project 10, session 3: the work, Within Sight of Itself, built from the same template without the study's blocks;
    // the bar of five states must sum to 624 and the first pair shown must be one nothing tells apart
    path: 'projects/light-characters/within-sight-of-itself/index.html',
    probe: () => {
      const who = document.getElementById('who').textContent;
      const cells = [...document.querySelectorAll('.bar div')].map((d) => +d.style.flexGrow || +d.style.flex.split(' ')[0]);
      return {
        canvas: !!document.querySelector('canvas#map'),
        bar_sum: cells.reduce((a, b) => a + b, 0),
        first_is_remainder: /Nothing the list says tells them apart/.test(who),
        study_hidden: !/What the list says/.test(document.body.textContent),
        not_for_navigation: /not for navigation/i.test(document.body.textContent),
      };
    },
    ok: (r) => r.canvas && r.bar_sum === 624 && r.first_is_remainder && r.study_hidden && r.not_for_navigation,
  },
  {
    // project 11, sessions 1-3: After the drogue (the study), built by projects/drifters/build.py;
    // the map is a canvas; the panel must describe a drifter and change when "Another drifter" is pressed;
    // session 2 adds two bars (before/after the re-dating), the shift canvas and the re-dated map mode; session 3 a third bar
    path: 'projects/drifters/index.html',
    probe: () => {
      const before = document.getElementById('who').textContent;
      document.getElementById('next').click();
      return {
        canvas: !!document.querySelector('canvas#map'),
        bar_cells: document.querySelectorAll('.bar div').length,
        described: /days following the water, \d+ days carried/.test(before),
        panel_changed: document.getElementById('who').textContent !== before,
        shift_canvas: !!document.querySelector('canvas#shift'),
        re_mode: (() => { document.getElementById('b-re').click(); const ok = !document.getElementById('lg-re').hidden; document.getElementById('b-end').click(); return ok; })(),
        version_cells: document.querySelectorAll('table tr:nth-child(2) td').length >= 18,
      };
    },
    ok: (r) => r.canvas && r.bar_cells === 9 && r.described && r.panel_changed && r.shift_canvas && r.re_mode && r.version_cells,
  },
  {
    // project 11, session 3: the work, After the Drogue, built from the same template without the study's blocks;
    // session 3 adds a bar of the 1,022 (three cells) and a fourth map mode, the 970 dated by hand and now unreadable
    path: 'projects/drifters/after-the-drogue/index.html',
    probe: () => {
      const before = document.getElementById('who').textContent;
      document.getElementById('b-u').click();
      document.getElementById('next').click();
      const u = document.getElementById('who').textContent;
      document.getElementById('b-end').click();
      return {
        canvas: !!document.querySelector('canvas#map'),
        bar_cells: document.querySelectorAll('.bar div').length,
        described: /days following the water, \d+ days carried/.test(before),
        u_mode: /cannot be read/.test(u),
        study_hidden: !/What was predicted/.test(document.body.textContent) && !document.querySelector('table tr:nth-child(2) td:nth-child(18)'),
      };
    },
    ok: (r) => r.canvas && r.bar_cells === 9 && r.described && r.u_mode && r.study_hidden,
  },
  {
    // project 12, session 1: Depending on who's counting (the study), built by projects/worldviews/build.py;
    // the map is a canvas; choosing the Taiwan edition must report drawn-otherwise pieces; 34 editions in the select and the bars
    path: 'projects/worldviews/index.html',
    probe: () => {
      const sel = document.getElementById('ed');
      sel.value = 'twn'; sel.dispatchEvent(new Event('change'));
      const said = document.getElementById('say').textContent;
      sel.value = 'default'; sel.dispatchEvent(new Event('change'));
      return {
        canvas: !!document.querySelector('canvas#map'),
        options: sel.options.length,
        bars: document.querySelectorAll('#eb .b').length,
        twn_said: /Taiwan: \d+ pieces/.test(said),
        preds: document.querySelectorAll('table tr').length,
        // session 2: the second map, "named by no one"
        ncanvas: !!document.querySelector('canvas#nmap'),
      };
    },
    // session 3 adds a third table (six predictions): 16 rows become 23, and a link to the work
    ok: (r) => r.canvas && r.ncanvas && r.options === 34 && r.bars === 33 && r.twn_said && r.preds === 23,
  },
  {
    // project 12, session 3: the work, Each by Its Own Map, built by projects/worldviews/build_work.py;
    // two mirror canvases (China, Taiwan) and one panel per other country its own edition draws larger (13); no predictions
    path: 'projects/worldviews/each-by-its-own-map/index.html',
    probe: () => ({
      mirror: !!document.querySelector('canvas#m-chn') && !!document.querySelector('canvas#m-twn'),
      panels: document.querySelectorAll('#grid canvas').length,
      captioned: /in its own edition: [\d,]+ km²/.test(document.getElementById('c-twn').textContent),
      study_hidden: !/predict/i.test(document.body.textContent.replace(/what was predicted and what failed are on/, '')) && !document.querySelector('table'),
    }),
    ok: (r) => r.mirror && r.panels === 13 && r.captioned && r.study_hidden,
  },
  {
    // project 13, session 1: Where each game leaves (the study), built by projects/departures/build.py;
    // two inline SVG charts (36 and 37 bars), three tables, no account names.
    // Session 2 (2026-10-20): the month as one figure (coast.png, 600x1000, loaded), its first-move labels
    // and ply axis; the figure's own text is held to at least 11 CSS px (SESSION2.md, form criteria)
    path: 'projects/departures/index.html',
    probe: () => {
      const fig = document.querySelector('.fig');
      const img = fig && fig.querySelector('img');
      const txt = fig ? [...fig.querySelectorAll('span, small')] : [];
      return {
        charts: document.querySelectorAll('svg.ch').length,
        bars: [...document.querySelectorAll('svg.ch')].map((s) => s.querySelectorAll('rect').length),
        tables: document.querySelectorAll('table').length,
        figure_loaded: !!img && img.complete && img.naturalWidth === 600 && img.naturalHeight === 1000,
        figure_labels: fig ? fig.querySelectorAll('.lab > span').length : 0,
        figure_min_font: txt.length ? Math.min(...txt.map((e) => parseFloat(getComputedStyle(e).fontSize))) : 0,
        figure_labels_inside: fig ? [...fig.querySelectorAll('.lab > span')].every((e) => e.getBoundingClientRect().left >= 0) : false,
      };
    },
    ok: (r) => r.charts === 2 && r.bars[0] === 36 && r.bars[1] === 37 && r.tables === 3 &&
      r.figure_loaded && r.figure_labels >= 5 && r.figure_min_font >= 11 && r.figure_labels_inside,
  },
  {
    // project 13, session 3 (2026-10-20): Against the month, a prototype (SESSION3.md, form criteria). Plays a scripted
    // line through the page and compares the shown count with the tree's own; an illegal tap (e2 to e5) must not move;
    // then a line off the tree must say "fewer than 2"; the page's own text is held to at least 11 CSS px.
    path: 'projects/departures/piece/index.html',
    probe: () => {
      const P = window.__piece;
      if (!P) return { loaded: false };
      const cells = document.querySelectorAll('#board button').length;
      document.querySelector('[data-sq="e2"]').click(); document.querySelector('[data-sq="e5"]').click();
      const illegal_refused = !document.getElementById('moves').textContent.trim();
      const line = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6'];
      let node = P.tree.tree, expect = 0;
      for (const s of line) { const v = node[s]; expect = Array.isArray(v) ? v[0] : v; node = Array.isArray(v) ? v[1] : {}; }
      line.forEach((s) => P.play(s));
      const shown = parseInt(document.getElementById('count').textContent.replace(/,/g, ''), 10);
      const next_buttons = document.querySelectorAll('#next button').length;
      ['h4', 'h5', 'Rh3', 'Rh6', 'Rg3'].forEach((s) => P.play(s));
      const off = document.getElementById('count').textContent === 'fewer than 2' && /left the month/.test(document.getElementById('say').textContent);
      const txt = [...document.querySelectorAll('main p, main div, main button, main span')].filter((e) => e.textContent.trim() && !e.closest('#board'));
      return {
        loaded: true, cells, illegal_refused, expect, shown, next_buttons, off,
        min_font: Math.min(...txt.map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.loaded && r.cells === 64 && r.illegal_refused && r.expect > 1 && r.shown === r.expect &&
      r.next_buttons > 0 && r.off && r.min_font >= 11,
  },
  {
    // project 14, session 1 (2026-10-20): Translations of translations (the study), built by projects/indirect/build.py;
    // one inline SVG chart (two bars), three tables, fifteen chains each with its word of two readings marked.
    // Session 2 (2026-10-21) added a second chart (twelve bars, one per thing standing between a French and a Russian translation)
    // and six example cards, each an English "you" sentence with four translations (five links per card).
    path: 'projects/indirect/index.html',
    probe: () => ({
      charts2: document.querySelectorAll('svg.ch2').length,
      bars2: document.querySelectorAll('svg.ch2 rect').length,
      cards: document.querySelectorAll('.xs .xc').length,
      charts: document.querySelectorAll('svg.ch').length,
      bars: document.querySelectorAll('svg.ch rect').length,
      tables: document.querySelectorAll('table').length,
      marks: document.querySelectorAll('mark').length,
      links: document.querySelectorAll('a[href^="https://tatoeba.org/en/sentences/show/"]').length,
      min_font: Math.min(...[...document.querySelectorAll('main p, main td, main th')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
    }),
    ok: (r) => r.charts === 1 && r.bars === 2 && r.tables === 3 && r.marks === 15 && r.links === 117 && r.charts2 === 1 &&
      r.bars2 === 12 && r.cards === 6 && r.min_font >= 11,
  },
  {
    // project 14, session 3 (2026-10-21): the work Which You, built by works/which-you/build.py; thirty English "you" sentences,
    // one shown at a time with its translations in two columns and the links people made drawn between them. Probed on sentence 11
    // (13 links, 2 across the choice), reached by the next button.
    path: 'works/which-you/index.html',
    probe: async () => {
      for (let k = 0; k < 10; k++) document.getElementById('next').click();
      await new Promise((r) => setTimeout(r, 50));
      const st = document.getElementById('stage').getBoundingClientRect();
      const cards = [...document.querySelectorAll('#stage .card')];
      return {
        count: document.getElementById('count').textContent,
        cards: cards.length,
        paths: document.querySelectorAll('#lines path').length,
        cross: document.querySelectorAll('#lines path.x').length,
        inside: cards.every((c) => { const b = c.getBoundingClientRect(); return b.left >= st.left - 1 && b.right <= st.right + 1; }),
        min_font: Math.min(...[...document.querySelectorAll('main p, .card a, .card .lg')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.count === '11 / 30' && r.cards === 9 && r.paths === 13 && r.cross === 2 && r.inside && r.min_font >= 11,
  },
  {
    // project 15, session 1 (2026-10-22): What is held back (the study), built by projects/held-back/build.py; nine treaties, one
    // inline SVG strip each, one column (a group of three rects) per coded provision, 567 in all; six predictions listed.
    // Session 2 (2026-10-22, outside the schedule's hour): a tenth SVG, the years after 2014, with one titled group per arrival (38),
    // inside a scrolling wrapper; five more predictions (11 in all).
    path: 'projects/held-back/index.html',
    probe: () => ({
      strips: document.querySelectorAll('svg.ch').length,
      cols: document.querySelectorAll('svg.ch g').length,
      preds: document.querySelectorAll('ul.pr li').length,
      min_font: Math.min(...[...document.querySelectorAll('main p, main li, h3.tt')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
    }),
    ok: (r) => r.strips === 10 && r.cols === 605 && r.preds === 11 && r.min_font >= 11,
  },
  {
    // project 15, session 3 (2026-10-22, outside the schedule's hour): the work The Common Treaty, built by
    // works/the-common-treaty/build.py; nine rows of squares, one per coded provision (567), lit when every party holds itself to it.
    // Opens on 2014; probed one step later, October 2026 read from the pages: 44 outlined (common in 2014, held back now), 2 given
    // back, 47 dots for parties with a general reservation (statements made only on signing left out).
    path: 'works/the-common-treaty/index.html',
    probe: async () => {
      const first = document.getElementById('yr').textContent;
      document.getElementById('next').click();
      await new Promise((r) => setTimeout(r, 50));
      return {
        first,
        yr: document.getElementById('yr').textContent,
        rows: document.querySelectorAll('#rows .row').length,
        cells: document.querySelectorAll('#rows .c').length,
        on: document.querySelectorAll('#rows .c.on').length,
        gone: document.querySelectorAll('#rows .c.gone').length,
        back: document.querySelectorAll('#rows .c.back').length,
        gen: document.querySelectorAll('#rows .g').length,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p, .head small, .head .n')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.first === '2014' && r.yr === 'October 2026' && r.rows === 9 && r.cells === 567 && r.on === 261 && r.gone === 44 &&
      r.back === 2 && r.gen === 47 && r.fits && r.min_font >= 11,
  },
  {
    // project 16, session 1 (2026-10-22): Why stopped (the study), built by projects/why-stopped/build.py; two inline SVGs: 142 month
    // columns (2015-01 to 2026-10), and 94 lines for reasons naming a pandemic on studies the register ends before 2020; six predictions.
    path: 'projects/why-stopped/index.html',
    probe: () => {
      const s = document.querySelectorAll('svg.ch');
      return {
        svgs: s.length,
        months: s[0] ? s[0].querySelectorAll('g').length : 0,
        lines: s[1] ? s[1].querySelectorAll('g line').length : 0,
        late: s[2] ? s[2].querySelectorAll('g').length : 0,
        preds: document.querySelectorAll('ul.pr li').length,
        min_font: Math.min(...[...document.querySelectorAll('main p, main li')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    // session 2 (2026-10-23): a third SVG, 20 rows for the late lines (late2.json); a second list of six predictions.
    ok: (r) => r.svgs === 3 && r.months === 142 && r.lines === 94 && r.late === 20 && r.preds === 12 && r.min_font >= 11,
  },
  {
    // project 16, session 3 (2026-10-24 Berlin, outside the schedule's hour): the work Came and Went, built by
    // works/came-and-went/build.py from projects/why-stopped/session3.json; one SVG field of squares (one per stopped study with an end
    // whose reason names the pandemic: came above the axis, went and the rest below), each a link to the study in the register; a strip
    // for the 198 suspended; a table by year.
    path: 'works/came-and-went/index.html',
    probe: () => {
      const f = document.querySelector('svg.field'), s = document.querySelector('svg.strip');
      return {
        field: f ? f.querySelectorAll('a rect').length : 0,
        strip: s ? s.querySelectorAll('a rect').length : 0,
        rows: document.querySelectorAll('table tbody tr').length,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.field > 2000 && r.strip === 198 && r.rows > 5 && r.fits && r.min_font >= 11,
  },
  {
    // project 17, session 1 (2026-10-24 Berlin): Looked for (the study), built by projects/looked-for/build.py from session1.json and
    // result1.json; three SVGs: absences by source (ten segments and the rest), the absent share by year (77 columns, 1950-2026),
    // the check (40 squares); six predictions.
    path: 'projects/looked-for/index.html',
    probe: () => {
      const s = document.querySelectorAll('svg.ch');
      return {
        svgs: s.length,
        sources: s[0] ? s[0].querySelectorAll('g').length : 0,
        years: s[1] ? s[1].querySelectorAll('g').length : 0,
        check: s[2] ? s[2].querySelectorAll('g').length : 0,
        units: s[3] ? s[3].querySelectorAll('g').length : 0,
        years3: s[4] ? s[4].querySelectorAll('g').length : 0,
        fits: document.documentElement.scrollWidth <= innerWidth,
        preds: document.querySelectorAll('ul.pr li').length,
        min_font: Math.min(...[...document.querySelectorAll('main p, main li')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    // session 2 (night 88): a fourth SVG, 60 units (20 per source), and five more predictions.
    // session 3 (night 89): a fifth SVG, 26 years in two rows (52 marks), six more predictions; the page must not overflow.
    ok: (r) => r.svgs === 5 && r.sources === 11 && r.years === 77 && r.check === 40 && r.units === 60 && r.years3 === 52 && r.preds === 17 && r.fits && r.min_font >= 11,
  },
  {
    // project 18, session 1 (2026-10-25 Berlin): How full the disc (the study), built by projects/full-disc/build.py from
    // session1.json, check1.json and explore1.json; three SVGs: every disc in 540 ten-second columns, and two panels of 120
    // one-second columns before each ceiling; eight predictions.
    // session 2 (night 91): two more SVGs, 600 one-frame columns either side of 74:00:00 and 80:00:00; a table of five rows;
    // eight more predictions.
    // session 3 (night 92): a sixth SVG, the 70 sets that hold a disc ending at 74:00:00, one square per disc (681); eight more
    // predictions; the page must not overflow.
    path: 'projects/full-disc/index.html',
    probe: () => {
      const s = document.querySelectorAll('svg.ch');
      return {
        svgs: s.length,
        cols: s[0] ? s[0].querySelectorAll('g').length : 0,
        a: s[1] ? s[1].querySelectorAll('g').length : 0,
        b: s[2] ? s[2].querySelectorAll('g').length : 0,
        f74: s[3] ? s[3].querySelectorAll('g').length : 0,
        f80: s[4] ? s[4].querySelectorAll('g').length : 0,
        rows: document.querySelectorAll('table.tb tbody tr').length,
        discs: s[5] ? s[5].querySelectorAll('g').length : 0,
        preds: document.querySelectorAll('ul.pr li').length,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p, main li')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.svgs === 6 && r.cols === 540 && r.a === 120 && r.b === 120 && r.f74 === 600 && r.f80 === 600 && r.rows === 5 && r.discs === 681 && r.preds === 24 && r.fits && r.min_font >= 11,
  },
  {
    // project 19, session 1 (2026-10-27 Berlin): On the grid (the study), built by projects/on-the-grid/build.py from session1.json,
    // session1b.json, check1.json, explore1.json and explore1b.json; four SVGs: declared calories by tenths (40-130), declared fat by
    // hundredths (3-10 g), three bars of six kinds (18 segments), the 4-4-9 gap in 21 bins; eight predictions.
    // Session 2 (2026-10-28 Berlin): two lattices (34 lawful calorie rows by 121 serving sizes), the predicted one drawn in runs,
    // the held one with one titled cell per combination present in session2_cells.json (3,645); eight more predictions.
    // Session 3 (2026-10-29 Berlin): three bars (calories, fat, sodium) of four fates each, 12 titled segments; eight more predictions
    // (five held, three not made).
    // Session 4 (2026-10-29 Berlin, second wake): no new figure; six more predictions (all held).
    path: 'projects/on-the-grid/index.html',
    probe: () => {
      const s = document.querySelectorAll('svg.ch');
      return {
        svgs: s.length,
        cal: s[0] ? s[0].querySelectorAll('g').length : 0,
        segs: s[2] ? s[2].querySelectorAll('g').length : 0,
        bins: s[3] ? s[3].querySelectorAll('g').length : 0,
        runs: s[4] ? s[4].querySelectorAll('rect').length : 0,
        held: s[5] ? s[5].querySelectorAll('g').length : 0,
        fates: s[6] ? s[6].querySelectorAll('g').length : 0,
        preds: document.querySelectorAll('ul.pr li').length,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p, main li')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.svgs === 7 && r.cal > 100 && r.segs === 18 && r.bins === 21 && r.runs > 34 && r.held === 3645 && r.fates === 12 && r.preds === 30 && r.fits && r.min_font >= 11,
  },
  {
    // project 19, session 4 (2026-10-29 Berlin, second wake): the work As Printed, built by works/as-printed/build.py from
    // projects/on-the-grid/session3.json, panels3.json and session4.json; 120 panels (96 given back, 24 with a gap), each a link to
    // the food in FoodData Central; one bar of four fates; three tables (fates by source, by nutrient, the blind reading of packages).
    path: 'works/as-printed/index.html',
    probe: () => ({
      panels: document.querySelectorAll('a.panel').length,
      lost: document.querySelectorAll('a.panel.lost').length,
      gaps: document.querySelectorAll('a.panel.lost .row.cal .n.gap').length,
      bar: document.querySelectorAll('svg.bar rect').length,
      tables: document.querySelectorAll('table').length,
      fits: document.documentElement.scrollWidth <= innerWidth,
      min_font: Math.min(...[...document.querySelectorAll('main p')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
    }),
    ok: (r) => r.panels === 120 && r.lost === 24 && r.gaps === 24 && r.bar === 4 && r.tables === 3 && r.fits && r.min_font >= 11,
  },
  {
    // project 20, session 3 (2026-10-31 Berlin): the work Between the Keys, built by works/between-the-keys/build.py from
    // projects/the-nominal/session3.json and explore3.json; one raster (75 rows: 74 decades and a no-year row, cells drawn where rings
    // stand), one table, a Play button that sounds the rings against A = 440 (pressed here; the page must not throw).
    path: 'works/between-the-keys/index.html',
    probe: async () => {
      document.getElementById('play').click();
      await new Promise((r) => setTimeout(r, 600));
      const on = document.querySelectorAll('.rb.on').length;
      document.getElementById('stop').click();
      return {
        rows: document.querySelectorAll('svg.raster rect.rb').length,
        cells: document.querySelectorAll('svg.raster rect.c').length,
        trs: document.querySelectorAll('table tbody tr').length,
        row_lit_on_play: on,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.rows === 75 && r.cells > 2000 && r.trs === 75 && r.row_lit_on_play === 1 && r.fits && r.min_font >= 11,
  },
  {
    // project 20, session 1 (2026-10-29 Berlin, third wake): The nominal (the study), built by projects/the-nominal/build.py from
    // session1.json, check1_compare.json and explore1.json; three SVGs: rings' and bells' cents (density, 59 titled bars), medians by
    // fifty-year era (two polylines), bells by year 1300-1599; ten predictions; seven numbered sections.
    // Session 2 (2026-10-30 Berlin): a fourth SVG (rings by position between the keys, 100 titled one-cent bars), eight more
    // predictions, section 8 with one table.
    // Session 3 (2026-10-31 Berlin): section 9 (decade by decade, and the work), prose and a link; no new figure.
    path: 'projects/the-nominal/index.html',
    probe: () => {
      const s = document.querySelectorAll('svg.ch');
      return {
        svgs: s.length,
        bars: s[0] ? s[0].querySelectorAll('g').length : 0,
        lines: s[1] ? s[1].querySelectorAll('polyline').length : 0,
        years: s[2] ? s[2].querySelectorAll('g').length : 0,
        cents: s[3] ? s[3].querySelectorAll('g').length : 0,
        tables: document.querySelectorAll('main table').length,
        preds: document.querySelectorAll('ul.pr li').length,
        sections: document.querySelectorAll('h2[id]').length,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p, main li')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.svgs === 4 && r.bars > 40 && r.lines === 2 && r.years > 100 && r.cents === 100 && r.tables === 1 && r.preds === 18 && r.sections === 9 && r.fits && r.min_font >= 11,
  },
  {
    // project 21, session 1 (2026-11-01 Berlin, the schedule's wake): The number on the concrete (the study), built by
    // projects/the-number-on-the-concrete/build.py from session1.json, check1.json, explore1.json and explore1b.json; two SVGs:
    // agreement with the field of each year 1900-2026 (four polylines), out-of-step runways by last right decade (13 titled bars);
    // one table; eleven predictions; seven numbered sections.
    path: 'projects/the-number-on-the-concrete/index.html',
    probe: () => {
      const s = document.querySelectorAll('svg.ch');
      return {
        svgs: s.length,
        lines: s[0] ? s[0].querySelectorAll('polyline').length : 0,
        bars: s[1] ? s[1].querySelectorAll('g').length : 0,
        tables: document.querySelectorAll('main table').length,
        preds: document.querySelectorAll('ul.pr li').length,
        sections: document.querySelectorAll('h2[id]').length,
        fits: document.documentElement.scrollWidth <= innerWidth,
        min_font: Math.min(...[...document.querySelectorAll('main p, main li')].map((e) => parseFloat(getComputedStyle(e).fontSize))),
      };
    },
    ok: (r) => r.svgs === 2 && r.lines === 4 && r.bars === 13 && r.tables === 1 && r.preds === 11 && r.sections === 7 && r.fits && r.min_font >= 11,
  },
];

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium',
    // 2026-09-18 (night 29): this session's pre-installed chromium build has
    // dropped "old" headless, which this playwright version still requests by
    // default against an executablePath override; explicit --headless=new
    // (a later flag overrides an earlier one) launches on both old and new
    // builds and is a no-op where the default already is "new". First found
    // and fixed the same way on an orphaned branch, night 27 by another
    // session's numbering (claude/fervent-hamilton-ym8pey, commit fbd271c,
    // pull request #2) that never reached main — verified independently in
    // this session's own container before porting (nights/55-twenty-ninth-night.md).
    args: ['--headless=new'],
  });
  let failed = false;
  for (const [width, height] of [[1440, 900], [390, 844]]) {
    for (const p of PAGES) {
      const page = await browser.newPage({ viewport: { width, height } });
      const errors = [];
      page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
      page.on('console', (m) => {
        if (m.type() === 'error') errors.push('console: ' + m.text());
      });
      await page.goto(`${BASE}/${p.path}`, { waitUntil: 'networkidle' });
      await page.waitForTimeout(400);
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth > document.documentElement.clientWidth
      );
      const counts = await page.evaluate(p.probe);
      const structOk = p.ok ? p.ok(counts) : true;
      const bad = errors.length > 0 || overflow || !structOk;
      if (bad) failed = true;
      console.log(
        `${bad ? 'FAIL' : 'ok  '} ${width}x${height} ${p.path}: ` +
          `errors=${errors.length} overflow=${overflow} ${JSON.stringify(counts)}`
      );
      errors.forEach((e) => console.log('     ', e));
      await page.close();
    }
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
