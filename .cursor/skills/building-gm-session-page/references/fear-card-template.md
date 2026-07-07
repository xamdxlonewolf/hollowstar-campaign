# Fear Card Template

For `fear_options_sessionN.html`. Copy page `<style>` from `fear_options.html`.

## Anchor ID Convention

```
fs-s{N}-{scene}-{slug}
```

Examples:
- `fs-s2-a1-crows`
- `fs-s2-c4-thorn`
- `fs-s2-rt-scout`

## Card HTML

```html
<div class="fear-card" id="fs-sN-scene-slug">
  <div class="fear-card-header">
    <div class="fear-card-scene">Act N — [Scene Name]</div>
    <div class="fear-card-title">[Fear Spend Title]</div>
    <div class="fear-card-cost">😨 1 Fear</div>
  </div>
  <div class="fear-card-body">

    <div class="trigger-box">
      <div class="tag">What triggers this</div>
      <p>[When to spend Fear — beat, mood, pacing note]</p>
    </div>

    <div class="say-box">
      <div class="tag">GM Say — Read this aloud</div>
      <p>"[Narration or dialogue to deliver]"</p>
    </div>

    <div class="gm-only-box">
      <div class="tag">GM Info — What's actually happening</div>
      <p>[Truth behind the moment — may reference 07_Campaign/GM_Only]</p>
    </div>

    <!-- Optional: if player roll involved -->
    <div class="roll-box">
      <div class="tag">Optional Roll — [context]</div>
      <div class="roll-row">
        <div class="roll-chip"><strong>Stat:</strong> Instinct</div>
        <div class="roll-chip"><strong>DIF:</strong> 12</div>
      </div>
      <div class="roll-outcomes">
        <div class="ro ro-fail"><div class="ro-label">Failure</div><p>...</p></div>
        <div class="ro ro-partial"><div class="ro-label">Partial</div><p>...</p></div>
        <div class="ro ro-success"><div class="ro-label">Success</div><p>...</p></div>
      </div>
    </div>

    <div class="consequence-grid">
      <div class="cq"><div class="cq-label cq-now">Right Now</div><p>...</p></div>
      <div class="cq"><div class="cq-label cq-soon">This Session</div><p>...</p></div>
      <div class="cq"><div class="cq-label cq-later">Long Term</div><p>...</p></div>
    </div>

    <div class="return-bar">📖 <a href="sessionN.html#section-id">Return to [Scene]</a> — [what to do next]</div>
  </div>
</div>
```

## Scene Dividers

Group cards by act/scene:
```html
<div class="scene-divider">🏛️ Council Meeting — Beat 3</div>
```

## Quick Nav (top of page)

```html
<div class="fear-nav">
  <a href="#fs-sN-anchor" class="fear-nav-btn">🐦 Short Label</a>
</div>
```

## Inline Session Reference (in sessionN.html)

Keep one-line summary in `.fear-box ul li`. Full expansion lives only on fear page.

## Economy Notes

Include `.fear-note` in session page fear-boxes:
- "Use one at most during Act 1"
- "Save Fear for combat"
- Match Session 1 pacing guidance tone
