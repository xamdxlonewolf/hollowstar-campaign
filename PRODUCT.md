# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static multi-page HTML/CSS (`gm_sessions_site/`), shared stylesheet, offline-first with no CDN dependencies. Served locally as files and via GitHub Pages.

## Users

Primary user is the GM (campaign runner), alone — both at the table during play and during prep. Players do not use the site.

## Product Purpose

A runnable GM toolkit for tabletop sessions: session scripts, Fear spend options, location bibles, calendar, notes, and GM screen reference. The campaign grows over time — potentially hundreds of sessions — so the GM picks a session to focus on and works from that focus. Success means staying inside that focused session view while still reaching other toolkit material without closing it or opening competing tabs/windows.

## Positioning

Session-centric table reference for a living campaign world (currently HollowStar / Daggerheart), built from vault session notes into offline HTML the GM can open anywhere. Neighboring note apps and PDFs do not keep the GM inside one running-session surface with Fear, locations, and rules reference immediately at hand.

## Operating Context

- Source prep lives in the HollowStar Obsidian vault (`HollowStar/08_GM_Notes/Sessions/` and related canon folders).
- Build flow: finalize session notes → convert to `gm_sessions_site/` HTML → sync new canon facts back into the vault.
- Used mid-session on whatever device has the folder or GitHub Pages open; must work without network once loaded (offline) and also publish cleanly to GitHub Pages.
- Current campaign: HollowStar — Lumencrest arc; party Greer, Lurielle, Basil; system Daggerheart.
- Sessions keep being added after each play; the site must remain usable as the session count grows into the dozens and potentially hundreds.

## Capabilities and Constraints

- Confirmed surfaces: hub, per-session scripts, per-session Fear option pages, location pages, calendar, notes, GM screen, interactive maps where present.
- Session focus selector: a dropdown (or equivalent compact control) to choose which session is in focus. Do not rely on a nav that lists every session as a peer link — that will not scale.
- Offline-first; no external runtime dependencies.
- Deploy targets: local folder and GitHub Pages.
- GM-only; keep secrets and GM notes out of player-facing read-aloud blocks.
- Product name / world focus today: HollowStar GM Toolkit. Future: other campaigns may be added to the same site — multi-campaign structure is planned but not yet designed.
- Undecided: exact in-session UX for reaching other toolkit material without leaving the active session page (overlay, drawer, embedded panels, etc.) — product requirement is confirmed; mechanism is open. Exact session-list data source and search/filter inside the dropdown as count grows are open, but the control pattern is confirmed.

## Brand Commitments

- Product identity: HollowStar GM Toolkit / HollowStar GM.
- Campaign world: HollowStar (Daggerheart). Other campaign names are future additions, not current brand replacements.

## Evidence on Hand

- Live site pages under `gm_sessions_site/` (sessions 1–3, locations, calendar, notes, GM screen, Fear pages).
- Canon and prep source under `HollowStar/`.
- Cursor skills encode build patterns: `.cursor/skills/building-gm-session-page/`, `.cursor/skills/adding-gm-location-page/`.
- Do not fabricate player testimonials, play counts, or third-party endorsements.

## Product Principles

1. Stay in the session — secondary toolkit info comes to the GM; the GM should not abandon the running session view.
2. Scale by focus, not by nav clutter — pick the session in focus via a compact selector; the UI must stay usable as hundreds of sessions accumulate.
3. Offline and publishable — works as a local folder and on GitHub Pages with the same static files.
4. Prep → table → canon — site content is derived from vault notes and pushes durable facts back into the world.
5. GM-private by default — secrets, Fear levers, and GM notes stay GM-only.
6. Campaign-shaped, expandable — HollowStar first; structure should not paint the site into a single-campaign dead end.
