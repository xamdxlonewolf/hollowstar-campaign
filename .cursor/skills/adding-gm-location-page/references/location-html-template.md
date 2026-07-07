# Location HTML Skeleton

Reference: `emberford.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[Location Name] — HollowStar GM</title>
<link rel="stylesheet" href="shared.css">
<style>
/* Page-specific only — copy from emberford.html as needed */
.location-badge{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;padding:3px 10px;border-radius:99px;margin-right:4px;margin-bottom:4px;}
.loc-town{background:var(--warn-bg);color:var(--warn-text);border:1px solid rgba(201,125,42,0.3);}
.room-card{background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);padding:12px 14px;margin-bottom:9px;}
.room-name{font-size:13px;font-weight:700;color:var(--accent-gold-light);margin-bottom:2px;}
.room-price{font-size:12px;color:var(--accent-gold);float:right;font-weight:700;}
.gossip-card{background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px 13px;margin-bottom:8px;display:flex;gap:10px;align-items:flex-start;}
.gossip-source{font-size:11px;font-weight:700;color:var(--accent-gold);min-width:80px;flex-shrink:0;}
.gossip-text{font-size:12.5px;color:var(--text-secondary);line-height:1.6;}
.gossip-truth{font-size:11px;color:var(--fear-text);font-style:italic;margin-top:3px;}
</style>
</head>
<body>

<nav class="site-nav">
  <div class="site-nav-brand">⭐ HollowStar GM</div>
  <a href="index.html">🏠 Hub</a>
  <!-- sessions -->
  <a href="[location].html" class="active">🏘️ [Location]</a>
  <a href="calendar.html">📅 Calendar</a>
  <a href="notes.html">📝 Notes</a>
  <a href="gmscreen.html">🎲 GM Screen</a>
</nav>

<header class="page-header">
  <div class="eyebrow">Location Reference</div>
  <h1>[Location Name]</h1>
  <p class="subtitle">Everything your players can see, ask about, buy, eat, drink, or discover.</p>
</header>

<div class="page-body">

  <div class="nav-tabs">
    <button class="nav-tab active" onclick="filterSections('all',this)">All</button>
    <button class="nav-tab" onclick="filterSections('town',this)">Town</button>
    <button class="nav-tab" onclick="filterSections('inn',this)">The Inn</button>
    <button class="nav-tab" onclick="filterSections('shops',this)">Shops & People</button>
    <button class="nav-tab" onclick="filterSections('gossip',this)">Gossip</button>
  </div>

  <div class="section" data-cat="town">
    <div class="section-header open" onclick="toggleSection(this)">
      <div class="section-icon" style="background:var(--warn-bg);color:var(--warn-text);">🏘️</div>
      <div style="flex:1;">
        <div class="section-label">Arriving in [Location]</div>
        <div class="section-sub">What to say · First impressions · Layout</div>
      </div>
      <span class="section-chevron">▾</span>
    </div>
    <div class="section-body open">
      <div class="gm-say">
        <div class="tag">GM: Say this when players first see [location]</div>
        <p>"..."</p>
      </div>
      <div class="ref-box">
        <div class="ref-title">Town facts — for if players ask</div>
        <ul>
          <li><strong>Population:</strong> ...</li>
          <li><strong>Economy:</strong> ...</li>
          <li><strong>Governance:</strong> ...</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- More sections: inn, shops, gossip -->

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

## NPC Card Pattern

```html
<div class="npc-card">
  <div class="npc-name">[Name]</div>
  <div class="npc-role">[Role] · [Ancestry] · [Age] · [Pronouns]</div>
  <div class="npc-voice">🎭 Voice: [delivery notes]</div>
  <p>[Player-visible description and behavior]</p>
  <div class="npc-secret">GM only: [secret]</div>
</div>
```

## Price Table Pattern

```html
<table class="price-table">
  <tr><th>Item</th><th>Price</th></tr>
  <tr><td>[Item]</td><td>[X copper/silver/gold]</td></tr>
</table>
```

## Gossip Pattern

```html
<div class="gossip-card">
  <div class="gossip-source">[Who says it]</div>
  <div>
    <div class="gossip-text">"[The rumor]"</div>
    <div class="gossip-truth">Truth: [what's actually going on]</div>
  </div>
</div>
```
