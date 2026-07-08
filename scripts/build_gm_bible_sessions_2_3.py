#!/usr/bin/env python3
"""Build GM Bible PDF for HollowStar Sessions 2 & 3."""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "HollowStar" / "08_GM_Notes"
OUT_MD = OUT_DIR / "GM_Bible_Sessions_2_3.md"
OUT_HTML = OUT_DIR / "GM_Bible_Sessions_2_3.html"
OUT_PDF = OUT_DIR / "GM_Bible_Sessions_2_3.pdf"

CSS = """
@page {
  size: letter;
  margin: 0.75in 0.85in;
  @bottom-center {
    content: counter(page);
    font-size: 9pt;
    color: #666;
  }
}
body {
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 10.5pt;
  line-height: 1.45;
  color: #1a1a1a;
}
h1 { font-size: 22pt; margin: 0 0 0.25em; page-break-after: avoid; }
h2 {
  font-size: 15pt; margin: 1.4em 0 0.4em;
  border-bottom: 2px solid #8b6914;
  padding-bottom: 0.15em;
  page-break-after: avoid;
}
h3 { font-size: 12pt; margin: 1em 0 0.35em; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin: 0.8em 0 0.25em; color: #333; page-break-after: avoid; }
p { margin: 0.35em 0 0.6em; }
ul, ol { margin: 0.3em 0 0.7em 1.2em; }
li { margin: 0.15em 0; }
table { border-collapse: collapse; width: 100%; margin: 0.5em 0 1em; font-size: 9.5pt; }
th, td { border: 1px solid #ccc; padding: 4px 6px; vertical-align: top; }
th { background: #f3efe4; text-align: left; }
.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 2.5in;
}
.cover .subtitle { font-size: 13pt; color: #555; margin-top: 0.5em; }
.cover .meta { margin-top: 2em; font-size: 10pt; color: #666; }
.toc { page-break-after: always; }
.toc ul { list-style: none; padding-left: 0; }
.toc li { margin: 0.35em 0; }
.toc a { color: inherit; text-decoration: none; }
blockquote {
  margin: 0.5em 0 0.8em;
  padding: 0.5em 0.75em;
  border-left: 3px solid #8b6914;
  background: #faf8f2;
  font-style: italic;
}
.gm-secret {
  background: #fff8e8;
  border: 1px solid #d4b84a;
  padding: 0.5em 0.75em;
  margin: 0.5em 0 0.8em;
  border-radius: 3px;
}
.gm-secret strong { color: #7a5c00; }
.fear-card {
  border: 1px solid #c9a0a0;
  margin: 0.6em 0 1em;
  padding: 0.5em 0.65em;
  page-break-inside: avoid;
}
.fear-card h4 { margin-top: 0; color: #8b3030; }
.label { font-size: 8.5pt; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; color: #666; }
.npc-block { margin: 0.6em 0 1em; padding-bottom: 0.4em; border-bottom: 1px dotted #ddd; }
.npc-block h4 { margin-bottom: 0.1em; }
.page-break { page-break-before: always; }
.small { font-size: 9pt; color: #555; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.2em 0; }
"""


def md_to_html(text: str) -> str:
    """Minimal markdown-ish to HTML for session notes."""
    lines = text.splitlines()
    out: list[str] = []
    in_table = False
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    for line in lines:
        if line.startswith("# "):
            close_list()
            close_table()
            out.append(f"<h3>{esc(line[2:])}</h3>")
        elif line.startswith("## "):
            close_list()
            close_table()
            out.append(f"<h4>{esc(line[3:])}</h4>")
        elif line.startswith("### "):
            close_list()
            close_table()
            out.append(f"<h4>{esc(line[4:])}</h4>")
        elif line.startswith("> "):
            close_list()
            close_table()
            out.append(f"<blockquote>{esc(line[2:])}</blockquote>")
        elif line.startswith("|") and "|" in line[1:]:
            close_list()
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c.replace("-", "").strip()) <= set() or c.replace("-", "").strip() == "" for c in cells):
                continue
            if not in_table:
                out.append("<table><thead><tr>")
                for c in cells:
                    out.append(f"<th>{inline_md(c)}</th>")
                out.append("</tr></thead><tbody>")
                in_table = True
            else:
                out.append("<tr>")
                for c in cells:
                    out.append(f"<td>{inline_md(c)}</td>")
                out.append("</tr>")
        elif line.startswith("- "):
            close_table()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_md(line[2:])}</li>")
        elif re.match(r"^\d+\.\s", line):
            close_table()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_md(re.sub(r'^\\d+\\.\\s', '', line))}</li>")
        elif line.strip() == "---":
            close_list()
            close_table()
            out.append("<hr>")
        elif line.strip() == "":
            close_list()
            close_table()
        else:
            close_list()
            close_table()
            out.append(f"<p>{inline_md(line)}</p>")

    close_list()
    close_table()
    return "\n".join(out)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline_md(s: str) -> str:
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", s)
    return s


def extract_fear_cards(html_path: Path) -> str:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    parts: list[str] = []
    for card in soup.select(".fear-card"):
        title_el = card.select_one(".fear-card-title")
        scene_el = card.select_one(".fear-card-scene")
        cost_el = card.select_one(".fear-card-cost")
        if not title_el:
            continue
        title = title_el.get_text(strip=True)
        scene = scene_el.get_text(strip=True) if scene_el else ""
        cost = cost_el.get_text(strip=True) if cost_el else ""
        parts.append(f'<div class="fear-card"><h4>{esc(title)} <span class="small">({esc(scene)} · {esc(cost)})</span></h4>')

        for box in card.select(".trigger-box, .say-box, .gm-only-box"):
            tag = box.select_one(".tag")
            tag_text = tag.get_text(strip=True) if tag else "Note"
            paras = [p.get_text(" ", strip=True) for p in box.find_all("p")]
            body = " ".join(paras)
            cls = "gm-secret" if "gm-only" in box.get("class", []) else ""
            if cls:
                parts.append(f'<div class="{cls}"><strong>{esc(tag_text)}:</strong> {esc(body)}</div>')
            else:
                parts.append(f'<p><span class="label">{esc(tag_text)}</span> {esc(body)}</p>')

        roll = card.select_one(".roll-box")
        if roll:
            tag = roll.select_one(".tag")
            tag_text = tag.get_text(strip=True) if tag else "Roll"
            chips = " · ".join(c.get_text(strip=True) for c in roll.select(".roll-chip"))
            parts.append(f'<p><span class="label">{esc(tag_text)}</span> {esc(chips)}</p>')
            for ro in roll.select(".ro"):
                label = ro.select_one(".ro-label")
                p = ro.find("p")
                if label and p:
                    parts.append(
                        f'<p class="small"><strong>{esc(label.get_text(strip=True))}:</strong> {esc(p.get_text(strip=True))}</p>'
                    )

        parts.append("</div>")
    return "\n".join(parts)


def party_section() -> str:
    return """
<h2 id="party">Party & PC Threads</h2>
<p><strong>Party:</strong> Greer (Faun Druid, 60) · Lurielle (Faerie/Ribbet Wizard, 16) · Basil (Half-Katari/Emberkin Rogue)</p>
<p><strong>Session 1 completed.</strong> You enter Lumencrest on Gold Month 8, Day 1. Session 2 is wonder before pressure. Session 3 is the fracture.</p>

<h3>Greer — Faun Druid (Tara)</h3>
<ul>
<li>Sent by <strong>Thorn Oakwise</strong> from Ember Grove to watch House Vael and read the land/spirits in Lumencrest.</li>
<li>Path of Spirits druid; Green Covenant adjacent. Spirits in the city feel thin, crowded, overwhelmed — not absent.</li>
<li>Session 2 spotlight: land read (Instinct DIF 13); spirits "drinking through pipes"; Speakers' Corner fringe hears logging/Covenant frustration.</li>
<li>Session 3: protest anger is <em>legitimate</em>; bombers are NOT the organizers. Blast pain in the land; spirits recoil east pre-blast.</li>
</ul>

<h3>Lurielle — Wizard (16, Endless Eye)</h3>
<ul>
<li>Researching Hollowstars; classified Endless Eye docs were reclassified before she left — she noticed.</li>
<li>The Network hum is a frequency she can read. Knowledge/Instinct DIF 14 for patterned periodicity (not random brownout).</li>
<li>Session 3: hum stutters before blast; ceramic capacitor residue; archives appointment Day 4 (Hen Brask).</li>
<li>Clanks may pause near her (Hollowstar-adjacent resonance). Dangerous and useful long-term.</li>
</ul>

<h3>Basil Silverhand — Rogue</h3>
<ul>
<li>Youngest Silverhand; proving himself vs. firstborn Sage. Target: House Vael diplomatic pouch, Radiant Core, Gold Month 14 handoff.</li>
<li>Cover to party: Katya is his "ex." Truth: professional assassin tracking him from Session 1 training job.</li>
<li>Session 2: heat check (Perception DIF 13 on him); Guild sigil chalk rumor; Silver Thread tail possible.</li>
<li>Session 3: chaos = opportunity + witnesses; exit routes and watch movement; Guild chalk on Ash token is logistics not authorship.</li>
</ul>

<h3>Session 1 Branch Carryover</h3>
<table>
<thead><tr><th>Branch</th><th>Effect in Sessions 2–3</th></tr></thead>
<tbody>
<tr><td>Guild scout escaped Session 1</td><td>Sergeant Maret at Pauper's Gate has rough description; extra questions; Insight DIF 13 connects Greer to Ember Grove.</td></tr>
<tr><td>Basil pickpocket success</td><td>Letter/schedule safe; Vael schedule may match Guild sigil chalk (Investigation DIF 13).</td></tr>
<tr><td>Caelen knows Basil (partial pickpocket / fs-pp-exit)</td><td>Vael-clothed courier double-take at gate; Perception DIF 14 (Basil) to notice. Marten Halwick may mention Vael pin in common room.</td></tr>
<tr><td>Runner did NOT escape</td><td>Gate entry unremarkable unless other flags active.</td></tr>
</tbody>
</table>
"""


def world_context() -> str:
    return """
<h2 id="world">World Context — Clocks & Factions</h2>
<p><strong>In-world date:</strong> 700 AR, Gold Month 8. Lumencrest is cracking while the Fourth Fall approaches (Stage 3 — daytime visible).</p>

<h3>Active Countdown Clocks (Sessions 2–3)</h3>
<table>
<thead><tr><th>Clock</th><th>Stage</th><th>What players feel</th></tr></thead>
<tbody>
<tr><td>Fourth Fall</td><td>3/6</td><td>Star visible in daylight; fear spreading; factions mobilizing.</td></tr>
<tr><td>Lumencrest Heart</td><td>3/5</td><td>20% production loss; brownouts; Council paralyzed; labor unrest.</td></tr>
<tr><td>Green Covenant / Lumencrest</td><td>3/5</td><td>Thorn escalation; cold standoff; radical wing operating independently.</td></tr>
<tr><td>Northern Refugee Crisis</td><td>2/4</td><td>Frostwell refugees at Pauper's Gate; relief registry friction.</td></tr>
</tbody>
</table>

<h3>Lumencrest Council (Gridlocked)</h3>
<ul>
<li><strong>Illuminists</strong> (Chair Mira Ashton): aggressive research; unauthorized Vault experiments running.</li>
<li><strong>Conservators</strong> (Sevan Vael public face): stability, caution — Vael family playing long game.</li>
<li><strong>Expansionists</strong> (Theron Ashwick): military solution; seize Endless Eye; use crises to vote.</li>
</ul>

<h3>Factions in Play These Sessions</h3>
<table>
<thead><tr><th>Faction</th><th>State</th><th>Sessions 2–3 relevance</th></tr></thead>
<tbody>
<tr><td>Green Covenant (mainstream)</td><td>Cold standoff with Lumencrest; Maren managing Thorns</td><td>Protest grievances legitimate. Radical wing (~40) bombing hubs — Maren doesn't know.</td></tr>
<tr><td>Green Covenant (radical / Thorns)</td><td>Wren's cell in Lumencrest 6 months</td><td>Hub blast Session 3. Wren calculating; Ash troubled. Thornwall in Heartgrove funds intel.</td></tr>
<tr><td>House Vael</td><td>Patient power play</td><td>Sevan moderate voice; Lyra runs darker ops (Shard Division) without father's full knowledge.</td></tr>
<tr><td>Unseen Guild</td><td>Standard ops + Shard Division</td><td>Mira Voss; Basil tail possible; Brinne's "wrong boots" asker may be capacity intel.</td></tr>
<tr><td>Ironwright Collective</td><td>Labor anger</td><td>Protest banners; rationing focus; Genna Cradle linked to Brinne.</td></tr>
<tr><td>City Watch</td><td>Overwhelmed, competent at street level</td><td>Containment not hostility at protest; investigation stalls after blast.</td></tr>
</tbody>
</table>

<h2 id="secrets">GM Secrets — The Truth Behind Sessions 2–3</h2>

<div class="gm-secret">
<strong>Who bombed the hub:</strong> Green Covenant radical wing, operational leader <strong>Wren</strong> (elf, 134). Targeted secondary Eastwick feed hub — residential hurt before commercial priority. Architecture-aware ceramic capacitor device. ~40 members in secret cells. Grievances are real; civilian casualties accepted in their framework.
</div>

<div class="gm-secret">
<strong>Wren</strong> — calm, methodical, has not personally witnessed consequences until now. On distant roofline north during blast. Not at site. Already planning next move if objective met (secondary hub down ✓).
</div>

<div class="gm-secret">
<strong>Ash</strong> (human, 29) — Wren's second. Rooftop observer two blocks south. Saw pre-blast figure at hub door. Left early — maintenance worker still inside. Troubled, potentially reachable with honest approach. Cornered line: <em>"I didn't know they'd still be inside."</em> Day 12: meets supplier at Pauper's Gate Taproom.
</div>

<div class="gm-secret">
<strong>Protest organizers (Tessa Morr, Docken Hale)</strong> — NOT connected to bombers. Wren timed blast mid-afternoon to avoid protest linkage. City will conflate them anyway.
</div>

<div class="gm-secret">
<strong>Theron Ashwick</strong> — uses deliberate blast to push military authorization. Has curated Heart timeline from Lyra Vael. Speaks to Sevan twice Day 3 Council. Not wrong that it was terrorism — wrong about who and why publicly.
</div>

<div class="gm-secret">
<strong>House Vael / Lyra</strong> — Shard Division kidnapping refugees for Hollostar shard experiments. Lyra funding; Mira Voss operating. Separate from hub bomb but same villain ecosystem. Theron and Sevan are different faces of House strategy.
</div>

<div class="gm-secret">
<strong>Watch investigation</strong> — 23 interviews Day 2, zero productive leads in official file. Deprioritized Day 5 without player push. Vault Guard logged event; did not deploy (jurisdiction).
</div>

<h3>What NOT to reveal yet</h3>
<ul>
<li>Do not name Wren or Green Covenant to players unless earned through investigation.</li>
<li>Ash gives one true line if cornered — not a full confession.</li>
<li>End Session 3 on Council announcement — Day 3 session is Session 4.</li>
</ul>
"""


def lumencrest_primer() -> str:
    return """
<h2 id="lumencrest">Lumencrest Primer</h2>
<table>
<thead><tr><th>District</th><th>Session use</th></tr></thead>
<tbody>
<tr><td>Pauper's Gate</td><td>Default entry; Old Pen's Taproom; Frostwell refugees; North Expanse cable terminus.</td></tr>
<tr><td>Lamplight Ward</td><td>Accord Arms (Merchant Square); protest border; Eastwick eastern edge.</td></tr>
<tr><td>Eastwick</td><td>Brinne's Cooperative; Lida's Bake; Wire Road hub; goes dark Session 3.</td></tr>
<tr><td>Shadowside</td><td>Dark Lantern (Solt); lamps thin; border chalk.</td></tr>
<tr><td>Copper Gate</td><td>Traveller's Mark (Henris Callow); welcome zone.</td></tr>
<tr><td>Entertainment Quarter</td><td>Copperstring — loses power mid-set Session 3.</td></tr>
<tr><td>Halfling Quarter</td><td>Ora Finch / Mending Room — 25 min from hub.</td></tr>
<tr><td>Radiant Core</td><td>Basil scouts; heavily watched; Vael presence.</td></tr>
<tr><td>Vault District</td><td>Glow on horizon; speaker may name it Session 2 dawn.</td></tr>
</tbody>
</table>

<h3>Key Locations Session 2–3</h3>
<ul>
<li><strong>Wire Road & Ninth Lamp</strong> — alley junction; secondary hub; protest 3 blocks west.</li>
<li><strong>Lamplight / Shadowside border</strong> — chalk: <em>WE PAID FOR THIS LIGHT</em>.</li>
<li><strong>North Expanse Station → Central Hub</strong> — cable car orientation; 2 copper/person.</li>
<li><strong>Accord Chamber</strong> — Emergency Council Day 3 AM, gallery opens 9.</li>
</ul>

<h3>Costs & DC Quick Reference</h3>
<table>
<thead><tr><th>Item</th><th>Value</th></tr></thead>
<tbody>
<tr><td>Gate vague answers</td><td>Presence DIF 12 · false identity Deception DIF 14</td></tr>
<tr><td>Cable car</td><td>2 copper/person</td></tr>
<tr><td>Traveller's Mark</td><td>1 gold/night (Henris Callow)</td></tr>
<tr><td>Accord Arms</td><td>2–5 gold/night (Marten Halwick)</td></tr>
<tr><td>Wren House (Eastwick)</td><td>6 silver/night</td></tr>
<tr><td>Hub blast time</td><td>~2:47pm Day 2</td></tr>
<tr><td>Forensics window</td><td>15 min before watch seals site</td></tr>
</tbody>
</table>
"""


def npc_reference() -> str:
    return """
<h2 id="npcs">NPC Reference — Sessions 2 & 3</h2>

<h3>Session 2 NPCs</h3>
<div class="npc-block"><h4>Old Pen — Pauper's Gate Taproom</h4>
<p>Short sentences; twenty-year neutrality. <em>"Drink first. Questions cost extra."</em> Logs gate traffic; 3 silver buys gossip about "wrong boots" asking about northern feed lines.</p></div>

<div class="npc-block"><h4>Sergeant Maret — City Watch, Pauper's Gate</h4>
<p>By-the-book, tired. Has scout description if Session 1 branch active. Insight DIF 13 connects Greer to Ember Grove.</p></div>

<div class="npc-block"><h4>Marten Halwick — Accord Arms</h4>
<p>Excellent innkeeper; common room intelligence hub. 2–5 gold/night. May mention Vael pin if Caelen branch active (Presence DIF 12).</p></div>

<div class="npc-block"><h4>Henris Callow — Traveller's Mark</h4>
<p>Reassuring, efficient; free ward map. Assesses complicated arrivals; won't report to watch.</p></div>

<div class="npc-block"><h4>Pella Marr — Cable car attendant</h4>
<p>Bored professional. <em>"Two coppers. Hold the rail."</em></p></div>

<div class="npc-block"><h4>Mama Voss — Night Market cart</h4>
<p>Presence DIF 11 for "weather report." Points to absent substance vendors or half-elf asking about feed hubs (Ash rumor).</p></div>

<div class="npc-block"><h4>Solt — Dark Lantern, Shadowside</h4>
<p>Flat, unhurried. Friend Derrin missing three days. Presence DIF 12 for sympathy → pours tea, says nothing more.</p></div>

<div class="npc-block"><h4>Bram Kettlemarch — Speakers' Corner</h4>
<p>Evening voice; legitimate grievance, not radical.</p></div>

<h3>Session 3 NPCs</h3>
<div class="npc-block"><h4>Brinne Halloway — Eastwick Cooperative chair, human 46</h4>
<p>Quietly fierce; lists not speeches. Candle/oil stockpile; expected grid failure not violence. Presence DIF 12 for trust. Pop-up triage if party helped morning.</p>
<div class="gm-secret"><strong>GM:</strong> Files Charter complaint Day 3 about repair priority. Not connected to bombers. Linked to Genna Cradle (Ironwright).</div></div>

<div class="npc-block"><h4>Lida Birch — Lida's Bake, human 55</h4>
<p>4am warmth; gossip hub. Watch asked organizers to keep protest peaceful. Free bread for helpers after blast.</p></div>

<div class="npc-block"><h4>Tessa Morr & Docken Hale — Protest organizers</h4>
<p>~200 people; rationing rollback demand. <em>"We paid. We marched. We did not ask for this."</em> Genuine horror at blast (Insight DIF 12).</p></div>

<div class="npc-block"><h4>Captain Isen Varr — City watch, human 45</h4>
<p>Command voice, overwhelmed. <em>"You want to help? Get names."</em> Sends runner to Accord Chamber. Emergency Council announcement evening.</p></div>

<div class="npc-block"><h4>Sergeant Pel Carr — Watch sweep, human 40s</h4>
<p>Tired competence. Presence DIF 13 credible account; helpful witness detail marks party cooperative.</p></div>

<div class="npc-block"><h4>Ora Finch — Mending Room, halfling 67</h4>
<p><em>"Someone meant this junction. This wasn't rage. This was a diagram."</em> Insight DIF 14 reads deliberate sabotage. Medicine path for serious injuries.</p></div>

<div class="npc-block"><h4>Ash — Wren's second, human ~29</h4>
<p>Rooftop witness; flees if spotted. Chase: Agility/Instinct DIF 14; cornered Presence DIF 15 → <em>"They weren't running like guilty. They were running like done."</em></p>
<div class="gm-secret"><strong>GM:</strong> Not the bomber. Guild chalk token if dropped is logistics. Day 12 supplier meet at Old Pen's.</div></div>

<div class="npc-block"><h4>Injured civilians</h4>
<p><strong>Edda/Toma Venn</strong> — serious, conduit shrapnel. <strong>Peten Strauss</strong> — leg laceration. <strong>Mira Jol</strong> — bruised, walking.</p></div>

<div class="npc-block"><h4>Theron Ashwick — Expansionist Councilor</h4>
<p>Public statement within 4 hours. Frames terrorism → military expansion. Ready for crisis — was prepared for something like this.</p></div>

<div class="npc-block"><h4>Wren — GM only, elf 134</h4>
<p>Operational leader; distant roofline north during blast. Calculating next move. Do not introduce on-screen unless players earned investigation trail.</p></div>
"""


def build_html() -> str:
    s2 = (ROOT / "HollowStar/08_GM_Notes/Sessions/Session_02_Lumencrest_Arrival.md").read_text(encoding="utf-8")
    s3 = (ROOT / "HollowStar/08_GM_Notes/Sessions/Session_03_The_Hub_Explosion.md").read_text(encoding="utf-8")
    fear2 = extract_fear_cards(ROOT / "gm_sessions_site/fear_options_session2.html")
    fear3 = extract_fear_cards(ROOT / "gm_sessions_site/fear_options_session3.html")

    # Strip front matter nav from session md
    for marker in ["**Back to", "**GM Site:**", "## Sync Checklist", "## GM Site Build Notes", "## Player Decisions"]:
        s2 = s2.split(marker)[0]
        s3 = s3.split(marker)[0]

    body = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HollowStar GM Bible — Sessions 2 & 3</title>
<style>{CSS}</style>
</head>
<body>

<div class="cover">
  <h1>HollowStar GM Bible</h1>
  <p class="subtitle">Sessions 2 & 3 — Lumencrest Arrival & The Hub Explosion</p>
  <p class="meta">700 AR · Gold Month 8 · Daggerheart<br>
  Party: Greer · Lurielle · Basil<br>
  GM Only — Contains secrets</p>
</div>

<div class="toc">
<h2>Contents</h2>
<ul>
<li>1. Party & PC Threads</li>
<li>2. World Context, Clocks & Secrets</li>
<li>3. Lumencrest Primer</li>
<li>4. Session 2 — Lumencrest Arrival</li>
<li>5. Session 2 — Fear Spend Appendix</li>
<li>6. Session 3 — The Hub Explosion</li>
<li>7. Session 3 — Fear Spend Appendix</li>
<li>8. NPC Reference</li>
</ul>
</div>

{party_section()}
{world_context()}
{lumencrest_primer()}

<div class="page-break"></div>
<h2 id="session2">Session 2 — Lumencrest Arrival</h2>
<p><strong>Date:</strong> Gold Month 8, Day 1 · <strong>Runtime:</strong> 3–4 hours · <strong>Goal:</strong> Wonder before pressure. End on dawn Day 2 protest chalk — do NOT run explosion.</p>
<blockquote>Plateau ending: Fresh chalk <em>WE PAID FOR THIS LIGHT</em>. Someone says: "They said we'd have light if we paid." Stop.</blockquote>
{md_to_html(s2)}

<div class="page-break"></div>
<h2 id="fear2">Session 2 — Fear Spend Appendix</h2>
<p>Full expansions from fear_options_session2.html. One Fear per gate scene unless table is comfortable.</p>
{fear2}

<div class="page-break"></div>
<h2 id="session3">Session 3 — The Hub Explosion</h2>
<p><strong>Date:</strong> Gold Month 8, Day 2 · <strong>Blast:</strong> ~2:47pm · <strong>Runtime:</strong> 3–4 hours</p>
<p><strong>Goal:</strong> Protest pressure → targeted hub blast → chaos forks → Council clock. Situation encounter, not default combat. Wren and Ash NOT at site.</p>
<blockquote>Plateau ending: Emergency Council tomorrow morning. Forensic hook: architecture-aware sabotage. Stop on Council clock + dark Eastwick.</blockquote>
{md_to_html(s3)}

<div class="page-break"></div>
<h2 id="fear3">Session 3 — Fear Spend Appendix</h2>
{fear3}

<div class="page-break"></div>
{npc_reference()}

<p class="small" style="margin-top:2em;">Generated from HollowStar vault + gm_sessions_site. Interactive reference: gm_sessions_site/session2.html, session3.html, fear_options_session2.html, fear_options_session3.html, lumencrest.html</p>

</body>
</html>
"""
    return body


def build_markdown_summary() -> str:
    return """# HollowStar GM Bible — Sessions 2 & 3

**GM Only** — Full prep document with secrets, factions, NPCs, act structure, and Fear spend appendix.

| | |
|---|---|
| **Sessions** | 2 — Lumencrest Arrival · 3 — The Hub Explosion |
| **In-world** | Gold Month 8, Days 1–2, 700 AR |
| **Party** | Greer · Lurielle · Basil |
| **Prerequisite** | Session 1 (Ember Grove) completed |

## Files

| File | Purpose |
|------|---------|
| `GM_Bible_Sessions_2_3.pdf` | Print/tablet reading copy |
| `GM_Bible_Sessions_2_3.html` | Same content; open in browser |
| `gm_sessions_site/session2.html` | Interactive runnable session |
| `gm_sessions_site/session3.html` | Interactive runnable session |
| `gm_sessions_site/fear_options_session2.html` | Linked Fear expansions |
| `gm_sessions_site/fear_options_session3.html` | Linked Fear expansions |

## Quick Session Flow

**Session 2:** Gate → lodging → cable car → PC spotlights → night texture → dawn protest (stop).

**Session 3:** Morning errands + protest → 2:47pm blast → response forks (injured / Ash / forensics / watch) → dark Eastwick evening → Emergency Council announced.

## Regenerate PDF

```bash
python3 scripts/build_gm_bible_sessions_2_3.py
```

**Back to [[08_GM_Notes/GM_Notes_Index|GM Notes Index]]**
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html()
    OUT_HTML.write_text(html, encoding="utf-8")
    OUT_MD.write_text(build_markdown_summary(), encoding="utf-8")
    print(f"Wrote {OUT_HTML}")
    HTML(string=html, base_url=str(OUT_DIR)).write_pdf(str(OUT_PDF))
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
