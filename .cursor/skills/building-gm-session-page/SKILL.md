---
name: building-gm-session-page
description: Builds interactive GM session pages in gm_sessions_site from HollowStar session notes — session HTML, per-session fear options, hub/nav updates, and canon sync back to HollowStar. Use when converting session notes to runnable table reference or adding a new session.
paths:
  - "gm_sessions_site/**"
  - "HollowStar/08_GM_Notes/Sessions/**"
---

# Building GM Session Pages

Creates runnable offline HTML for the HollowStar GM toolkit from `HollowStar/08_GM_Notes/Sessions/` notes.

## When to Use

- Session notes marked `READY FOR SITE`
- "Build session 2 page," "convert notes to HTML"
- Adding Fear spend pages for a session

## Golden Rules

1. **Clone Session 1 patterns** — Read `session1.html` and `fear_options.html` before building
2. **Use `shared.css` only** — No new theme colors/fonts. Page-specific CSS in `<style>` only when necessary (see `emberford.html`)
3. **Offline-first** — No external CDN dependencies
4. **Sync canon** — After building, update HollowStar world files with any new detail

## Files to Create/Update

| Artifact | Path |
|----------|------|
| Session script | `gm_sessions_site/sessionN.html` |
| Fear expansions | `gm_sessions_site/fear_options_sessionN.html` |
| Hub card + nav | `gm_sessions_site/index.html` |
| Site nav (all pages) | Add `sessionN.html` link to every page's `<nav class="site-nav">` |
| Calendar marker | `gm_sessions_site/calendar.html` if date known |
| Location page | `adding-gm-location-page` if new/updated town |

**Legacy note:** Session 1 uses `fear_options.html` (no suffix). Sessions 2+ use `fear_options_sessionN.html`.

## Session Page Structure

See `references/session-html-template.md`. Required elements:

```
<!DOCTYPE html> + shared.css
<nav class="site-nav"> — consistent across all pages
<header class="page-header"> — eyebrow, h1, party-chips, session-meta
<div class="page-body">
  <div class="nav-tabs"> — filter buttons
  <div class="section" data-cat="..."> — collapsible acts
  <div class="quick-ref"> — GM cheat sheet at bottom
<script> toggleSection, filterSections
```

### Section `data-cat` values

Use consistent categories: `open`, `council`, `npc`, `travel`, `combat`, `ref` — add as needed. Match tab buttons.

### Content block classes (from shared.css)

| Class | Use |
|-------|-----|
| `.gm-say` | GM narration, scene-setting |
| `.npc-say` | NPC dialogue + `.note` for stage direction |
| `.thorn-say` | Thorn Oakwise — include `.voice-guide` |
| `.gm-note` | GM info, roll prompts, secrets-lite |
| `.danger-note` | Serious warnings |
| `.fear-box` | Inline Fear spend list — **link to fear page** |
| `.ref-box` | Reference lists, facts |
| `.npc-card` | NPC stat blocks with `.npc-secret` |
| `.stat-block` | Combat enemies |
| `.timeline` + `.timeline-badge` | Act flow with time badges |
| `.handout` | Player-facing read-aloud summary |
| `.tip-box` | Pacing advice |
| `.outcome-grid` | Fail/Partial/Success |
| `.path-grid` | Branching choices (road vs grove) |
| `.combat-primer` | Daggerheart reminder if first combat |

### Fear box linking

Inline session page:
```html
<li><a href="fear_options_session2.html#fs-s2-council-thorn"><strong>Thorn says "No"</strong></a> — ...</li>
```

Fear page return link:
```html
<div class="return-bar">📖 <a href="session2.html#council">Return to Council Meeting</a></div>
```

Use matching `id` on session sections for anchor targets: `<div class="section" id="council" ...>`.

## Fear Options Page (per session)

File: `fear_options_sessionN.html`

1. Copy structure from `fear_options.html` — page-specific `<style>` for `.fear-card`, `.fear-nav`, etc.
2. Quick nav bar at top linking all `#fs-*` anchors
3. Each fear card: see `references/fear-card-template.md`
4. Anchor ID convention: `fs-{act}{beat}-{slug}` e.g. `fs-s2-a1-crows`, `fs-s2-c4-thorn`
5. Link fear page from session nav optional; always link from session fear-boxes

## index.html Updates

Add hub card:
```html
<a href="sessionN.html" class="hub-card session">
  <div class="card-icon">📖</div>
  <div class="card-title">Session N — [Title]</div>
  <div class="card-desc">[one-line summary]</div>
  <div class="card-tags">...</div>
  <div class="hub-status ready">● Ready to run</div>
</a>
```

Update `campaign-banner` **Current Session** and **In-World Date** when appropriate.

## Nav Bar Update

Every HTML file in `gm_sessions_site/` shares nav. When adding session 2, add to ALL files:
```html
<a href="session2.html">📖 Session 2</a>
```

Keep Session 1 link. Order: Hub → Sessions (numeric) → Locations → Calendar → Notes → GM Screen.

## JavaScript (copy verbatim)

```javascript
function toggleSection(h){const o=h.classList.contains('open');h.classList.toggle('open',!o);h.nextElementSibling.classList.toggle('open',!o);}
function filterSections(cat,btn){
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.section').forEach(s=>{
    if(cat==='all'||s.dataset.cat===cat)s.classList.remove('hidden');
    else s.classList.add('hidden');
  });
}
```

## Build Workflow

1. Read `HollowStar/08_GM_Notes/Sessions/Session_NN_*.md`
2. Explore related HollowStar + existing gm_site location pages
3. Create `sessionN.html` with full act structure
4. Create `fear_options_sessionN.html` for every Fear window in notes
5. Update `index.html` + all nav bars
6. Update `calendar.html` session marker
7. Create/update location page if needed (`adding-gm-location-page`)
8. **Canon sync back to HollowStar:**
   - New NPCs → `adding-hollowstar-npcs`
   - Location detail → `adding-hollowstar-locations`
   - Mark session note `SYNCED` with checklist complete
9. Open `sessionN.html` in browser mentally verify: nav links, fear links, anchors

## Player Additions During Campaign

When session notes include player-established facts:

1. Add to session HTML (players may reference site next session)
2. Sync to HollowStar in same pass — vault is long-term canon
3. Update location pages if player-named shops, NPCs, or rumors

## Quality Checklist

- [ ] All acts have time pills and timeline entry
- [ ] Every Fear spend has fear page card + return link
- [ ] `quick-ref` cheat sheet at bottom with key DCs, names, dates
- [ ] Party chips match current roster
- [ ] Plateau ending / cliffhanger section exists
- [ ] No broken relative links
- [ ] HollowStar vault updated to match
