---
name: adding-gm-location-page
description: Creates or updates interactive location reference pages in gm_sessions_site (towns, cities, sites). Use when the party will spend time somewhere and needs player-askable detail — inns, shops, gossip, NPCs — with canon sync to HollowStar.
paths:
  - "gm_sessions_site/**"
  - "HollowStar/02_Regions/**"
---

# Adding GM Location Pages

Player-askable location bibles for the GM toolkit. Reference: `emberford.html`.

## When to Use

- Party arriving at a new town/city for a session+
- Expanding an existing location (Lumencrest arrival → full city page)
- Syncing richer gm_site detail back to HollowStar vault

## Golden Rules

1. **Match `emberford.html` patterns** — tabs, sections, block types
2. **`shared.css` + minimal page-specific CSS** in `<style>` (`.room-card`, `.gossip-card`, etc.)
3. **Player-askable detail** — prices, names, menus, layout, gossip
4. **GM secrets** in `.npc-secret` inside `.npc-card`, never in `.gm-say` player read-alouds
5. **Sync to HollowStar** after every create/update

## File Naming

```
gm_sessions_site/<location-slug>.html
```

Examples: `emberford.html`, `lumencrest.html`, `greenwatch.html`

Lowercase, no spaces. Link from `index.html` hub and session nav.

## Page Structure

See `references/location-html-template.md`.

### Standard Tabs (`data-cat`)

Adapt to location — not every tab required:

| Tab | `data-cat` | Content |
|-----|------------|---------|
| All | (filter all) | — |
| Town | `town` | Arrival narration, layout, facts |
| The Inn | `inn` | Rooms, menu, staff |
| Shops & People | `shops` | Buildings, proprietors |
| [Feature] | `grove`, `district`, etc. | Location-specific |
| Gossip | `gossip` | Rumors with `.gossip-truth` GM notes |

### Essential Blocks

- **Arriving** — two `.gm-say` blocks (distant view, entering)
- **Town facts** — `.ref-box` with population, economy, governance
- **Layout** — `.ref-box` bullet list of districts/areas
- **NPC cards** — `.npc-card` with `.npc-voice` and `.npc-secret`
- **Prices** — `.price-table` for rooms, food, services
- **Gossip** — `.gossip-card` with `.gossip-source` and `.gossip-truth`

### Location Badges (optional CSS)

```html
<span class="location-badge loc-town">Town</span>
<span class="location-badge loc-grove">Grove</span>
<span class="location-badge loc-inn">Inn</span>
```

Copy badge styles from `emberford.html` `<style>` block.

## index.html Hub Card

```html
<a href="lumencrest.html" class="hub-card location">
  <div class="card-icon">🏙️</div>
  <div class="card-title">Lumencrest</div>
  <div class="card-desc">[what players can query]</div>
  <div class="card-tags">...</div>
  <div class="hub-status ready">● Ready</div>
</a>
```

## Nav Bar

Add location link to every page:
```html
<a href="lumencrest.html">🏙️ Lumencrest</a>
```

## Canon Sync → HollowStar

After building/updating location page:

1. **Town/Landmark file** — `adding-hollowstar-locations` to merge facts, governance, tensions
2. **NPCs** — `adding-hollowstar-npcs` for every `.npc-card`
3. **Population/stats** — reconcile conflicts; prefer most recent played detail
4. **Session note** — link location page in GM Site Build Notes section

### What to sync

| gm_site content | HollowStar target |
|-----------------|-------------------|
| Population, economy | Town `.md` OVERVIEW |
| Named elders, governance | Town `.md` + NPCs |
| Innkeeper, shopkeepers | `09_NPCs/` + town file |
| Grove/landmark lore | `Landmarks/` file |
| Gossip (true) | Adventure hooks or GM notes |
| Gossip (false) | "What People Are Saying" or town rumors |

## Player Additions

When players name a shop, NPC, or local fact during play:

1. Add to location HTML immediately (or next build)
2. Add to HollowStar town + NPC files
3. Mark as player-established in session notes

## Lumencrest Note

Lumencrest is Tier 1 in HollowStar (`Lumencrest/` subfolder with districts). The gm_site page should start as **arrival + first district players enter** — not the entire city at once. Expand tabs as campaign progresses. Link to HollowStar district files for deep reference.

## Quality Checklist

- [ ] Arrival read-alouds sound like Session 1 quality prose
- [ ] Every NPC has voice guide + GM secret
- [ ] Prices are internally consistent with `01_World_Overview/Economy_Trade_Currency.md`
- [ ] Gossip includes truth layer for GM
- [ ] Linked from index.html + all nav bars
- [ ] HollowStar vault updated to match
