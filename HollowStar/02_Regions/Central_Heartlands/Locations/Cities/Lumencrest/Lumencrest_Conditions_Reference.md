# Lumencrest — Custom Conditions Reference

_This file defines the custom and standard conditions used across Lumencrest's district documents, substance mechanics, and encounter design. Where a condition is standard Daggerheart, it is noted as such. Where a condition is custom to this campaign, full mechanical detail is provided. All substance documents, district guides, and encounter files reference this document when applying conditions._

_Cross-reference: [[Controlled_Substances_Trade]] | [[Lumencrest_Index]]_

---

## How Conditions Work in This Campaign

Conditions in Lumencrest follow the Daggerheart framework with the following campaign-specific additions:

- Conditions are either **temporary** (cleared by rest, specific action, or time) or **persistent** (remain until a specific trigger resolves them, noted in each entry)
- **Stacking:** Unless noted, the same condition cannot stack on itself. Applying a condition to a character who already has it either extends its duration or, where noted, escalates it to the next tier
- **Clearing conditions:** Unless the condition specifies otherwise, a short rest clears temporary conditions. Persistent conditions require the specific resolution noted in their entry
- Some conditions have **tiers** — a progression from mild to severe. Substance dependency uses tiered conditions extensively

---

## Standard Daggerheart Conditions

_Listed here for reference completeness. Full rules in the Daggerheart core rulebook._

**Restrained** — The character cannot move from their current position.

**Vulnerable** — Attacks against this character deal damage directly to their Hit Points, bypassing armor.

**Frightened** — The character must move away from the source of their fear on their turn if able. Rolls made against the source of fear are made with Fear.

**Hidden** — The character cannot be directly targeted. Ends when they take an action that reveals their position.

---

## Custom Conditions — General

---

### SHAKEN

_Temporary_

**What it means:** The character has been rattled — emotionally, psychologically, or physically destabilized in a way that disrupts their focus and decision-making.

**Mechanical effect:** The character rolls all actions with Fear until the condition clears.

**Clears when:** The character takes a short rest in a safe location, or another character takes a Help action specifically to ground them (no roll required, costs the helping character their action).

**Sources:** Severe brownout while under Hollostar Dust, critical failures on withdrawal rolls, witnessing shard exposure experiments, certain Collector encounters.

---

### DISTRACTED

_Temporary_

**What it means:** The character's attention is pulled in too many directions — sensory overload, intrusive thoughts, pain, or environmental interference.

**Mechanical effect:** The character cannot use Reactions. All rolls involving precision, awareness, or focus are made with Fear.

**Clears when:** The character spends their action to collect themselves (no roll required) or moves to a significantly quieter/less stimulating environment.

**Sources:** Hollostar Dust in high-Network-density areas, Veilbloom overdose, certain arcane environmental effects.

---

### OVERWHELMED

_Temporary — can escalate to Persistent if trigger is not resolved_

**What it means:** The character is at or beyond their functional limit. This goes beyond Distracted — the character is struggling to act at all.

**Mechanical effect:** The character rolls all actions with Fear and cannot spend Hope on rolls until the condition clears.

**Escalation:** If the character takes another action that would apply Overwhelmed while already Overwhelmed, they instead gain the **Broken** condition.

**Clears when:** Short rest in a safe location AND the trigger that caused the condition is removed (e.g., leaving the area of Network density, ending a withdrawal episode).

**Sources:** Extended Hollostar Dust withdrawal, severe Fade crash, extended exposure to brownout environments while chemically sensitized.

---

### BROKEN

_Persistent_

**What it means:** The character has been pushed past functional capacity — physically, psychologically, or neurologically. This is not a temporary state. Something has given.

**Mechanical effect:** The character rolls all actions with Fear. They cannot benefit from Hope spent by other players on their behalf. They cannot clear Stress through short rest — only through long rest with specific care (medical attention, safety, time).

**Clears when:** A full long rest with active care (another character or NPC providing support — Brother Carwell, Vael, etc.) AND a successful Presence (Composure) roll against DC 14. Failure on this roll means the condition persists through another long rest cycle.

**Sources:** Hollostar Dust overdose (survived), catastrophic Fade withdrawal, direct partial shard exposure (survived), severe psychological trauma events in the campaign.

---

### MARKED

_Persistent — special_

**What it means:** The character has been identified by a hostile party — the Unseen Guild, the Vault Guard, a specific faction — as a person of interest. This is not paranoia. Someone is watching.

**Mechanical effect:** In any location where the marking faction has presence, the GM may declare that the character is being observed. NPC attitudes within that faction's sphere shift to Suspicious by default. The character cannot benefit from the Hidden condition in areas of faction presence unless they have taken active steps to change their appearance or identity (Threadbare, Inkhand's documents, etc.).

**Clears when:** The circumstances that caused the Marking are resolved — the specific investigation is closed, the character has successfully disappeared via Underground routes, or the faction's attention has been redirected through significant in-world action.

**Does not stack** — being Marked by multiple factions is tracked separately per faction, not as a stacking condition.

**Sources:** Being identified investigating Shadowside disappearances, Vault Guard sighting during Hollostar Dust possession, drawing Guild attention through repeated interference.

---

### GRIEF (Hollostar Dust specific)

_Persistent — tiered_

**What it means:** The character has developed a perceptual connection to the Lumen Network and the Heart through extended Hollostar Dust use. They feel the Heart's decline as a personal, constant loss — a diminishing at the center of their perception that does not stop when the drug wears off.

**Tier 1 — The Ache** _(2+ weeks of regular Dust use)_ The character is aware of the Heart's condition as background sensation. Not disabling — just present. No mechanical penalty, but the GM should reflect this in description and NPC reactions (something is different about the character's eyes, their attention drifts toward walls and floors where the Network runs).

**Tier 2 — The Weight** _(1+ month of regular Dust use)_ The Grief is constant and affects social and emotional function. **-1 to all Presence rolls** as the character's connection to something vast makes ordinary human interaction feel thin. In areas of high Network density, the character must succeed on a DC 12 Instinct roll to maintain focus during conversation or tasks.

**Tier 3 — The Hollow** _(2+ months of regular Dust use, or permanent after failed detox)_ The character experiences the Heart's decline as physical pain at moments of significant Network fluctuation (brownouts, heavy power draw from the Manufactories, Vault Guard activity near the Heart). During a brownout, the character automatically gains the **Shaken** condition. **-2 to all Presence rolls** as baseline. Cannot benefit from long rest in locations with active Network infrastructure unless under Dust's effect.

**Clears:** Tier 1 and 2 clear with successful full detox (3 weeks, Vael's support). Tier 3 does not fully clear — successful detox reduces it to Tier 1 permanently. Some characters learn to manage Tier 3 rather than cure it.

---

### BURNING NEED

_Persistent — tiered, substance-specific_

**What it means:** The character's body or mind has reorganized around a substance. This is dependency made mechanical — the condition tracks what the character needs to function, not what they want.

_This condition is applied by individual substance mechanics rather than directly. See [[Controlled_Substances_Trade]] for the specific triggers for each substance._

**Tier 1 — Preference** The character notes a strong preference for using. No mechanical effect yet. The GM tracks this privately.

**Tier 2 — Need** Without the substance for 24+ hours, the character takes **-1 to all rolls associated with that substance's primary trait** (Strength for Red Cradle, Knowledge/Instinct for Fade, etc.). With the substance, they function normally.

**Tier 3 — Dependent** Without the substance for 24+ hours, the character takes **-2 to the associated trait rolls** and gains **Distracted** at the start of any demanding scene. With the substance, the Boon functions but no longer provides its peak effect — it returns the character to baseline only.

**Tier 4 — Broken Need** _(long-term, see substance entries for timelines)_ The character's baseline is now permanently affected until full medical detox. See individual substance entries for permanent debuff details. Detox at this stage requires Vael's full treatment protocol and takes 3-6 weeks depending on substance.

**Clears by tier:** Tier 1 — one week abstinence, no roll required. Tier 2 — two weeks abstinence, DC 12 Fortitude roll at end of each week. Tier 3 — three weeks with medical support (Vael), DC 14 Fortitude weekly. Tier 4 — cannot clear without Vael's protocol; weekly DC 15 Fortitude; failure extends treatment by one week.

---

## Custom Conditions — Hollostar Dust Specific

_These conditions apply only to Hollostar Dust use and the Shard Division's experiments. They represent the drug's unique interaction with Hollostar energy and the perceptual changes that result._

---

### RESONANT

_Temporary — positive condition_

**What it means:** The character's perception is currently aligned with the Lumen Network's energy field. They can feel and, with focus, interpret what the Network is doing around them.

**Mechanical effect:**

- The character can detect Network infrastructure, active power draw, and energy fluctuations within 100 feet without rolling
- The character gains **Advantage on Instinct rolls** involving arcane energy, Network infrastructure, or Hollostar-related knowledge
- Once per Resonant episode, the character may attempt a DC 12 Knowledge (Mystical) roll to receive a specific piece of information about the Heart or Network that would not be accessible through ordinary means (GM determines content)

**Duration:** Equal to the active window of Hollostar Dust (2-4 hours standard dose)

**Ends:** When the Dust's active period ends. If the character has Tier 2+ Grief, a faint echo of Resonant perception persists — not the condition, but a flavour of it.

---

### SIGNAL BLEED

_Temporary — negative_

**What it means:** The character is receiving more Network signal than they can filter. The Resonant state has become noise rather than information — too much, too fast, uninterpretable.

**Mechanical effect:** The character is **Distracted** (see above) and additionally cannot use the Resonant condition's benefits while Signal Bleed is active — the clarity has become interference.

**Triggers:** Being Resonant in an area of very high Network density (Radiant Core, Academic Quarter near nodes, within 200 feet of a distribution hub) OR during a brownout while Resonant (the fluctuation hits like a physical blow).

**Clears:** Moving to a lower-density area (Shadowside has no Network — Signal Bleed ends within minutes of entering the district) OR the Dust's active period ending.

---

### TRANSFORMED (Shard Exposure — Dust long-term or experiment)

_Persistent — permanent if full shard exposure_

**What it means:** The character has been changed by Hollostar shard material at a cellular and arcane level. For recreational Dust users, this manifests as the ability granted by the Hollostar Dust ability table (see [[Controlled_Substances_Trade]]). For experiment subjects, this is something more significant and less controlled.

**Recreational Dust transformation:** The character has gained one ability from the Hollostar Dust ability table. This ability is permanent. The character does not know it came from the Dust — it manifests gradually over weeks of use, easily misattributed to growth, stress, or luck. The ability is real. It cannot be taken away by detox. It can, however, become dependent on Dust if the character continues using (see [[Controlled_Substances_Trade]] for the impairment mechanics).

**Experiment transformation (GM-controlled):** Not for player use under normal circumstances. Subjects of the Shard Division's experiments who survive gain abilities from a more extreme version of the table, with correspondingly more severe physical changes. Some survive in ways that are not functional. The Transformed condition in this context is a campaign event, not a player mechanic.

**This condition does not clear.** Detox removes the Burning Need. It does not remove the Transformation.

---

## Condition Interaction Notes

**Grief + Resonant:** A character with Tier 2+ Grief who takes Hollostar Dust experiences a specific version of Resonant — the Ache temporarily resolves, the Grief lifts, and the Network perception is clear and painless. This is mechanically identical to standard Resonant but experientially distinct and narratively important. The GM should describe this differently from a first-time user's Resonant experience.

**Broken Need + Burning Need Tier 4:** A character who has reached Burning Need Tier 4 and then attempts cold-turkey cessation automatically gains the **Broken** condition at the start of the withdrawal period. This cannot be avoided without Vael's taper protocol.

**Marked + Shaken:** A character who is both Marked by the Unseen Guild and Shaken in a location where the Guild has presence must succeed on a DC 13 Presence roll or their distressed state draws attention — a Guild-adjacent NPC notices something is wrong with someone they've been told to watch.

---

_This document is referenced by: [[Controlled_Substances_Trade]] | [[05_Shadowside_Expanded]] | [[08_The_Underground_Expanded]] | [[Lumencrest_Index]]_