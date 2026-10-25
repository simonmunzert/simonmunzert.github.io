/* IDS Mock Exam · app logic
   Questions live in questions.csv (see README.md for the format). */
(function () {
  'use strict';

  const SESSIONS = {
    1: { title: 'What is data science?', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/01_introduction/01-introduction.html' },
    2: { title: 'Programming I: Functions, debugging, project management', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/02_functions/02-functions.html' },
    3: { title: 'Programming II: Iteration, automation, scheduling', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/03_iteration/03-iteration.html' },
    4: { title: 'Working at the command line', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/04_command-line/04-command-line.html' },
    5: { title: 'Web data and technologies', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/05_webdata/05-webdata.html' },
    6: { title: 'Web scraping and APIs', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/06_scraping-apis/06-scraping-apis.html' },
    7: { title: 'Relational databases and SQL', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/07_databases/07-databases.html' },
    8: { title: 'Modeling and evaluation', url: 'https://raw.githack.com/intro-to-data-science-26/lectures/main/08_modeling/08-modeling.html' }
  };
  const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];
  const STORAGE_KEY = 'ids-mock-exam-history';

  /* ---------- CSV parsing (RFC 4180: quotes, embedded newlines) ---------- */
  function parseCSV(text) {
    const rows = []; let row = []; let field = ''; let inQ = false;
    text = text.replace(/^﻿/, '');
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (inQ) {
        if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else { inQ = false; } }
        else field += c;
      } else if (c === '"') inQ = true;
      else if (c === ',') { row.push(field); field = ''; }
      else if (c === '\n' || c === '\r') {
        if (c === '\r' && text[i + 1] === '\n') i++;
        row.push(field); field = ''; rows.push(row); row = [];
      } else field += c;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    const header = rows.shift().map(h => h.trim());
    return rows.filter(r => r.length > 1 || (r[0] && r[0].trim())).map(r => {
      const o = {}; header.forEach((h, i) => { o[h] = (r[i] || '').replace(/\r/g, ''); }); return o;
    });
  }

  function normalize(raw) {
    const q = {
      id: raw.id.trim(), session: parseInt(raw.session, 10), type: raw.type.trim(),
      topic: (raw.topic || '').trim(), lang: (raw.lang || '').trim(),
      question: raw.question.trim(), code: (raw.code || '').replace(/\s+$/, ''),
      explanation: (raw.explanation || '').trim(), source: (raw.source || '').trim()
    };
    if (q.type === 'choice') {
      q.options = ['option_a', 'option_b', 'option_c', 'option_d'].map(k => (raw[k] || '').trim()).filter(Boolean);
      q.answer = LETTERS.indexOf(raw.answer.trim().toUpperCase());
      q.isTF = q.options.length === 2;
    } else {
      q.options = [];
      q.answer = raw.answer.split(/[,; ]+/).map(s => parseInt(s, 10)).filter(n => !isNaN(n)).sort((a, b) => a - b);
      q.lines = q.code.split('\n');
    }
    return q;
  }

  /* ---------- Seeded RNG ---------- */
  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, rnd) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }

  /* Pick n questions, spread across sessions, with a mix of types. */
  function selectQuestions(pool, sessions, n, seed) {
    const rnd = mulberry32(seed);
    const bySession = {};
    pool.filter(q => sessions.includes(q.session)).forEach(q => { (bySession[q.session] = bySession[q.session] || []).push(q); });
    const groups = shuffle(Object.keys(bySession).map(k => shuffle(bySession[k], rnd)), rnd);
    const total = groups.reduce((s, g) => s + g.length, 0);
    if (n === 'all' || n > total) n = total;
    const picked = [];
    let i = 0;
    while (picked.length < n && groups.some(g => g.length)) {
      const g = groups[i % groups.length];
      if (g.length) picked.push(g.shift());
      i++;
    }
    return shuffle(picked, rnd).map(q => {
      const inst = { q: q, display: null };
      if (q.type === 'choice') {
        const idx = q.options.map((_, k) => k);
        if (q.isTF) inst.display = idx;
        else {
          /* "all/none of the above"-type options always go last */
          const isCatchAll = k => /\b(all|none|both|neither) of (the above|these)\b/i.test(q.options[k]);
          const regular = shuffle(idx.filter(k => !isCatchAll(k)), rnd);
          inst.display = regular.concat(idx.filter(isCatchAll));
        }
      }
      return inst;
    });
  }

  /* ---------- Rendering helpers ---------- */
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function md(s) {
    return esc(s)
      .replace(/`([^`]+)`/g, (_, c) => '<code>' + c + '</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
  }
  function codeBlock(code, opts) {
    opts = opts || {};
    const lines = code.split('\n');
    const cls = 'code' + (opts.marks ? ' marks' : '') + (opts.locked ? ' locked' : '');
    const lang = opts.lang ? '<p class="code-lang">' + esc(opts.lang) + '</p>' : '';
    return lang + '<pre class="' + cls + '">' + lines.map((l, i) => {
      const n = i + 1; let c = 'cline';
      if (opts.state) c += ' ' + (opts.state[n] || '');
      return '<div class="' + c + '" data-n="' + n + '"><span class="ln">' + n + '</span><span class="src">' + (esc(l) || ' ') + '</span></div>';
    }).join('') + '</pre>';
  }
  const LANG_LABEL = { r: 'R', bash: 'Shell', html: 'HTML', sql: 'SQL', text: 'Strings', xpath: 'XPath', regex: 'Regex' };

  function isCorrect(inst, ans) {
    const q = inst.q;
    if (ans === undefined || ans === null) return false;
    if (q.type === 'choice') return inst.display[ans] === q.answer;
    const a = ans.slice().sort((x, y) => x - y);
    return a.length === q.answer.length && a.every((v, i) => v === q.answer[i]);
  }

  /* Build the review/feedback state for a mark question. */
  function markState(q, ans) {
    const st = {}; const a = new Set(ans || []); const c = new Set(q.answer);
    for (let n = 1; n <= q.lines.length; n++) {
      if (a.has(n) && c.has(n)) st[n] = 'hit';
      else if (a.has(n)) st[n] = 'miss';
      else if (c.has(n)) st[n] = 'should';
    }
    return st;
  }

  function hasAnswer(inst, ans) {
    if (ans === undefined || ans === null) return false;
    return inst.q.type !== 'mark' || ans.length > 0;
  }

  function fmtTime(s) { const m = Math.floor(s / 60); return m + ':' + String(s % 60).padStart(2, '0'); }

  /* ---------- Storage ---------- */
  function loadHistory() { try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch (e) { return []; } }
  function saveHistory(h) { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(h.slice(-50))); } catch (e) { /* ignore */ } }

  /* ====================================================================== */
  /*  QUIZ PAGE                                                             */
  /* ====================================================================== */
  function initQuiz() {
    const $ = id => document.getElementById(id);
    const state = { pool: [], items: [], answers: [], checked: [], current: 0, mode: 'exam', seed: 0, n: 10, sessions: [], startedAt: 0, timer: null, elapsed: 0 };

    function show(view) {
      ['view-start', 'view-quiz', 'view-result'].forEach(v => $(v).classList.toggle('hidden', v !== view));
      window.scrollTo({ top: 0 });
    }

    /* ----- Start screen ----- */
    function renderStart() {
      const counts = {};
      state.pool.forEach(q => { counts[q.session] = (counts[q.session] || 0) + 1; });
      $('fact-pool').textContent = state.pool.length + ' questions, ' + Object.keys(counts).length + ' sessions';
      $('session-chips').innerHTML = Object.keys(SESSIONS).filter(s => counts[s]).map(s =>
        '<label class="chip" title="' + esc(SESSIONS[s].title) + '"><input type="checkbox" value="' + s + '" checked><span class="chip-num">' + s + '</span> ' + esc(shortTitle(SESSIONS[s].title)) + ' <span class="muted">(' + counts[s] + ')</span></label>'
      ).join('');
      renderHistory();
    }
    function shortTitle(t) { return t.replace(/^Programming I+: /, '').split(':')[0]; }

    function renderHistory() {
      const h = loadHistory();
      $('history-block').classList.toggle('hidden', h.length === 0);
      if (!h.length) return;
      const per = {};
      h.forEach(a => Object.keys(a.perSession || {}).forEach(s => {
        per[s] = per[s] || { c: 0, n: 0 }; per[s].c += a.perSession[s].c; per[s].n += a.perSession[s].n;
      }));
      const bars = Object.keys(per).sort().map(s => {
        const p = per[s].n ? Math.round(100 * per[s].c / per[s].n) : 0;
        const cls = p < 50 ? 'low' : p < 75 ? 'mid' : 'high';
        return '<li><span class="sn">S' + s + '</span><div class="bar ' + cls + '"><span style="width:' + p + '%"></span></div><span class="lab">' + per[s].c + '/' + per[s].n + '</span></li>';
      }).join('');
      $('session-bars').innerHTML = '<h3>Accuracy by session (all rounds)</h3><ul class="bars">' + bars + '</ul>';
      const rows = h.slice().reverse().slice(0, 8).map(a =>
        '<tr><td>' + esc(new Date(a.date).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })) + '</td><td>' + esc(a.sessions.join(', ')) + '</td><td>' + esc(a.mode) + '</td><td class="num">' + a.score + ' / ' + a.n + '</td><td class="num">' + Math.round(100 * a.score / a.n) + '%</td></tr>'
      ).join('');
      $('history-table').innerHTML = '<h3>Recent rounds</h3><table class="history-table"><thead><tr><th>When</th><th>Sessions</th><th>Mode</th><th class="num">Score</th><th class="num"></th></tr></thead><tbody>' + rows + '</tbody></table>';
    }

    function selectedSessions() { return [...document.querySelectorAll('#session-chips input:checked')].map(i => parseInt(i.value, 10)); }

    function startRound(opts) {
      state.sessions = opts.sessions; state.n = opts.n; state.mode = opts.mode; state.seed = opts.seed;
      state.items = selectQuestions(state.pool, state.sessions, state.n, state.seed);
      if (!state.items.length) { notice('No questions available for this selection.', true); return; }
      state.answers = state.items.map(() => undefined);
      state.checked = state.items.map(() => false);
      state.current = 0; state.elapsed = 0; state.startedAt = Date.now();
      clearInterval(state.timer);
      state.timer = setInterval(() => { state.elapsed = Math.round((Date.now() - state.startedAt) / 1000); $('timer').textContent = fmtTime(state.elapsed); }, 1000);
      $('timer').textContent = '0:00';
      const p = new URLSearchParams({ seed: state.seed, n: state.n, s: state.sessions.join(','), mode: state.mode });
      history.replaceState(null, '', '?' + p.toString());
      show('view-quiz');
      renderQuestion();
    }

    /* ----- Quiz screen ----- */
    function renderQuestion() {
      const i = state.current, inst = state.items[i], q = inst.q, ans = state.answers[i];
      const total = state.items.length;
      $('progress-count').textContent = 'Question ' + (i + 1) + ' of ' + total;
      $('progress-fill').style.width = (100 * i / total) + '%';
      $('dots').innerHTML = state.items.map((it, k) => {
        let c = 'dot';
        if (k === i) c += ' current';
        if (state.mode === 'practice' && state.checked[k]) c += isCorrect(it, state.answers[k]) ? ' right' : ' wrong';
        else if (hasAnswer(it, state.answers[k])) c += ' answered';
        return '<button class="' + c + '" data-k="' + k + '" aria-label="Question ' + (k + 1) + '">' + (k + 1) + '</button>';
      }).join('');
      const locked = state.mode === 'practice' && state.checked[i];
      let html = '<div class="question"><div class="q-meta"><span class="tag' + (q.type === 'mark' ? ' mark' : '') + '">' + (q.type === 'mark' ? 'Mark lines' : (q.isTF ? 'True or false' : 'Single choice')) + '</span><span>Session ' + q.session + ' · ' + esc(SESSIONS[q.session].title) + '</span></div>';
      html += '<p class="q-text">' + md(q.question) + '</p>';
      if (q.type === 'choice') {
        if (q.code) html += codeBlock(q.code, { lang: LANG_LABEL[q.lang] });
        html += '<ul class="options">' + inst.display.map((orig, k) => {
          let c = 'opt'; if (ans === k) c += ' selected'; if (locked) c += ' locked';
          if (locked) { if (orig === q.answer) c += ' correct'; else if (ans === k) c += ' incorrect'; }
          return '<li><button class="' + c + '" data-k="' + k + '"' + (locked ? ' disabled' : '') + '><span class="letter">' + LETTERS[k] + '</span><span class="otext">' + md(q.options[orig]) + '</span></button></li>';
        }).join('') + '</ul>';
      } else {
        html += '<p class="q-instruction">' + (q.answer.length > 1 ? 'Several lines may apply. ' : '') + 'Tap a line to mark it, tap again to unmark.</p>';
        const st = {}; (ans || []).forEach(n => { st[n] = 'selected'; });
        html += codeBlock(q.code, { marks: true, lang: LANG_LABEL[q.lang], locked: locked, state: locked ? markState(q, ans) : st });
      }
      if (locked) html += feedbackBox(inst, ans);
      html += '</div>';
      $('question').innerHTML = html;

      const answered = hasAnswer(inst, ans);
      $('btn-prev').disabled = i === 0;
      $('btn-check').classList.toggle('hidden', state.mode !== 'practice' || locked);
      $('btn-check').disabled = !answered;
      $('btn-next').classList.toggle('hidden', i === total - 1);
      $('btn-finish').classList.toggle('hidden', i !== total - 1);
      if (state.mode === 'practice' && !locked) { $('btn-next').classList.add('btn-ghost'); $('btn-next').classList.remove('btn-primary'); }
      else { $('btn-next').classList.remove('btn-ghost'); $('btn-next').classList.add('btn-primary'); }
    }

    function feedbackBox(inst, ans) {
      const q = inst.q, ok = isCorrect(inst, ans);
      let h = '<div class="feedback ' + (ok ? 'ok' : 'nok') + '"><div class="verdict">' + (ok ? 'Correct.' : (ans === undefined || (q.type === 'mark' && !ans.length) ? 'Not answered.' : 'Not quite.')) + '</div>';
      if (q.type === 'choice' && !ok) h += '<p>Correct answer: <strong>' + LETTERS[inst.display.indexOf(q.answer)] + '</strong> – ' + md(q.options[q.answer]) + '</p>';
      if (q.type === 'mark' && !ok) h += '<p>Correct line' + (q.answer.length > 1 ? 's' : '') + ': <strong>' + q.answer.join(', ') + '</strong></p>';
      if (q.explanation) h += '<p>' + md(q.explanation) + '</p>';
      if (q.source) h += '<p class="src">' + esc(q.source) + ' · ID ' + esc(q.id) + '</p>';
      return h + '</div>';
    }

    $('question').addEventListener('click', e => {
      const i = state.current, q = state.items[i].q;
      if (state.mode === 'practice' && state.checked[i]) return;
      const opt = e.target.closest('.opt');
      if (opt) { state.answers[i] = parseInt(opt.dataset.k, 10); renderQuestion(); return; }
      const line = e.target.closest('.cline');
      if (line && q.type === 'mark') {
        const n = parseInt(line.dataset.n, 10);
        const cur = new Set(state.answers[i] || []);
        cur.has(n) ? cur.delete(n) : cur.add(n);
        state.answers[i] = [...cur].sort((a, b) => a - b);
        renderQuestion();
      }
    });
    $('dots').addEventListener('click', e => { const d = e.target.closest('.dot'); if (d) { state.current = parseInt(d.dataset.k, 10); renderQuestion(); } });
    $('btn-prev').addEventListener('click', () => { if (state.current > 0) { state.current--; renderQuestion(); } });
    $('btn-next').addEventListener('click', () => { if (state.current < state.items.length - 1) { state.current++; renderQuestion(); window.scrollTo({ top: 0, behavior: 'smooth' }); } });
    $('btn-check').addEventListener('click', () => { state.checked[state.current] = true; renderQuestion(); });
    $('btn-abort').addEventListener('click', () => { if (confirm('Quit this round? Your answers will be discarded.')) { clearInterval(state.timer); history.replaceState(null, '', location.pathname); show('view-start'); } });
    $('btn-finish').addEventListener('click', () => {
      const open = state.answers.filter((a, k) => !hasAnswer(state.items[k], a)).length;
      if (open && !confirm(open + ' question' + (open > 1 ? 's are' : ' is') + ' still unanswered and will count as wrong. Finish anyway?')) return;
      finish();
    });
    document.addEventListener('keydown', e => {
      if ($('view-quiz').classList.contains('hidden') || e.metaKey || e.ctrlKey || e.altKey) return;
      const q = state.items[state.current].q;
      if (q.type === 'choice' && /^[1-4]$/.test(e.key)) {
        const k = parseInt(e.key, 10) - 1;
        if (k < q.options.length && !(state.mode === 'practice' && state.checked[state.current])) { state.answers[state.current] = k; renderQuestion(); }
      } else if (e.key === 'ArrowRight') $('btn-next').classList.contains('hidden') || $('btn-next').click();
      else if (e.key === 'ArrowLeft') $('btn-prev').click();
      else if (e.key === 'Enter' && !$('btn-check').classList.contains('hidden') && !$('btn-check').disabled) $('btn-check').click();
    });

    /* ----- Results ----- */
    function finish() {
      clearInterval(state.timer);
      state.elapsed = Math.round((Date.now() - state.startedAt) / 1000);
      const results = state.items.map((inst, k) => ({ inst, ans: state.answers[k], ok: isCorrect(inst, state.answers[k]) }));
      const score = results.filter(r => r.ok).length, n = results.length, pct = Math.round(100 * score / n);
      const perSession = {};
      results.forEach(r => { const s = r.inst.q.session; perSession[s] = perSession[s] || { c: 0, n: 0 }; perSession[s].n++; if (r.ok) perSession[s].c++; });
      const h = loadHistory();
      h.push({ date: Date.now(), score, n, mode: state.mode, seed: state.seed, sessions: state.sessions, perSession });
      saveHistory(h);

      const cls = pct < 50 ? 'low' : pct < 75 ? 'mid' : 'high';
      const msg = pct === 100 ? ['Flawless.', 'Every single one. Try a new round with other sessions to make sure it was not luck.']
        : pct >= 80 ? ['Very solid.', 'You have the concepts down. Have a look at the few misses below.']
        : pct >= 60 ? ['Decent, with gaps.', 'Review the explanations below and revisit the sessions where you lost points.']
        : pct >= 40 ? ['Room for improvement.', 'Go back to the lecture slides for the weak sessions and take another round afterwards.']
        : ['Time to hit the slides.', 'Work through the explanations below, then revisit the lectures and labs before trying again.'];
      const circ = 2 * Math.PI * 45;
      $('score-box').innerHTML = '<svg class="score-ring" viewBox="0 0 100 100"><circle class="track" cx="50" cy="50" r="45"/><circle class="fill ' + cls + '" cx="50" cy="50" r="45" stroke-dasharray="' + circ + '" stroke-dashoffset="' + (circ * (1 - score / n)) + '"/><text x="50" y="50" text-anchor="middle" dominant-baseline="central" font-size="26" font-weight="500" fill="#1D375B">' + pct + '%</text></svg>' +
        '<div><div class="score-num">' + score + ' <small>of ' + n + ' correct</small></div><p class="score-msg"><strong>' + msg[0] + '</strong>' + msg[1] + '</p><p class="score-meta">' + (state.mode === 'exam' ? 'Exam mode' : 'Practice mode') + ' · ' + fmtTime(state.elapsed) + ' min · sessions ' + state.sessions.join(', ') + '</p></div>';

      const sess = Object.keys(perSession).sort();
      $('result-sessions').innerHTML = '<h2>By session</h2><ul class="bars">' + sess.map(s => {
        const p = Math.round(100 * perSession[s].c / perSession[s].n); const c = p < 50 ? 'low' : p < 75 ? 'mid' : 'high';
        return '<li><span class="sn">S' + s + '</span><div class="bar ' + c + '"><span style="width:' + p + '%"></span></div><span class="lab">' + perSession[s].c + '/' + perSession[s].n + '</span></li>';
      }).join('') + '</ul><p class="small muted">Review the slides: ' + sess.map(s => '<a target="_blank" rel="noopener" href="' + SESSIONS[s].url + '">Session ' + s + '</a>').join(' · ') + '</p>';

      $('result-dots').innerHTML = results.map((r, k) => {
        const skipped = !hasAnswer(r.inst, r.ans);
        return '<button class="dot ' + (r.ok ? 'right' : skipped ? 'skipped' : 'wrong') + '" data-k="' + k + '" aria-label="Jump to question ' + (k + 1) + '" title="Question ' + (k + 1) + ': ' + (r.ok ? 'correct' : skipped ? 'not answered' : 'wrong') + '">' + (k + 1) + '</button>';
      }).join('');
      $('review').innerHTML = results.map((r, k) => {
        const q = r.inst.q, skipped = !hasAnswer(r.inst, r.ans);
        let h = '<li id="rev-' + k + '" class="' + (r.ok ? 'ok' : skipped ? 'skipped' : 'nok') + '"><div class="r-head"><span class="r-num">Question ' + (k + 1) + '</span><span class="r-verdict">' + (r.ok ? 'correct' : skipped ? 'not answered' : 'wrong') + '</span><span class="r-meta">Session ' + q.session + ' · ' + esc(q.topic || SESSIONS[q.session].title) + '</span></div>';
        h += '<p class="q-text">' + md(q.question) + '</p>';
        if (q.type === 'choice') {
          if (q.code) h += codeBlock(q.code, { lang: LANG_LABEL[q.lang] });
          h += '<ul class="options">' + r.inst.display.map((orig, j) => {
            let c = 'opt locked'; if (orig === q.answer) c += ' correct'; else if (r.ans === j) c += ' incorrect'; else if (r.ans === j) c += ' selected';
            return '<li><div class="' + c + '"><span class="letter">' + LETTERS[j] + '</span><span class="otext">' + md(q.options[orig]) + (r.ans === j ? ' <span class="muted small">(your pick)</span>' : '') + '</span></div></li>';
          }).join('') + '</ul>';
        } else {
          h += codeBlock(q.code, { marks: true, locked: true, lang: LANG_LABEL[q.lang], state: markState(q, r.ans) });
        }
        h += feedbackBox(r.inst, r.ans);
        return h + '</li>';
      }).join('');
      $('share-url').value = location.href;
      $('progress-fill').style.width = '100%';
      show('view-result');
    }

    $('result-dots').addEventListener('click', e => {
      const d = e.target.closest('.dot'); if (!d) return;
      const el = $('rev-' + d.dataset.k);
      const top = el.getBoundingClientRect().top + window.scrollY - $('result-dots').offsetHeight - 12;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
    $('btn-again').addEventListener('click', () => startRound({ sessions: state.sessions, n: state.n, mode: state.mode, seed: newSeed() }));
    $('btn-retake').addEventListener('click', () => startRound({ sessions: state.sessions, n: state.n, mode: state.mode, seed: state.seed }));
    $('btn-home').addEventListener('click', () => { history.replaceState(null, '', location.pathname); renderStart(); show('view-start'); });
    $('btn-copy').addEventListener('click', () => {
      const inp = $('share-url'); inp.select();
      (navigator.clipboard ? navigator.clipboard.writeText(inp.value) : Promise.reject()).then(() => { $('btn-copy').textContent = 'Copied'; setTimeout(() => { $('btn-copy').textContent = 'Copy link'; }, 1500); }).catch(() => { document.execCommand && document.execCommand('copy'); });
    });

    /* ----- Start controls ----- */
    function newSeed() { return Math.floor(Math.random() * 1e9); }
    $('btn-start').addEventListener('click', () => {
      const sessions = selectedSessions();
      if (!sessions.length) { $('start-hint').textContent = 'Select at least one session.'; return; }
      const nv = document.querySelector('#n-seg input:checked').value;
      startRound({ sessions, n: nv === 'all' ? 'all' : parseInt(nv, 10), mode: document.querySelector('#mode-seg input:checked').value, seed: newSeed() });
    });
    $('sel-all').addEventListener('click', e => { e.preventDefault(); document.querySelectorAll('#session-chips input').forEach(i => { i.checked = true; }); });
    $('sel-none').addEventListener('click', e => { e.preventDefault(); document.querySelectorAll('#session-chips input').forEach(i => { i.checked = false; }); });
    $('clear-history').addEventListener('click', e => { e.preventDefault(); if (confirm('Delete your stored results in this browser?')) { localStorage.removeItem(STORAGE_KEY); renderHistory(); } });
    document.querySelectorAll('#n-seg input').forEach(i => i.addEventListener('change', () => { $('fact-n').textContent = i.value === 'all' ? 'all questions' : i.value + ' questions'; }));

    function notice(msg, isErr) { $('notice').innerHTML = '<div class="notice' + (isErr ? ' error' : '') + '">' + esc(msg) + '</div>'; }

    fetch('questions.csv', { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error(r.status); return r.text(); }).then(t => {
      state.pool = parseCSV(t).map(normalize).filter(q => q.id && SESSIONS[q.session]);
      renderStart();
      const p = new URLSearchParams(location.search);
      if (p.get('seed')) {
        const s = (p.get('s') || '').split(',').map(Number).filter(x => SESSIONS[x]);
        const nraw = p.get('n');
        startRound({ seed: parseInt(p.get('seed'), 10) || 1, n: nraw === 'all' ? 'all' : (parseInt(nraw, 10) || 10), mode: p.get('mode') === 'practice' ? 'practice' : 'exam', sessions: s.length ? s : Object.keys(SESSIONS).map(Number) });
      }
    }).catch(err => notice('Could not load the question database (questions.csv): ' + err.message, true));
  }

  /* ====================================================================== */
  /*  PRINT PAGE                                                            */
  /* ====================================================================== */
  function initPrint() {
    const $ = id => document.getElementById(id);
    let pool = [];
    function render() {
      const sessions = [...document.querySelectorAll('#p-sessions input:checked')].map(i => parseInt(i.value, 10));
      const n = $('p-n').value === 'all' ? 'all' : parseInt($('p-n').value, 10) || 20;
      const seed = parseInt($('p-seed').value, 10) || 1;
      const withKey = $('p-key').checked;
      const items = selectQuestions(pool, sessions, n, seed);
      let h = '<div class="exam-head"><div><h1>Introduction to Data Science · Mock exam</h1><p class="muted small">' + items.length + ' questions · sessions ' + sessions.join(', ') + ' · set #' + seed + '</p></div></div>';
      h += '<p class="name-line">Name: ______________________________________ &nbsp;&nbsp; Programme: ❒ MDS &nbsp; ❒ MPP &nbsp; ❒ MIA &nbsp; ❒ Exchange &nbsp; ❒ PhD</p>';
      h += items.map((inst, k) => {
        const q = inst.q;
        let s = '<div class="pq"><p class="pq-stem">Question ' + (k + 1) + ': ' + md(q.question) + '</p>';
        if (q.type === 'choice') {
          if (q.code) s += codeBlock(q.code);
          s += '<ul class="popts' + (q.isTF ? ' tf' : '') + '">' + inst.display.map(o => '<li>' + md(q.options[o]) + '</li>').join('') + '</ul>';
        } else {
          s += codeBlock(q.code) + '<p class="pq-note">Circle the line number(s).</p>';
        }
        return s + '</div>';
      }).join('');
      if (withKey) {
        h += '<div class="key"><h2>Answer key · set #' + seed + '</h2><table><thead><tr><th>#</th><th>ID</th><th>Answer</th><th>Explanation</th></tr></thead><tbody>' + items.map((inst, k) => {
          const q = inst.q;
          const a = q.type === 'choice' ? LETTERS[inst.display.indexOf(q.answer)] + ' – ' + md(q.options[q.answer]) : 'line' + (q.answer.length > 1 ? 's ' : ' ') + q.answer.join(', ');
          return '<tr><td>' + (k + 1) + '</td><td>' + esc(q.id) + '</td><td>' + a + '</td><td>' + md(q.explanation) + '</td></tr>';
        }).join('') + '</tbody></table></div>';
      }
      $('sheet').innerHTML = h;
    }
    fetch('questions.csv', { cache: 'no-cache' }).then(r => r.text()).then(t => {
      pool = parseCSV(t).map(normalize).filter(q => q.id && SESSIONS[q.session]);
      const counts = {}; pool.forEach(q => { counts[q.session] = (counts[q.session] || 0) + 1; });
      $('p-sessions').innerHTML = Object.keys(SESSIONS).filter(s => counts[s]).map(s => '<label class="chip"><input type="checkbox" value="' + s + '" checked><span class="chip-num">' + s + '</span></label>').join('');
      $('p-seed').value = Math.floor(Math.random() * 100000);
      render();
      document.querySelectorAll('.print-controls input').forEach(i => i.addEventListener('change', render));
      $('p-shuffle').addEventListener('click', () => { $('p-seed').value = Math.floor(Math.random() * 100000); render(); });
      $('p-print').addEventListener('click', () => window.print());
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (document.body.dataset.page === 'print') initPrint(); else initQuiz();
  });
})();
