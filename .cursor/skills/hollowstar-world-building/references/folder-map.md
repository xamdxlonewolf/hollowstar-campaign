# HollowStar Folder Map

```
HollowStar/
├── 00_Index/              Master README, entry point
├── 01_Core_Concepts/      Hollowstars, Darkness, Themes and Tone
├── 01_World_Overview/     Geography, calendar, economy, peoples
├── 02_Regions/            All regional content
│   └── <Region>/
│       ├── <Region>_Index.md
│       ├── Geography.md, Culture_and_Society.md, Adventure_Hooks.md
│       └── Locations/
│           ├── Location_Index.md
│           ├── Cities/          Major cities (file or subfolder)
│           ├── Towns/           Smaller settlements (usually single .md)
│           ├── Landmarks/       Groves, ruins, natural features
│           └── Dungeons/
├── 04_Factions/           Faction_Overview + regional faction files
├── 05_Religion/           Faith systems
├── 07_Campaign/           GM-only campaign arc docs
│   └── GM_Only/           The_Truth, Faction_Clocks, Living_Factions
├── 08_GM_Notes/           GM toolkit (player-safe when noted)
│   ├── Sessions/          Per-session prep & play notes
│   └── Player_Characters/
└── 09_NPCs/               Regional NPC compendiums
```

## City Depth Tiers

**Tier 1 — Major city** (Lumencrest): Subfolder with Index, districts, `_Expanded` deep dives, local NPCs, conditions reference.

**Tier 2 — Significant city** (Kingsrest, Ironhold): Single rich `.md` file or small subfolder if session-heavy.

**Tier 3 — Town** (Emberford): Single file in `Towns/`. Landmark nearby → separate `Landmarks/` file.

**Tier 4 — Village / site**: Mention in regional geography or adventure hooks until session-relevant.

## When to Promote a Location

Promote from Tier 3 → Tier 2 (or create gm_sessions_site location page) when:
- Party spends a full session or more there
- 5+ named NPCs need tracking
- Economic/political details players will query repeatedly
