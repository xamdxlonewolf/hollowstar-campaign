---
name: hollowstar-world-building
description: Manages the HollowStar campaign world vault — tone, folder structure, wikilinks, canon consistency, and cross-referencing. Use when adding or editing lore, locations, NPCs, factions, session notes, or any file under HollowStar/.
paths:
  - "HollowStar/**"
---

# HollowStar World Building

Umbrella skill for all work in the `HollowStar/` Obsidian vault (World of Hollowstars, Daggerheart campaign).

## When to Use

- Any create, edit, or expand task under `HollowStar/`
- Canon questions, consistency checks, or "where does this go?"
- After sessions when player actions change the world
- Syncing facts from `gm_sessions_site/` or session notes back into the vault

## Do Not Touch

- `HollowStar/.obsidian/` — Obsidian config/plugins
- `apex/` or root `f*.sql` files if present — APEX exports

## Core Principles

Read `references/tone-guardrails.md` before writing new content.

1. **Mystery stays mysterious** — Hollowstar origin, the Dreamer, ultimate answers live in `07_Campaign/GM_Only/`. Player-facing text hints; it does not explain.
2. **Moral gray** — Factions have valid concerns. Avoid cartoon villains.
3. **Grounded wonder** — Beautiful impossible things, political stakes, personal consequences.
4. **Player agency changes the world** — When players establish facts at the table, record them in session notes AND propagate to the relevant world files.

## Folder Map

See `references/folder-map.md` for the full placement guide. Quick rules:

| Content | Location |
|---------|----------|
| Session prep & play notes | `08_GM_Notes/Sessions/` |
| Player characters | `08_GM_Notes/Player_Characters/` |
| GM operating docs | `08_GM_Notes/` (clocks, factions, secrets) |
| Regional geography & cities | `02_Regions/<Region>/` |
| Regional NPC compendiums | `09_NPCs/<Region>/NPCs.md` |
| Major city deep dives | `02_Regions/.../Cities/<City>/` |
| GM-only truth | `07_Campaign/GM_Only/` |

## Wikilink Conventions

- Use Obsidian wikilinks: `[[path/to/file|Display Name]]`
- New location files must link back to their regional index and include a back-link footer
- Cross-reference related factions in `04_Factions/`, religion in `05_Religion/`
- Calendar: Accord Reckoning (700 AR current), months per `01_World_Overview/Calendar_and_Timekeeping.md`

## Workflow for Any Addition

1. **Read first** — Search existing files for the topic. Never duplicate without checking.
2. **Place correctly** — Use the folder map. Delegate to specialized skills when appropriate:
   - NPCs → `adding-hollowstar-npcs`
   - Locations → `adding-hollowstar-locations`
   - Session prep → `drafting-hollowstar-session-notes`
   - Research only → `exploring-hollowstar-world`
3. **Write in vault voice** — Prose paragraphs for lore; scannable headers for reference. Match nearby files.
4. **Update indexes** — Every new file gets linked from its parent index (`Location_Index`, `*_Index.md`, `09_NPCs/README.md`).
5. **Sync canon** — If `gm_sessions_site/` has richer detail, treat the more specific recent version as authoritative unless it contradicts `07_Campaign/GM_Only/`. Reconcile conflicts; ask the user if GM-only truth is involved.
6. **Post-session sync** — After sessions, update:
   - `08_GM_Notes/Sessions/Session_N_*.md` (decisions, new facts)
   - `08_GM_Notes/Faction_Tension_Tracker.md` if reputations shifted
   - `08_GM_Notes/Countdown_Clocks.md` if timelines advanced
   - `02_Regions/` and `09_NPCs/` for permanent world changes
   - Player-created facts (new shop, NPC name, local rumor) → appropriate location/NPC file

## Naming by Region

From `08_GM_Notes/Session Prep.md`:

- Lumencrest / Heartlands: Latin-ish (Cassius, Valeria)
- Endless Eye / Starfall Basin: Nature-themed (Dewleaf, Stoneskipper)
- Northern / Frostwell: Norse-ish (Bjorn, Freya)
- Verdant Crescent: Elvish (Aelindra, Theron)
- Rivermark: Mixed elven-Faun conventions

## Daggerheart Awareness

- Hope/Fear economy, Stress, countdown clocks — see `08_GM_Notes/Daggerheart Integration.md`
- Difficulty numbers in world docs are optional; session site carries table-ready stats

## Handoff to GM Session Site

When session notes are ready for the table, use `building-gm-session-page` to create `gm_sessions_site/` pages. World vault remains the long-term canon store; session site is the run-time reference.
