#!/usr/bin/env python3
"""Build the prose-first HollowStar opening adventure PDF.

The output intentionally reads like an adventure module instead of a converted
checklist. Sessions 2 and 3 remain the focus, with Session 1 included as the
prologue that explains why the party is walking into Lumencrest.
"""

from __future__ import annotations

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
  margin: 0.72in 0.82in;
  @bottom-center {
    content: "HollowStar: Lights Over Lumencrest  ·  " counter(page);
    font-size: 8.5pt;
    color: #786b54;
  }
}
body {
  color: #201b16;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 10.8pt;
  line-height: 1.58;
}
h1, h2, h3, h4 {
  color: #2b2118;
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.15;
  page-break-after: avoid;
}
h1 { font-size: 30pt; margin: 0 0 0.25em; }
h2 {
  font-size: 18pt;
  margin: 1.4em 0 0.45em;
  padding-bottom: 0.18em;
  border-bottom: 2px solid #8b6914;
}
h3 {
  font-size: 14pt;
  margin: 1.15em 0 0.35em;
  color: #5b3f14;
}
h4 {
  font-size: 11.5pt;
  margin: 0.95em 0 0.25em;
  color: #6a281f;
}
p { margin: 0 0 0.72em; }
.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 2.2in;
}
.cover .kicker {
  color: #8b6914;
  font-size: 10pt;
  font-weight: bold;
  letter-spacing: 0.18em;
  margin-bottom: 0.5em;
  text-transform: uppercase;
}
.cover .subtitle {
  color: #4a4138;
  font-size: 14pt;
  margin-top: 0.6em;
}
.cover .meta {
  color: #786b54;
  font-size: 10pt;
  margin-top: 2em;
}
.toc {
  page-break-after: always;
}
.toc-entry {
  border-bottom: 1px dotted #c7bda6;
  margin: 0.35em 0;
  padding-bottom: 0.15em;
}
.part-title {
  page-break-before: always;
  margin-top: 0;
}
.readaloud {
  background: #f7f1df;
  border-left: 4px solid #8b6914;
  margin: 0.85em 0 1em;
  padding: 0.7em 0.85em;
  font-style: italic;
}
.gm-secret {
  background: #fff7e2;
  border: 1px solid #d0aa36;
  border-radius: 4px;
  margin: 0.85em 0 1em;
  padding: 0.72em 0.85em;
}
.gm-secret .label,
.sidebar .label,
.reference .label {
  color: #7a5600;
  display: block;
  font-size: 8.5pt;
  font-weight: bold;
  letter-spacing: 0.09em;
  margin-bottom: 0.2em;
  text-transform: uppercase;
}
.sidebar {
  background: #f4f1ea;
  border: 1px solid #cfc6b5;
  border-radius: 4px;
  margin: 0.85em 0 1em;
  padding: 0.72em 0.85em;
}
.scene {
  border-top: 1px solid #d9d0bd;
  margin-top: 1em;
  padding-top: 0.85em;
}
.npc {
  border-bottom: 1px dotted #d1c6b4;
  margin: 0.7em 0 0.9em;
  padding-bottom: 0.65em;
}
.npc h4 { margin-top: 0; }
table {
  border-collapse: collapse;
  font-size: 9.2pt;
  margin: 0.65em 0 1em;
  width: 100%;
}
th, td {
  border: 1px solid #cfc6b5;
  padding: 4px 6px;
  vertical-align: top;
}
th {
  background: #eee5d1;
  color: #3c2e1d;
  text-align: left;
}
.reference {
  page-break-inside: avoid;
}
.small { color: #6d6258; font-size: 9.2pt; }
.chapter-note {
  color: #6d6258;
  font-size: 10pt;
  font-style: italic;
}
"""


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def p(text: str) -> str:
    return f"<p>{text}</p>"


def readaloud(text: str) -> str:
    return f'<div class="readaloud">{p(text)}</div>'


def secret(label: str, text: str) -> str:
    return f'<div class="gm-secret"><span class="label">{label}</span>{p(text)}</div>'


def sidebar(label: str, text: str) -> str:
    return f'<div class="sidebar"><span class="label">{label}</span>{p(text)}</div>'


def scene(title: str, text: str) -> str:
    return f'<div class="scene"><h3>{title}</h3>{text}</div>'


def extract_fear_titles(html_path: Path) -> list[tuple[str, str, str]]:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    cards: list[tuple[str, str, str]] = []
    for card in soup.select(".fear-card"):
        title = card.select_one(".fear-card-title")
        scene_name = card.select_one(".fear-card-scene")
        say = card.select_one(".say-box p")
        if title:
            cards.append(
                (
                    title.get_text(" ", strip=True),
                    scene_name.get_text(" ", strip=True) if scene_name else "",
                    say.get_text(" ", strip=True) if say else "",
                )
            )
    return cards


def cover_and_toc() -> str:
    return """
<div class="cover">
  <div class="kicker">HollowStar Campaign</div>
  <h1>Lights Over Lumencrest</h1>
  <p class="subtitle">An Opening Adventure Module Through Session 3<br>with full preparation for Sessions 2 and 3</p>
  <p class="meta">GM Only. Contains secrets, faction truth, NPC motives, and future hooks.<br>Gold Month 8, 700 AR · Daggerheart · Greer, Lurielle, Basil</p>
</div>

<div class="toc">
  <h2>Contents</h2>
  <div class="toc-entry">Introduction: How to Read This Book</div>
  <div class="toc-entry">Chapter One: The Shape of the Opening</div>
  <div class="toc-entry">Chapter Two: The City of Lumencrest</div>
  <div class="toc-entry">Chapter Three: The Powers Moving Under the Lights</div>
  <div class="toc-entry">Chapter Four: The Player Characters in This Arc</div>
  <div class="toc-entry">Chapter Five: Session One, The Ember Grove Prologue</div>
  <div class="toc-entry">Chapter Six: Session Two, Arrival Day in Lumencrest</div>
  <div class="toc-entry">Chapter Seven: Session Three, The Hub Explosion</div>
  <div class="toc-entry">Chapter Eight: People of the Opening Arc</div>
  <div class="toc-entry">Appendix: Table Reference and Fear Windows</div>
</div>
"""


def introduction() -> str:
    return f"""
<h2>Introduction: How to Read This Book</h2>
{p("This document is meant to be read like an adventure module rather than used as a checklist. The purpose is not to lock the table into a single path. The purpose is to give the Game Master a deep enough grasp of what is happening in Lumencrest that, when the players move sideways, the world can answer with confidence.")}
{p("The first version of this material was a bible in the narrow sense: a dense reference that collected scenes, secrets, and mechanics. This version is a campaign book. It explains why each scene matters, what the city is doing before the players touch it, what NPCs want when they speak, and which truths should remain below the surface until the party earns them. It still contains the practical material needed to run the sessions, but the practical material is embedded in context so that it is easier to absorb before the table.")}
{p("The book begins with Session 1 because that session gives emotional shape to everything that follows. Ember Grove is the wound that sends the party west. It introduces House Vael, Green Covenant pressure, Basil's heist, Lurielle's research, and Greer's obligation to listen to what the land is saying. Sessions 2 and 3 are the main focus. They are where Lumencrest becomes real and then immediately reveals that its order is brittle.")}
{sidebar("Current scope", "This volume intentionally stops at Session 3 because that is the prepared material right now. It includes Session 1 as the prologue and fully supports Sessions 2 and 3. As future sessions are planned, add them as new chapters after Session 3 rather than rewriting this book around table outcomes.")}
{sidebar("Using this over time", "Treat this as the first volume of a growing adventure module. It should not be rewritten after every player choice. If the party changes an outcome, mark it in your table notes and keep the book as the prepared baseline. Later volumes can describe what the world would have done, what it did at your table, and what changed because of the party.")}
"""


def opening_shape() -> str:
    return f"""
<h2>Chapter One: The Shape of the Opening</h2>
{p("The opening movement of HollowStar is about a beautiful system revealing its cost. Ember Grove begins small: a council room, a timber offer, a road, a first glimpse of the city. Lumencrest begins vast: walls, lamps, cable cars, the hum under every street, and a civilization that appears to have solved darkness itself. The hub explosion then reframes that wonder. The lights are not simply magic or progress. They are dependence. They are politics. They are something old being consumed by a city that no longer understands the source of its own power.")}
{p("The players should feel the city before they understand it. Arrival day should be allowed to breathe. Do not rush the first gate, the first cable car, or the first walk through a lit street. The central trick of Session 2 is that nothing truly catastrophic happens on-screen. Instead, the city teaches the party how it works. It shows them who is lit and who is not, who gets recorded at the gate, who rides above the rooftops without wonder, who sleeps against the wall with everything they own in a bundle, and who has learned to ignore the hum.")}
{p("Session 3 breaks that first impression. The explosion is not random chaos. It is precise, political, and personal. It does not destroy the city; it wounds a neighborhood. That distinction matters. The bomber did not try to collapse the main spine or kill as many people as possible. The target is a secondary distribution hub that serves Eastwick and part of the Entertainment Quarter. The immediate result is darkness, injury, panic, and a political narrative forming before the smoke clears.")}
{secret("The central truth of Sessions 2-3", "The protest is real and legitimate. The bombing is real and deliberate. They are not the same thing, but Lumencrest's political machine will try to make them the same thing because that is useful to people who want force authorized.")}
{p("By the end of Session 3, the players should not have solved the bombing. They should have enough to know that the official story will be incomplete. They should know that the injured were not acceptable background damage. They should know that someone watched from a roof and ran. They should know that the Council will speak in the morning while Eastwick eats by candlelight.")}
"""


def lumencrest_chapter() -> str:
    return f"""
<h2>Chapter Two: The City of Lumencrest</h2>
{p("Lumencrest is a city of approximately eighty-seven thousand residents and another fifteen thousand transient workers, visitors, refugees, and people waiting for circumstances to decide whether they belong. It was founded around the Heart, the fallen Hollostar beneath the Vault District, and the city has spent twelve centuries learning how to turn that gift into infrastructure. Its lamps, factories, cable cars, public buildings, and civic mythology all depend on the Lumen Network. The Heart is not merely a power source. It is the reason the city believes it is the center of the world.")}
{p("The first thing outsiders notice is light. The second is the hum. The light is steady in a way oil lamps never are. The hum is harder to describe because residents stop hearing it after a week, but newcomers hear it in walls, railings, cable housings, and the stone underfoot. It is not loud. It is constant. It gives the impression that the city is holding a note. When the Network falters, the absence of that note becomes frightening.")}
{readaloud("The street is lit. Not by torches, not by lanterns. The light comes from glass globes on iron posts every twenty feet, steady and white-gold, casting no flicker. Above you, a cable runs between towers, and an enclosed car glides along it carrying passengers who look out the windows as if hanging above the street is ordinary. The road is wide enough for six carts and full of people. Coal smoke from the west, bread from the south, and underneath all of it a faint metallic warmth that seems to come from the walls themselves. It is the middle of the night. It does not look like the middle of the night.")}
{p("The city is divided by priority as much as by geography. The Radiant Core and Academic Quarter are fully lit and treated as essential. Lamplight Ward and the Halfling Quarter are mostly reliable, though Lamplight's eastern edge has begun to fail in ways residents notice before officials admit anything. The Manufactories receive power according to productivity, which means factory floors are prioritized over worker housing. Shadowside has never had the Network. It lives by candle, coal, oil, and the stubborn competence of people the rest of the city misnames as disorderly because they are not convenient to govern.")}
{p("Pauper's Gate is the default arrival point from the Kingroad. It is practical, busy, and honest in the way of places that have processed travelers for generations. City watch records names, origins, lodging intentions, and business in the city. They are managing flow rather than conducting deep investigation, but the registry is real. A wanted person or a person matching a recent description can be slowed, questioned, or marked. Immediately inside the gate stands Old Pen's Taproom, the first building many travelers pass, and nearby the North Expanse cable terminus lifts passengers toward the city's center. Frostwell refugees gather along the interior wall in small numbers that add up if anyone keeps count.")}
{p("Copper Gate, by contrast, is the face Lumencrest prefers to show visitors. It opens into Lamplight Ward's welcome zone, where currency exchanges, inns, and licensed guides make arrival feel managed and profitable. Tomm at the Welcome Gate is the kind of person who tells travelers which exchange booth overcharges them even though that honesty costs him referrals. If the party reaches Copper Gate after entering through Pauper's Gate, the difference should be obvious. One gate shows the city functioning. The other shows the city selling functionality.")}
{p("The cable car is the fastest way to make Lumencrest comprehensible. Four lines run from the Central Hub in the Radiant Core. The North Line reaches the North Expanse Station and the edge of Manufactories and Shadowside. The East Line reaches the Academic Quarter and river access. The South Line reaches Merchant Square and Copper Gate. The West Line reaches the Halfling Quarter and Mill Quarter. A ride costs two copper marks, any distance on a line. From above, the party sees the dome of the Accord Chamber, the Vault District wall and the unnatural brightness above it, the Manufactories smoke, the Halfling Quarter's lower rooftops, and the way Shadowside becomes dark by degrees.")}
{p("Lamplight Ward is where Sessions 2 and 3 live. It is the city's middle-class commercial heart, full of shops, inns, guild halls, entertainment venues, and the people who want to believe that civic systems work if enough competent people keep them oiled. Merchant Square gives the party a respectable base if they choose the Accord Arms. Copper Gate offers anonymity through the Traveller's Mark. Eastwick, on the Ward's eastern edge, is more residential, more vulnerable, and better organized from below than from above. Brinne Halloway's Cooperative, Lida's Bake, and the Wire Road hub are all part of Eastwick's neighborhood ecosystem.")}
{p("Shadowside matters even when the party does not enter it. It sits at the border of visibility. The Dark Lantern, Solt's bar, is a place where people speak carefully because they have learned which kinds of truth are dangerous. The Night Market's southern stretch is tolerated, and Mama Voss's cart serves food good enough to cross district lines for. The people here know the difference between city law and community safety. When the protest forms at the Lamplight-Shadowside border, it forms where the city's promise of light has visibly stopped.")}
{p("The Halfling Quarter is not central to the first two Lumencrest sessions, but it is a source of safety and practical mercy. Ora Finch's Mending Room becomes important after the blast because the Quarter understands care as infrastructure. Lumencrest depends on Quarter bread and Quarter beer more than it likes to say. Anyone who earns Halfling Quarter trust gains something more useful than official permission: a place to be helped without needing to become a case file.")}
{p("The Radiant Core is the city performing authority. Basil's heist points there. The Accord Chamber dome is visible from the cable car and becomes central after Session 3, when the emergency Council session is announced. The Vault District is stranger. It is not a neighborhood. It is a wall, guards, restricted access, and the knowledge that the Heart below makes everything else possible. Brownouts are forcing ordinary residents to think about the Vault more directly than they have in years. That attention is dangerous to everyone who benefits from opacity.")}
{sidebar("Lumencrest at the table", "Whenever players ask what a place feels like, answer with light, sound, class, and priority. Is the street lit or dark? Is the hum steady, strained, or absent? Do city systems treat the people here as important? Those three questions make Lumencrest coherent even when the party wanders.")}
"""


def factions_chapter() -> str:
    return f"""
<h2>Chapter Three: The Powers Moving Under the Lights</h2>
{p("Lumencrest's visible government is the Council of Lumens, thirty-two seats divided into factions that still know how to administer streets and permits but have forgotten how to make a decision about the future. The Heart has been declining for decades. Official language calls the failures maintenance, optimization, and load management. The public hears brownout. Workers hear rationing. Researchers hear a clock. Expansionists hear opportunity.")}
{p("The Illuminists believe the solution exists inside research, engineering, and the Heart itself. They hold the current chair through Councilor Mira Ashton and run enough programs to look energetic even as the most important answers fail to arrive. They want data, access, and time. They are not innocent; some unauthorized Vault experiments are happening under their umbrella. But in the opening sessions, they are the faction most likely to ask for investigation rather than retaliation.")}
{p("The Conservators are the city's institutional spine. They maintain what exists because for twelve centuries what existed worked. Sevan Vael appears near them as a moderate voice of calm and measured response. Publicly, he is the sort of politician people praise for not panicking. Privately, House Vael has spent decades preparing to catch Lumencrest when it falls. Sevan does not know every detail of his daughter Lyra's arrangements with the Unseen Guild, but he knows enough to know that ignorance is politically useful.")}
{p("The Expansionists are led by Theron Ashwick. They argue that Lumencrest cannot wait for a miracle when another Hollowstar exists under the Endless Eye. Their program begins as preparedness and becomes military authorization. Theron is charming, patient, and ready with language that turns fear into permission. The hub explosion gives him exactly the rhetorical instrument he needs: a deliberate attack on vital infrastructure, performed in a city already afraid its lights are going out.")}
{secret("Theron's move", "Theron is not inventing the danger. The blast is deliberate, architecture-aware sabotage. His lie is not that Lumencrest was attacked; his lie is that the attack proves his desired solution. By evening of Session 3, his public statement should feel prepared because he has been waiting for an event he can use.")}
{p("The Green Covenant is both a legitimate political grievance and the source of the immediate act of violence, which is what makes the opening morally alive. Lumencrest has exploited forest resources, dismissed Covenant objections, and prepared to solve power problems by taking from somewhere else. The mainstream Covenant has tried protest, negotiation, and resistance. A radical wing of roughly forty members has concluded that none of that works. Their plan is to target Lumen Network distribution hubs, cause power failures, and make Lumencrest too unstable to mount operations into Verdant Crescent timber territory.")}
{p("Wren leads the cell inside Lumencrest. She is methodical, not theatrical, and has convinced herself that short-term casualties are acceptable if they prevent a larger ecological and political harm. Ash, her second, is younger and less certain. He is not innocent, but he is reachable. He watches the hub because he is part of the operation's eyes, not because he is meant to fight. When the blast catches people still inside the danger window, Ash's doubts become sharper than Wren's calculations.")}
{p("The Unseen Guild runs alongside this conflict without causing the blast. That distinction matters. Basil's story touches House Vael and Guild logistics. Lyra Vael funds the Shard Division, which kidnaps vulnerable people and exposes them to Hollowstar fragments to study and weaponize transformation. Mira Voss runs Lumencrest operations for the Guild. The Shard Division is not Session 3's culprit, but its presence explains why the city contains multiple kinds of hidden predation at once.")}
{p("The Ironwright Collective gives voice to worker anger. It is not an abstract faction for later; its banners appear in the protest because power rationing has a class shape. Workers see the factory floor prioritized over worker housing, the Core untouched, and official explanations written by people who do not stand in dark kitchens after shift. The Eastwick Cooperative is smaller but more immediately useful. Brinne Halloway's network stockpiles candles, oil, food, and routes of care because it has stopped trusting institutions to respond quickly enough.")}
{p("City watch is not the villain of these sessions. At street level, the watch is tired, overworked, and often competent. They hold a protest line without immediate violence. They try to take witness statements after the blast. They also serve a system that will ask them for forms instead of truth. Captain Isen Varr and Sergeant Pel Carr should be played as people doing what they can inside a response apparatus that is already being outpaced by politics.")}
{secret("The shape of blame", "Wren's cell intends distance from the protest. The blast is timed away from the protest's peak culpability window, but still close enough to exploit the city's tension. The Council and broadsheets will chain protest and bombing together because simple narratives move faster than accurate ones.")}
"""


def pc_chapter() -> str:
    return f"""
<h2>Chapter Four: The Player Characters in This Arc</h2>
{p("The opening sessions work best when each character experiences Lumencrest through a different pressure. Greer feels what the city has done to the spirit layer. Lurielle hears the Network as a cousin to forbidden knowledge from the Endless Eye. Basil sees a city of sightlines, access routes, professional watchers, and the House Vael target that brought him west.")}
{p("Greer arrives as a druid of the Path of Spirits, carrying decades of listening. For years the spiritual presences of the Central Heartlands have seemed quieter, not dead but watchful. Ember Grove gave that feeling a local shape; Lumencrest reveals scale. The city spirit layer is thin and crowded, compressed by Network density and the Heart below. It is not evil. It is overwhelmed. In Session 2, Greer's land reading should feel like stepping into a room where everyone is speaking over something sleeping beneath the floor. In Session 3, the blast makes the spiritual cost immediate: the web recoils, screams, and then falls silent in dark blocks.")}
{p("Lurielle arrives as someone too young to be treated as an authority and too observant to be safely dismissed. She grew up around the Endless Eye and noticed that deep lake research documents were reclassified before she left. Lumencrest's hum gives her a new language for old questions. The Network is not identical to the Endless Eye, but the family resemblance is there. When the hum spikes, stutters, or cuts out, she is not simply hearing city infrastructure; she is hearing resonance between Hollowstar-derived systems. The explosion's forensic clues should give her the feeling that theory has become a street injury.")}
{p("Basil arrives for a job. The House Vael diplomatic pouch, the Radiant Core handoff on Gold Month 14, and the need to prove himself to the Silverhand family all give him a practical reason to study the city. He is not here to solve Lumencrest's politics. That is useful. He will notice watchers because he thinks like one. He will understand that chaos creates both opportunity and evidence. If Session 1 left Caelen aware of him, use that awareness as pressure rather than punishment. A double-take at the gate, a Vael pin in a common room, or a professional tail for three blocks reminds Basil that his heist is moving while the city's crisis unfolds.")}
{p("The group should not be told what to care about. Session 2 gives them enough sensory and social material to choose. Session 3 gives them enough emergency to reveal what they choose under pressure. If they help the injured, Eastwick remembers. If they pursue Ash, the investigation thread sharpens. If they study the hub, the technical truth appears early. If they get caught in the watch sweep, the city records them. Each path is valid because each path teaches them a different layer of Lumencrest.")}
"""


def session_one_chapter() -> str:
    return f"""
<h2>Chapter Five: Session One, The Ember Grove Prologue</h2>
{p("Session 1 is the prologue of the adventure module. It has already been played at the table, but it belongs in this book because it establishes why the party is walking into Lumencrest with unfinished business. Ember Grove is smaller than Lumencrest, but it contains the opening arc in seed form: House Vael wants resources, the Green Covenant is divided between patience and anger, Basil sees a heist opportunity, Lurielle sees a research path, and Greer is asked to listen westward.")}
{p("The day begins in the grove with Gold Month light, watchful crows, a warm Heart Stone, and the sense that the spirit web has become quieter than it should be. This is not an emergency yet; it is an omen in the old sense, a signal that becomes meaningful only after later events teach the party how to read it. Greer is at home enough for the contrast with Lumencrest to matter. Lurielle has spent two weeks trying to describe threshold phenomena in academic language and failing. Basil has been watching the road and the Vael arrival because his own business hides behind civic business.")}
{p("The council meeting gives the module its inciting bargain. House Vael, through Caelen, offers to purchase controlled logging rights: fifty acres per year on the eastern managed woodland, eighteen gold per acre, reforestation language, operations after Frostmonth, final offer. Fen Crane can see the bridge money and the stalled Accord subsidy. Elder Marta wants a reason to say no but has to govern a town's finances, not just its conscience. Thorn Oakwise refuses to let the timber question remain merely timber. The eastern edge touches the grove's spirit boundary. What is taken from there goes somewhere else.")}
{p("Caelen is not a cackling villain. He is polished, prepared, and young enough to believe preparation is the same as superiority. He has Thorn's name ready. He has survey language ready. He may not know the full purpose of what House Vael is moving, including refugee ships, Guild logistics, and the deeper supply chain, but he knows enough to manage the room. Basil's pickpocket window matters because it can turn polite pressure into evidence. The letter and schedule card point toward Verdean ships, refugee transit Phase 2, an Unseen Guild eye sigil, and the Radiant Core handoff on Gold Month 14.")}
{p("The road encounter after the meeting gives the party their first taste of how the hidden world moves. If they took the road, hired thugs and a possible runner can report party composition into later Lumencrest awareness. If they took the grove path, the shard-infected bear shows that Hollowstar material is not safely contained in academic papers. Either way, the session ends on a ridge. Lumencrest glows below. Some outer-district lights flicker. No one explains it yet.")}
{readaloud("The road crests, and the city is there. Not a campfire glow. Not dawn. Lumencrest burns white-gold against the night, towers and walls shaped in the light of thousands of lamps. For one breath it is beautiful enough to quiet every argument behind you. Then, along the outer edge, a section of lights flickers and steadies again. Someone takes the first step down the hill.")}
{sidebar("What Session 1 leaves in motion", "The Vael offer remains deferred for one week. Basil's Radiant Core heist clock continues toward Gold Month 14. Greer carries Thorn's instruction to watch the people around the Vael name and where what they take goes next. Lurielle has a reason to seek Lumencrest's archives. The Green Covenant and Thorns activity are no longer distant rumors. The party enters the city with personal reasons to look beneath the lights.")}
"""


def session_two_chapter() -> str:
    return f"""
<h2>Chapter Six: Session Two, Arrival Day in Lumencrest</h2>
{p("Session 2 should feel like arrival, not mission briefing. The party has seen the glow from the ridge. Now they cross into the machine. The purpose of the session is to let the city land as wonder before it becomes pressure. The explosion belongs to tomorrow. Today belongs to first impressions, lodging, orientation, personal spotlights, and the quiet social facts that will make tomorrow's violence intelligible.")}
{scene("The descent and Pauper's Gate", p("Begin by letting the plateau image become a road. The light remains ahead of them while the smell of coal, river water, human density, and metallic warmth arrives before the gate. Pauper's Gate is efficient rather than dramatic. The watch asks for names, origin, lodging, and business. A vague but plausible answer requires Presence DIF 12 only if the party is actively trying to avoid specificity; a false identity or dangerous lie calls for Deception DIF 14. The important thing is not to turn the gate into a wall. It is a lens. Lumencrest sees people by recording them.") + p("If the Session 1 scout escaped, Sergeant Maret has a rough description: three travelers from the grove road, one with a staff. He asks extra questions, but this is not an arrest. If Caelen knows Basil, a Vael-clothed courier at the registry desk looks twice and looks away. Let Basil notice on Perception DIF 14. These beats should feel like the city taking fingerprints, not closing a trap."))}
{readaloud("The northern wall is old stone rebuilt three times, iron braced and lamp-bright. The queue moves faster than it should. Above the gate a cable runs south into the city, and a wooden car glides along it with passengers looking out as if this is ordinary. Near the interior wall, refugees sit with their lives bundled in cloth. The watch officer does not look cruel. He looks busy. 'Names. Where you're from. Where you're staying tonight. What's your business.'")}
{scene("First hours and finding a bed", p("After the gate, give the party food, a map, and a choice of base. The Accord Arms in Lamplight Ward is expensive but rich in passive intelligence; its common room carries Council talk, merchant anxiety, and rumors about brownouts. Marten Halwick is professional enough to be useful without being intimate. The Traveller's Mark near Copper Gate is cheaper and more anonymous. Henris Callow is a good first city contact because he explains what is useful and withholds what is not his to share. Wren House in Eastwick is the community option if the party drifts toward ordinary residents rather than polished commerce.") + p("Common room information should come as overheard texture, not exposition. Brownouts have happened three times this month. Council factions are named casually, as if everyone already knows the argument. The Manufactories are angry. Yesterday's protest at the Lamplight-Shadowside border was tense but controlled. Someone says the watch will be back tomorrow. No one says explosion because no ordinary person knows that yet."))}
{scene("The cable car", p("The cable car is the city's geography lesson. Put the party above the rooftops and let them see priority. The Radiant Core never dims. The Vault wall glows with a different quality of light. The Academic Quarter keeps late windows. The Halfling Quarter sits lower and warmer. The Manufactories smoke. Shadowside becomes less lit by degrees. A ride costs two copper marks per person, and locals' boredom is part of the scene. The party should feel that something wondrous has become commute.") + p("If you spend Fear here, do it quietly. A shudder mid-line, a block of Lamplight Ward lamps dying and returning, or the hum sharpening around Lurielle should not become a disaster. It should reveal that locals have learned to accept minor failures that newcomers still recognize as alarming."))}
{readaloud("Inside the car it smells like warm metal and other people. The attendant closes the door, speaks two words into a tube, and the room begins to move. Below you, the city resolves itself: dome, wall, smoke, market roofs, bright avenues, darkening edges. Nobody else is impressed. A dwarf reads. A Clank stares out the window. A woman sleeps through the view. This is how they commute.")}
{scene("Greer's spotlight", p("Ask Greer what she does when she first has a quiet moment in the city. The correct answer is not a plot hook but a feeling. The spirit layer is thin and crowded. The Network's hum presses through stone and metal. The land is not dead, but it is forced to breathe through pipes. On Instinct DIF 13, Greer understands that the spirits are present but starved and that something below the Vault wall direction is too large to be named by ordinary city language. Failure should not mean nothing; it should mean headache, ache, and inability to separate voices from noise."))}
{scene("Lurielle's spotlight", p("Lurielle should receive the city as data she cannot yet prove. Near a junction box, street lamp, or cable mechanism, ask what she wishes she had brought from the Endless Eye. Knowledge or Instinct DIF 14 reveals a secondary periodicity in the hum. It is not a random brownout pattern. It resembles things she saw in reclassified Endless Eye catalogues before those documents vanished. The archives become the next logical step, but Hen Brask can only give her an appointment on Day 4. This delay matters. It keeps the first answer out of reach while tomorrow's evidence arrives in the street."))}
{scene("Basil's spotlight", p("Basil's first night is a heat check. In Lumencrest, everyone important knows how to watch without appearing to watch. If Session 1 created Vael awareness, use a courier, a common room glance, or a tail who matches Basil's pace for three blocks. If Basil looks into the Gold Month 14 handoff, let him learn that the Radiant Core is visible but not casually enterable without reason, referral, or cover. The city is not stopping him yet. It is teaching him that perfection will require patience."))}
{scene("Night texture and Shadowside", p("If the party goes south or follows curiosity toward the border, let them feel the lamps thin. The Lamplight-Shadowside border carries yesterday's chalk: WE PAID FOR THIS LIGHT. Workers have scrubbed part of it away, but someone on the Shadowside side has answered with WHO PAID FOR YOURS. At the Dark Lantern, Solt speaks little and watches enough to know who listens to things others cannot hear. If engaged honestly, he mentions Derrin, missing three days after an errand to the Maze. Do not make this a quest unless the players insist. Let it be a missing tooth in the city's smile."))} 
{scene("The plateau ending: dawn Day 2", p("End Session 2 at dawn. The city wakes before the sun because the Manufactories wake before the sun. Return the party to the border, or bring the border to them through sound, chalk, and crowd movement. The protest is larger than yesterday, still controlled, and more organized. Organizers carry clipboards. Watch stands present but not aggressive. The final image should be people gathering around the demand that light paid for should not be withdrawn without answer. Stop before the day becomes violent."))}
{readaloud("Gold Month, Day Two. Dawn in Lumencrest is not quiet. The city wakes in layers: factory rhythm, cart wheels, bakery smoke, electric amber fading into morning. At the border, the chalk is fresh again. WE PAID FOR THIS LIGHT, written darker over scrubbed stone. More people gather than yesterday. Someone in the crowd says, loud enough to hear, 'They said we'd have light if we paid.' The sun finishes coming up. The protest does not stop.")}
"""


def session_three_chapter() -> str:
    return f"""
<h2>Chapter Seven: Session Three, The Hub Explosion</h2>
{p("Session 3 is the first fracture. It should not begin with the explosion. It begins with a city that seems to have survived the night and is now choosing how loudly to demand an answer. The blast matters because it interrupts a legitimate civic grievance and allows powerful people to reframe that grievance as threat. Run the day in three movements: the morning pressure, the mid-afternoon wound, and the evening narrative war.")}
{scene("Morning in Eastwick", p("Open wherever the party ended Session 2. If they stayed in Eastwick, Lida's Bake gives them coffee, bread, and neighbors already speaking in careful tones. Lida mentions that watch asked organizers to keep things peaceful. At the Cooperative hall, Brinne Halloway quietly organizes candles and oil. Presence DIF 12 earns enough trust for her to admit that Eastwick has been preparing for brownouts longer than the Council admits. If the party treats her like an information dispenser, she closes the basement door. If they help load candles without performance, she becomes a strong ally after the blast.") + p("Morning errands let each character touch their thread without resolving it. Lurielle can get the archives appointment date: Day 4. Basil can scout the Courtyard approach and learn that Radiant Core access is not solved by confidence. Greer can stand near Speakers' Corner and hear rationing stories that are angry, specific, and true."))}
{scene("The protest builds", p("By late morning, roughly two hundred people gather near the Lamplight-Shadowside border, three blocks west of the Eastwick secondary hub at Wire Road and Ninth Lamp. Ironwright banners mix with residents. Tessa Morr and Docken Hale are organizers, not radicals. Their demand is a rationing rollback and a real explanation. Captain Isen Varr has about twenty officers holding containment rather than hostility. The scene should be tense because it could become ugly, not because the organizers intend violence.") + p("Before the blast, ask each player where they are at 2:30pm. This positioning is crucial because it determines which truth they are closest to when the city breaks. If they are near the protest, they experience panic and public blame. If they are near Eastwick, they see injuries and hub damage. If they are moving toward Copperstring, they may glimpse Ash or hear the music die. If they are elsewhere, the hum stops, the lights fail, and the sound reaches them anyway."))}
{scene("The blast at 2:47pm", p("The explosion is a deep pressured crack, not a fireball. The hub housing blows outward with glass, ceramic, and blue-white spark along conduit. Eastwick's lamps die in a rolling wave east to west. Copperstring stage lights cut mid-song. The protest hears the blast three blocks away, and the crowd splits between panic, flight, and people running toward the sound. This is a situation encounter. Do not default to combat. The enemies are time, smoke, confusion, fear, and the speed at which a wrong story forms."))} 
{readaloud("The sound arrives before you understand it: a pressured crack, like the city inhaling wrong. The lamps on Wire Road die in sequence. Eastwick goes dark. Somewhere on Copperstring, music stops mid-note. Then screaming.")}
{p("Give Lurielle the pre-blast tell if she is anywhere near the Network layer: the hum stutters once, cuts out for a heartbeat, or returns at the wrong pitch. Give Greer the spiritual tell: the web recoils east before the hub breaks. Give Basil the city tell: watch lines, exit routes, and who starts moving before everyone else understands why movement matters.")}
{secret("What actually happened", "Wren's cell targeted a secondary distribution hub that serves Eastwick residential blocks and part of the Entertainment Quarter. The device is custom and directional, tuned to coupling architecture with ceramic capacitor residue. It is sabotage by someone with feed-map knowledge, not an amateur bomb thrown by an angry protester. Wren is watching from a distance and calculating. Ash is closer, on a rooftop two blocks south, and guilt is already changing him.")}
{scene("The first ten minutes", p("The first ten minutes after the blast should be concrete. Mira Jol is bruised but walking. Peten Strauss has a leg laceration. Edda Venn or Toma Venn, depending on which name you prefer at your table, has serious conduit shrapnel and needs stabilization. The hub smolders with non-chemical fire texture. The watch surges east. Some protesters are horrified, some are angry, and some are simply afraid. Ash is visible only if someone looks high or follows the trail quickly: a young man, dark hair, plain clothes, traveler's boots, leaving too fast and looking too scared to be triumphant."))}
{scene("Response path: helping the injured", p("If the party helps the injured, run it as urgent care rather than a medical puzzle. Medicine DIF 13 stabilizes the serious casualty. Presence DIF 12 clears enough crowd for space to work. Magical healing works, but the social fact of who stopped to help still matters. If Brinne trusts the party, her volunteers establish a lamp-lit triage point eight minutes away. Otherwise the Mending Room in the Halfling Quarter is twenty-five minutes by streets, less with a guide. Ora Finch stabilizes the casualty if reached before sundown and can tell, if asked, that the injury pattern is deliberate coupling damage rather than ordinary Network exposure."))} 
{scene("Response path: pursuing Ash", p("If the party pursues the witness trail, Ash should remain a thread rather than a captured antagonist. Agility or Instinct DIF 14 keeps the chase through dark Eastwick and toward the Entertainment Quarter roofs. Basil's Finesse can shine here. On a partial success, they see the hood, the movement, perhaps a dropped token marked with Guild chalk that points to logistics rather than authorship. On a strong success, they see his face and can later recognize him. If cornered, Presence DIF 15 earns one true line before he bolts: he did not know they would still be inside. Do not reveal Wren. Do not confirm Green Covenant by name. Let the line haunt the investigation."))}
{scene("Response path: reading the blast site", p("If they reach the hub before the cordon closes, Investigation DIF 14 reveals that the device was directional and architecture-aware. Lurielle's Knowledge DIF 13 identifies the hub as a secondary feed that hurts residential Eastwick before it affects commercial priority. A strong read combines residue, tool marks, and witness timing into the conclusion that this was not random protest violence. It opens the Session 4 investigation thread, but it does not solve it."))}
{scene("Response path: the watch sweep", p("If the watch catches them in the sweep, make the interaction bureaucratic and tense rather than villainous. Sergeant Pel Carr wants names, positions, and whether anyone saw the access door open. Presence DIF 13 gives a credible account. Knowledge DIF 12 with technical witness detail marks them as useful. Deception DIF 15 lets Basil hide what he must, but a partial success should still put suspicion in Carr's file. Failure means delay, logging, possibly a two-hour ward station hold, and lost pursuit time."))}
{scene("Evening fallout", p("By evening, Eastwick is still dark. Candles appear in Cooperative windows. Lida's line stretches because darkness makes people hungry and her ovens still hold heat. Copperstring becomes an acoustic set or a closed door depending on how frightened you want the Entertainment Quarter to feel. The Evening Broadsheet extra names the event a hub attack without naming a culprit. Watch investigation produces interviews and no useful direction. Then Theron Ashwick's statement reaches the street."))} 
{readaloud("Today's attack on Lumencrest's Lumen infrastructure was not an accident. It was an act of anti-civilization terrorism, a deliberate strike against the Network that sustains eighty thousand lives. Those who believe that disruption of the common good is a legitimate form of political speech have now shown us the cost of that belief. The Expansionist faction has long argued that our city requires the capacity to defend its essential systems. Today's events demonstrate why.")}
{p("Theron is not present, but his statement is. Sevan Vael will call for calm tomorrow. Mira Ashton will argue for investigation over expansion. The party does not need to meet these people yet. They need to feel politics arriving faster than care. While Eastwick eats cold bread in the dark, the Council's language is already deciding what the blast means.")}
{scene("The plateau ending", p("End with the emergency Council session. Do not run the Council meeting at the end of Session 3. The announcement should feel like a public performance being scheduled over a private wound. If the party earned the forensic hook, give it one final image: ceramic residue, hub choice, and architecture knowledge. If they helped the injured, give them names and gratitude. If they chased Ash, give them a remembered face. If they were logged by watch, give them the knowledge that the city has written them down. Then stop."))} 
{readaloud("Word comes after dark, not from the watch but from a crier running Wire Road with a fresh broadsheet. Emergency Council session. Tomorrow morning. Accord Chamber gallery open to the public. The city will perform its response while Eastwick eats by candlelight. Someone knew that hub. Someone chose secondary over catastrophic. Someone watched from a roof and ran. The protest did not do this, but the protest and the blast will be chained together anyway. You are standing in the dark between them.")}
"""


def npc_chapter() -> str:
    npc_entries = [
        ("Thorn Oakwise", "Thorn is the still center of Ember Grove's prologue. He speaks little because silence is part of how he weighs truth. His lost history with earlier logging pressure means he recognizes House Vael's offer as more than economics. His instruction to Greer is not to stop timber extraction in one village; it is to watch the people around the Vael name and where what they take goes next."),
        ("Caelen Vael", "Caelen is polished, pleasant, and more prepared than a village council expects. He knows how to make exploitation sound like partnership. He does not need to know the whole family machine to serve it well. If Basil crossed him in Session 1, Caelen's awareness can echo in Session 2 through couriers, glances, and tighter security."),
        ("Elder Marta Dawnbrook", "Marta is not naive. She wants a reason to reject Vael's offer, but she is responsible for bridges, harvest reports, and a community that needs coin. Play her as a practical leader who recognizes moral danger but cannot spend morality at the sawmill."),
        ("Old Pen", "Old Pen runs the taproom immediately inside Pauper's Gate. He has survived by knowing exactly what a question costs. He can sell small truths about who passed through, who asked about feed lines, and which boots did not fit their claimed work."),
        ("Marten Halwick", "Marten at the Accord Arms is a professional host in a city where common rooms are information machines. He is not a spy, but he understands that people who pay for better rooms expect discretion and that discretion teaches a careful innkeeper a great deal."),
        ("Henris Callow", "Henris at the Traveller's Mark specializes in making strangers functional by morning. He notices complicated arrivals and does not report them simply because they are complicated. His map and advice can make him the party's first decent civic contact."),
        ("Solt", "Solt at the Dark Lantern speaks as if every sentence costs him something. He knows Shadowside's absences, including Derrin's disappearance, but he does not hand names to strangers. Honest sympathy opens more than pressure."),
        ("Mama Voss", "Mama Voss's cart is Night Market weather in human form. She does not broker information formally. She describes who is nervous, which stalls are absent, and which half-elf asked the wrong question about feed hubs."),
        ("Brinne Halloway", "Brinne chairs the Eastwick Cooperative. She is the most important neighborhood NPC in Session 3 because she turns vague civic failure into organized response. She stocks candles before officials admit the need. She trusts action, not speeches. If the party carries crates, clears space, or brings injured without asking for reward, Eastwick begins to know their names."),
        ("Lida Birch", "Lida runs the bakery that knows the Ward at hours most institutions are asleep. Her warmth is practical, not sentimental. She hears watch patterns, protest talk, and who stood in line after the lights failed."),
        ("Tessa Morr and Docken Hale", "The protest organizers are angry and controlled. They condemn the blast because it horrifies them and because it destroys the moral clarity of their demand. Their sincerity is important. If the party understands that, they can resist the city's first wrong story."),
        ("Captain Isen Varr", "Varr commands at street level during a crisis no one gave him enough people to manage. He is not cruel; he is overwhelmed. His order to get names is both practical and inadequate."),
        ("Sergeant Pel Carr", "Carr is the face of the watch sweep. He fills forms because command wants forms, but a useful witness still matters to him. Cooperative players should be remembered as cooperative civilians rather than suspects."),
        ("Ora Finch", "Ora at the Mending Room is a healer whose calm makes panic smaller. She can read injury patterns and knows the difference between ordinary Network exposure and deliberate coupling damage. She should feel like a future ally if the party cares about consequences."),
        ("Ash", "Ash is Wren's second and the most reachable member of the radical cell. He is not the bomber. He is the watcher who did not expect the human cost to land the way it did. His fear is not innocence, but it can become a door."),
        ("Wren", "Wren is the operation's mind. She is calm, old enough to have watched negotiations fail, and convinced that violence can prevent a greater theft. She is not onscreen yet unless the party radically changes the investigation. Keep her distant, calculating, and real."),
        ("Theron Ashwick", "Theron is the Expansionist voice waiting for proof that fear should become authority. His statement after the blast is polished because his faction has language ready for this kind of moment. He weaponizes truth by attaching it to the wrong conclusion."),
        ("Sevan Vael", "Sevan is the calm Conservator-adjacent voice who will seem reasonable when everyone else sounds frightened. He is dangerous because his moderation gives House Vael room to move. He does not need to approve every dark action to profit from the structure that produces them."),
        ("Lyra Vael and Mira Voss", "Lyra and Mira are not the hub bombers, but they are the reminder that Lumencrest contains deeper predators than one radical cell. Lyra funds the Shard Division; Mira runs the Guild's Lumencrest operation. Their thread waits behind Basil's heist and Shadowside disappearances.")
    ]
    entries = "\n".join(f'<div class="npc"><h4>{name}</h4>{p(text)}</div>' for name, text in npc_entries)
    return f"<h2>Chapter Eight: People of the Opening Arc</h2>{entries}"


def reference_appendix() -> str:
    fear2 = extract_fear_titles(ROOT / "gm_sessions_site/fear_options_session2.html")
    fear3 = extract_fear_titles(ROOT / "gm_sessions_site/fear_options_session3.html")
    fear2_rows = "\n".join(
        f"<tr><td>{html_escape(title)}</td><td>{html_escape(scene_name)}</td><td>{html_escape(say)}</td></tr>"
        for title, scene_name, say in fear2
    )
    fear3_rows = "\n".join(
        f"<tr><td>{html_escape(title)}</td><td>{html_escape(scene_name)}</td><td>{html_escape(say)}</td></tr>"
        for title, scene_name, say in fear3
    )
    return f"""
<h2>Appendix: Table Reference and Fear Windows</h2>
{p("The main body of this book is prose-first. This appendix keeps the small amount of structured information that is useful while running the table. Use it as an index, not as the primary way to understand the adventure.")}
<div class="reference">
  <h3>Core Difficulties and Timers</h3>
  <table>
    <thead><tr><th>Moment</th><th>Value</th></tr></thead>
    <tbody>
      <tr><td>Gate vague answers</td><td>Presence DIF 12</td></tr>
      <tr><td>False identity at gate</td><td>Deception DIF 14</td></tr>
      <tr><td>Cable car fare</td><td>2 copper marks per person</td></tr>
      <tr><td>Greer city land read</td><td>Instinct DIF 13</td></tr>
      <tr><td>Lurielle hum read</td><td>Knowledge or Instinct DIF 14</td></tr>
      <tr><td>Basil heat check</td><td>Perception or Instinct DIF 13</td></tr>
      <tr><td>Blast time</td><td>Gold Month 8, Day 2, about 2:47pm</td></tr>
      <tr><td>Stabilize serious injury</td><td>Medicine DIF 13</td></tr>
      <tr><td>Ash chase</td><td>Agility or Instinct DIF 14, then Presence DIF 15 for a true line</td></tr>
      <tr><td>Blast site forensics</td><td>Investigation DIF 14, Lurielle Knowledge DIF 13</td></tr>
      <tr><td>Watch sweep</td><td>Presence DIF 13 or Deception DIF 15</td></tr>
    </tbody>
  </table>
</div>
<div class="reference">
  <h3>Session 2 Fear Windows</h3>
  <table>
    <thead><tr><th>Fear</th><th>Scene</th><th>Opening line or effect</th></tr></thead>
    <tbody>{fear2_rows}</tbody>
  </table>
</div>
<div class="reference">
  <h3>Session 3 Fear Windows</h3>
  <table>
    <thead><tr><th>Fear</th><th>Scene</th><th>Opening line or effect</th></tr></thead>
    <tbody>{fear3_rows}</tbody>
  </table>
</div>
"""


def build_html() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HollowStar: Lights Over Lumencrest</title>
<style>{CSS}</style>
</head>
<body>
{cover_and_toc()}
{introduction()}
{opening_shape()}
<div class="part-title">{lumencrest_chapter()}</div>
<div class="part-title">{factions_chapter()}</div>
<div class="part-title">{pc_chapter()}</div>
<div class="part-title">{session_one_chapter()}</div>
<div class="part-title">{session_two_chapter()}</div>
<div class="part-title">{session_three_chapter()}</div>
<div class="part-title">{npc_chapter()}</div>
<div class="part-title">{reference_appendix()}</div>
</body>
</html>
"""


def build_markdown_summary() -> str:
    return """# Lights Over Lumencrest — Opening Adventure Module

**GM Only** — Prose-first adventure module covering the Ember Grove prologue and the Lumencrest arrival/explosion sessions.

This volume intentionally goes **through Session 3 only** because that is the currently planned material. Future planned sessions should be appended as new chapters over time.

| File | Purpose |
|------|---------|
| `GM_Bible_Sessions_2_3.pdf` | Primary print/tablet reading copy |
| `GM_Bible_Sessions_2_3.html` | Same content in browser form |
| `scripts/build_gm_bible_sessions_2_3.py` | Regenerates the PDF and HTML |

This version is written like a campaign setting/adventure book rather than a checklist. Session 1 is included as the prologue, while Sessions 2 and 3 remain the main focus.

Regenerate with:

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
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(OUT_PDF))
    print(f"Wrote {OUT_HTML}")
    print(f"Wrote {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
