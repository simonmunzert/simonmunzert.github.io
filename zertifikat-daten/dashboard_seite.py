"""Erzeugt dashboard/index.html aus data/dashboard.json. Wird von build.py aufgerufen."""
import json
from pathlib import Path

ROOT = Path(__file__).parent

def fmt(n):
    return f"{n:,}".replace(",", ".")

def dashboard_body(page_fn, pages_url):
    d = json.loads((ROOT / "data" / "dashboard.json").read_text(encoding="utf-8"))
    S = d["sessions"]
    tot = lambda k: sum(s[k] for s in S)
    decks = [s for s in S if s["folien"]]
    dichteste = max(decks, key=lambda s: s["woerter_je_folie"])
    laengste = max(decks, key=lambda s: s["folien"])
    bildreich = max(decks, key=lambda s: s["bilder"] / s["folien"])
    praxis = [s for s in S if s["praxis"]]
    tag2 = sum(s["folien"] for s in S if s["tag"] == 2)
    stunden = sum(s["dauer"] for s in S)
    beobachtungen = [
        f"<strong>Session {laengste['n']}</strong> („{laengste['titel']}“) ist mit {laengste['folien']} Folien das längste Deck und zugleich das mit den meisten Links ({laengste['links']}): Visualisierung lebt von Beispielen aus dem Netz.",
        f"<strong>Session {dichteste['n']}</strong> ist mit rund {dichteste['woerter_je_folie']} Wörtern je Folie die textdichteste Session. Tabellen, XML und Standards brauchen Erklärung; <strong>Session {bildreich['n']}</strong> kommt dagegen auf gut {bildreich['bilder'] / bildreich['folien']:.1f} Bilder je Folie.",
        f"Die beiden <strong>Praxis-Sessions</strong> haben zusammen nur {sum(s['folien'] for s in praxis)} Folien, dafür {fmt(sum(s['r_zeilen'] for s in praxis))} Zeilen R-Code, {sum(s['fallstudien'] for s in praxis)} Fallstudien und {sum(s['datendateien'] for s in praxis)} Daten- und Beispieldateien.",
        f"<strong>Tag 2</strong> ist der dichteste Tag: {tag2} Folien in vier Sessions, dazu die zweite Praxis-Session. Tag 3 lässt mit dem Gastvortrag und dem Wrap-up bewusst Luft für Diskussion.",
        f"Zur Vorbereitung und Vertiefung gibt es {tot('literatur')} Literatur-, Podcast- und Link-Hinweise, im Schnitt {tot('literatur') / 10:.0f} je Session; der Gastvortrag bringt mit {max(S, key=lambda s: s['literatur'])['literatur']} die meisten mit.",
    ]
    body = r"""
<p class="breadcrumb"><a href="../index.html">Überblick</a> › Dashboard</p>
<p class="kicker">Der Kurs in Zahlen</p>
<h1>Dashboard</h1>
<p class="lead">Was steckt in drei Tagen Modul 2? Dieses Dashboard zählt, was in den Folien, Fallstudien und Materialien liegt, und zeigt, wie sich Inhalt und Zeit über die elf Sessions verteilen. Es ist zugleich ein Beispiel für Session 8: ein kleines, von Hand gebautes Dashboard ohne Framework, aus einer JSON-Datei, die ein Skript aus dem Kurs-Repository erzeugt.</p>

<div class="filters" role="group" aria-label="Filter">
  <span class="filter-label">Tag</span>
  <div class="seg" id="f-tag"><button type="button" data-v="alle" class="on">Alle</button><button type="button" data-v="1">Tag 1</button><button type="button" data-v="2">Tag 2</button><button type="button" data-v="3">Tag 3</button></div>
  <span class="filter-label">Format</span>
  <div class="seg" id="f-art"><button type="button" data-v="alle" class="on">Alle</button><button type="button" data-v="vortrag">Vortrag</button><button type="button" data-v="praxis">Praxis</button></div>
  <span class="muted filter-note">Stand: __STAND__ · <a href="#tabelle">Tabelle</a> · <a href="#methodik">Wie gezählt wurde</a></span>
</div>

<section class="kpis" id="kpis" aria-live="polite"></section>

<section class="dash-grid">
  <div class="panel panel-wide">
    <div class="panel-head">
      <div><h2 id="chart-title">Folien je Session</h2><p class="muted" id="chart-sub">Seiten der PDF-Fassung; Praxis-Session II und der Gastvortrag kommen ohne Folien aus.</p></div>
      <div class="seg seg-small" id="f-metrik" role="group" aria-label="Kennzahl">
        <button type="button" data-v="folien" class="on">Folien</button><button type="button" data-v="woerter">Wörter</button><button type="button" data-v="woerter_je_folie">Wörter je Folie</button><button type="button" data-v="bilder">Bilder</button><button type="button" data-v="links">Links</button><button type="button" data-v="uebungen">Übungen</button><button type="button" data-v="literatur">Literatur</button><button type="button" data-v="r_zeilen">R-Zeilen</button>
      </div>
    </div>
    <div class="legend" id="legend"></div>
    <div class="chart" id="bars"></div>
  </div>

  <div class="panel">
    <h2>Stundenplan</h2>
    <p class="muted">21 Stunden an drei Tagen. Fahrt mit der Maus über einen Block, klickt für Details.</p>
    <div class="chart" id="timeline"></div>
  </div>

  <div class="panel">
    <h2 id="detail-title">Session im Detail</h2>
    <p class="muted" id="detail-hint">Klickt auf einen Balken oder einen Block im Stundenplan.</p>
    <div id="detail"></div>
  </div>
</section>

<section class="two-col">
  <div>
    <h2>Was auffällt</h2>
    <ul class="plain">__BEOBACHTUNGEN__</ul>
  </div>
  <div>
    <h2 id="methodik">Wie gezählt wurde</h2>
    <ul class="plain font-small">
      <li><strong>Folien</strong>: Seiten der PDF-Fassung, also der Endzustand jeder Folie (Zwischenschritte von Animationen zählen nicht).</li>
      <li><strong>Wörter</strong>: Fließtext der Rmd-Quelle ohne Code, HTML-Markup und Links. <strong>Bilder</strong>: eingebettete Grafiken und Fotos. <strong>Links</strong>: verschiedene URLs je Deck.</li>
      <li><strong>Übungen</strong>: Folien mit Diskussions- oder Übungsaufgabe (Klasse <code>exercise</code>). <strong>Literatur</strong>: Kernliteratur, Podcasts und Weiterlesen laut Session-Seiten.</li>
      <li><strong>R-Zeilen</strong>: nicht-leere Zeilen in den R-Skripten der Fallstudien und Materialien. <strong>Dateien</strong>: Materialien je Session ohne Archive und Render-Ordner.</li>
      <li>Erzeugt mit <code>dashboard_daten.py</code> aus dem <a href="https://github.com/hertie-ai-certificate/modul-2-2026">Kurs-Repository</a>; der Stand entspricht dem letzten Lauf.</li>
    </ul>
  </div>
</section>

<section>
  <h2 id="tabelle">Alle Kennzahlen</h2>
  <div class="table-wrap"><table class="grades dash-table" id="tabelle-daten"></table></div>
  <p class="muted font-small">Die Tabelle folgt den Filtern oben. <a href="../data/dashboard.json">Rohdaten als JSON</a>.</p>
</section>

<div class="tooltip" id="tt" role="tooltip" hidden></div>

<script type="application/json" id="daten">__DATEN__</script>
<script>
(function () {
  const D = JSON.parse(document.getElementById('daten').textContent);
  const S = D.sessions;
  const FARBE = { 1: '#2F6CB5', 2: '#E07A18', 3: '#C2001A' };   // Tag 1, 2, 3: feste Reihenfolge, mit validate_palette.js geprüft (CVD, Chroma, Kontrast)
  const TAGNAME = { 1: 'Tag 1 · Mo', 2: 'Tag 2 · Di', 3: 'Tag 3 · Mi' };
  const METRIK = {
    folien: ['Folien je Session', 'Seiten der PDF-Fassung; Praxis-Session II und der Gastvortrag kommen ohne Folien aus.', ''],
    woerter: ['Wörter je Session', 'Fließtext der Folien ohne Code und Markup.', ''],
    woerter_je_folie: ['Wörter je Folie', 'Textdichte: Wie viel Text trägt eine Folie im Schnitt?', ''],
    bilder: ['Bilder je Session', 'Eingebettete Grafiken, Fotos und Screenshots.', ''],
    links: ['Links je Session', 'Verschiedene Webadressen im Deck.', ''],
    uebungen: ['Übungen je Session', 'Folien mit Diskussions- oder Übungsaufgabe.', ''],
    literatur: ['Literaturhinweise je Session', 'Kernliteratur, Podcasts und Weiterlesen auf den Session-Seiten.', ''],
    r_zeilen: ['R-Code je Session', 'Nicht-leere Zeilen in den Skripten der Fallstudien und Materialien.', ' Zeilen'],
  };
  const fmt = n => (n == null ? '–' : n.toLocaleString('de-DE'));
  const $ = id => document.getElementById(id);
  let filter = { tag: 'alle', art: 'alle', metrik: 'folien' }, aktiv = null;

  function sichtbar() {
    return S.filter(s => (filter.tag === 'alle' || s.tag == filter.tag) && (filter.art === 'alle' || (filter.art === 'praxis') === s.praxis));
  }
  function seg(id, key, after) {
    $(id).addEventListener('click', e => {
      const b = e.target.closest('button'); if (!b) return;
      [...$(id).children].forEach(x => x.classList.toggle('on', x === b));
      filter[key] = b.dataset.v; after();
    });
  }
  seg('f-tag', 'tag', renderAll); seg('f-art', 'art', renderAll); seg('f-metrik', 'metrik', renderBars);

  // Tooltip
  const tt = $('tt');
  function zeigeTip(html, x, y) { tt.innerHTML = html; tt.hidden = false; const r = tt.getBoundingClientRect(); const px = Math.min(x + 14, window.innerWidth - r.width - 12); tt.style.left = px + 'px'; tt.style.top = (y + 14) + 'px'; }
  function versteckeTip() { tt.hidden = true; }
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const key = s => `<span class="key" style="background:${FARBE[s.tag]}"></span>`;

  function renderKpis() {
    const v = sichtbar(), sum = k => v.reduce((a, s) => a + s[k], 0);
    const decks = v.filter(s => s.folien);
    const std = sum('dauer');
    const tiles = [
      ['Sessions', v.length, std + ' Stunden'],
      ['Folien', sum('folien'), decks.length ? Math.round(sum('folien') / decks.length) + ' je Deck' : 'keine Folien'],
      ['Wörter', sum('woerter'), decks.length ? Math.round(sum('woerter') / sum('folien')) + ' je Folie' : ''],
      ['Bilder', sum('bilder'), decks.length ? (sum('bilder') / sum('folien')).toFixed(1).replace('.', ',') + ' je Folie' : ''],
      ['Übungen', sum('uebungen'), 'Diskussion und Aufgaben'],
      ['Literaturhinweise', sum('literatur'), 'Texte, Podcasts, Links'],
      ['Zeilen R-Code', sum('r_zeilen'), sum('fallstudien') + ' Fallstudien, ' + sum('dateien') + ' Dateien'],
    ];
    if (filter.tag === 'alle' && filter.art === 'alle') tiles.push(['Teilnehmende', D.teilnehmende, D.behoerden + ' Behörden']);
    $('kpis').innerHTML = tiles.map(t => `<div class="kpi"><span class="kpi-label">${t[0]}</span><span class="kpi-value">${fmt(t[1])}</span><span class="kpi-sub">${t[2]}</span></div>`).join('');
  }

  function renderBars() {
    const m = filter.metrik, [titel, sub, einheit] = METRIK[m];
    $('chart-title').textContent = titel; $('chart-sub').textContent = sub;
    const v = sichtbar(); const max = Math.max(1, ...v.map(s => s[m] || 0));
    const tage = [...new Set(v.map(s => s.tag))];
    $('legend').innerHTML = tage.map(t => `<span class="legend-item"><span class="key" style="background:${FARBE[t]}"></span>${TAGNAME[t]}</span>`).join('') + '<span class="legend-item"><span class="key key-praxis"></span>Praxis-Session</span>';
    const W = 640, L = 150, R = 56, rowH = 30, H = v.length * rowH + 8;
    const x = val => L + (val / max) * (W - L - R);
    const ticks = schoeneTicks(max);
    let svg = `<svg viewBox="0 0 ${W} ${H + 22}" width="100%" role="img" aria-label="${esc(titel)}">`;
    ticks.forEach(t => { svg += `<line x1="${x(t)}" x2="${x(t)}" y1="0" y2="${H}" class="grid"/><text x="${x(t)}" y="${H + 16}" class="tick" text-anchor="middle">${fmt(t)}</text>`; });
    v.forEach((s, i) => {
      const y = i * rowH + 6, val = s[m] || 0, w = Math.max(0, x(val) - L), leer = !val;
      const name = (s.praxis ? 'Praxis ' : '') + 'S' + s.n;
      svg += `<g class="bar${aktiv === s.n ? ' aktiv' : ''}" data-n="${s.n}" tabindex="0">`;
      svg += `<rect x="${L - 150}" y="${y - 3}" width="${W}" height="${rowH}" class="hit"/>`;
      svg += `<text x="${L - 10}" y="${y + 15}" class="label" text-anchor="end">${esc(name)}</text>`;
      if (leer) svg += `<text x="${L + 6}" y="${y + 15}" class="note">${s.gast ? 'Gastvortrag' : 'Fallstudien statt Folien'}</text>`;
      else {
        const r = Math.min(4, w / 2);
        svg += `<path d="M${L},${y} h${w - r} a${r},${r} 0 0 1 ${r},${r} v${18 - 2 * r} a${r},${r} 0 0 1 -${r},${r} h-${w - r} z" fill="${FARBE[s.tag]}" class="${s.praxis ? 'praxis-fill' : ''}"/>`;
        if (s.praxis) svg += `<path d="M${L},${y} h${w - r} a${r},${r} 0 0 1 ${r},${r} v${18 - 2 * r} a${r},${r} 0 0 1 -${r},${r} h-${w - r} z" fill="url(#schraffur)"/>`;
        svg += `<text x="${x(val) + 6}" y="${y + 15}" class="value">${fmt(val)}${einheit}</text>`;
      }
      svg += '</g>';
    });
    svg += `<defs><pattern id="schraffur" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#fff" stroke-width="2" stroke-opacity=".55"/></pattern></defs></svg>`;
    $('bars').innerHTML = svg;
    $('bars').querySelectorAll('.bar').forEach(g => {
      const s = S.find(z => z.n == g.dataset.n);
      g.addEventListener('mousemove', e => zeigeTip(tipHtml(s, m), e.clientX, e.clientY));
      g.addEventListener('mouseleave', versteckeTip);
      g.addEventListener('click', () => { aktiv = s.n; renderDetail(); renderBars(); renderTimeline(); });
      g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); g.click(); } });
    });
  }
  function schoeneTicks(max) {
    const roh = max / 4, p = Math.pow(10, Math.floor(Math.log10(roh))), f = roh / p;
    const step = (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p; const t = [];
    for (let v = 0; v <= max; v += step) t.push(v); return t;
  }
  function tipHtml(s, m) {
    const zeilen = [['Folien', s.folien], ['Wörter', s.woerter], ['Bilder', s.bilder], ['Übungen', s.uebungen], ['Literatur', s.literatur], ['R-Zeilen', s.r_zeilen]];
    return `<div class="tt-head">${key(s)}<strong>Session ${s.n}</strong> · ${esc(TAGNAME[s.tag])} · ${esc(s.zeit)}</div><div class="tt-title">${esc(s.titel)}</div>` +
      zeilen.map(z => `<div class="tt-row${z[0].toLowerCase().startsWith(m.slice(0, 4)) ? ' tt-on' : ''}"><strong>${fmt(z[1])}</strong><span>${z[0]}</span></div>`).join('');
  }

  function renderTimeline() {
    const v = sichtbar(); const W = 420, L = 56, T = 8, rowH = 46, h0 = 9, h1 = 19;
    const tage = [1, 2, 3]; const H = tage.length * rowH + T;
    const x = h => L + (h - h0) / (h1 - h0) * (W - L - 8);
    let svg = `<svg viewBox="0 0 ${W} ${H + 20}" width="100%" role="img" aria-label="Stundenplan">`;
    for (let h = h0; h <= h1; h += 2) svg += `<line x1="${x(h)}" x2="${x(h)}" y1="${T}" y2="${H}" class="grid"/><text x="${x(h)}" y="${H + 15}" class="tick" text-anchor="middle">${h} Uhr</text>`;
    tage.forEach((t, i) => {
      const y = T + i * rowH;
      svg += `<text x="${L - 8}" y="${y + 27}" class="label" text-anchor="end">Tag ${t}</text>`;
      S.filter(s => s.tag === t).forEach(s => {
        const an = v.includes(s), w = x(s.ende) - x(s.start) - 2;
        svg += `<g class="block${an ? '' : ' aus'}${aktiv === s.n ? ' aktiv' : ''}" data-n="${s.n}" tabindex="0"><rect x="${x(s.start) + 1}" y="${y + 8}" width="${w}" height="30" rx="4" fill="${FARBE[t]}"/>` +
          (s.praxis ? `<rect x="${x(s.start) + 1}" y="${y + 8}" width="${w}" height="30" rx="4" fill="url(#schraffur2)"/>` : '') +
          `<text x="${x(s.start) + w / 2 + 1}" y="${y + 27}" class="block-label" text-anchor="middle">S${s.n}</text></g>`;
      });
    });
    svg += `<defs><pattern id="schraffur2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#fff" stroke-width="2" stroke-opacity=".55"/></pattern></defs></svg>`;
    $('timeline').innerHTML = svg;
    $('timeline').querySelectorAll('.block').forEach(g => {
      const s = S.find(z => z.n == g.dataset.n);
      g.addEventListener('mousemove', e => zeigeTip(tipHtml(s, filter.metrik), e.clientX, e.clientY));
      g.addEventListener('mouseleave', versteckeTip);
      g.addEventListener('click', () => { aktiv = s.n; renderDetail(); renderBars(); renderTimeline(); });
      g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); g.click(); } });
    });
  }

  function renderDetail() {
    const s = S.find(z => z.n === aktiv); if (!s) return;
    $('detail-title').textContent = 'Session ' + s.n + ': ' + s.titel;
    $('detail-hint').textContent = TAGNAME[s.tag] + ' · ' + s.zeit + ' · ' + s.dauer + (s.dauer === 1 ? ' Stunde' : ' Stunden') + (s.praxis ? ' · Praxis-Session' : s.gast ? ' · Gastvortrag' : '');
    const facts = s.folien ? [['Folien', s.folien, s.folien_je_stunde + ' je Stunde'], ['Wörter', s.woerter, s.woerter_je_folie + ' je Folie'], ['Bilder', s.bilder, (s.bilder / s.folien).toFixed(1).replace('.', ',') + ' je Folie'], ['Links', s.links, ''], ['Übungen', s.uebungen, ''], ['Abschnitte', s.abschnitte, '']]
      : [['Fallstudien', s.fallstudien, ''], ['Zeilen R-Code', s.r_zeilen, ''], ['Dateien', s.dateien, s.datendateien + ' Daten- und Beispieldateien'], ['Literatur', s.literatur, '']];
    facts.push(['Literaturhinweise', s.literatur, s.kern + ' Kern · ' + s.hoeren + ' Hören · ' + s.lesen + ' Lesen']);
    const seen = new Set();
    $('detail').innerHTML = '<div class="facts-mini">' + facts.filter(f => !seen.has(f[0]) && seen.add(f[0])).map(f => `<div><span class="fact-label">${f[0]}</span><span class="fact-value">${fmt(f[1])}</span><span class="muted font-small">${f[2]}</span></div>`).join('') + '</div>' +
      `<p class="btn-row"><a class="btn btn-small" href="../sessions/s${String(s.n).padStart(2, '0')}.html">Zur Session-Seite</a></p>`;
  }

  function renderTable() {
    const v = sichtbar();
    const cols = [['n', 'Nr.'], ['titel', 'Session'], ['tag', 'Tag'], ['zeit', 'Zeit'], ['folien', 'Folien'], ['woerter', 'Wörter'], ['woerter_je_folie', 'Wörter/Folie'], ['bilder', 'Bilder'], ['links', 'Links'], ['uebungen', 'Übungen'], ['literatur', 'Literatur'], ['r_zeilen', 'R-Zeilen'], ['dateien', 'Dateien']];
    $('tabelle-daten').innerHTML = '<thead><tr>' + cols.map(c => `<th>${c[1]}</th>`).join('') + '</tr></thead><tbody>' +
      v.map(s => '<tr>' + cols.map(c => `<td class="${typeof s[c[0]] === 'number' ? 'num' : ''}">${c[0] === 'titel' ? key(s) + esc(s.titel) : fmt(s[c[0]])}</td>`).join('') + '</tr>').join('') + '</tbody>';
  }
  function renderAll() { renderKpis(); renderBars(); renderTimeline(); renderTable(); }
  renderAll();
})();
</script>
"""
    body = body.replace("__DATEN__", json.dumps(d, ensure_ascii=False)).replace("__STAND__", d["stand"]).replace("__BEOBACHTUNGEN__", "".join(f"<li>{b}</li>" for b in beobachtungen))
    return page_fn("Dashboard", body, depth=1, active="dashboard", description="Der Kurs in Zahlen: Folien, Wörter, Bilder, Übungen, Literatur und Code je Session, interaktiv.")
