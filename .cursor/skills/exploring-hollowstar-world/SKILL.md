---
name: exploring-hollowstar-world
description: Explores and summarizes the HollowStar vault for canon lookup, consistency checks, and prep research. Use when asking what exists about a topic, finding connections between regions/factions, or verifying lore before writing.
paths:
  - "HollowStar/**"
---

# Exploring HollowStar World

Read-only research skill. Do not edit files unless the user explicitly asks to record findings.

## When to Use

- "What do we know about X?"
- "Is this consistent with canon?"
- "What factions care about Y?"
- Prep research before drafting session notes or world additions
- Finding gaps before building gm_sessions_site pages

## Search Strategy

1. **Start at indexes:** `00_Index/README.md`, regional `*_Index.md`, `Location_Index.md`
2. **Broad grep:** Topic name across `HollowStar/`
3. **Follow wikilinks:** Trace `[[...]]` references depth-first
4. **Check GM layers:**
   - Player-safe: `02_Regions/`, `09_NPCs/`, `04_Factions/`
   - GM operating: `08_GM_Notes/`
   - GM-only truth: `07_Campaign/GM_Only/` — **only include if user requests spoilers**
5. **Cross-check gm_sessions_site:** Session-local detail may be richer (Emberford NPCs, prices)

## Output Format

Structure findings as:

### Summary
[2–4 sentences answering the question]

### Canon Sources
| File | What it says |
|------|--------------|
| `path` | [fact] |

### Connections
- [Related faction, location, clock, mystery]

### Gaps & Conflicts
- [Missing info or contradictions — cite both sources]

### Suggested Next Steps
- [Which skill to invoke: add NPC, expand location, draft session notes, build site]

## Spoiler Handling

| User ask | Include GM_Only? |
|----------|------------------|
| "What would Greer know?" | No — player character knowledge only |
| "Prep session 2" | Yes — GM operating + relevant secrets tier |
| "What are Hollowstars?" | Player-facing theories + note GM_Only has definitive truth |

## Key Relationship Maps

**The dimming pattern (30 years):**
- Lumencrest Heart dimming ↔ ancient sites awakening ↔ approaching star

**Party entry points (Session 1+):**
- Greer → Thorn, Green Covenant, Ember Grove protection
- Lurielle → Endless Eye research, Hollostar resonance
- Basil → House Vael, Silverhand family, heist thread

**Faction pressure on current arc:**
- House Vael / Council of Lumens ↔ Emberford timber ↔ Green Covenant Thorns

## Do Not Touch

- `HollowStar/.obsidian/`
