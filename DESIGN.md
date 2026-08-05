---
name: HollowStar GM Toolkit
description: Candlelit table reference for running HollowStar sessions offline.
colors:
  candlewick-gold: "#c9a84c"
  candlewick-gold-light: "#e8c86a"
  candlewick-gold-dim: "rgba(201,168,76,0.15)"
  inkwood: "#1a1714"
  desk-primary: "#242018"
  desk-secondary: "#2d2920"
  desk-card: "#2a251e"
  nav-black: "#13110e"
  parchment: "#f0ead8"
  parchment-secondary: "#a89f8a"
  parchment-muted: "#7a7060"
  border-soft: "rgba(255,255,255,0.1)"
  border-med: "rgba(255,255,255,0.18)"
  grove-hope: "#4a9e6e"
  grove-hope-bg: "rgba(74,158,110,0.15)"
  grove-hope-text: "#7dd4a0"
  ember-fear: "#b85450"
  ember-fear-bg: "rgba(184,84,80,0.15)"
  ember-fear-text: "#e88884"
  amber-warn: "#c97d2a"
  amber-warn-bg: "rgba(201,125,42,0.15)"
  amber-warn-text: "#e8a86a"
  lamp-info: "#4a7fb5"
  lamp-info-bg: "rgba(74,127,181,0.15)"
  lamp-info-text: "#7aafdf"
  violet-npc: "#8a60c8"
  violet-npc-bg: "rgba(138,96,200,0.15)"
  violet-npc-text: "#c4a0f0"
  marsh-teal: "#3a9898"
  marsh-teal-bg: "rgba(58,152,152,0.15)"
  marsh-teal-text: "#78d4d4"
typography:
  display:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(1.45rem, 3vw, 2.1rem)"
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: "0.015em"
  title:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "normal"
  body:
    fontFamily: "Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "normal"
  label:
    fontFamily: "Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.1em"
  ui-compact:
    fontFamily: "Segoe UI, system-ui, -apple-system, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "normal"
rounded:
  sm: "6px"
  md: "10px"
  lg: "14px"
  pill: "99px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "28px"
  page-x: "1.5rem"
  page-y: "1.75rem"
components:
  nav-tab:
    backgroundColor: "transparent"
    textColor: "{colors.parchment-secondary}"
    rounded: "{rounded.pill}"
    padding: "5px 13px"
    typography: "{typography.label}"
  nav-tab-active:
    backgroundColor: "{colors.candlewick-gold-dim}"
    textColor: "{colors.candlewick-gold-light}"
    rounded: "{rounded.pill}"
    padding: "5px 13px"
  chip:
    backgroundColor: "{colors.desk-secondary}"
    textColor: "{colors.parchment-secondary}"
    rounded: "{rounded.pill}"
    padding: "3px 12px"
  card-section:
    backgroundColor: "{colors.desk-card}"
    textColor: "{colors.parchment}"
    rounded: "{rounded.md}"
    padding: "13px 16px"
  fear-box:
    backgroundColor: "rgba(184,84,80,0.1)"
    textColor: "{colors.parchment}"
    rounded: "{rounded.md}"
    padding: "13px 15px"
  callout-gm-say:
    backgroundColor: "{colors.lamp-info-bg}"
    textColor: "{colors.parchment}"
    rounded: "{rounded.sm}"
    padding: "11px 15px"
---

# Design System: HollowStar GM Toolkit

## Overview

**Creative North Star: "The Candlelit GM Desk"**

This is a late-night prep table brought to the browser: warm lamp light on dark wood, parchment text, and dense reference sheets you can scan without breaking the flow of play. The mood is warm, scholarly, and tavern-quiet — utility dressed in candlelight, never spectacle. Gold marks authority and campaign identity; Hope and Fear carry mechanical meaning; everything else stays subordinate so the GM can read the room and the script at once.

Depth is tonal and bordered at rest. Interactive elements may take a soft lift on hover, but the surface never becomes a glowing dashboard. Neon and pastel palettes are rejected; saturation belongs to semantic callouts, not decoration.

**Key Characteristics:**
- Warm parchment-on-inkwood dark UI with Candlewick Gold as scarce authority
- Georgia for names and titles; system UI for scannable body and labels
- Semantic left-rail callouts (GM say, NPC, Hope, Fear, warn)
- Flat tonal layering; soft hover lift only on interactive controls
- Dense, collapsible session content inside a narrow reading column (~900px)

## Colors

A warm dark desk palette: inkwood grounds, parchment type, one gold authority accent, and semantic Hope/Fear/warn/info rails for content type.

### Primary
- **Candlewick Gold** (`{colors.candlewick-gold}` / `#c9a84c`): Brand, active nav underline, quick-ref frame, emphasis strongs. Pair with **Candlewick Gold Light** (`#e8c86a`) for titles and active labels, and **Candlewick Gold Dim** for selected tab fills.

### Secondary
- **Grove Hope** (`#4a9e6e`) / **Ember Fear** (`#b85450`): Mechanical and emotional poles of Daggerheart at the table. Used for Hope/Fear UI, success/fail outcomes, secrets, and danger — never as generic decoration.

### Tertiary
- **Lamp Info** (`#4a7fb5`): GM-say / narration rails.
- **Violet NPC** (`#8a60c8`): NPC dialogue and combat-primer accents.
- **Amber Warn** (`#c97d2a`): GM notes and caution.
- **Marsh Teal** (`#3a9898`): Lore/meta pills.

### Neutral
- **Inkwood** (`#1a1714`): Page background.
- **Desk Primary / Secondary / Card** (`#242018` / `#2d2920` / `#2a251e`): Nested surfaces.
- **Nav Black** (`#13110e`): Sticky site nav bar.
- **Parchment** (`#f0ead8`): Primary text.
- **Parchment Secondary / Muted** (`#a89f8a` / `#7a7060`): Supporting and quiet text.
- **Border Soft / Med** (`rgba(255,255,255,0.1)` / `0.18`): Hairline structure without heavy chrome.

### Named Rules
**The Scarce Gold Rule.** Candlewick Gold is authority, not fill. Prefer muted neutrals and semantic rails; gold appears on brand wordmark, Focus/active controls, and true emphasis — not page titles, eyebrows, or header rules.

**The Callout Color Rule.** Left-rail and box colors encode content type (GM say = info, Fear = ember, Hope = grove, warn = amber, NPC = violet). Never reuse Ember Fear red for decoration or generic alerts that are not Fear/danger/secret.

## Typography

**Display Font:** Georgia (with Times New Roman, serif)
**Body Font:** Segoe UI (with system-ui, sans-serif)
**Label/Mono Font:** Segoe UI labels — small, bold, tracked uppercase (no separate mono)

**Character:** Scholarly serif for names and page titles; quiet system sans for the dense operational body the GM actually scans mid-scene.

### Hierarchy
- **Display** (normal/400, `clamp(1.45rem, 3vw, 2.1rem)`, ~1.2): Page `h1` in the header — parchment primary (gold reserved for brand + Focus/active).
- **Title** (normal/400, ~15–18px): NPC names, fear-card titles, stat-block names — Georgia + gold or Fear text.
- **Body** (400, 14–15.5px, 1.65–1.75): Script paragraphs, callout copy, list items. Spoken/narrated lines (`gm-say` / `npc-say`) sit at the top of this range. Italics reserved for spoken/narrated lines. A Type slider (`--type-scale`, `localStorage` key `hs-type-scale`) multiplies the reading ramp at the table.
- **Label** (700, 10–11px, ~0.08–0.2em, uppercase): Eyebrows, callout tags, section pills, quick-ref titles.

### Named Rules
**The Spoken Italic Rule.** Player-facing or spoken lines (`.gm-say`, `.npc-say`, handouts) set in italic body; GM logistics stay roman so the eye knows what is sayable vs. private.

## Layout

Single reading column: `.page-body` max-width **900px**, horizontal padding **1.5rem**, bottom padding generous for scroll. Sticky horizontal site nav above a centered page header (eyebrow → h1 → subtitle → optional party chips / meta). In-page filter tabs sit above stacked collapsible sections. Dense vertical rhythm (~8–16px between blocks). At **600px** and below, multi-column grids (outcomes, paths, combat primer) collapse to one column; nav stays horizontally scrollable. Print hides the site nav and forces section bodies open.

## Elevation & Depth

Surfaces are flat at rest: depth comes from nested Inkwood → Desk → Card tones and soft white borders, not drop shadows. Interactive elements may take a soft lift (`translateY(-2px)` class of motion) and slightly stronger border on hover — never a neon glow or multi-layer shadow stack.

### Shadow Vocabulary
- **None normative.** Do not introduce ambient card shadows as the default language.

### Named Rules
**The Soft Lift Rule.** Elevation is a response to interaction (hover/active), not a resting property of containers. Resting cards stay tonal and bordered.

## Shapes

Gently softened rectangles: **6px / 10px / 14px** (`sm` / `md` / `lg`). Pills (**99px**) for tabs, chips, tags, and small meta. Callout blocks use a **3px left rail** with square-to-soft right corners (`0 sm sm 0`) — the system's signature silhouette. Circles appear only for step numbers and token/clock controls on the GM screen.

## Components

### Buttons / Tabs
Quiet and softly tactile. Filter `.nav-tab` pills: transparent + medium border at rest; gold border/text on hover; gold-dim fill + gold-light text when active. Transitions ~0.15s. Primary “buttons” in this system are mostly these tabs and small circular token controls — not large marketing CTAs.

### Chips
Party chips, stat chips, player tags, lore pills: pill radius, quiet fill or tinted semantic fill, 11–12px type. Selected/active state borrows gold or the relevant Hope/Fear tint.

### Cards / Containers
Section headers + bodies, NPC cards, ref boxes, hub cards, fear cards: desk-card/secondary fills, soft border, `md`–`lg` radius, internal padding ~13–15px. Hub cards may lift slightly on hover; fear cards use a stronger Ember Fear border. Quick-ref uses a gold border as the end-of-page authority frame.

### Inputs / Fields
Native form controls are rare today. When adding session focus dropdowns or similar, match desk-secondary fills, medium borders, pill or `md` radius, parchment text, and gold focus border — no neon rings.

### Navigation
Sticky Inkwood-black bar, gold brand wordmark (Georgia 13px), muted 12px links, gold-light + gold underline when active. Horizontal scroll on narrow viewports. Session lists must not grow as endless peer links — product requires a compact session focus selector as count scales.

### Signature: Callout Blocks
Left-rail typed blocks (`.gm-say`, `.npc-say`, `.thorn-say`, `.gm-note`, `.danger-note`) plus enclosed `.fear-box` / `.handout` / `.ref-box`. Each has an uppercase tracked `.tag`, consistent padding, and color locked to content type per **The Callout Color Rule**.

### Signature: Collapsible Section
Clickable header row (icon + label + optional pill + chevron) that opens a matching body. Open state squares the bottom of the header into the body. Default closed for scanability mid-session.

## Do's and Don'ts

### Do:
- **Do** keep Candlewick Gold scarce — brand, active focus, true emphasis.
- **Do** encode content type with callout colors (info / violet / hope / warn / fear).
- **Do** use Georgia for titles and names; system UI for operational body.
- **Do** prefer tonal nesting + borders; soft lift only on interactive hover.
- **Do** design for a dense 900px reading column and sticky nav under table pressure.

### Don't:
- **Don't** use neon, pastel, or purple-glow “AI dark mode” aesthetics.
- **Don't** paint Fear red onto decorative chrome or non-Fear UI.
- **Don't** add resting drop shadows or glowing focus halos as the default language.
- **Don't** list every session as a peer nav link as the library grows — use a compact focus selector.
- **Don't** introduce external webfonts/CDNs that break offline or GitHub Pages simplicity.
