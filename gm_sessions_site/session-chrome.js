/*!
 * HollowStar GM — stay-in-session chrome
 * Peek-panel shell: session stays mounted; Fear / location / calendar / combat peeks;
 * always-on Hope·Fear·clocks; session focus dropdown. Candlelit GM Desk.
 */
(function () {
  'use strict';

  var STORAGE = {
    tokens: 'hs-tokens',
    clocks: 'hs-clocks',
    combat: 'hs-combat-tracker',
    locPrimary: 'hs-loc-primary',
    locSecondary: 'hs-loc-secondary',
    scrollPrefix: 'hs-scroll:',
    notes: 'hollowstar-notes',
    notesDock: 'hs-notes-dock-open'
  };

  var SESSIONS = [
    {
      id: 1,
      file: 'session1.html',
      label: 'Session 1 — Ember Grove',
      short: 'Session 1',
      fear: 'fear_options.html',
      locations: [
        { id: 'emberford', file: 'emberford.html', label: 'Emberford' }
      ],
      defaultPrimary: 'emberford',
      defaultSecondary: null
    },
    {
      id: 2,
      file: 'session2.html',
      label: 'Session 2 — Lumencrest Arrival',
      short: 'Session 2',
      fear: 'fear_options_session2.html',
      locations: [
        { id: 'lumencrest', file: 'lumencrest.html', label: 'Lumencrest' },
        { id: 'lamplight', file: 'lumencrest-lamplight.html', label: 'Lamplight Ward' },
        { id: 'shadowside', file: 'lumencrest-shadowside.html', label: 'Shadowside' },
        { id: 'map', file: 'lumencrest-map.html', label: 'City Map' }
      ],
      defaultPrimary: 'lumencrest',
      defaultSecondary: 'lamplight'
    },
    {
      id: 3,
      file: 'session3.html',
      label: 'Session 3 — The Hub Explosion',
      short: 'Session 3',
      fear: 'fear_options_session3.html',
      locations: [
        { id: 'lumencrest', file: 'lumencrest.html', label: 'Lumencrest' },
        { id: 'lamplight', file: 'lumencrest-lamplight.html', label: 'Lamplight Ward' },
        { id: 'shadowside', file: 'lumencrest-shadowside.html', label: 'Shadowside' },
        { id: 'map', file: 'lumencrest-map.html', label: 'City Map' }
      ],
      defaultPrimary: 'lumencrest',
      defaultSecondary: 'shadowside'
    }
  ];

  var LOCATION_FILES = {
    'emberford.html': 'emberford',
    'lumencrest.html': 'lumencrest',
    'lumencrest-lamplight.html': 'lamplight',
    'lumencrest-shadowside.html': 'shadowside',
    'lumencrest-map.html': 'map',
    'locations.html': null
  };

  var FEAR_RE = /^fear_options(_session\d+)?\.html/i;
  var CALENDAR_FILE = 'calendar.html';

  var tokens = { hope: 0, fear: 0 };
  var clocks = [];
  var combat = { name: '', foes: [] };
  var openPeek = null;
  var peekIframe = null;
  var notesDockOpen = false;
  var notesSaveTimer = null;

  function normalizeFile(name) {
    var p = (name || '').split('?')[0].split('#')[0].split('/').pop().toLowerCase();
    if (!p || p === '') return 'index.html';
    if (p.indexOf('.') < 0) p += '.html';
    return p;
  }

  function pageFile() {
    return normalizeFile(location.pathname);
  }

  function currentSession() {
    var file = pageFile();
    for (var i = 0; i < SESSIONS.length; i++) {
      if (SESSIONS[i].file === file) return SESSIONS[i];
    }
    var body = document.body;
    if (body && body.dataset.hsSession) {
      var id = parseInt(body.dataset.hsSession, 10);
      for (var j = 0; j < SESSIONS.length; j++) {
        if (SESSIONS[j].id === id) return SESSIONS[j];
      }
    }
    return null;
  }

  function isSessionPage() {
    return !!currentSession();
  }

  function isEmbed() {
    try {
      return window.self !== window.top || /[?&]peek=1(?:&|$)/.test(location.search);
    } catch (e) {
      return true;
    }
  }

  function readJSON(key, fallback) {
    try {
      var s = localStorage.getItem(key);
      if (s) return JSON.parse(s);
    } catch (e) {}
    return fallback;
  }

  function writeJSON(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) {}
  }

  function saveScroll() {
    try {
      sessionStorage.setItem(STORAGE.scrollPrefix + pageFile(), String(window.scrollY || 0));
    } catch (e) {}
  }

  function restoreScroll() {
    try {
      var key = STORAGE.scrollPrefix + pageFile();
      var s = sessionStorage.getItem(key);
      if (s == null) return;
      var y = parseInt(s, 10);
      if (!isNaN(y)) {
        requestAnimationFrame(function () {
          window.scrollTo(0, y);
        });
      }
      sessionStorage.removeItem(key);
    } catch (e) {}
  }

  function loadTokens() {
    tokens = readJSON(STORAGE.tokens, { hope: 0, fear: 0 });
    if (typeof tokens.hope !== 'number') tokens.hope = 0;
    if (typeof tokens.fear !== 'number') tokens.fear = 0;
  }

  function saveTokens() {
    writeJSON(STORAGE.tokens, tokens);
  }

  function loadClocks() {
    clocks = readJSON(STORAGE.clocks, null);
    if (!clocks || !clocks.length) {
      clocks = [
        { id: 1, name: 'Heart Failure', segments: 8, filled: 2 },
        { id: 2, name: 'Vael Lumber Deal', segments: 6, filled: 0 },
        { id: 3, name: 'Thorns Attack', segments: 6, filled: 1 },
        { id: 4, name: 'Fourth Fall Approach', segments: 8, filled: 2 }
      ];
    }
  }

  function saveClocks() {
    writeJSON(STORAGE.clocks, clocks);
  }

  function loadCombat() {
    combat = readJSON(STORAGE.combat, { name: '', foes: [] });
    if (!combat.foes) combat.foes = [];
  }

  function saveCombat() {
    writeJSON(STORAGE.combat, combat);
  }

  function locKey(sessionId, role) {
    return (role === 'secondary' ? STORAGE.locSecondary : STORAGE.locPrimary) + ':' + sessionId;
  }

  function getLocId(session, role) {
    try {
      var saved = localStorage.getItem(locKey(session.id, role));
      if (saved) return saved === 'null' ? null : saved;
    } catch (e) {}
    return role === 'secondary' ? session.defaultSecondary : session.defaultPrimary;
  }

  function setLocId(session, role, id) {
    try {
      localStorage.setItem(locKey(session.id, role), id == null ? 'null' : id);
    } catch (e) {}
  }

  function findLoc(session, id) {
    if (!id) return null;
    for (var i = 0; i < session.locations.length; i++) {
      if (session.locations[i].id === id) return session.locations[i];
    }
    return null;
  }

  function withPeek(url, hash) {
    var base = url.split('#')[0];
    var h = hash || (url.indexOf('#') >= 0 ? url.split('#')[1] : '');
    var joiner = base.indexOf('?') >= 0 ? '&' : '?';
    return base + joiner + 'peek=1' + (h ? '#' + h : '');
  }

  /* ── Embed mode: hide chrome inside peeks ── */
  function applyEmbedMode() {
    if (!isEmbed()) return;
    document.documentElement.classList.add('hs-peek-embed');
    document.body.classList.add('hs-peek-embed');

    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      var href = a.getAttribute('href') || '';
      var file = href.split('?')[0].split('#')[0].split('/').pop().toLowerCase();
      var hash = href.indexOf('#') >= 0 ? href.split('#')[1] : '';
      if (!/^session\d+\.html$/i.test(file)) return;
      e.preventDefault();
      try {
        if (window.parent && window.parent !== window && window.parent.HSChrome) {
          window.parent.HSChrome.closePeek();
          if (hash) {
            var el = window.parent.document.getElementById(hash);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      } catch (err) {}
    }, true);
  }

  /* ── Nav: session focus dropdown ── */
  function isPeerSessionLink(a) {
    var href = normalizeFile(a.getAttribute('href') || '');
    for (var i = 0; i < SESSIONS.length; i++) {
      if (SESSIONS[i].file === href) return true;
    }
    var t = (a.textContent || '').replace(/\s+/g, ' ').trim();
    return /^📖?\s*Session\s+\d+/i.test(t);
  }

  function buildFocusControl(activeFile) {
    var wrap = document.createElement('div');
    wrap.className = 'hs-session-focus';
    wrap.setAttribute('data-hs-session-focus', '');

    var lab = document.createElement('label');
    lab.className = 'hs-session-focus-label';
    lab.setAttribute('for', 'hs-session-select');
    lab.textContent = 'Focus';

    var sel = document.createElement('select');
    sel.id = 'hs-session-select';
    sel.className = 'hs-session-select';
    sel.setAttribute('aria-label', 'Session in focus');

    var placeholder = document.createElement('option');
    placeholder.value = '';
    placeholder.textContent = 'Choose session…';
    if (!activeFile || !SESSIONS.some(function (s) { return s.file === activeFile; })) {
      placeholder.selected = true;
    }
    sel.appendChild(placeholder);

    SESSIONS.forEach(function (s) {
      var opt = document.createElement('option');
      opt.value = s.file;
      opt.textContent = s.short + ' — ' + s.label.replace(/^Session \d+ — /, '');
      if (s.file === activeFile) opt.selected = true;
      sel.appendChild(opt);
    });

    sel.addEventListener('change', function () {
      if (!sel.value) return;
      if (sel.value === pageFile()) return;
      saveScroll();
      location.href = sel.value;
    });

    wrap.appendChild(lab);
    wrap.appendChild(sel);
    return wrap;
  }

  function rewriteNav() {
    var nav = document.querySelector('.site-nav');
    if (!nav || nav.dataset.hsNavReady === '1') return;
    nav.dataset.hsNavReady = '1';

    var file = pageFile();
    var peers = [];
    Array.prototype.slice.call(nav.querySelectorAll('a')).forEach(function (a) {
      if (isPeerSessionLink(a)) peers.push(a);
    });
    if (!peers.length && nav.querySelector('[data-hs-session-focus]')) return;

    var insertBefore = peers[0] || null;
    var focus = buildFocusControl(file);
    if (insertBefore) {
      nav.insertBefore(focus, insertBefore);
    } else {
      var brand = nav.querySelector('.site-nav-brand');
      if (brand && brand.nextSibling) nav.insertBefore(focus, brand.nextSibling);
      else nav.appendChild(focus);
    }
    peers.forEach(function (a) { a.parentNode.removeChild(a); });

    if (isSessionPage()) {
      Array.prototype.slice.call(nav.querySelectorAll('a')).forEach(function (a) {
        var href = (a.getAttribute('href') || '').split('?')[0].split('#')[0].toLowerCase();
        if (href === 'index.html' || href === 'locations.html' || href === 'calendar.html' || href === 'gmscreen.html' || href === 'notes.html') {
          a.classList.add('hs-nav-secondary');
        }
      });
    }
  }

  /* ── Instrument strip ── */
  function changeToken(type, delta) {
    tokens[type] = Math.max(0, (tokens[type] || 0) + delta);
    saveTokens();
    syncTokenUI();
  }

  function syncTokenUI() {
    document.querySelectorAll('[data-hs-token="hope"]').forEach(function (el) {
      el.textContent = String(tokens.hope);
    });
    document.querySelectorAll('[data-hs-token="fear"]').forEach(function (el) {
      el.textContent = String(tokens.fear);
    });
  }

  function renderClocksInto(container) {
    if (!container) return;
    container.innerHTML = '';
    clocks.forEach(function (cl, ci) {
      var danger = cl.filled >= Math.floor(cl.segments * 0.75);
      var item = document.createElement('div');
      item.className = 'hs-clock-item';
      var head = document.createElement('div');
      head.className = 'hs-clock-head';
      var name = document.createElement('input');
      name.className = 'hs-clock-name';
      name.value = cl.name;
      name.setAttribute('aria-label', 'Clock name');
      name.addEventListener('input', function () {
        clocks[ci].name = name.value;
        saveClocks();
      });
      var del = document.createElement('button');
      del.type = 'button';
      del.className = 'hs-clock-del';
      del.setAttribute('aria-label', 'Remove clock');
      del.textContent = '✕';
      del.addEventListener('click', function () {
        clocks.splice(ci, 1);
        saveClocks();
        renderAllClocks();
      });
      head.appendChild(name);
      head.appendChild(del);

      var pips = document.createElement('div');
      pips.className = 'hs-clock-pips';
      for (var i = 0; i < cl.segments; i++) {
        (function (idx) {
          var pip = document.createElement('button');
          pip.type = 'button';
          pip.className = 'hs-clock-pip' + (idx < cl.filled ? ' filled' + (danger ? ' danger' : '') : '');
          pip.setAttribute('aria-label', 'Segment ' + (idx + 1));
          pip.addEventListener('click', function () {
            if (clocks[ci].filled === idx + 1) clocks[ci].filled = idx;
            else clocks[ci].filled = idx + 1;
            saveClocks();
            renderAllClocks();
          });
          pips.appendChild(pip);
        })(i);
      }

      var meta = document.createElement('div');
      meta.className = 'hs-clock-meta';
      meta.textContent = cl.filled + '/' + cl.segments + ' · ';
      var size = document.createElement('select');
      size.className = 'hs-clock-size';
      [4, 6, 8].forEach(function (n) {
        var o = document.createElement('option');
        o.value = String(n);
        o.textContent = n + ' seg';
        if (cl.segments === n) o.selected = true;
        size.appendChild(o);
      });
      size.addEventListener('change', function () {
        clocks[ci].segments = parseInt(size.value, 10);
        clocks[ci].filled = Math.min(clocks[ci].filled, clocks[ci].segments);
        saveClocks();
        renderAllClocks();
      });
      meta.appendChild(size);

      item.appendChild(head);
      item.appendChild(pips);
      item.appendChild(meta);
      container.appendChild(item);
    });
  }

  function renderAllClocks() {
    document.querySelectorAll('[data-hs-clocks]').forEach(renderClocksInto);
  }

  function buildInstrumentStrip() {
    var strip = document.createElement('div');
    strip.className = 'hs-instrument-strip';
    strip.setAttribute('data-hs-instrument', '');
    strip.innerHTML =
      '<div class="hs-instrument-inner">' +
        '<div class="hs-token-group hope">' +
          '<span class="hs-token-label">Hope</span>' +
          '<button type="button" class="hs-token-btn" data-hs-delta="hope:-1" aria-label="Decrease Hope">−</button>' +
          '<span class="hs-token-count" data-hs-token="hope">0</span>' +
          '<button type="button" class="hs-token-btn" data-hs-delta="hope:1" aria-label="Increase Hope">+</button>' +
        '</div>' +
        '<div class="hs-token-group fear">' +
          '<span class="hs-token-label">Fear</span>' +
          '<button type="button" class="hs-token-btn" data-hs-delta="fear:-1" aria-label="Decrease Fear">−</button>' +
          '<span class="hs-token-count" data-hs-token="fear">0</span>' +
          '<button type="button" class="hs-token-btn" data-hs-delta="fear:1" aria-label="Increase Fear">+</button>' +
        '</div>' +
        '<div class="hs-clocks-wrap">' +
          '<div class="hs-clocks-label">Clocks</div>' +
          '<div class="hs-clocks" data-hs-clocks></div>' +
          '<button type="button" class="hs-clock-add" data-hs-add-clock>+ Clock</button>' +
        '</div>' +
      '</div>';

    strip.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-hs-delta]');
      if (btn) {
        var parts = btn.getAttribute('data-hs-delta').split(':');
        changeToken(parts[0], parseInt(parts[1], 10));
        return;
      }
      if (e.target.closest('[data-hs-add-clock]')) {
        clocks.push({ id: Date.now(), name: 'New Clock', segments: 6, filled: 0 });
        saveClocks();
        renderAllClocks();
      }
    });

    return strip;
  }

  /* ── Peek shell ── */
  function ensurePeekShell() {
    if (document.getElementById('hs-peek-root')) return;
    var root = document.createElement('div');
    root.id = 'hs-peek-root';
    root.className = 'hs-peek-root';
    root.hidden = true;
    root.innerHTML =
      '<div class="hs-peek-backdrop" data-hs-peek-close></div>' +
      '<aside class="hs-peek-panel" role="dialog" aria-modal="true" aria-labelledby="hs-peek-title">' +
        '<header class="hs-peek-header">' +
          '<h2 id="hs-peek-title" class="hs-peek-title">Peek</h2>' +
          '<div class="hs-peek-tools" data-hs-peek-tools></div>' +
          '<button type="button" class="hs-peek-close" data-hs-peek-close aria-label="Close">✕</button>' +
        '</header>' +
        '<div class="hs-peek-body" data-hs-peek-body></div>' +
      '</aside>';
    document.body.appendChild(root);

    root.addEventListener('click', function (e) {
      if (e.target.closest('[data-hs-peek-close]')) closePeek();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && openPeek) closePeek();
    });
  }

  function closePeek() {
    var root = document.getElementById('hs-peek-root');
    if (!root) return;
    root.hidden = true;
    root.classList.remove('open');
    document.body.classList.remove('hs-peek-open');
    var body = root.querySelector('[data-hs-peek-body]');
    if (body) body.innerHTML = '';
    var tools = root.querySelector('[data-hs-peek-tools]');
    if (tools) tools.innerHTML = '';
    openPeek = null;
    peekIframe = null;
  }

  function openPeekPanel(kind, title, buildFn) {
    ensurePeekShell();
    var root = document.getElementById('hs-peek-root');
    var titleEl = document.getElementById('hs-peek-title');
    var body = root.querySelector('[data-hs-peek-body]');
    var tools = root.querySelector('[data-hs-peek-tools]');
    titleEl.textContent = title;
    tools.innerHTML = '';
    body.innerHTML = '';
    openPeek = kind;
    buildFn(body, tools);
    root.hidden = false;
    requestAnimationFrame(function () {
      root.classList.add('open');
      document.body.classList.add('hs-peek-open');
    });
  }

  function openIframePeek(kind, title, url) {
    openPeekPanel(kind, title, function (body) {
      var frame = document.createElement('iframe');
      frame.className = 'hs-peek-iframe';
      frame.title = title;
      frame.src = url;
      body.appendChild(frame);
      peekIframe = frame;
    });
  }

  function openFearPeek(hash) {
    var session = currentSession();
    if (!session) return;
    var url = withPeek(session.fear, hash || '');
    openIframePeek('fear', 'Fear spends — ' + session.short, url);
  }

  function openCalendarPeek() {
    openIframePeek('calendar', 'Calendar', withPeek(CALENDAR_FILE));
  }

  function openLocationPeek(preferredId) {
    var session = currentSession();
    if (!session) return;

    openPeekPanel('location', 'Locations — ' + session.short, function (body, tools) {
      var primaryId = getLocId(session, 'primary');
      var secondaryId = getLocId(session, 'secondary');
      var activeId = preferredId || primaryId || (session.locations[0] && session.locations[0].id);

      var switcher = document.createElement('div');
      switcher.className = 'hs-loc-switcher';

      function optList(select, selected, allowNone) {
        select.innerHTML = '';
        if (allowNone) {
          var none = document.createElement('option');
          none.value = '';
          none.textContent = '— none —';
          select.appendChild(none);
        }
        session.locations.forEach(function (loc) {
          var o = document.createElement('option');
          o.value = loc.id;
          o.textContent = loc.label;
          if (loc.id === selected) o.selected = true;
          select.appendChild(o);
        });
      }

      var pLab = document.createElement('label');
      pLab.className = 'hs-loc-field';
      pLab.innerHTML = '<span>Primary</span>';
      var pSel = document.createElement('select');
      pSel.className = 'hs-loc-select';
      optList(pSel, primaryId, false);
      pLab.appendChild(pSel);

      var sLab = document.createElement('label');
      sLab.className = 'hs-loc-field';
      sLab.innerHTML = '<span>Secondary</span>';
      var sSel = document.createElement('select');
      sSel.className = 'hs-loc-select';
      optList(sSel, secondaryId, true);
      sLab.appendChild(sSel);

      var tabs = document.createElement('div');
      tabs.className = 'hs-loc-tabs';

      function loadLoc(id) {
        activeId = id;
        Array.prototype.forEach.call(tabs.querySelectorAll('button'), function (b) {
          b.classList.toggle('active', b.dataset.locId === id);
        });
        var loc = findLoc(session, id);
        frame.src = loc ? withPeek(loc.file) : 'about:blank';
      }

      function rebuildTabs() {
        tabs.innerHTML = '';
        var ids = [];
        if (primaryId) ids.push(primaryId);
        if (secondaryId && secondaryId !== primaryId) ids.push(secondaryId);
        session.locations.forEach(function (loc) {
          if (ids.indexOf(loc.id) < 0) ids.push(loc.id);
        });
        ids.forEach(function (id) {
          var loc = findLoc(session, id);
          if (!loc) return;
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'hs-loc-tab';
          b.dataset.locId = id;
          var role = id === primaryId ? ' · primary' : id === secondaryId ? ' · secondary' : '';
          b.textContent = loc.label + role;
          b.addEventListener('click', function () { loadLoc(id); });
          tabs.appendChild(b);
        });
      }

      pSel.addEventListener('change', function () {
        primaryId = pSel.value;
        setLocId(session, 'primary', primaryId);
        rebuildTabs();
        loadLoc(primaryId);
      });
      sSel.addEventListener('change', function () {
        secondaryId = sSel.value || null;
        setLocId(session, 'secondary', secondaryId);
        rebuildTabs();
      });

      switcher.appendChild(pLab);
      switcher.appendChild(sLab);
      tools.appendChild(switcher);

      var frame = document.createElement('iframe');
      frame.className = 'hs-peek-iframe';
      frame.title = 'Location';

      body.appendChild(tabs);
      body.appendChild(frame);
      peekIframe = frame;
      rebuildTabs();
      loadLoc(activeId && findLoc(session, activeId) ? activeId : primaryId);
    });
  }

  function openCombatPeek(seed) {
    if (seed && seed.foes && seed.foes.length) {
      if (!combat.foes.length || confirm('Load encounter roster into the combat tracker?')) {
        combat.name = seed.name || combat.name || 'Encounter';
        combat.foes = seed.foes.map(function (f, i) {
          return {
            id: Date.now() + i,
            name: f.name || 'Foe',
            hp: f.hp != null ? f.hp : 10,
            maxHp: f.maxHp != null ? f.maxHp : (f.hp != null ? f.hp : 10),
            dif: f.dif != null ? f.dif : '',
            notes: f.notes || '',
            conditions: f.conditions || ''
          };
        });
        saveCombat();
      }
    }

    openPeekPanel('combat', 'Combat — rules & tracker', function (body) {
      var rules = document.createElement('div');
      rules.className = 'hs-combat-rules';
      rules.innerHTML =
        '<div class="hs-combat-rules-block">' +
          '<div class="hs-combat-rules-title">Core loop</div>' +
          '<p>No initiative. Players act freely. Spend <strong>Fear</strong> for enemy actions. Every roll: Hope die + Fear die + stat. Hope higher → player Hope; Fear higher → you gain Fear.</p>' +
          '<ul>' +
            '<li><strong>1 Fear</strong> — enemy attacks (damage, no roll) or moves / complication</li>' +
            '<li><strong>2 Fear</strong> — enemy special ability</li>' +
            '<li><strong>3 Fear</strong> — major escalation</li>' +
            '<li>Hit ≥ DIF · Partial DIF−1 to DIF−4 (cost) · Armor subtracts from damage</li>' +
            '<li>HP 0 → Death Move · Ally stabilize: 2 Hope</li>' +
          '</ul>' +
        '</div>';

      var tracker = document.createElement('div');
      tracker.className = 'hs-combat-tracker';
      tracker.setAttribute('data-hs-combat-tracker', '');

      function renderTracker() {
        tracker.innerHTML = '';
        var head = document.createElement('div');
        head.className = 'hs-combat-tracker-head';
        var nameIn = document.createElement('input');
        nameIn.className = 'hs-combat-name';
        nameIn.placeholder = 'Encounter name';
        nameIn.value = combat.name || '';
        nameIn.addEventListener('input', function () {
          combat.name = nameIn.value;
          saveCombat();
        });
        var addBtn = document.createElement('button');
        addBtn.type = 'button';
        addBtn.className = 'hs-btn';
        addBtn.textContent = '+ Foe';
        addBtn.addEventListener('click', function () {
          combat.foes.push({
            id: Date.now(),
            name: 'Foe',
            hp: 10,
            maxHp: 10,
            dif: '',
            notes: '',
            conditions: ''
          });
          saveCombat();
          renderTracker();
        });
        var clearBtn = document.createElement('button');
        clearBtn.type = 'button';
        clearBtn.className = 'hs-btn quiet';
        clearBtn.textContent = 'Clear';
        clearBtn.addEventListener('click', function () {
          if (!confirm('Clear combat tracker?')) return;
          combat = { name: '', foes: [] };
          saveCombat();
          renderTracker();
        });
        head.appendChild(nameIn);
        head.appendChild(addBtn);
        head.appendChild(clearBtn);
        tracker.appendChild(head);

        if (!combat.foes.length) {
          var empty = document.createElement('p');
          empty.className = 'hs-combat-empty';
          empty.textContent = 'No foes yet. Add one, or open a combat glyph from the session script to seed a roster.';
          tracker.appendChild(empty);
          return;
        }

        combat.foes.forEach(function (foe, fi) {
          var card = document.createElement('div');
          card.className = 'hs-foe-card';
          card.innerHTML =
            '<div class="hs-foe-row">' +
              '<input class="hs-foe-name" data-f="name" value="' + escapeAttr(foe.name) + '" aria-label="Foe name">' +
              '<button type="button" class="hs-foe-del" data-del aria-label="Remove">✕</button>' +
            '</div>' +
            '<div class="hs-foe-row stats">' +
              '<label>HP <input type="number" data-f="hp" value="' + foe.hp + '" min="0"></label>' +
              '<label>Max <input type="number" data-f="maxHp" value="' + foe.maxHp + '" min="0"></label>' +
              '<label>DIF <input type="text" data-f="dif" value="' + escapeAttr(String(foe.dif)) + '"></label>' +
            '</div>' +
            '<div class="hs-foe-row dmg">' +
              '<button type="button" data-dmg="-1">−1</button>' +
              '<button type="button" data-dmg="-3">−3</button>' +
              '<button type="button" data-dmg="-5">−5</button>' +
              '<button type="button" data-dmg="1">+1</button>' +
            '</div>' +
            '<label class="hs-foe-notes">Conditions <input data-f="conditions" value="' + escapeAttr(foe.conditions) + '"></label>' +
            '<label class="hs-foe-notes">Notes <input data-f="notes" value="' + escapeAttr(foe.notes) + '"></label>';

          card.addEventListener('click', function (e) {
            var del = e.target.closest('[data-del]');
            if (del) {
              combat.foes.splice(fi, 1);
              saveCombat();
              renderTracker();
              return;
            }
            var dmg = e.target.closest('[data-dmg]');
            if (dmg) {
              combat.foes[fi].hp = Math.max(0, (combat.foes[fi].hp || 0) + parseInt(dmg.getAttribute('data-dmg'), 10));
              saveCombat();
              renderTracker();
            }
          });
          card.addEventListener('input', function (e) {
            var inp = e.target.closest('[data-f]');
            if (!inp) return;
            var key = inp.getAttribute('data-f');
            var val = inp.value;
            if (key === 'hp' || key === 'maxHp') val = parseInt(val, 10) || 0;
            combat.foes[fi][key] = val;
            saveCombat();
          });
          tracker.appendChild(card);
        });
      }

      body.appendChild(rules);
      body.appendChild(tracker);
      renderTracker();
    });
  }

  function escapeAttr(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;');
  }

  function parseSeed(btn) {
    var raw = btn.getAttribute('data-combat-seed');
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  /* ── Notes dock (non-modal — for constant jotting) ── */
  function loadNotesStore() {
    var data = readJSON(STORAGE.notes, null);
    if (!data || typeof data !== 'object') {
      data = { sessions: [], threads: [], decisions: [], npcs: [], misc: '' };
    }
    if (!data.sessions) data.sessions = [];
    if (!data.threads) data.threads = [];
    if (!data.decisions) data.decisions = [];
    if (!data.npcs) data.npcs = [];
    if (typeof data.misc !== 'string') data.misc = '';
    return data;
  }

  function saveNotesStore(data) {
    writeJSON(STORAGE.notes, data);
  }

  function findOrCreateSessionNote(store, session) {
    var match = null;
    var i;
    for (i = 0; i < store.sessions.length; i++) {
      var title = store.sessions[i].title || '';
      if (title.indexOf(session.short) === 0 || title === session.label) {
        match = store.sessions[i];
        break;
      }
    }
    if (!match) {
      match = {
        id: Date.now(),
        title: session.label,
        date: '',
        text: ''
      };
      store.sessions.push(match);
      saveNotesStore(store);
    }
    return match;
  }

  function ensureNotesDock() {
    if (document.getElementById('hs-notes-dock')) return document.getElementById('hs-notes-dock');
    var session = currentSession();
    var dock = document.createElement('aside');
    dock.id = 'hs-notes-dock';
    dock.className = 'hs-notes-dock';
    dock.setAttribute('aria-label', 'Session notes dock');
    dock.hidden = true;
    dock.innerHTML =
      '<header class="hs-notes-dock-header">' +
        '<div class="hs-notes-dock-titles">' +
          '<div class="hs-notes-dock-eyebrow">Live notes</div>' +
          '<h2 class="hs-notes-dock-title" data-hs-notes-title></h2>' +
        '</div>' +
        '<div class="hs-notes-dock-actions">' +
          '<span class="hs-notes-saved" data-hs-notes-saved aria-live="polite"></span>' +
          '<button type="button" class="hs-btn quiet" data-hs-notes-full>Full notes</button>' +
          '<button type="button" class="hs-peek-close" data-hs-notes-close aria-label="Close notes">✕</button>' +
        '</div>' +
      '</header>' +
      '<p class="hs-notes-dock-hint">Stays open while you run the script — no backdrop. Press <kbd>N</kbd> to toggle.</p>' +
      '<textarea class="hs-notes-dock-pad" data-hs-notes-pad spellcheck="true" placeholder="Jot as you go — key moments, player choices, Fear spends used, what to prep next…"></textarea>';

    dock.querySelector('[data-hs-notes-close]').addEventListener('click', closeNotesDock);
    dock.querySelector('[data-hs-notes-full]').addEventListener('click', function () {
      openNotesToolkitPeek();
    });

    var pad = dock.querySelector('[data-hs-notes-pad]');
    pad.addEventListener('input', function () {
      var sess = currentSession();
      if (!sess) return;
      var store = loadNotesStore();
      var note = findOrCreateSessionNote(store, sess);
      note.text = pad.value;
      saveNotesStore(store);
      var saved = dock.querySelector('[data-hs-notes-saved]');
      saved.textContent = 'Saved';
      saved.classList.add('show');
      clearTimeout(notesSaveTimer);
      notesSaveTimer = setTimeout(function () {
        saved.classList.remove('show');
      }, 1200);
    });

    document.body.appendChild(dock);
    if (session) {
      dock.querySelector('[data-hs-notes-title]').textContent = session.short;
    }
    return dock;
  }

  function hydrateNotesDock() {
    var session = currentSession();
    var dock = ensureNotesDock();
    if (!session) return;
    dock.querySelector('[data-hs-notes-title]').textContent = session.short;
    var store = loadNotesStore();
    var note = findOrCreateSessionNote(store, session);
    var pad = dock.querySelector('[data-hs-notes-pad]');
    if (document.activeElement !== pad) {
      pad.value = note.text || '';
    }
  }

  function setNotesToolActive(on) {
    document.querySelectorAll('[data-hs-peek="notes"]').forEach(function (btn) {
      btn.classList.toggle('active', !!on);
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  function openNotesDock() {
    if (!isSessionPage() || isEmbed()) return;
    ensureNotesDock();
    hydrateNotesDock();
    var dock = document.getElementById('hs-notes-dock');
    dock.hidden = false;
    requestAnimationFrame(function () {
      dock.classList.add('open');
      document.body.classList.add('hs-notes-dock-open');
    });
    notesDockOpen = true;
    setNotesToolActive(true);
    try { sessionStorage.setItem(STORAGE.notesDock, '1'); } catch (e) {}
    var pad = dock.querySelector('[data-hs-notes-pad]');
    if (pad && !pad.value) {
      setTimeout(function () { pad.focus(); }, 180);
    }
  }

  function closeNotesDock() {
    var dock = document.getElementById('hs-notes-dock');
    if (!dock) return;
    dock.classList.remove('open');
    document.body.classList.remove('hs-notes-dock-open');
    notesDockOpen = false;
    setNotesToolActive(false);
    try { sessionStorage.setItem(STORAGE.notesDock, '0'); } catch (e) {}
    setTimeout(function () {
      if (!notesDockOpen) dock.hidden = true;
    }, 220);
  }

  function toggleNotesDock() {
    if (notesDockOpen) closeNotesDock();
    else openNotesDock();
  }

  function openNotesToolkitPeek() {
    openIframePeek('notes-full', 'Notes toolkit', withPeek('notes.html'));
  }

  /* ── Session toolbar (peek triggers) ── */
  function buildSessionToolbar() {
    var bar = document.createElement('div');
    bar.className = 'hs-session-toolbar';
    bar.setAttribute('data-hs-session-toolbar', '');
    bar.innerHTML =
      '<button type="button" class="hs-tool-btn notes" data-hs-peek="notes" aria-pressed="false">Notes</button>' +
      '<button type="button" class="hs-tool-btn fear" data-hs-peek="fear">Fear</button>' +
      '<button type="button" class="hs-tool-btn loc" data-hs-peek="location">Locations</button>' +
      '<button type="button" class="hs-tool-btn cal" data-hs-peek="calendar">Calendar</button>' +
      '<button type="button" class="hs-tool-btn combat" data-hs-peek="combat">Combat</button>';
    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-hs-peek]');
      if (!btn) return;
      var kind = btn.getAttribute('data-hs-peek');
      if (kind === 'notes') toggleNotesDock();
      else if (kind === 'fear') openFearPeek();
      else if (kind === 'location') openLocationPeek();
      else if (kind === 'calendar') openCalendarPeek();
      else if (kind === 'combat') openCombatPeek();
    });
    return bar;
  }

  function mountSessionChrome() {
    var session = currentSession();
    if (!session || isEmbed()) return;

    document.body.classList.add('hs-session-shell');
    document.body.dataset.hsSession = String(session.id);

    var nav = document.querySelector('.site-nav');
    if (nav && !document.querySelector('[data-hs-session-toolbar]')) {
      nav.appendChild(buildSessionToolbar());
    }

    if (!document.querySelector('[data-hs-instrument]')) {
      var strip = buildInstrumentStrip();
      if (nav && nav.parentNode) {
        nav.parentNode.insertBefore(strip, nav.nextSibling);
      } else {
        document.body.insertBefore(strip, document.body.firstChild);
      }
    }

    syncTokenUI();
    renderAllClocks();
    wireSessionLinks();
    wireNotesHotkey();
    try {
      if (sessionStorage.getItem(STORAGE.notesDock) === '1') openNotesDock();
    } catch (e) {}
  }

  function wireNotesHotkey() {
    document.addEventListener('keydown', function (e) {
      if (!isSessionPage() || isEmbed()) return;
      if (e.key !== 'n' && e.key !== 'N') return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var tag = (e.target && e.target.tagName) || '';
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (e.target && e.target.isContentEditable)) return;
      e.preventDefault();
      toggleNotesDock();
    });
  }

  function wireSessionLinks() {
    document.addEventListener('click', function (e) {
      if (!isSessionPage() || isEmbed()) return;
      var a = e.target.closest('a[href]');
      if (!a) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === '_blank') return;

      var href = a.getAttribute('href') || '';
      var parts = href.split('#');
      var file = normalizeFile(parts[0]);
      var hash = parts[1] || '';

      if (FEAR_RE.test(file)) {
        e.preventDefault();
        openFearPeek(hash);
        return;
      }
      if (file === CALENDAR_FILE) {
        e.preventDefault();
        openCalendarPeek();
        return;
      }
      if (file === 'notes.html') {
        e.preventDefault();
        openNotesDock();
        return;
      }
      if (Object.prototype.hasOwnProperty.call(LOCATION_FILES, file)) {
        e.preventDefault();
        openLocationPeek(LOCATION_FILES[file]);
        return;
      }
    }, true);

    document.addEventListener('click', function (e) {
      var glyph = e.target.closest('.combat-glyph, [data-hs-combat]');
      if (!glyph) return;
      e.preventDefault();
      openCombatPeek(parseSeed(glyph));
    });
  }

  function enhanceCombatHeaders() {
    if (!isSessionPage() || isEmbed()) return;
    document.querySelectorAll('.stat-block').forEach(function (block) {
      if (block.querySelector('.combat-glyph')) return;
      var nameEl = block.querySelector('.stat-block-name');
      var name = nameEl ? nameEl.textContent.trim() : 'Encounter';
      var hp = 10, dif = '';
      block.querySelectorAll('.stat-chip').forEach(function (chip) {
        var t = chip.textContent;
        var mHp = t.match(/HP:\s*(\d+)/i);
        var mDif = t.match(/DIF:\s*(\d+)/i);
        if (mHp) hp = parseInt(mHp[1], 10);
        if (mDif) dif = mDif[1];
      });
      var countMatch = name.match(/×\s*(\d+)/);
      var count = countMatch ? parseInt(countMatch[1], 10) : 1;
      var baseName = name.replace(/\s*×\s*\d+/, '').trim();
      var foes = [];
      for (var i = 0; i < count; i++) {
        foes.push({
          name: count > 1 ? baseName + ' ' + (i + 1) : baseName,
          hp: hp,
          maxHp: hp,
          dif: dif
        });
      }
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'combat-glyph';
      btn.setAttribute('aria-label', 'Open combat tracker for ' + name);
      btn.setAttribute('data-combat-seed', JSON.stringify({ name: name, foes: foes }));
      btn.innerHTML = '<span class="combat-glyph-mark" aria-hidden="true">⚔</span><span>Tracker</span>';
      if (nameEl) {
        nameEl.style.display = 'flex';
        nameEl.style.alignItems = 'center';
        nameEl.style.gap = '10px';
        nameEl.style.flexWrap = 'wrap';
        nameEl.appendChild(btn);
      } else {
        block.insertBefore(btn, block.firstChild);
      }
    });
  }

  /* ── Sync gmscreen live tokens if present ── */
  function bridgeGmScreen() {
    if (pageFile() !== 'gmscreen.html') return;
    var hopeEl = document.getElementById('hope-count');
    var fearEl = document.getElementById('fear-count');
    if (!hopeEl || !fearEl) return;
    hopeEl.textContent = tokens.hope;
    fearEl.textContent = tokens.fear;
    if (typeof window.changeToken === 'function') {
      var orig = window.changeToken;
      window.changeToken = function (type, delta) {
        orig(type, delta);
        loadTokens();
        syncTokenUI();
      };
    }
  }

  function init() {
    applyEmbedMode();
    if (isEmbed()) return;

    loadTokens();
    loadClocks();
    loadCombat();
    rewriteNav();
    mountSessionChrome();
    enhanceCombatHeaders();
    bridgeGmScreen();
    restoreScroll();

    window.addEventListener('pagehide', saveScroll);
    window.addEventListener('beforeunload', saveScroll);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.HSChrome = {
    openFear: openFearPeek,
    openLocation: openLocationPeek,
    openCalendar: openCalendarPeek,
    openCombat: openCombatPeek,
    openNotes: openNotesDock,
    closeNotes: closeNotesDock,
    toggleNotes: toggleNotesDock,
    closePeek: closePeek,
    sessions: SESSIONS
  };
})();
