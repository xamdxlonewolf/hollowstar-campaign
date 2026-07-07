# Session HTML Skeleton

Copy from `session1.html` and replace content. Do not alter `shared.css`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Session N — [Title] · HollowStar GM</title>
<link rel="stylesheet" href="shared.css">
</head>
<body>

<nav class="site-nav">
  <div class="site-nav-brand">⭐ HollowStar GM</div>
  <a href="index.html">🏠 Hub</a>
  <a href="session1.html">📖 Session 1</a>
  <!-- add sessionN.html, active on this page -->
  <a href="emberford.html">🏘️ Emberford</a>
  <a href="calendar.html">📅 Calendar</a>
  <a href="notes.html">📝 Notes</a>
  <a href="gmscreen.html">🎲 GM Screen</a>
</nav>

<header class="page-header">
  <div class="eyebrow">GM Reference & Script — Session N</div>
  <h1>[Session Title]</h1>
  <p class="subtitle">[In-world date]. [One-line pitch.]</p>
  <div class="party-chips">
    <span class="party-chip">🌿 Greer — Faun Druid</span>
    <!-- party present -->
  </div>
  <div class="session-meta">
    <div class="meta-item">⏱ <strong>X–Y hours</strong></div>
    <div class="meta-item">📅 <strong>[Month Day, 700 AR]</strong></div>
    <div class="meta-item">📍 <strong>[Location]</strong></div>
  </div>
</header>

<div class="page-body">
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="filterSections('all',this)">All</button>
    <button class="nav-tab" onclick="filterSections('open',this)">Opening</button>
    <!-- more tabs matching data-cat -->
  </div>

  <!-- Session Overview -->
  <div class="section" data-cat="ref">
    <div class="section-header open" onclick="toggleSection(this)">
      <div class="section-icon" style="background:var(--accent-gold-dim);color:var(--accent-gold);">🗺️</div>
      <span class="section-label">Session Overview & Flow</span>
      <span class="section-pill" style="background:var(--info-bg);color:var(--info-text);border:1px solid rgba(74,127,181,0.3);">Read First</span>
      <span class="section-chevron">▾</span>
    </div>
    <div class="section-body open">
      <div class="timeline">
        <div class="timeline-item">
          <div class="timeline-badge tb-1">~40 min</div>
          <div class="timeline-text"><strong>Act 1 — [Name].</strong> [summary] <em>Goal: ...</em></div>
        </div>
        <!-- more acts -->
      </div>
    </div>
  </div>

  <!-- Acts: repeat section pattern -->
  <div class="section" id="act1" data-cat="open">
    <div class="section-header open" onclick="toggleSection(this)">
      <!-- icon, label, sub, pill, chevron -->
    </div>
    <div class="section-body open">
      <div class="gm-say"><div class="tag">GM Say — [context]</div><p>"..."</p></div>
      <div class="fear-box">
        <div class="fear-box-title">😨 Fear Spends — [Scene]</div>
        <ul>
          <li><a href="fear_options_sessionN.html#fs-sN-anchor"><strong>[Title]</strong></a> — [one line]</li>
        </ul>
        <div class="fear-note">[economy guidance]</div>
      </div>
    </div>
  </div>

  <div class="quick-ref">
    <div class="quick-ref-title">⚡ GM Cheat Sheet</div>
    <div class="stat-grid">
      <div class="stat-item"><strong>Date:</strong> ...</div>
    </div>
  </div>
</div>

<script>
function toggleSection(h){const o=h.classList.contains('open');h.classList.toggle('open',!o);h.nextElementSibling.classList.toggle('open',!o);}
function filterSections(cat,btn){
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.section').forEach(s=>{
    if(cat==='all'||s.dataset.cat===cat)s.classList.remove('hidden');
    else s.classList.add('hidden');
  });
}
</script>
</body>
</html>
```

## Timeline Badge Colors

- `tb-1` — hope (opening)
- `tb-2` — warn (main scenes)
- `tb-3` — purple (social/planning)
- `tb-4` — fear (combat/danger)
- `tb-5` — info (ending)
