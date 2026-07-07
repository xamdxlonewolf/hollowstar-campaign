---
name: drafting-hollowstar-session-notes
description: Drafts and updates per-session prep notes in HollowStar/08_GM_Notes/Sessions/. Use when prepping a new session, outlining scenes, recording player decisions, or preparing notes for gm_sessions_site conversion.
paths:
  - "HollowStar/08_GM_Notes/**"
---

# Drafting HollowStar Session Notes

## When to Use

- "Prep session 2," "outline next session," "record what happened"
- Before converting notes to `gm_sessions_site/` (hand off to `building-gm-session-page`)
- After play — capture decisions, new NPCs, world changes

## File Location & Naming

```
HollowStar/08_GM_Notes/Sessions/Session_NN_<Short_Title>.md
```

Examples: `Session_01_Ember_Grove.md`, `Session_02_Lumencrest_Arrival.md`

Use zero-padded session numbers. See `references/session-note-template.md` for full template.

## Workflow

### Before Session (Prep)

1. Read `exploring-hollowstar-world` outputs or run exploration yourself
2. Check `08_GM_Notes/Countdown_Clocks.md` and `Faction_Tension_Tracker.md`
3. Read previous session note — carry forward **Active Threads** and **Unresolved**
4. Draft acts, beats, NPCs, Fear windows (outline level — not full dialogue)
5. Note which locations need gm_site pages (new town? existing `emberford.html`?)

### After Session (Record)

1. Fill **Player Decisions** and **Consequences**
2. List **New NPCs / Player Establishments** — flag for `adding-hollowstar-npcs`
3. Update **World State Changes** — flag for clocks, factions, location files
4. Mark note status: `DRAFT` → `READY FOR SITE` → `PLAYED` → `SYNCED`

### Canon Propagation (required after play)

| Session note section | Update target |
|---------------------|---------------|
| New NPCs | `09_NPCs/`, location files |
| Player-named facts | Location + session note |
| Faction shifts | `Faction_Tension_Tracker.md` |
| Timeline advances | `Countdown_Clocks.md` |
| Secrets revealed | `Secrets_and_Revelations.md` (GM only) |
| Permanent location detail | `02_Regions/` via `adding-hollowstar-locations` |

## Handoff Checklist → gm_sessions_site

When notes reach `READY FOR SITE`:

- [ ] Metadata complete (date, location, runtime, party present)
- [ ] Acts with time estimates
- [ ] NPC list with voice notes for scripted scenes
- [ ] Fear windows identified (scene + trigger + 1-line effect)
- [ ] Combat/stat blocks sketched if needed
- [ ] Session end image/cliffhanger defined
- [ ] Location page needs noted (new / update existing)

Invoke `building-gm-session-page` with the session note path.

## Retroactive Session 1

`Session_01_Ember_Grove.md` can be backfilled from `gm_sessions_site/session1.html` to establish the pattern. Extract acts, key beats, NPCs, threads — not full dialogue duplication.

## Integration with Player Characters

Reference `08_GM_Notes/Player_Characters/` for PC hooks. Note per-player spotlight moments in each act.
