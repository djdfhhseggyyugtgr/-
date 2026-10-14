# AI LIMIT: combat, enemies, bosses in numbers (round 2, branch 1b), 2026-10-13

Scope: everything the combat team needs to rebuild AI LIMIT's feel on Epic Fight (20 ticks/s). Facts already in
`docs/design/sources/notes_ailimit.md` are repeated only where a number is added or corrected.

Tags: **[V]** primary or datamined source / major wiki confirmed by a second source; **[C]** community (guide video,
Reddit, Steam, Chinese player guide) or a single source; **[?]** estimate or unconfirmed.
"Est." timings are my estimates from guide descriptions. Nobody has published frame data for these bosses, so the team
must check every timing against fight footage before it is final (see section 9).

Raw material (all under `scratchpad/research/r2/1b/`):
- `tz/catalog.json`: 1.46 MB datamined game tables from the fan archive **ailim.tzrain.wiki**. Source: Steam build
  23010530, Unity 2022.3.39f1, extracted 2026-08-29 from GameAssembly/global-metadata/bundles. Announced at
  https://steamcommunity.com/app/2407270/discussions/0/590688141302567739/. Contains boss HP, damage, poise, stun windows,
  turn rates, seals, weapons, skills, spells, buffs and level curves.
- `tz/bosses_table.txt`: one line per boss variant (110 variants: story, roguelike DLC, boss rush).
- `tz/index.js`, `tz/system.js`: formulas recovered by the site, e.g. the Fatal Strike formula and the Life Dew table.
- `F_*.json` / `S_*.json`: fetched pages. YouTube transcripts are in `scratchpad/research/youtube/`.

**Unreliable sources. Do not cite them:** ludo.guide (AI-written; invents "Ice" resistances and phases),
w12z.com (AI-written; gives Lore a gun and Panic Reaper "dark element" and a "fluorescent shield"), and xmodhub
"parry frame data" (SEO for a cheat tool; claims UE5 and stamina, but the game is Unity with no stamina).

---------------------------------------------------------------------
## 0. Datamined tables: how to read them  [V, ailim.tzrain.wiki catalog]
- Boss fields: `hp`, `basePhysicsDamage` (base attack; per-move multipliers are not in the table),
  `confidenceDamage` (Sync damage factor, 2–5), and four **defence fields, which are damage-reduction fractions**:
  `physicsDefense / fireDefense / electricDefense / psychoDefense(=Shatter)`. Example: 0.45 means the boss takes 55%.
  The site states this explicitly: "40% reduction = x0.60 received". The table also has
  `poison/puncture(=Piercing)/infectResistance` (1.0 = immune) and `maxTenacity` (poise). Bladers have 100000,
  which means "not poise-breakable; use the Sync gauge". It also has `tenacityBrokenTime` (stagger length after a
  poise break), `weakTime` (length of the stun after a Counter Field parry or a Sync break) and `weakCanExecuteTime`
  [start, end] (when the Fatal Strike prompt is live inside that stun). Also `rotationSpeed` (deg/s),
  `run` (speed factor), `newGameHpRate/AttackRate` (NG+ multipliers), `weakReturnConfidence` (Sync refilled after a
  Blader's break, 50) and `baseConfidence`.
- Player: `attributeCurve` (Life 10 → 500 LP, 15 → 585, 20 → 685, 25 → 785, 30 → 910, 40 → 1210, 50 → 1410,
  99 → 1800; Vitality 10 → absorbFix 1.0 = Conversion 100). `levelCurve`: level 1 has Stability 50 and all defences 10.
  Crystals needed for the next level: L1 500, L10 700, L15 1,696, L20 2,894, L30 5,952, L50 15,140.
- Weapon AR = base × (1 + strScaling × strFix + tecScaling × tecFix). Elemental = base × (1 + spiScaling × spiFix).
  Spell = power × mentalPowerFix. At Spirit 10 mentalPowerFix is 0.2, so Railgun does 1100 × 0.2 = 220.

---------------------------------------------------------------------
## 1. Player kit

### 1.1 Base stats and levels
- Start: all 5 attributes at 10 → **500 LP** [V data + namu], Stability 50 (level) + 30 (Seal of Newborn) [V],
  Conversion 100 [V].
- LP per Life point: +15 (11–13), +20 (14–25), +25 (26–30), +30 (31–40), +20 (41–50), +8 after 50 [V Fextralife, data].
- Typical player levels in guide videos: **Lore at L14** (Forged Steel Blade +1), **Patriarch at L19**
  (Bonecrackers +2), **Panic Reaper at L22** (Bonecrackers +3) [C BluBlu Gaming VziYX7GuPyw, hp6aVvpocxM,
  CGr2BqsXx9c]. Players who struggle report "Life 20" (685 LP) at the Patriarch [C Reddit 1lwwald].
- Death: you lose 100% − Retention of carried Crystals, with no corpse run. Retention values: Standard Nucleus 75%
  (Absorption 75%), **Void Nucleus** from Lore 65% (Absorption 80%), **Turbid Nucleus** from the Patriarch 85%
  (Absorption 70%), **Elite Necro's Nucleus** from the Panic Reaper 60% (Absorption 90%) [V data]. In the demo players
  lost about 20% [C NGA].

### 1.2 Sync Rate (stamina, mana and posture in one bar)
- 0–100%, split into levels 0/I/II/III/IV. **Main Seal widths `confidenceAreas` [L0, I, II, III, IV] in %** [V data]:

| Main Seal | widths % | So the levels are | Slots | Stability | Where |
|---|---|---|---|---|---|
| Newborn | 50/30/20/0/0 | 0–50 L0, 50–80 I, 80–100 II | 0 | +30 | start |
| **Pilgrim** | 40/30/20/10/0 | 0–40, 40–70, 70–90, 90–100 III | 5 | +70 | Shirley, Slums (needs Golden Seal Needle, also Slums) |
| Standard Seal of Bladers | 50/20/15/15/0 | | 4 | +40 | Feylia (area 3) |
| Investigator | 40/40/0/20/0 | | 5 | +50 | later |
| Executor | 70/0/0/0/30 | L0 up to 70, then straight to IV | 4 | +30 | later |
| Tree | 40/20/15/15/10 | | 5 | +60 | later |
| Clergies | 50/0/20/15/15 | | 4 | +80 | later |

  The normal seals Conversion/Deviation/Variation turn the I→II, II→III and III→IV bands into the next level up [V].
- **Damage by level** (I = 100%): attacks 90/100/110/120/130%. Skills 90% with no effects at 0, then 100/130/142.5/155%.
  Spells cannot be cast at 0, then 100/144/158/172% [V Fextralife Sync Rate]. **Fatal Strike: x0.9/1.0/1.1/1.2/1.3** [V tzrain formula].
- **Gains**: per hit, **3% with small weapons (longsword, dual, claw) and 4% with large weapons (greatsword, lance)** at
  Conversion 100, scaling exactly with Conversion/100 [V namu + Fextralife]. Per-weapon table (Light/Run/Dodge | Heavy |
  Swap | Charged): Rusty Longsword/Forged Steel 3|4|5|6; lances 4→5→6 (rising through the light chain)|6|7|9; dual
  blades heavy 3, charged 6×1.5; greatswords charged 2×5 [V Fextralife]. Fatal Strike gives +20% base [V].
  A kill gives +1/2/3% (Nucleus "Energy Absorption" Low/Med/High) [V namu]. Shield Overload Burst gives about +20% [V].
  Items: Pure Crystal +30%, Sacred Blood Crystal +100% (plus full heal and cleanse), Disordered Fetus +10% [V].
- **Passive regen** only up to the top of level 0 (Newborn: 50%). It starts 2 s after Sync was spent, runs faster the
  lower the bar is, and is scaled by Conversion [V Fextralife]. The Tree seal regenerates up to 50–75% [V data, wiki].
- **Losses**: taking a hit (scaled by Stability; at 1000 Stability hits cost nothing). Measured on the training dummy:
  Stability 215 → 2.6% per hit, 255 → 2.5%, 465 → 1.8%, 505 → 1.6% [C namu]. Weapon skills cost 20–40%. Spells cost
  20–100%. A missed Counter Field costs 10%. Shield drains while held and per block. Thunder Step costs 10% (free on a
  timed dodge). Being parried by a Blader also drains Sync. Infection drains 1%/s for 180 s
  (buff: 0.1 every 0.1 s) [V data].
- **Sync break ("Emergency Recovery")**: if a hit pushes you below 0% you are stunned for a few seconds and take extra
  damage. Afterwards the bar refills to 50% [V]. Enemy Bladers work the same way: `weakReturnConfidence` = 50 [V data].
- Design reading [C Darkbblue yqPlN-qBMoU, I4Vd91S4i0E]: **light, heavy and charged attacks barely stagger anything**,
  even mobs that have "temporary stagger resistance" moves. **Skills and spells stagger strongly, even bosses.**
  Combat therefore alternates between an *interactive generator phase* (dodge/parry, chip with normal attacks, build
  Sync) and a *safe spender phase* (skills/spells stun-lock). This loop is the core of the design.

### 1.3 Defence tools
- **Dodge**: free and spammable. **When locked on it is a Bloodborne-style dash; unlocked it is a slower roll** with
  "generous" i-frames [C Reddit 1lmrrrk]. **I-frames are front-loaded (start to mid-animation); the tail is vulnerable**,
  so dodge late rather than early [C lowhound1 VwttqgY-6UE, Reddit 1k4su2p]. One player reports a few startup frames
  without i-frames [C]. No numbers have been published [?].
- **Counter Field (parry)**: a "wind-up" parry. **You must press it about 0.5 s before the hit** [C AltChar, Reddit
  1pf460v and 1uon5ca "half second early", Steam 834997553301965726]. The startup is *not* protected: the NexusMods mod
  "Extended Parry Time" offers `IncludeWindupFrames` (wind-up counted as parry) and `ExtraParrySeconds=0.5`, which
  confirms that in vanilla the wind-up is excluded [C nexusmods.com/ailimit/mods/43]. A 3DM cheat table likewise
  "moves the judgement earlier so the wind-up state also parries" [C bbs.3dmgame.com thread-6584517].
  The active window is variously reported as "12 frames, like Sekiro" [C Reddit 1qrfhz4], "nearly 1 s?" [C NGA demo
  review] and "one of the most forgiving in the genre" [C Steam] **[?]**. Use with ≥10% Sync. A miss costs 10% and
  briefly stops regen [V]. A success costs nothing and puts a non-Blader enemy into the **weak state** for `weakTime`
  (2.4–7.3 s per boss, table in §4). The **Fatal Strike prompt is live only inside `weakCanExecuteTime`**. Some
  bosses start it 1.0 s late, e.g. the Panic Reaper ("stand farther back than you'd expect to get the prompt" [C
  Fextralife]). Any stagger damage you deal cancels the stun [V]. Parry and Shield **cannot cancel your own attack
  animation** [C Steam]. **It deflects projectiles and single beams** back at the shooter. It does not work on grabs,
  "mega" AoE blasts, big beams or Church lightning bolts [C Reddit 1t0n8nl, 1q2a42z]. Being hit by the first hit of
  a combo locks you out of parrying the rest of it [C Reddit 1ore75q].
  Seal *Scattered Stars* makes it free but you take more damage while it is up (the buff value shows defence ×0.5)
  [V data]. *Lightning Retaliation* adds a lightning strike on a successful counter [V].
- **Shield** (Sewer SW): hold to block. Unelemented physical damage is fully blocked while Sync lasts. Elemental damage
  and status buildup leak through (reduced), floor eruptions are unblockable, and **5 blocks (2–3 with an upgrade)
  overload it** (purple). Double-tap for **Overload Burst**: hyper-armour, damage about a Fatal Strike, +~20% Sync and
  a ducking i-frame. A 1.6 s defence buff follows a shield counter [V namu, Fextralife; C lowhound1; V data buff 92].
- **Piercing Claw** (Panic Reaper reward): sets off Piercing on yourself (20% max LP + 150), gives +Sync (Fextralife
  says 20%, the data buff gives 15 [?]) and extra claw hits at about 30% of AR for **20 s** (+50% with a seal), extended
  by landing hits [V data, namu].
- **Thunder Step** (late): long lightning dash for 10% Sync, with longer i-frames than a dodge. A perfectly timed
  dodge is free and leaves an exploding afterimage. The DLC upgrade adds **2 s of invincibility** after a perfect dodge
  [V namu, C Reddit].
- **Materialism "Eureka"** (katana, area 3) is a *reactive* parry: 5% to stance, a counter costs another 25% (data
  says 20 total) [V Fextralife, namu].
- Frame ability unlock order: **Counter Field** (Maintenance Access memory, Sewer SW) → **Shield** (Sewer SW, just
  before Lost Blader #1) → **Piercing Claw** (Panic Reaper, Slums) → Thunder Step (Choirmaster) [V].
  Swapping uses Frame button + face button and is "clunky" [C NGA].

### 1.4 Fatal Strike (riposte/backstab)  [V tzrain formula + "community tested" Tieba 9647083828]
- It **does not use your weapon**. It uses a hidden weapon picked by character level: base **350 (L1), 400 (L10),
  470 (L20)**, 525 (L35), 580 (L50) … 875 (L170). Damage = base × (1 + 0.4·strFix + tecFix) × Sync multiplier
  (0.9–1.3) × seals (Burst +15%, Collapse +30%) × (1 − boss Shatter reduction). **It deals Shatter damage**, and most
  bosses have their lowest defence against Shatter. Front ripostes and backstabs share the same panel.
- Example: at L14 with 12/12 Str/Tec it is about 400 × 1.08 = ~430 raw. Against Lore P1 (Shatter 0.2) that is ~345,
  about **9% of one 4000-HP phase**. The NGA "Lore dies in ~5 fatals" comment was about the demo's L101 boss-challenge
  character (~1,600 per fatal).
- Weak state boosts damage taken from all sources [V Fextralife]. Players report "2–3 parries + follow-ups ≈ 50% of
  the Panic Reaper's bar" [C SpookyFairy VQ4tm0yqecA]. That includes the free hits inside the 4.4 s stun.
- Sneak attacks one-shot weak mobs and take a chunk from big ones. They show an orange lock prompt [V Fextralife].
  Pipe-wielding Voids survive backstabs [V].

### 1.5 Healing
- **Life Dew base heal: 270 LP**. With Dew Essence 1/2/3/4/5/…/10 it heals 390/500/590/670/720/750/780/810/840/870
  [V, recovered from GameAssembly by tzrain]. Start with **3 charges**. Delpha gives the first Purified Soil in the
  Slums, so the second area has **4 charges** (max 10). The Slice has **2 Dew Essences** (Sewer SW snail and Slums
  butterfly), so the Slice ends at **500 LP per sip**. The seal *Gush* adds +20% [V].
- Mud Ball heals 300 over 12 s (1 LP every 0.04 s). Salted Mud Ball heals 600 over 12 s. Eucharist heals 1,200 over
  24 s [V data buffs]. **Partial Reconstruction** (spell, hidden Sewer SW reservoir) costs **60% Sync** and heals a
  big chunk; NGA calls it "better than flasks early" [V data, C].
- Branch rest: full LP, Sync 100%, Dew refilled, enemies respawn [V].

### 1.6 Status effects
- **Piercing** (red bar): burst of **20% max LP + 150** [V Fextralife]. That is ~250 of a 500-LP bar, and guides
  describe it as "obliterating the bar" at low level [C]. The Shield does not stop buildup [V].
- **Poison**: damage over time every 0.4 s for 90 s [V data]. **Infection**: 180 s, −1% Sync/s and more damage taken
  [V data]. Cures: Antidote, Devitalized Fetus (Piercing), Disordered Fetus (Infection, +10% Sync).

### 1.7 Early spells (Slice)
- **Railgun** (Sewer Cleaner): 20% Sync, power 1100, Spirit 10. **It interrupts boss attacks.** Guides use it as the
  "panic button" against Lore and the Patriarch [V data; C BluBlu].
- **Partial Reconstruction**: heal for 60% Sync [V data].
- **Flame Jet** (flamethrower robot, Slums): 25%, power 150, Spirit 12. Considered poor [V data, C Neoseeker].
- Throwables: Mini Bomb, Magnetic Surge, Shriek Core, Portable Lightning Bolt/Orb. Weapon buffs: Portable
  Ignition/Electrification. Guides open every early boss with throwables plus a buff [V Fextralife].
- Before v1.2 there was 1 spell slot; v1.2 (Mar 2026) gives 3 slots with quick-swap [V].

---------------------------------------------------------------------
## 2. Weapons

### 2.1 Moveset structure  [V data + Fextralife]
- Internally there are **5 action groups**: `LongSword`, `DoubleBladeSword` (dual blades and dual axes), `Halberd`
  (**greatswords and lances share one group**), `Gloves` (claws/drills) and `TaChi` (katana). Each weapon then adds an
  **R2 special variant** (`r2Type` 0–13; e.g. longsword type 0 = Jab/Impale, type 1 = Smite/Leaping Smite,
  type 2 = Jab/Impale variant) and **one fixed skill** (`skillId`).
- Inputs: R1 light chain; **R2 tap = special, R2 hold = charged** special; running and dodge attacks count as light;
  **swap attack** = weapon swap mid-combo performs an attack with the other weapon (more Sync per hit: longsword
  light 3 / swap 5); L1+R1 weapon skill, whose cost is paid per hit (Blader Longsword 8+8+9 = 25%).
- Light chain length: no hard source. Hints: dual blades "4-hit combo" [C notes]; Chinese players warn "don't greed
  the 4th or even 3rd normal hit" with greatswords [C 3loumao]; lance Sync gain rises over 3 steps [V] **[?]**.
- Speed/reach: longsword balanced; dual blades fastest, least damage; greatsword/lance slow, long reach.
  A player summary: "all the weapons are slow in this game actually; dual blades are the least slow" [C lowhound1].
  Heavy/charged attacks work as delayed punishers. Skill startup sometimes has i-frames: e.g. "first slash of the
  melee combo skill has i-frames" [C NGA]; Red Deer backstep [C Reddit].

### 2.2 Weapons obtainable up to the end of the Slums  [V data; locations V PowerPyx/Fextralife]
AR is the +0 attack rating at Str/Tec 10/10. Skill cost is in Sync%.

| Weapon | Type (group/R2) | Where | AR +0 → base +10 | Scaling Str/Tec | Req S/T | Skill (cost) |
|---|---|---|---|---|---|---|
| Rusty Longsword | longsword / Jab-Impale | start | 92 → 180 | .35/.15 | 10/10 | Homerun Swings (20) |
| Blader Longsword* | longsword | Asteria choice | 134 → 260 | .40/.20 | 10/10 | Refined Combo (25: 3 slashes + thrust) |
| Blader Swords* | dual | Asteria choice | 104 → 200 | .20/.60 | 10/12 | Swift Stabs (20) |
| Blader Greatsword* | halberd group | Asteria choice | 166 → 320 | .50/.20 | 12/10 | Brute Combo (20: 2 rising slashes) |
| Forged Steel Blade | longsword | Sewer SW, past first Branch | 145 → 280 | .45/.20 | 12/11 | Onslaught Slash (25: sliding dash + overhead) |
| Bonecrackers | dual | Sewer SW, room with 2 humans | 118 → 230 | .20/.40 | 11/12 | Bone Pulverizer (30: dash, 2 slashes, thrust) |
| Serrated Halberd | lance | Sewer SW, room full of boxes | 169 → 328 | .40/.20 | 12/11 | Charging Sweep (25: sprint + horizontal slash) |
| Rusty Pipe | longsword / Smite-Leaping Smite | Slums sewer cage | 106 → 204 | .60/.15 | 10/10 | Homerun Swing (20; hyper-armour, can also parry) |
| Pickaxe | longsword / Smite | Slums canyon crate (sniper) | 129 → 250 | .40/.20 | 13/10 | Windmill Swings (30) |
| Corrupted Blader Greatsword | halberd / Cleave-Cross Slash | Lost Blader #2 (Cemetery, needs 2,500-crystal key) | 147 → 284, Piercing 17 | .45/.20 | 15/10 | Primal Blast (35) |
| Cast Iron Greatsword | halberd | Frank's shop, 3,000–3,600 | 156 → 302 | .58/.14 | 13/11 | Earth-shattering Strike (30) |
| Impact Drill | claw / Jab-Haymaker | Frank's shop, 3,000 | 125 → 240 | .50/.29 | 13/12 | Engineering Impact (30) |
| (Opossums Sais) | dual + fire | Deluxe DLC chest | 80+20 fire | .05/.75/.4 Spi | 10/15 | Execution Flame (35) |

\*You pick one; the other two come much later. Upgrades: +1…+10, Crystals 100…1,000 per step, plus Luminous Carbon
to +3 [V data]. Community favourite for the Slice: **Corrupted Blader Greatsword**, "early end-game weapon, piercing
is OP" [C Reddit 1v747p1, 3loumao]. Katanas arrive only in area 3.

---------------------------------------------------------------------
## 3. Enemies: Sewer Town–Southwest and Slums
(Behaviour notes come from Fextralife/PowerPyx/Neoseeker walkthroughs [V] and Darkbblue's "all regular enemies"
video 83MjWFGyIK0 [C]. Regular-mob HP is not in the public tables [?].)

### 3.1 Sewer Town–Southwest (tutorial area; 4 Branches)
| Enemy | Behaviour / tells | Notes |
|---|---|---|
| Half-body (crawling) Void, bare-handed Void | weakest; no resistance to light-attack stagger, but they may hit first | block, then stun-lock [C] |
| Small-pipe Void | one "temporary stagger resistance" move: **two-handed pipe smash** → dodge front-right, not back | [C] |
| **Large-pipe Void** (elite-ish) | **counter-attacks after you land 2 hits** → hit twice, then dodge. Survives a backstab. Climbs ladders after you. Often ambushes (breaks through planks, waits behind boxes, on a bridge where you can fall) | Serrated Halberd chains stop its combo [C Neoseeker] |
| Rock-throwing Void | ranged from elevated spots | rush it or use a Mini Bomb [V] |
| **Void Beast** (quadruped) | strong for the start; **tail swipe is slower than its tell** (delayed); hides in fog/smoke, eats corpses | "attack from behind, short series, back off" [V Fextralife] |
| **Sewer Cleaner robots** | **eye flashes red before every attack = the parry cue** (easiest parry targets); they also fight Voids (infighting) | some are damaged with a human operator; one patrols a broken bridge [V/C] |
| Humans (incl. flamethrower) | pairs in rooms (Bonecrackers room) | [V] |
| Giant laser mech | **corridor hazard**: shoots lasers down a long tunnel; use sandbag cover. Later a set piece: stationary, **slams its hand; hit the hand until it falls into the pit** | drops the Reservoir Key [V] |
| Floating shriek miniboss (Reservoir hidden area) | **swipes and spinning attacks, plus a Shriek (back away or get Infection)** | drops Shriek Core ×3; guards Partial Reconstruction [V] |
| Glowing snail | hides in its shell, then **builds up a rolling spin; side-step so it hits a wall and stuns itself**, then attack the belly. Super-armour ×2 buff while rolling [V data] | drops Dew Essence [V] |
| **Lost Blader #1** (female, dual swords) | erratic; long combos then a big opening; drops Ragged Hood | blocks the path just after the Shield pickup [V] |
| Ambushes | enemy behind a door at an exit, enemy in the fog, "his friend ambushes you down the corridor", several hidden behind boxes in the Reservoir room, plank-breakers | [V Fextralife/Neoseeker] |

### 3.2 Outer-Wall Ruins–Slums (5 Branches, Temporary Campsite hub)
| Enemy | Behaviour / tells | Notes |
|---|---|---|
| Rock-throwers on bridges | ranged | Railgun them [V] |
| **Snipers** (laser sight) | **visible laser aim, then a shot**; break line of sight. **Killing one removes it permanently** (no respawn) | 2 snipers on the main path and in the canyon [V] |
| Scavengers: scythe, firearm, dual sword, **grenade thrower**, "body burners" | grenade thrower first; one **drops from above** in a hallway | [V Neoseeker] |
| "Hat" Church guards (gatekeeper type) | **electric AoE and mid-range attacks**; strike from his right can chain into a two-handed strike. Dodge back *before* he attacks | sneak-attack them [V/C] |
| Flamethrower robot (Sewer Cleaner variant) + roof enemies | drops **Flame Jet** + Luminous Carbon ×3 (450 Crystals) | [V] |
| Scavenger camp | 3 diggers + 1 guard under a sniper. **Necro flies (beam shooters) and a blade-armed Necro attack the camp; let factions fight** | [V Neoseeker] |
| **Blade-arm Necro** | long, weird combos; Piercing on hit. Stand at mid range and dodge back; parry the combo starters (front-right starters are the easiest) | the first one guards the slope after the Patriarch [V/C] |
| Faster Necro variant | **close-range Infection AoE + stab series** | [V Neoseeker] |
| Necro flies | ranged beams | [V] |
| **Spiked egg "hedgehog" traps** | dormant; spikes out when you come close | Cemetery approach [V Neoseeker] |
| Giant butterfly | poison; weak | Dew Essence + Pure Crystal [V] |
| **Explosive barrels** | 3 rolled down the slope before the Patriarch arena; hide behind the wall | [V] |
| **Lost Blader #2** (Corrupted Blader, female) | **fast, Piercing on hit**; use dodge/parry, not Shield | drops Corrupted Blader Greatsword [V] |

---------------------------------------------------------------------
## 4. Slice bosses: data sheet  [V tzrain catalog]

| | Sewer Cleaner | Lore P1 (lance) | Lore P2 (claws) | Scavenger Patriarch | Panic Reaper |
|---|---|---|---|---|---|
| HP | **500** | **4,000** | **4,000** (separate record; HUD shows one bar → P2 at 50%) | **4,800** | **4,600** (one bar; P2 at ~50–60%) |
| Base attack | 110 | 160 | 150 | **300** (heaviest) | 200 + Piercing |
| Poise (`maxTenacity`) / stagger after break | 40 / 1.4 s | 60 / 2.0 s | 70 / 2.0 s | 42 / 2.0 s | 80 / 2.5 s |
| Parry stun `weakTime` | 3.1 s | 2.83 s | **7.33 s** | 3.33 s | 4.4 s |
| Fatal prompt window | 0.1–2.5 s | 0.0–1.9 s | 0.0–3.6 s | 0.2–2.67 s | **1.0–3.1 s** |
| Turn speed | 120°/s | 180°/s | 180°/s | 200°/s | **300°/s** |
| Run factor | 0.6 | 0.75 | 0.75 | 1.0 | 0.7 |
| Reduction Phys/Fire/Elec/Shatter | .60/.65/**.30**/.40 | .45/.30/.40/**.20** | .35/.20/.30/**.10** | .45/**.25**/.35/**.15** | .48/.50/.35/.35 |
| Poison/Piercing/Infection res. | 1/1/1 (immune) | .6/.4/.2 | .6/.3/.2 | **0.0**/.8/.3 | .7/.4/**1.0** |
| NG+ HP / attack | ×3.1 / ×2.4 | ×3.1 / ×2.4 | ×3.1 / ×2.4 | ×2.7 / ×1.95 | ×2.7 / ×1.95 |
| Reward | **Railgun** | Void Nucleus, Arboretum Key | (same) | Turbid Nucleus, Luminous Diamond, **7,200 Crystals** [C Neoseeker] | **Piercing Claw**, Elite Necro's Nucleus, **12,600 Crystals** [C Neoseeker] |
| Typical kill-video length | 0:37–1:08 | 1:40–2:30 (both phases) | | 1:00–2:40 | 1:10–2:30 |
| Steam achievement % | — | The Lost **77.0%** (start 91.7%) | | — | **67.8%** |

Reading: Lore P2 is softer (lower reductions) and has a 7.3 s parry stun. That supports the Chinese "parry-loop"
strategy: parry his crawl-dash or the 3rd leap, and he falls back into the same pattern [C guhive]. The Patriarch is
a glass hammer: low poise (42), no poison resistance, weak to fire and Shatter, but the hardest hitter.
The Panic Reaper has high poise, fast turning, no Infection on it, and a delayed Fatal prompt.

---------------------------------------------------------------------
## 5. Slice boss move tables (draft)
Columns: move | telegraph | est. timing (tell → hit; recovery) | punish | source. Timings are estimates [?] unless
quoted. 1 s = 20 ticks.

### 5.1 Sewer Cleaner (boss #1; tutorial robot; small room before Sewer Confluence)
| Move | Telegraph | Est. timing | Punishable? | Src |
|---|---|---|---|---|
| Overhead arm smash | **eye flashes red**, arm rises | flash → hit ≈ 0.6–0.9 s | yes: side-dodge on the flash, 2–3 hits; ideal parry | PowerPyx [V], Darkbblue [C] |
| Horizontal arm lunge | eye flash + arm held level, then it **launches at you** | ≈ 0.8–1.0 s | yes, after the lunge | PowerPyx [V] |
| Arm-cannon beam | raises arm and points at you | **"after about a second"** | run sideways or dodge; a single beam can be deflected | PowerPyx [V], Fextralife [V] |
| Death self-destruct | dies → explodes (corpse lingers `realDeadTime` 4 s) | ≈ 1–2 s [?] | move away | PowerPyx [V], data |
Notes: 500 HP means ~5–6 light hits. It is weak to electricity (reduction 0.3) and "surprisingly fast" [V Fextralife].
Ordinary Sewer Cleaners reuse this kit later.

### 5.2 Lore, the Lost Lancer (Large Reservoir; end of Sewer SW; was the demo's final boss)
Fight start: you drop in from the Branch area and he **opens with a leap slam** [V/C].

Phase 1, lance (4,000 HP)
| Move | Telegraph | Est. timing | Punishable? | Src |
|---|---|---|---|---|
| Leap slam → spin follow-up | **spear held behind him**, crouch, leap; hangs in the air then slams; spin (2nd hit) after landing | leap ≈ 1.0–1.3 s to impact; spin ≈ 0.5 s later. Parry **"after the hang-time hitch"** [C CN] | **parry the slam** (easiest parry) or dodge both, then punish | Fextralife [V], hardcoregamer [V], guhive [C], NGA [C] |
| Charge ("pig rush") | **two-handed grip**, runs at you, knockdown | ≈ 0.8 s wind-up, then a fast run | yes: side-dodge, then **full combo + charged heavy** | hardcoregamer [V], NGA [C] |
| 2–3-hit slash strings (one ends in an upward thrust) | **backhand grip** = swing coming; big sweeps start from his right and don't swing back behind him | per-hit ≈ 0.6–0.9 s; after the **3rd ground thud he "tires"** | yes after the 3rd hit; Shield blocks the slashes | Fextralife [V], hardcoregamer [V], PowerPyx [V] |
| Feint thrust → sweep | fakes a forward jab, swings instead | ≈ 0.4 s fake + 0.7 s sweep [?] | dodge late | guhive [C] |
| Delayed vertical slash → fast thrust | long hold, then two hits | hold ≈ 1.0–1.5 s [?] | dodge the second | guhive [C] |
| **Ground pound vs grab** | raises a hand: **fast raise = pound, slow raise = grab** | grab: **unblockable, unparryable**; 2 slams + throw ≈ 30–50% LP [?] | dodge away/sideways; only used at close front range just after he re-targets | Fextralife, PowerPyx [V], guhive [C] |
| Approach | | | **Railgun interrupts his attacks** | BluBlu [C] |

Transition at 50%: he **holds his head, red mist, AoE burst** (back off), drops the lance; a few seconds to heal or
buff [V Fextralife, hardcoregamer]. Hardcoregamer says it happens at ~25%; trust 50%, since the HP data has two
4,000 records.

Phase 2, claws/berserk (4,000 HP, 7.33 s parry stun)
| Move | Telegraph | Est. timing | Punishable? | Src |
|---|---|---|---|---|
| Fixed opening 3-hit | starts P2 | 3 hits over ≈ 2 s | dodge the 2nd, go left, gain distance | guhive [C] |
| **Crawl dash ×3** (+ sweep) | low crawling charge; repeats 3× | each ≈ 0.6–0.8 s; at mid range the first 2 miss | dodge the 3rd, mind the sweep. **Parry when he is 2–3 body lengths away → 7.3 s stun** | Darkbblue [C], guhive [C] |
| Left/right leap pounces ×3 ("sweep-stomp-leap" guaranteed combo) | rhythmic hops | 3 beats ≈ 0.7 s apart [?] | **parry the 3rd leap on rhythm** | Darkbblue [C], guhive [C] |
| Long claw-swipe strings | short reach, many hits | 4–6 swipes ≈ 0.35 s apart [?] | back-dodge out of range; he **slides sideways after the string = opening** | PowerPyx [V] |
| Jump attack | jumps at you, **stays in place** | ≈ 1 s | yes | PowerPyx [V] |
| Exhaustion | "after a while it gets tired" | several s | free hits | hardcoregamer [V] |

### 5.3 Scavenger Patriarch (Slums mid-boss; large open yard after the barrel slope; jumps down to start)
| Move | Telegraph | Est. timing | Punishable? | Src |
|---|---|---|---|---|
| Hammer strings (2–4 hits) | hammer on shoulder; **some swings hold the wind-up longer than they look** (delays) | hits ≈ 0.8–1.2 s, delayed ones up to ≈ 1.5–2 s [?] | yes: dodge right-forward or straight back; **2 hits after a 4-hit string** | PowerPyx [V], BluBlu [C] |
| Jump/leap smash | leaps at you | ≈ 1 s | **parry it**, then a strong punish | Neoseeker [V], BluBlu [C] |
| Shotgun arm | raises the gun arm. **Only when you are far.** 1 shot or **3 shots sweeping from your right to your left**, spread widens with range | ≈ 0.7–1.0 s aim; shots ≈ 0.4 s apart [?] | dodge **left**; the Shield blocks it, then rush in | PowerPyx [V], Neoseeker [V], Fextralife [V] |
| Melee starters → triple shot | some melee openers chain into the 3-shot | — | circle counter-clockwise to avoid it | Darkbblue [C] |
| Spinning charge / charge | spins and charges | ≈ 1 s | **dodge inward, end up behind him** → big punish | Neoseeker [V], BluBlu [C] |
| **Grab** | **puts the hammer onto his back (hard to see, it is already on his shoulder); watch his right hand** | ≈ 1 s [?] | not parryable; back off 2 steps then side-dodge | Darkbblue [C], CN [C] |
Counter-clockwise close orbit dodges most attacks without i-frames and stops the gun [C Darkbblue].
**Weak to fire** [C BluBlu; data fire 0.25] and to poison (0 resistance). Hits "two-shot" a 685-LP player [C Reddit
1lwwald]. Steam players report that **parrying him is awkward because of the delays** [C Steam 834997553301965726].

### 5.4 Necro, the Panic Reaper (Cemetery; end of the Slice; floating 2-armed Necro → 4-armed)
Main threat: **Piercing buildup on every hit (the Shield does not stop it), so the 2nd–3rd hit taken can end the
fight**. Very parry-friendly: "a few parries + Fatal Strike take huge chunks" [C].

Phase 1
| Move | Telegraph | Est. timing | Punishable? | Src |
|---|---|---|---|---|
| **Fixed opener** | 2 harmless dashes, then "taking aim" (floats on its back, slowly rotating); **the attack starts when it turns on its side** | aim ≈ 1.5–2.5 s, then a fast strike | dodge in any direction (back is best) → **1 safe hit** | Reddit 1nm62gy [C] |
| Dash/slide slash | slow start (the opening one is slower than mid-fight versions) | ≈ 1 s | parry, or forward-dodge and counter | Darkbblue [C] |
| "Uncommon" arm swings | long wind-up, **rises higher** | ≈ 1.2 s | 1 safe / 2 risky hits | Reddit [C] |
| "Common" swing v1 | starts with the right arm, single swing, **almost no wind-up**. Its anti-greed punisher, can repeat | ≈ 0.3–0.4 s [?] | dodge; at most 1 hit | Reddit [C] |
| "Common" swing v2 | starts with the left arm, always 2 swings | ≈ 0.4 s each | 1 safe hit after | Reddit [C] |
| **Whirlwind ×3** | 2 quick 360° spins (short wind-up), then 1 strong 360° that **lunges to your position**. The wind-up ends when its right arm bends to ~90° | quick ≈ 0.4 s each; big ≈ 1.0 s | walk away from the quick spins, dodge the big one (forward or back); **2 safe / 3 risky hits**; parry the last | Reddit [C], Darkbblue [C] |
| Double pierce | two stabs | — | side-dash, 1–2 hits | Reddit [C] |
| Cross-slash | medium wind-up | ≈ 0.8 s | dodge side/forward, get behind, 1–2 hits | Reddit [C] |
| Ranged laser | Necro-fly-style beam | — | Shield it if dodge timing is hard | Darkbblue [C], Neoseeker [V] |
| **Dash grab** | from far away: slowly raises its right arm, then **rushes at very high speed** | raise ≈ 1 s, then near-instant | side-dodge as it starts the rush; big damage if caught | PowerPyx [V], Reddit [C] |
| Poise break | enough damage → **goes limp for a few seconds** (2.5 s) | — | 3 safe / 4 risky hits or a weapon skill | PowerPyx [V], data |

Transition (**~50% per guides, ~60% per one player**): **crosses its arms, levitates, Infection scream AoE**
(back off; use the time to heal or Railgun). It **grows a second pair of arms**, then **immediately rushes you**
(be ready to parry) [V PowerPyx, Fextralife; C Reddit].

Phase 2 (same moves, bigger hitboxes and longer strings)
| Move | Telegraph | Est. timing | Punishable? | Src |
|---|---|---|---|---|
| Opener: sky dive | floats high, then dives at you; **blind spot right under it** | ≈ 1.5–2 s hover | dodge forward → **3 safe hits** | Reddit [C] |
| "Dancing" combo | small hitboxes, intuitive rhythm | — | 2–3 hits after, 1 between moves | Reddit [C] |
| "Double right" | right swing → left-arm swings → 1 pierce with the right arms | — | keep dashing right, 1–2 hits | Reddit [C] |
| Thrust → dash-slash → dash-slash | fixed triple | — | parry or dodge-counter the last | Darkbblue [C] |
| Whirlwind (enlarged final spin) | as in P1 | — | **parry the last spin** (preferred in P2) | Darkbblue [C] |
| **"Berserk"** | huge lengthy swings **L-R-R-L** | ≈ 0.6 s apart [?] | dodge precisely, then **3–4 hits** | Reddit 1nm62gy (at 1:30 in its video) [C] |
| Dash grab | as in P1 | | | |
Parry note: after a parry, step back to get the Fatal prompt (it opens at +1.0 s) [V Fextralife, data].

---------------------------------------------------------------------
## 6. Other bosses (short)  [data V; behaviour V PowerPyx/namu, C Darkbblue/3loumao/Reddit]
| Boss | HP (data) | Key mechanics |
|---|---|---|
| Three-Faced Pardoner | 5,400; poise 80; weak 5.33 s | scythe sweeps (dodge right/forward); AoE pulse, then 2 homing spinning blades (left, then right), then a sliding spin; yellow ground circles → lightning. **The most parry-friendly boss** [V namu, PowerPyx] |
| Cleansing Knight | 6,400; poise 120; turn 150 | big lance knight: rear-up stomp, shield bash, **turns fast (circling gets you a turn-bash)**. At 2/3: lightning lance beam sweeping left→right (dodge left into it), **triple charge** (punish after the 3rd), tornado + **leap slam across the arena** (dodge ~0.5 s after the lightning line appears; long recovery). A CN first-timer needed 25 min [V/C] |
| Saint / Winged Colossaint / Saint of Goldnight | 7,000 / 9,600 / 5,800; poise ∞ | caster; orbs, bolt volleys, double ranged slashes; interrupt casts with heavy attacks. The Colossaint pushes you with wind on a gapped bridge (Stone's coffin shields you) [V] |
| Choirmaster / Inspector of the Uncharted Realm | 8,000 / 7,000; weak 2.4 s | teleporting caster; summons illusion mobs (roll away from them); at 50% floats in a vortex that pulls you in → landing burst (Shield it); **heals: interrupt** [V/C] |
| **Hunter of Bladers** (masked Ursula) | 11,000; **Sync gauge, poise ∞** | P1 katana: knife fan after a backstep, sheathe → crouch → dash slash (watch the sound), aerial kick (parry), spin-jump overhead, **guard stance → instant counter if you hit it**. At 50%: two swords, more aggressive, grab with an audio cue (~1 s after a skill-like sound). Drain her Sync for Fatal Strikes. First death → abducted to jail [V/C] |
| Persephone | 9,500 + 10,500 (2 bars) | P1: 5 lasers (strafe; dodge twice from the 3rd), underground wing thrust (hits ~0.5 s after the wings spread), sweeping beam, scream + orbs. P2: crawling, claw strings, 3-laser fan, orbs → leap smash ~1 s after the orbs stop. Finale: **hide behind falling slabs or die, then Fatal Strike the core**. 40 min for a CN first-timer [V/C] |
| Eunomia (+ Dike) | 6,000 (chair) → Dike 3,000 → 20,000 (arms phase) | slow hammer on a floating chair; Dike casts from a ledge; Eunomia drains Dike twice, then fights with floating fists (faster, area spells, open-hand grab). The final phase restarts on death [V/C] |
| Seraphim Absolver, Winged Punisher | 11,000 / 5,000 | Pardoner repeat with wings; gauntlet brute repeat [V] |
| Vikas | 11,500 (starts damaged) | sword + gun / dual swords; easily stun-locked first time through; hard in Semi-Void [V namu] |
| **Loskid** P1 / P2 | 6,000 / 12,500; Sync gauge; **turn 400°/s** | P1 lance 3–4-hit strings (parry them), dashes leave damage trails, at ~50% a full-arena lightning move. P2: arena buff regenerates both Sync bars (Loskid +1.25%/s, player +1%/s). **Above 70% Sync she ranks up (spends 30–35%) to rank IV, damage ×1.05/1.10/1.15/1.20**; rank IV = arena-wide moves. A golden-arm grab steals your Sync. She uses Thunder Step. "Hardest main boss" [V data/PowerPyx, C 3loumao/Darkbblue] |
| Aether | 10,000 (summon phase) + 24,000 (body) | P1: kill golden summons while dodging circles and exploding figures. P2: human-sized, slow but long combos (parry them), grab sphere (Thunder Step out of it) [V/C] |
| Charon (+ Harpy) | 8,000 bird → 18,000 | crystal shield: break it, Fatal Strike = −1/3 HP, ×3; pink/blue floor squares; after the 2nd fatal comes a scripted instakill (stand in a blue square) [V] |
| Hunter Squad | Brawler 4,500, Shooter/Scout 1,500 each, Leader 5,500 | ranged hunters join at 2/3 and 1/3; the Leader has a flame sword, a dash-sweep and a rolling kick (both easy parries from range) [V/C] |
| Wanderer of Undersea | 22,000 (weak 23.7 s) | climbing puzzle; break 4 abscesses on its back [V] |
| Guardians of the Tree | (group) | 6 Bladers sharing one bar, with Millaire [V] |
| **Ursula, the Mutated** | 12,000 (P1, Sync gauge) + 11,000 (P2, Sync 50) | P1 = all Hunter moves from the start (dart → teleport slash, sheathe → teleport dash, floaty spin kick, 4-hit with a slow flaming last hit, guard counter). P2: Necro arm, teleport grab, jump slams, fire lines, laser array, Infection screams that refill ~20% of her Sync, **Piercing**; delayed 3rd hit "frame traps" button-mashers. **Hardest boss in the game** (1 h CN first-timer) [V/C] |
| DLC: Eirene; Firebearer → Prometheus; simulacra | 10,000 + 10,000; 3,000 + 6,000 (story) | Heavenfire DoT (0.1 s ticks for 2 s); Prometheus has very long strings, all with Heavenfire. Trials meta: Thunder Step upgrade with 2 s invulnerability [V namu, data; C Reddit] |

---------------------------------------------------------------------
## 7. Difficulty and tuning evidence
- **Attrition (Steam global achievements):** Journey Begins 91.7% → **The Lost (Lore) 77.0%** → Branch Growth 69.8% →
  **Panic Reaper 67.8%** → Cleansing Knight 56.9% → Choirmaster 53.3% → Hunter of Bladers 50.8% → … → Aether 43.8%
  (main ending). **About 24 points of the 48-point total drop happen inside the two Slice areas** [V
  steamcommunity.com/stats/2407270/achievements]. The Slice is the gate where players quit.
- Perceived difficulty: "easiest bosses in the genre except Ursula and Loskid"; parry "the win button"; Patriarch
  and Hunter of Bladers are the early walls for newcomers ("43 attempts on Hunter of Bladers") [C Reddit 1t8krm2,
  1mw3fc3]. CN first-timer times: Cleansing Knight 25 min, Choirmaster 25 min, Persephone 40 min, Loskid 15 min,
  Ursula 1 h + 1 h [C 3loumao]. Lore took one NGA player 30+ minutes in the demo, then 3 tries [C NGA]. Darkbblue's
  first run took 16.5 h, and he "got stuck with two bosses" [C].
- Common causes of death: **falls** (bridges, gaps; fighting a Large-pipe Void on a bridge); **ambushes**; the
  **Piercing proc** (20% + 150 at ~500–700 LP); **grabs** (Lore, Patriarch, Reaper, Hunter); **delayed/fast-slow
  swings** that bait early dodges or parries; snipers; parrying too late because of the wind-up parry [V/C].
- What players liked: frantic, "conversational" fights, clear tells and sound cues; Blader duels [C].
  What they disliked: the wind-up parry feels unintuitive; parry plus Fatal Strike trivialises bosses; tracking and
  hitbox mismatches; Choirmaster and Persephone "marathons" with little interaction [C].
- Semi-Void (hard mode): enemies +40% damage and +50% HP, more Sync disruption, Blader bosses lose Sync slower [V].
  NG+ multiplies early bosses heavily (HP ×2.7–3.1) and late bosses lightly (×1.1–1.3), which flattens the curve [V data].
- Ideal fight length from kill videos at the intended level: **tutorial boss ~40–60 s; Slice bosses ~1–2.5 min**;
  late main bosses ~1–3 min. All-bosses no-damage run: 28 min for ~24 bosses [C YouTube].

---------------------------------------------------------------------
## 8. Sources (main)
- Datamined tables: https://ailim.tzrain.wiki/ (archive, /bestiary/bosses, /systems/fatal-strike, /systems/life-dew);
  Steam thread 590688141302567739.
- Fextralife: Sync_Rate, Counter_Field, Status_Effects, Stats, Life_Dew, Walkthrough (Sewer SW), Slums+Walkthrough,
  Seal_of_Pilgrim, Blader_Longsword/Swords/Greatsword, Serrated_Halberd, Impact_Drill, Materialism, Railgun.
- PowerPyx: ai-limit-boss-guide-all-bosses, sewer-town-southwest-walkthrough, outer-wall-ruins-slums-walkthrough.
- Neoseeker walkthroughs: Large_Reservoir, Abandoned_Houses, Cemetery, Entryway. hardcoregamer Lore guide.
  AltChar Panic Reaper guide.
- namu.moe AI LIMIT §9–16 (stats, frame abilities, enemy list) and /무기 및 의상 (weapon locations, skill costs).
- YouTube transcripts (Darkbblue "INTO DEPTH"): yqPlN-qBMoU (combat deep dive), 83MjWFGyIK0 (all regular enemies),
  LDZDiFzdCF0 (Lore/Patriarch/Reaper), fUFlmotVHlk (Hunter/Ursula/Persephone), jtilZri3DaA (Loskid),
  QNVadDh_V_s (Aether/Charon/Hunter Squad), WBatZUP2_Zg (Bishop/Wanderer), I4Vd91S4i0E (stamina design).
  lowhound1 XnMl93B7IXc, VwttqgY-6UE (parry reviews). SpookyFairy VQ4tm0yqecA, 9KOLR_plLv8.
  BluBlu hp6aVvpocxM, VziYX7GuPyw, CGr2BqsXx9c. IGN Jk4EIGDXBLw.
- Reddit r/ai__limit: 1nm62gy (Panic Reaper breakdown), 1pf460v, 1qrfhz4, 1t0n8nl, 1ore75q, 1q2a42z (parry),
  1lwwald (Patriarch damage), 1mw3fc3, 1vgixs6 (Ursula), 1uvr61y. Steam 834997553301965726 (parry debate).
- Chinese: 3loumao 532687576 (top-5 hardest), guhive Lore parry-loop, gamersky/NGA 1830133 (demo mechanics),
  3DM CT thread 6584517. NexusMods ailimit/mods/43.

---------------------------------------------------------------------
## 9. Gaps / next steps
- Frame-accurate telegraph and recovery timings for the 4 Slice bosses are **not published anywhere**. Proposal: on the
  user's PC, download 2–3 kill videos per boss (e.g. no-damage runs TCGOmpx9mbw, Vtt4lN4RFk0; Lore 0mo4TUtgz7c; Reaper
  E_zzerYe9TE; Patriarch XjLsllp3RN0) and frame-step them to fill the timing columns. Cloud sessions cannot do video.
- Light-combo hit counts per weapon type, dodge i-frame frames, and the exact Counter Field active window: unconfirmed.
- Regular-mob HP is not in the public tables. The fan site only has boss variants.
- Player damage mitigation formula (equipment defence → reduction) is not known.
