---
name: adding-hollowstar-npcs
description: Adds or updates NPCs in the HollowStar vault using established templates, regional naming, and index cross-links. Use when creating characters, shopkeepers, faction contacts, or syncing NPCs from session notes or gm_sessions_site.
paths:
  - "HollowStar/**"
---

# Adding HollowStar NPCs

## When to Use

- "Add an NPC," "who runs the inn," "create a contact in Lumencrest"
- Syncing NPCs introduced in play or built in `gm_sessions_site/`
- Expanding regional or city NPC lists

## Before Writing

1. Search `09_NPCs/` and the target location's `NPCs.md` / `*_NPC_INDEX.md`
2. Read `hollowstar-world-building/references/tone-guardrails.md`
3. Check `08_GM_Notes/Sessions/` for session-specific introductions

## Placement

| NPC scope | File |
|-----------|------|
| Regional wanderers, city outsiders | `09_NPCs/<Region>/NPCs.md` |
| Lumencrest locals | `02_Regions/.../Lumencrest/NPCs.md` + `Lumencrest_NPC_INDEX.md` |
| Town-local (Emberford-scale) | Add to town `.md` AND `09_NPCs/Central_Heartlands/NPCs.md` if notable |
| Cross-continental movers | `09_NPCs/Cross_Regional/Key NPCs.md` |

Append to existing regional files unless the user requests a standalone file.

## Template

Use `references/npc-template.md`. Minimum fields for table-ready NPCs:

- **Role**, **Ancestry/Age**, **Appearance**, **Personality**
- **Goals**, **Secret** (GM-facing)
- **Quote**, **Hook** (adventure entry point)

For city NPCs, add **What they reveal about the city** and **Working with them** when appropriate (see Lumencrest `NPCs.md`).

## Naming by Region

| Region | Style | Examples |
|--------|-------|----------|
| Lumencrest / Heartlands | Latin-ish | Cassius, Valeria, Caelen Vael |
| Endless Eye / Basin | Nature-themed | Dewleaf, Stoneskipper |
| Frostwell / Northern | Norse-ish | Bjorn, Freya |
| Verdant Crescent | Elvish | Aelindra, Theron |
| Salt Shore | Practical maritime | Voss, Brinehaven locals |

## Voice Guides

Session-important NPCs should include a one-line voice note for GM delivery:

> Voice: Efficient, direct. Warm once she's decided you're all right.

Match `thorn-say` / `npc-say` patterns in `gm_sessions_site/` when the NPC will appear in session pages.

## Cross-Linking

1. Add wikilink from location file: `[[09_NPCs/Central_Heartlands/NPCs#NPC Name|NPC Name]]` or inline mention
2. Update `Lumencrest_NPC_INDEX.md` (or equivalent) if city has an index
3. If NPC appears in active session notes, link both ways

## Canon Sync from gm_sessions_site

When an NPC exists in `gm_sessions_site/` (e.g. Bess Hollowell in `emberford.html`) but not HollowStar:

1. Extract: name, role, ancestry, personality, secrets, voice, hooks
2. Add to appropriate `09_NPCs/` and/or town file
3. Resolve population/stat conflicts — prefer the more recently played detail; note discrepancies in session notes if unresolved

## Player-Created NPCs

When players name or flesh out an NPC at the table:

1. Record in `08_GM_Notes/Sessions/Session_N_*.md` under **Player Establishments**
2. Add to world files within the same update pass
3. Mark player-established facts clearly (e.g. "Established in Session 2 by Tara")
