---
target: gm_sessions_site
total_score: 28
max_score: 40
na_heuristics: 
p0_count: 1
p1_count: 2
timestamp: 2026-08-05T15-09-28Z
slug: gm-sessions-site
---
Method: dual-agent (A: 169e5fde-547b-446a-af9b-68fad5ef08cf · B: 95438a2a-f1c8-4c47-9e3a-db6de232ecd6)

#### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 3 | Focus, Hope/Fear, clocks, resume clear; peek/tool active state quieter |
| 2 | Match System / Real World | 4 | GM / Daggerheart language fluent (Fear, Hope, GM Say, clocks) |
| 3 | User Control and Freedom | 3 | Peek close, Focus switch, section toggles; weak undo on token/clock deletes |
| 4 | Consistency and Standards | 3 | Shared tokens strong; dual Notes paths, Fear-red hub card, gold on loc titles |
| 5 | Error Prevention | 2 | Storage warn exists; destructive clock/foe deletes lightly guarded |
| 6 | Recognition Rather Than Recall | 3 | Labeled peeks; mobile truncates peer nav so toolkit paths must be remembered |
| 7 | Flexibility and Efficiency | 3 | Peeks, Focus, filters, combat glyphs; limited keyboard beyond sections |
| 8 | Aesthetic and Minimalist Design | 2 | Operate chrome + peer nav + filters compete with the script |
| 9 | Error Recovery | 2 | Plain storage warn; little constructive recovery elsewhere |
| 10 | Help and Documentation | 3 | Inline tips and primers; no global task help |
| **Total** | | **28/40** | **Good — solid Operate kit; chrome density is the drag** |

#### Design Specificity Verdict

**LLM assessment**: Authored for HollowStar GM Toolkit, not category-interchangeable SaaS dark mode. Inkwood/parchment/Candlewick Gold, Georgia titles, left-rail GM-say / NPC / Fear / Hope callouts, Hope·Fear·clocks, Fear boxes, and peek-panel session shell read as a Candlelit GM Desk for Daggerheart mid-session Operate. Hub card grids and emoji nav are the most transferable bits; the operate grammar (Focus, peeks, semantic rails, scarce gold) is campaign-specific and largely lands against DESIGN.md — not neon/purple-glow AI dark mode, not resting drop shadows.

**Deterministic scan**: CLI detector exit 2 — **106 findings** (41 warnings, 65 advisory) across 7 rules: `design-system-font-size` (63), `em-dash-overuse` (13), `side-tab` (13), `flat-type-hierarchy` (8), `aphoristic-cadence` (5), `design-system-radius` (2), `monotonous-spacing` (2). Hotspots: `shared.css` callout left rails flagged as `side-tab`; session/fear pages with high em-dash counts; location/calendar pages with off-ramp font sizes; `gmscreen.html` / `shared.css` radius outliers (3–4px vs token ramp).

**False positives / brief alignment**: `side-tab` on `.gm-say` / Fear / Hope rails is the DESIGN.md signature silhouette, not decorative AI chrome — treat as intentional. Em-dash and aphoristic hits largely reflect RPG beat cadence, not UI slop. Font-size advisory volume is useful as drift signal (e.g. 10px / 16px / 20px off the documented ramp) but should not drive a blind global rewrite.

**Visual overlays**: No reliable user-visible overlay. Browser MCP tab lifecycle failed for Assessment B (create → evaporate → navigate refused); mutation preflight and `detect.js` injection never ran. Assessment A used a companion `serve` on port 51201 + Playwright screenshots for visual review. Live server on port 8400 was started and stopped cleanly.

#### Overall Impression

This already *feels* like your product: warm desk, parchment type, semantic rails, Hope/Fear as mechanical color. The gap versus PRODUCT.md / DESIGN.md is not “wrong aesthetic” — it’s Operate density and a few rule leaks. Biggest opportunity: put the **script above the instruments** and make Focus + peeks the only secondary path, so the site scales and stays in-session as designed.

#### What's Working

1. **Semantic callout system** — GM say / NPC / warn / Fear rails make sayable vs private scannable under table pressure; this is the design’s signature and it lands.
2. **Stay-in-session peeks + Focus dropdown** — embody PRODUCT principles 1–2 better than tab-hopping; the grammar is right even where chrome is heavy.
3. **Palette / type / tonal nesting** — Candlelit GM Desk without neon glow or resting shadows; Georgia + system UI hierarchy matches the brief.

#### Priority Issues

1. **[P0] Operate chrome buries the script**
   - **What**: Sticky nav + Focus + 5 tools + Hope/Fear/clocks (+ filters) consume the first viewport; worst on mobile.
   - **Why it matters**: Breaks “Stay in the session” — GM hunts for the next line while players wait.
   - **Fix**: Collapse instruments to one compact row; hide peer nav behind Focus/Tools on session shell; default sections closed except current act; script above the fold.
   - **Suggested command**: `$impeccable distill` (session operate chrome)

2. **[P1] Duplicate leave paths (peer nav + peeks)**
   - **What**: Hub / Locations / Calendar / Notes / GM Screen remain as peers while peeks exist for the same destinations.
   - **Why it matters**: Extraneous choice; invites abandoning the mounted session view; fights scale-by-focus.
   - **Fix**: On session shell, demote or remove peer toolkit links; peeks (+ resume) are the only secondary path.
   - **Suggested command**: `$impeccable quieter` (session-chrome / site-nav)

3. **[P1] Wall of options at filters & tools**
   - **What**: 5–7 equal-weight pills at tools, session filters, gmscreen, and location filters.
   - **Why it matters**: Exceeds ≤4 working-memory rule under table stress.
   - **Fix**: Group tools (Run: Fear·Combat · Lore: Loc·Cal · Notes); collapse filters into Acts + overflow.
   - **Suggested command**: `$impeccable clarify` (nav-tabs + session toolbar)

4. **[P2] Scarce Gold / Fear color leaks**
   - **What**: Location card titles in gold-light/hope; hub GM Screen card titled in Fear red.
   - **Why it matters**: Weakens Scarce Gold + Callout Color rules; Fear reads as chrome, not danger.
   - **Fix**: Parchment titles; semantic color only on rails/borders/status.
   - **Suggested command**: `$impeccable colorize` (locations + index)

5. **[P2] Hub session peer cards vs Focus scaling**
   - **What**: Sessions listed as equal hub cards while Focus says “Choose session…”.
   - **Why it matters**: Fine at 3; fights “scale by focus” as sessions grow into dozens/hundreds.
   - **Fix**: Hub = Focus CTA + current arc context; archive/list sessions inside Focus.
   - **Suggested command**: `$impeccable layout` (index.html)

#### Persona Red Flags

**Alex (Power User / power GM)**: Wants Fear spend + script without chrome scroll; five peek pills + five nav peers is one click too many; GM Screen instrument strip duplicates Live Token Tracker mental model.

**Sam (Accessibility-Dependent)**: Emoji as primary icon language; muted parchment-secondary on inkwood is borderline; mobile nav truncates Locations/Calendar/Notes; clock pips lean color-only for filled state.

**Morgan (Mid-Session GM — project)**: Opens session1 on phone/tablet → sees Hope/Fear/clocks/tools before Act 1 line; hub “Current Session” status can disagree with empty Focus until chosen; party/time/location meta hidden on narrow session shell when a glanceable where/when is most needed.

#### Minor Observations

- Session shell widens `.page-body` to ~1120px vs DESIGN ~900px.
- Many Act sections default `open` — disclosure exists but isn’t progressive.
- Hub campaign banner packs five meta fields (chunking edge).
- `prefers-reduced-motion` and gold `focus-visible` outlines are present — keep.
- Detector also flagged radius outliers (3–4px) and monotonous ~12px spacing on session pages — polish-level vs P0 chrome.

#### Questions to Consider

1. If the script is the product mid-session, why does the instrument strip get a better seat than Act 1’s first GM-say?
2. What would “Focus” mean if the only primary chrome were Focus + Hope/Fear + one Tools menu?
3. Should clocks collapse until Fear is spent, instead of four cards always on?
4. Is the hub a prep lobby or an Operate launcher — and should it stop looking like a dashboard of equal cards?
5. When Fear hits mid-council, should the visual winner be the Fear peek or the in-script Fear box?
