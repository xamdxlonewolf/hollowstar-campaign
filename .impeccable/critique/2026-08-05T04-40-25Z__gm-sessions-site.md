---
target: the whole site
total_score: 24
max_score: 40
na_heuristics: 
p0_count: 1
p1_count: 2
timestamp: 2026-08-05T04-40-25Z
slug: gm-sessions-site
---
#### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | Peek tools lack pressed state; no act/scroll cue; GM Screen drops the instrument strip |
| 2 | Match System / Real World | 4 | Fluent table language (Fear, DIF, clocks, GM Say) throughout |
| 3 | User Control and Freedom | 3 | Escape closes peeks; no undo for Hope/Fear; Focus is hard navigation |
| 4 | Consistency and Standards | 2 | Dual Hope/Fear UIs; Fear `.say-box` vs `.gm-say`; emoji nav vs semantic rails |
| 5 | Error Prevention | 2 | Clock delete / token swings unguarded; Focus switch can strand mid-act |
| 6 | Recognition Rather Than Recall | 3 | Callouts excel; Fear jump-nav is a 12-pill recall wall |
| 7 | Flexibility and Efficiency | 2 | Only `N` accelerator; Fear/Combat/Focus/acts are mouse-only |
| 8 | Aesthetic and Minimalist Design | 2 | First viewport chrome stack; default-open sections; gold scarcity broken |
| 9 | Error Recovery | 2 | Sparse confirms; silent localStorage failure; muted error paths |
| 10 | Help and Documentation | 2 | Tip boxes help; stay-in-session chrome has no first-run guidance |
| **Total** | | **24/40** | **Acceptable** |

#### Design Specificity Verdict

**LLM assessment**: Authored, not category-interchangeable. The left-rail semantic callouts (`.gm-say` / `.npc-say` / `.thorn-say` / `.gm-note` / `.danger-note` / `.fear-box`), Hope·Fear instrument language, and parchment-on-inkwood tokens are unmistakably a Daggerheart GM desk. Specificity is diluted by emoji-stuffed site nav, a hub of generic admin-style `.hub-card` tiles, and gold applied as wallpaper (eyebrow + h1 + header border + brand + pills) instead of scarce authority. The product soul lives in the script callouts and Fear cards; the chrome still reads like a themed multi-page toolkit shell.

**Deterministic scan**: Detector exited 2 with **192 findings** (41 warning / 151 advisory) across the site. Breakdown: `design-system-font-size` 148, `em-dash-overuse` 13, `side-tab` 13, `flat-type-hierarchy` 8, `aphoristic-cadence` 5, `design-system-radius` 3, `monotonous-spacing` 2. Heaviest files: `shared.css` (52), `gmscreen.html` (24), Fear pages and `calendar.html`. Detector caught density/type-ramp drift the LLM review underweighted (tiny 9–12px ops type vs DESIGN.md ramp; flat hierarchy on locations/Fear/notes). Suspected false positives: `em-dash-overuse` and `aphoristic-cadence` hit GM narrative prose; `side-tab` flags the intentional 3px callout left-rails (signature silhouette, not UI side-tabs).

**Visual overlays**: No reliable user-visible overlay. Browser mutation preflight failed (`BROWSER_MUTATION_UNAVAILABLE` — tabs created then vanished before navigate/lock). Live-server inject path skipped. Fallback: CLI detector + source review only.

#### Overall Impression

The Candlelit GM Desk identity is real where it matters — mid-script callouts and Fear expansions feel like table tools, not a generic dark admin theme. The Operate promise breaks at the edges: the session first viewport is a dashboard before Act 1, and GM Screen still forces a hard leave exactly when Hope/Fear/rules pressure peaks. Biggest opportunity: make the running session page the only surface that matters for a 4-hour run, with everything else as peeks/docks that never kill place-in-script.

#### What's Working

1. **Semantic callout system** — GM Say / NPC / Hope-voice / warn / Fear are scannable mid-sentence without leaving the reading column; this is the design win.
2. **Stay-in-session chrome intent** — Focus dropdown (peer session links stripped), Fear/Location/Calendar/Combat peeks, non-modal notes dock with `N` show the product principle landing in code.
3. **Fear expansion cards** — trigger → say → rolls → now/soon/later is a table-native pattern that builds confidence under pressure.

#### Priority Issues

**[P0] GM Screen (and full Hub) force a hard leave from the running session**
- **Why it matters**: Product success = stay inside focused session while reaching toolkit; rules/Hope·Fear reference is exactly when leaving hurts most. `session-chrome.js` never peeks `gmscreen.html`.
- **Fix**: Peek or dock GM Screen (or surface critical rules inside Combat peek); stop treating GM Screen as a peer page exit mid-run.
- **Suggested command**: `$impeccable shape` (mechanism) then `$impeccable harden`

**[P1] Session first viewport chrome overload + default-open sections**
- **Why it matters**: Mid-session GM needs the next line, not sticky nav + Focus + 5 tools + instrument strip + hero + filter tabs before Act 1. Most `.section-header.open` burns attentional budget while players wait. Cognitive load checklist: 7/8 failures (high).
- **Fix**: Collapse prep by default; pin/collapse instrument strip; shrink hero metadata; make filter tabs the progressive-disclosure spine.
- **Suggested command**: `$impeccable distill` / `$impeccable layout`

**[P1] Candlewick Gold scarcity broken**
- **Why it matters**: Brand, eyebrow, h1, header rule, active nav, Focus, and pills all shout gold — authority becomes noise; Hope/Fear semantics lose relative weight. Detector also flags type-ramp drift that flattens hierarchy further.
- **Fix**: Reserve gold for brand + one status/control (Focus or active session); demote titles/meta to parchment hierarchy; tighten display/body steps.
- **Suggested command**: `$impeccable quieter` / `$impeccable typeset`

**[P2] Dual Hope/Fear + clock UIs**
- **Why it matters**: Session `.hs-instrument-strip` vs GM Screen `.token-tracker` — same state, two grammars → mis-clicks and distrust mid-combat.
- **Fix**: One token/clock component; GM Screen consumes or peeks the same strip.
- **Suggested command**: `$impeccable harden`

**[P2] Collapsible sections are non-keyboard `div onclick`; Fear jump-nav is 12 equal pills**
- **Why it matters**: Keyboard/AT users cannot collapse the default-open wall; Mid-Session GM burns seconds hunting Fear under stress.
- **Fix**: Real `<button>` headers with `aria-expanded`; group Fear nav by act (≤4 visible groups).
- **Suggested command**: `$impeccable audit` / `$impeccable adapt`

#### Persona Red Flags

**Alex (Power User)**: Primary run-session path has one accelerator (`N`). No Fear/Combat/Focus/act keys; must mouse the 5-tool strip and scroll walls of open sections. Session Focus is a full navigation — no recent-acts jump. Will open multiple browser tabs, defeating stay-in-session.

**Sam (Accessibility)**: Section toggles are non-focusable `div`s with `onclick`; emoji + color carry meaning alongside labels; peek iframes are a second document for AT. Keyboard-only cannot collapse the default-open wall. Detector’s tiny font sizes (9–12px) compound low-vision risk.

**Mid-Session GM (primary)**: Needs next GM Say + Fear option + Hope/Fear count without looking away from players. Instrument strip and peeks help — until a rules question sends them to GM Screen and kills place-in-script. Default-open Branch Tracker + Overview above Act 1 forces scroll past prep while players wait. Fear’s 12-pill nav inside a peek is unusable under time pressure.

#### Minor Observations

- Hub subtitle sells “organized and linked” like a library, not “pick Focus and run.”
- Fear `return-bar` fights peek UX (“return to Session”) and should become “Close peek” when embedded.
- Party chips + session-meta duplicate a compact Focus/context line.
- Clock pip targets are 16×16 — harsh for tablet at the table.
- Emoji in brand/nav/section icons undercut the tavern-quiet scholarly brief.
- Notes full-page and notes dock share storage but different IA — easy to think they are separate systems.
- Location Primary/Secondary selects in peek header add a second decision layer before content.
- Detector: location pages show very flat type (~1.3:1); sessions 2/3 show monotonous ~12px spacing rhythm.

#### Questions to Consider

- If the GM never left the session page for an entire 4-hour run, what chrome would earn the right to stay sticky?
- Should GM Screen exist as a page at all, or only as a combat/rules peek summoned from the script?
- What if every session opened on the current Act only — prep collapsed, Focus already set, Hope/Fear at last-saved — and Hub was prep-only?
- Is Candlewick Gold marking “this is HollowStar,” or marking “look here now”? It can’t do both on every header.
- When Fear is spent, should the UI debit Fear and jump to the expansion in one gesture — or is the GM still expected to hunt a pill?
