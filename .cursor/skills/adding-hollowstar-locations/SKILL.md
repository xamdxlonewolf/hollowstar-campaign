---
name: adding-hollowstar-locations
description: Adds or expands towns, cities, landmarks, and districts in the HollowStar vault. Use when creating settlements, promoting locations to session importance, or syncing location detail from gm_sessions_site.
paths:
  - "HollowStar/**"
---

# Adding HollowStar Locations

## When to Use

- New town, city, landmark, or district
- Expanding Emberford-scale locations toward Lumencrest depth
- Syncing `gm_sessions_site/` location pages back to the vault

## Decision Tree

```
Is it a major campaign hub (10k+ pop, multi-session)?
  YES → City subfolder (see Lumencrest pattern)
  NO → Is it a distinct geographic feature (grove, ruin, lake)?
    YES → Locations/Landmarks/<Name>.md
    NO → Locations/Towns/<Name>.md
```

See `hollowstar-world-building/references/folder-map.md` for full map.

## Town Template (Tier 3)

File: `02_Regions/<Region>/Locations/Towns/<Name>.md`

```markdown
# [Name]

**Population:** ~[number]  
**Region:** [[02_Regions/<Region>/<Region>_Index|<Region>]]  
**Location:** [geographic context]  
**Economy:** [primary industries]  
**Notable:** [one-line hook]

---

## OVERVIEW

[2–3 paragraphs: what it feels like, why it exists, current tension]

---

## [KEY SUBSYSTEM]

[e.g. governance, ford/bridge, grove connection, faction presence]

---

## CURRENT TENSIONS

[What's actively contested or changing]

---

## ADVENTURE HOOKS

- [Hook 1]
- [Hook 2]

---

**Back to [[02_Regions/<Region>/Locations/Location_Index|Location Index]]**
```

## Landmark Template

File: `Locations/Landmarks/<Name>.md`

Sections: Overview, Protection/Guardians, Sacred Nature, Current Threat, Adventure Hooks.

See `Ember_Grove.md` as reference.

## Major City Subfolder (Tier 1)

Mirror `Lumencrest/`:

| File | Purpose |
|------|---------|
| `<City>_Index.md` | How to use, at-a-glance, links to all files |
| `Arriving_in_<City>.md` | First impressions, sensory entry |
| `Districts_Overview.md` | Spatial layout |
| `01_`–`08_` district files | Compact run reference |
| `*_Expanded.md` | Deep dives (optional pairs) |
| `NPCs.md` + `*_NPC_INDEX.md` | Local characters |
| `Factions_and_Reputation.md` | Player-facing faction interactions |

Start with Index + Arriving + Districts_Overview + one district. Expand as sessions demand.

## Required Index Updates

Every new location file must be linked from:
- `Locations/Location_Index.md` (table row)
- Parent `<Region>_Index.md` if listed there
- `00_Index/README.md` only if major campaign significance

## Canon Sync from gm_sessions_site

When `emberford.html` (or similar) has detail not in HollowStar:

1. Merge player-askable facts into town/landmark `.md`
2. Merge NPCs via `adding-hollowstar-npcs`
3. Keep **prices, menus, room names** in gm_site for table speed; summarize in vault ("The Emberflow Arms — see session site for menu") OR copy full detail if vault is canonical store — **prefer full copy to vault** per user preference for sync
4. GM-only secrets stay in NPC Secret fields, not player handouts

## Promoting Emberford-Style Towns

When party returns or location recurs:
- Add **Governance** section with named elders
- Add **Notable Establishments** with proprietors
- Link grove/landmark files
- Consider `adding-gm-location-page` if not already built
