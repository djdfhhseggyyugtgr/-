# R2-1A — AI LIMIT: areas and level layout (2026-10-13)

Scope: how the original game's areas are built, so our builders can recreate the **feel and structure** of the two slice areas (Sewer Town–Southwest, Outer-Wall Ruins–Slums) without copying them. Facts already in `docs/design/sources/notes_ailimit.md` (area list, branch counts, boss list, story beats) are not repeated here.

Tags: **[V]** a wiki or guide page, an official page, or a dialogue line heard in a transcript; **[C]** one reviewer, a forum post, or my reading of a video frame; **[?]** an inference or something I could not confirm.
Raw files: `research/r2/1a/` (`F_*.json` pages, `S_*.json` searches, `img/` YouTube auto-frames plus contact sheets `img/sheet_*.jpg`). YouTube transcripts are in `research/youtube/`.

---
## 0. Sources used (and what each one gives)

| Source | Gives | URL |
|---|---|---|
| Fextralife walkthroughs (Sewer SW is the "Walkthrough" page; Slums, Rooftop, Flooded, Withered, Parish 1/2, North, Spirit Depths, Center, Elysium) | the most narrative route text: shortcuts, hidden rooms, fights | https://ailimit.wiki.fextralife.com/Walkthrough ; https://ailimit.wiki.fextralife.com/Slums+Walkthrough (others: `<Area>+Walkthrough`) |
| Neoseeker branch-by-branch (Jaska) | the best step-by-step text, ambush spots, which enemy sits where | https://www.neoseeker.com/ai-limit/walkthrough/Maintenance_Access , /Large_Reservoir , /Before_Upward_Elevator , /Path_of_Pilgrimage , /Temporary_Campsite , /Abandoned_Houses , /Cemetery , /Entryway |
| PowerPyx | item lists and the branch list with "reached from" | https://www.powerpyx.com/ai-limit-sewer-town-southwest-walkthrough/ ; https://www.powerpyx.com/ai-limit-outer-wall-ruins-slums-walkthrough/ ; https://www.powerpyx.com/ai-limit-all-branch-locations/ |
| JP charts (al-gest, otoki-game) | numbered route charts, JP branch names, extra mechanics notes | https://al-gest.com/ai-limit/ai-limit-trial/ ; https://al-gest.com/ai-limit/ai-limit-story02/ ; https://otoki-game.com/ai-limit-firststage/ ; https://otoki-game.com/ai-limit-2nderea/ |
| Kihra 100% walkthrough parts 1–2 (transcripts with in-world NPC dialogue) | NPC lines and environmental storytelling | https://www.youtube.com/watch?v=Iol-oUgsFiA (Sewer, 52:45) ; https://www.youtube.com/watch?v=lPM5xXYbFUM (Slums, 51:51) |
| TurboAchiever collectible timelines | timestamped route = segment lengths | https://www.youtube.com/watch?v=utZ2jIFgPs4 (Sewer 25:31) ; https://www.youtube.com/watch?v=WARhbOMefgg (Slums 25:48) |
| gcores player essay (CN) | level-design analysis: loops, verticality, upward guidance | https://www.gcores.com/talks/1069047 |
| vgover essay (CN) on Spirit Depths guidance | the best design analysis found (frustration, pause, cycle) | https://www.vgover.com/news/159457 (the page now 404s; full text was kept in the search result, `research/r2/1a/S_无限机兵_关卡设计*.json`) |
| IGN China review | critique of routes, ambush frequency, empty geometry | https://www.ign.com.cn/wu-xian-ji-bing/53484/review/er-ci-yuan-lei-hun-dong-zuo-rpgwu-xian-ji-bing-ping-ce-7-fen-ign-zhong-guo |
| PCGamesN interview (lead designer Yang Ruichen, producer Yang Bin) | design intent, *Blame!* inspiration, the manhole exit | https://www.pcgamesn.com/ai-limit/interview |
| UK Anime Network demo impressions | scale moments in the sewer (fogged cistern, laser mech) | https://www.uk-anime.net/articles/AI_Limit_(Demo_Impressions).html |
| Reviews: RPGamer, FingerGuns, TheSixthAxis, GameRant, GamingBible | praise and criticism of the levels | URLs in §7 |
| Reddit r/soulslikes threads | player views of the level design | 1uh6gdn, 1ujk5lx, 1ve2h7h, 1x54pxi |

**Unreliable, do not use:** `w12z.com/art/1546.html` and `/1549.html` (machine-written fiction: crossbows, a "West Gate", bonfires that cost items) and `ludo.guide` (a regurgitation of Fextralife, partly made up). Both are flagged so nobody cites them later.

---
## 1. Sewer Town – Southwest (지하 수로·남서 / JP 地底水路・南西)

### 1.1 Snapshot
- Role: tutorial area and the **free-demo content**; the demo ends when you ride the final elevator out. [V al-gest/otoki]
- Official tagline: "cold and damp sewers". [V Steam] Inspiration is the *Blame!* megastructure (Tsutomu Nihei). [V PCGamesN]
- **4 Branches**: Sewer Confluence (JP 集水エリア) → Maintenance Access (メンテナンス通路) → Large Reservoir (貯水池) → Before Upward Elevator (上りエレベーター前). [V PowerPyx/al-gest]
- Fights: Sewer Cleaner (gate miniboss), giant laser mech (environmental "boss"), snail (optional), spherical scythe-armed Necro "meatball" (optional miniboss), Lost Blader #1 (miniboss), **Lore, the Lost Lancer** (area boss). [V]
- Time: efficient all-collectibles run 11:50 (Jun Guides https://www.youtube.com/watch?v=4KZgFkYXQjM) to 25:31 (TurboAchiever). Full 100% runs with commentary: 42–72 min (bgLPs 42:02, Kihra 52:45, SilveRO 58:55, Akilles no-commentary 1:11:42). A first blind demo run took **~2.5 h** including deaths. [V video lengths; C UK Anime]
- Segment lengths from TurboAchiever's timeline (collect run, so treat as relative): start→Confluence 1:31 · →Maintenance Access 5:30 · →Large Reservoir ~13:45 (the big loop plus the key detour) · Lore→exit ~4:20. [V]

### 1.2 Route, beat by beat (main path in **bold**, optional in *italics*)
**A. Start → Sewer Confluence (tutorial spine, linear)**
1. **Wake face-down in mud in a narrow corridor**; Rusty Longsword lies by a broken machine. [V otoki/PCGamesN] Stairs up give Mud Ball ×3 by a corpse, then **drop down**. [V Fextralife]
2. *Left: a Void Beast in a cell behind iron bars* (it cannot pass the bars, so players cheese it from behind them; Pure Crystal ×3; Luminous Carbon on kill). **Right: ladder down = main route.** [V otoki/Fextralife]
3. **Tutorial corridors**: dodge, weapon skill, then a **pipe interior with the backstab (Fatal Strike) tutorial**, Mini Bomb ×3, a rock-thrower, then a room with **Old Notepad** (the tips journal). [V]
4. **Door → Sewer Cleaner** (fast robot, explodes on death, drops the Railgun spell) in an amber-lit machine room with hazard stripes on the floor. [V; C frame py0FKYKEHMw_2]
5. **Old man NPC**: "Finally a Blader... Thank you for helping us deal with the Void... go and meet the Branchweaver. Her lordship is waiting... not much time left." [V Kihra transcript] *Dead-end tunnel with a Pure Crystal.*
6. **Sewer Confluence**: a round tank chamber of big rounded concrete and steel tanks, **ankle-deep black water**, the Branch growing out of the pool, **Asteria** on a raised ledge. Repair the Branch, get Life Dew ×3, pick a weapon. The Deluxe container stands by the exit door. [V; C frames Nxc0wPY3edY_2/3]

**B. Confluence → Maintenance Access (first fork, first reveal)**
7. **Corridor left past a broken bridge**: *an item is visible across the gap but unreachable* (reached at the very end via the vending-machine elevator, which closes a loop to the start). Sewer dwellers talk here ("Stay away from the mud", "You want to escape to the surface too? How pathetic... The monster is still there"). [V Fextralife/Kihra]
8. **Elevator up.** Step on the raised square in the middle; if the platform is on the other floor you fall to your death, a classic Souls elevator. [V Neoseeker] **Room with an enemy ambushing from behind a door**, Mud Ball, stairs, double doors. [V]
9. *Right: smash crates, **running jump** across a broken walkway → a Sewer Cleaner guards the Forged Steel Blade and a locked double door with voices behind it.* [V]
10. **Three enemies plus a rock-thrower** → stairs up (a pipe-wielder; fighting from lower steps makes it harmless) → *side room with a safe (Traveler's Outfit)*. [V Neoseeker]
11. **Signature reveal: a collapsed drainage tunnel opens onto a cistern so big its far side is lost in fog**, and a **giant laser mech** anchored at the far end fires laser sequences, also obliterating Void crawlers. Move from **sandbag to sandbag**, then dive into a **pipe on the right** (it cannot reach you there); loot left behind is collected later. [V; C UK Anime "a one-scene wonder"; gcores compares it to DS1's Hellkite Bridge]
12. **Maintenance Access Branch** sits just inside, past the pipe. The door to the left of it stays locked (it is the shortcut, opened from the other side). [V]

**C. Maintenance Access → Large Reservoir (the hub loop, the only real labyrinth)**
13. **Memory orb → Counter Field** (parry), with three resting enemies right after it to practise on. [V]
14. **Foggy corridors with an enemy hidden in smoke** (twice, one a quadruped). Then **cross a pipe to a scaffold**: on a **narrow bridge** a pipe-wielder can knock you off while **a thrower stands higher up**. "Rush it or pull it to your side." [V Fextralife/Neoseeker]
15. Ladder up → backstab → bars → **robot vs Void fight** (lure the robot onto the others, or let them fight). [V]
16. *Crates hide a **floor hatch**: drop to a lower room (Mini Bomb, Luminous Carbon, an NPC who tells you to get lost), running-jump back over a broken bridge, ladder up.* **Walk along a big pipe** to the next scaffold. [V]
17. **Fork: drop through a hole OR jump the gap; both rejoin.** Upper route: a Void eating a body, then a **pipe-wielder bursts through a wooden wall**, a room with a note, a room of three enemies with a **safe (Blader Armor/Visor)**, and a **door with a GREEN light = shortcut back to Maintenance Access**. [V Fextralife/PowerPyx/al-gest]
18. *Crates and planks hide a room with the **Mud Ball maker NPC** (sewer folk share the machine on a "schedule") and Mud Ball ×5.* **Ladder down into a pitch-dark box room ambush** (several hidden enemies including a pipe-wielder; Serrated Halberd by a wrecked Sewer Cleaner). A **gap behind the ladder** leads to a corridor and a **door with a RED light** that is locked; its sign reads "**Mud collection site number five**" (Reservoir Key). [V Kihra/otoki/PowerPyx]
19. Back at the safe room, a **hole in the wall** leads past three enemies to a corridor ending **beside the mech's anchor hand**. Strike the hand from the corridor mouth between its slam sequences (punch, double punch, flamethrower). It loses its grip and **falls into the bottomless chasm**, which opens the tunnel it guarded. The **Reservoir Key** lies on a narrow beam (easy fall). [V Fextralife wiki Reservoir Key page]
20. *Key detour, a loop: the door to the right of the chasm (the other side of the red door) → ladder down → room (Crystallized Remains under stairs) → glowing snail (poison cloud, Dew Essence) → ladder → the spherical scythe-armed Necro miniboss (Infection scream; Partial Reconstruction, Tiny Resonance) → a **super-long ladder** up opens a door by the key spot. That closes the loop.* [V]
21. **Main tunnel behind the mech**: two backstab-able enemies, then the **Shield frame ability** on a corpse with a purple glow, then **Lost Blader #1, introduced killing a Void creature** before turning on you. The arena is a curved wall with three huge round culvert mouths. [V; C frame 0ZhWimMczeU_2]
22. In the arena: *a planked-up middle tunnel = hidden area (pipes, running jump for loot)*; *the left tunnel has a side branch where an enemy rises from the ground*; **main: going uphill, an enemy with its back turned is bait and two more rise from the ground (trap)**. [V Neoseeker]
23. **Human sitting by a damaged Sewer Cleaner (both attack)** → crates block bars → intact Sewer Cleaner → *door opposite: a flamethrower man bursts out as you open it (Bonecrackers)* → bridge with a body hanging from it (Mud Ball) → staircase down. [V]
24. **A yard of giant rusted robot shells** (bullet-shaped hulks, catwalk above, grey fog). Fork: *left = elevator up to the far side of the step-7 broken bridge (item) and **Opossum's Vending Machine** (Mud Balls, Crystallized Remains, the Ponytail cosmetic); this loops back to the start*; forward = **Large Reservoir Branch**, which overlooks the boss pit. Bitter NPC nearby: "As soon as her lordship perished, those wretches ran away... all killed by Lore... They all wanted to go to the surface... I'd rather die collecting mud." [V; C frame KH6UsQs3QkM_3]

**D. Boss and exit**
25. **Jump down (one-way) into the reservoir floor → Lore.** A huge flooded hall with a brick tunnel mouth, shallow black water, **drifting embers, fog**, and Lore's orange glowing crystal crest as the only warm light. [V; C frames l5a1ayG8EgI_1/2] After the fight Asteria speaks over Lore's remains: the Void are "consciousness within the mud" that "succumb to madness". [V transcript]
26. **Before Upward Elevator Branch** in the next room, with a **Memory beside it (Metastability seal)**. A robbed NPC: "My life savings... give it back, you bastard." [V; C frame SHESuQi42SQ_1]
27. **Stairs → walk while "seeing Asteria's shadow" → the upward elevator.** [V otoki] Area complete.

### 1.3 Shortcuts and loops (Sewer SW)
| Shortcut | Opens from | Connects | Type |
|---|---|---|---|
| Green-light door | safe room (step 17) | Maintenance Access Branch | door opened from the far side |
| Super-long ladder + door | Reservoir-key basement (step 20) | the key ledge by the chasm | ladder + one-sided door |
| Elevator by the vending machine | robot-shell yard (step 24) | the broken bridge near Sewer Confluence | elevator (closes the loop to the start) |
| Red-light door | inside, with the Reservoir Key | the dark box room ↔ the basement detour | key door |
| Mech's tunnel | killing the mech | the main route onward | an obstacle you destroy |
[V Fextralife/PowerPyx/Neoseeker/al-gest]

### 1.4 Verticality sketch (inferred from route text; [?] for exact counts)
```
L3  broken-bridge level near Confluence  <-- elevator (end) --- vending machine          (loop back to start)
L2  upper catwalks/rooms: Forged Steel Blade, safe rooms, green-light shortcut, scaffolds over the cistern
L1  main tunnels: Confluence pool, laser-mech cistern (fogged, huge), Maintenance Access, Lost Blader arena
L0  basement: dark box room, red-light door, snail and scythe-Necro rooms, Lore's reservoir floor (one-way drop)
```
Elevator up at the start, then the route winds down to L0 for the boss and back up by elevator to the exit. Players remember it as a loop "with multi-level interconnections". [C IGN China calls the route "simple"; the gcores essay praises the "hidden middle layers"]

### 1.5 Enemies and ambush spots
- Roster: red Void humanoids (zombie-like, some rise out of the floor), rock/stone throwers placed above you, quadruped Void (one eating a corpse), big pipe-wielding Void, Void Beast (caged, optional), Sewer Cleaner robots (some fighting the Void), the anchored giant laser mech, poison snail, spherical scythe-Necro, flamethrower humans and hooded humans (hostile sewer folk), Lost Blader #1 (enemy Blader with a Sync gauge), Lore. [V; C FingerGuns "red zombie-like creatures in the sewers"]
- Ambush grammar: **behind a door you open** (steps 8 and 23), **in smoke** (14), **through a wooden wall** (17), **a pitch-dark room** (18), **out of the floor beside bait** (22), a **thrower above a narrow bridge** (14), **a fall-risk bridge with a heavy** (14). [V]

### 1.6 Storytelling devices seen here
- **Item Memories**: every pickup carries a voice fragment. Reservoir Key: "Necros...! Necros are coming down with that big guy!" / "Must warn everyone... Run..."; Arboretum Key (from Lore): "She... will be... back... Find... the key... Fight... again!" [V Fextralife item pages]
- **Notes are read in the world** (blue spherical glow) and stay stuck to the floor (players dislike this). Door signs ("Mud collection site No.5"). [V Kihra; C Reddit 1ve2h7h]
- **Sewer folk**: sparse survivors behind doors who curse their god, share a mud-ball machine, and scorn people who flee to the surface. [V transcripts; C UK Anime]
- **Machines fight monsters on their own**: the robot-vs-Void ecosystem. [V]
- **Memories at Branches** (flashback cutscenes) and memory orbs that grant abilities. [V]

### 1.7 Look and mood (frames in `img/sheet_sewer1.jpg`, `sheet_sewer2.jpg`)
Desaturated **blue-grey and teal**, black reflective water, big round tanks and culvert mouths, teal-painted railings, rust. Warm accents only at machines (amber), embers, and enemy cores (orange-red). Fog gives scale. The anime character art contrasts strongly with brutalist concrete (PCGamesN). Reviewers' complaint: "dingy dull brown subterranean tunnels" (TheSixthAxis). [C]

---
## 2. Transition: Sewer → Slums
1. The upward elevator from Before Upward Elevator, then "a change in atmosphere, though still underground". Pure Crystal on the right; stairs up a wall to the surface **through an open manhole**. [V Neoseeker; V PCGamesN: "venture beyond an open manhole cover and emerge on the outskirts of a ramshackle shanty town banking a colossal city wall"]
2. Small alley (Mechanical Part) → door into a building → two flights of stairs → a **"welcome" cutscene and title card**: a wide shot of Havenswell and the wall. A corpse on the railing holds the **Ancient Map** (it shows only how areas connect: "Blocked roads, collapsed bridges, earthquake faults, and that Mud Lake..."). [V Fextralife Ancient Map; Steam thread 601900196106936746]
3. **Stairs/ladder down → Path of Pilgrimage Branch** (JP 巡礼の道). [V]
→ The design sequence is **elevator up → dark-to-light reveal → title card vista → map pickup → checkpoint right below**. Only about 1–2 minutes of playtime.

---
## 3. Outer-Wall Ruins – Slums (성벽 밖의 폐허·빈민가 / JP 壁外の廃墟・スラム街)

### 3.1 Snapshot
- Official tagline: "layers of slums". [V Steam] A shanty town of refugees outside the wall; scavengers prey on people but fear the Church, so they leave pilgrims alone. Their noise drew Necros, and in the second half the Necros slaughter them in scripted fights. [V namu 지역; Delpha dialogue]
- **5 Branches**: Path of Pilgrimage → Temporary Campsite (hub) → Abandoned Houses (廃屋群) → Cemetery (墓地) → Entryway (JP 高架橋 "viaduct"). [V]
- Fights: snipers (2), flamethrower robot (Flame Jet), butterfly (crystal cave, optional), **Scavenger Patriarch**, Lost Blader #2 (optional, behind a key gate), **Necro, the Panic Reaper**. [V]
- Time: collect runs 12:27 (Jun Guides https://www.youtube.com/watch?v=MlYmR-hMED4) to 25:48 (TurboAchiever). Full 100% runs: 40–75 min (bgLPs 39:55, trueeevil 46:38, Kihra 51:51, SilveRO 1:14:27). [V]
- Segments (TurboAchiever): Map 0:06 → Pilgrimage 0:31 → Campsite 1:31 → Drizzle 3:38 → shortcut 4:37 → Flame Jet 5:41 → **Abandoned Houses 7:24** → optional elevator loop 9:22–14:52 → Patriarch 15:35 → tree memory 17:11 → Iron Pot + ladder shortcut 17:49 → cemetery gate 18:23–19:08 → **Cemetery 20:53** → Panic Reaper 21:58 → **Entryway 24:10** → Stone 24:42. [V]

### 3.2 Route, beat by beat
**A. Path of Pilgrimage → Temporary Campsite (street descent to a safe hub)**
1. Ramp down-left (Mini Bomb) → **three scavengers: an explosive-charge shooter in front plus two scythe-wielders, one backstab-able**. [V Neoseeker]
2. Stairs left: one enemy with its back turned, one stepping out of a house → passage with more stairs → a house with a gunman → **a body hanging over a railing** (Portable Ignition ×2) → **a grenadier on a bridge above you**. **Flammable drums inside buildings** go off when enemies use fire. A route through a building rejoins the slope and lets you kill enemies hiding above safely. An enemy sits on a roof; Noise Tape. [V Neoseeker/otoki]
3. A street of scattered enemies → **Temporary Campsite**: no enemies (Delpha: "this camp has some kind of barrier against the Necros"). [V transcript] Look: a log bonfire in the middle, corrugated-metal shacks, pallets, caged plastic tanks, crates with candles, a huge curved hull or wall behind, overcast sepia light. NPCs: **Shirley** sitting on crates (names you, gives the Seal of Pilgrim), **Delpha** (soil, Purified Soil), **Merchant Frank** (Grayrhino Grocery: Cemetery Key, two weapons), a **target dummy**, a man sleeping. The Branch is right of the shop. *Along the left wall, crates hide a **wired door you cannot open yet*** (foreshadows the late-game return from the Ancient Machine Works). [V; C frames lPM5xXYbFUM_hq, SHESuQi42SQ_2]
4. **Gatekeeper** (a man in a hat): "Order from the great patriarch. No one shall disturb the pilgrims... Show me the Pilgrim's Seal." He blocks the exit until you have it. [V transcript]

**B. Campsite → Abandoned Houses (the sniper gauntlet; "go up")**
5. Past the gate (Portable Lightning Bolt): a **hanging bridge**, then a **sniper on a tower**. A **red laser line tracks you, turns orange, then fires**; break line of sight behind walls and under roofs, or keep rolling. Players call it "very, very annoying". **Once killed, the sniper never respawns.** [V Fextralife/Kihra]
6. Under the sniper's roof: a resting scythe-man; gate → **hat-wearing electric mage** (AoE lightning under your feet at range; sneak along the left wall past a phone booth) → stairs near gates → building (scythe + gunman) → hallway (dual-sword man) → *gated loot seen for later* → building on the left: **room full of red barrels** (Drizzle seal) → light-blue metal door → grenadier first → descending hallway where an **enemy drops from above** → two **flamethrower men burning bodies behind a fence**. [V Neoseeker/otoki]
7. **Stairs up → small stairs → building → down inside → double door = shortcut to the Campsite.** A *manhole/ladder down to a short sewer stub (Luminous Carbon; "a preview of a later area")*. A **woman with a pack** here warns: "If I had known not even Sienna could get rid of the monsters... Run away. It's not too late." [V Fextralife/Kihra; name spelling "Sienna" [?]]
8. **Plank bridge** across the gap → building → terrace (an enemy behind boxes) → bridge → stairs down (connects back) → **kick-down ladder shortcut** → scaffold up to the sniper (he barely resists). [V otoki/Kihra]
9. Across roofs: a **flamethrower robot plus two grenadiers on two rooftops** (clear the roofs first, jumping roof to roof) → Flame Jet spell + Luminous Carbon ×3. *Breakable boxes on that roof → drop to the roof below (Salt Brick)*. From the roof edge **you see the optional elevator (right) and the gate path (left)**. [V Neoseeker]
10. **Grated door → hat mages (backstab one)** → a building on the left: **Seal Needle** (the seal-rewrite tutorial), pilgrims, and **a note about an old man carrying a coffin who attacks pilgrims** (foreshadows Stone). → ramp to scaffold → two staircases → **ladders → Abandoned Houses Branch on a high platform**. [V Neoseeker/Kihra]

**C. Optional loop: elevator down into the canyon (a separate lower layer)**
11. Elevator → a **scavenger dig site** (three diggers plus a guard; a second sniper). Wait and **Necro flies (laser) and a blade-armed Necro arrive and fight the scavengers**: a faction-war set piece you can exploit. Ladder → Pickaxe chest; Antidote; a cave with a Necro. [V Fextralife/Neoseeker]
12. Stairs up → **boxes hide a hallway → a blue crystal cave with dark water** (butterfly that poisons: Dew Essence; also Luminous Diamond, Tiny Resonance, Sacred Blood Crystal). [V; C frame WARhbOMefgg_2] gcores links the blue-crystal-and-butterfly pairing to DS1's Moonlight Butterfly. [C]
13. Stairs to the top → **a short sewer section (Rusty Pipe in a cell)** → ladder **up into a building** (Scavenger's Clothing chest; the Luminous Carbon you saw earlier from the bridge) → a roof door. This returns to the slum level. Next to the Abandoned Houses Branch a ladder and a **locked gate you can jump over** link the same loop. [V]

**D. Abandoned Houses → Cemetery (uphill, the Necro takeover)**
14. **Drop from the Branch; three barrels roll down the slope at you, so hide behind a wall** → up the slope, left → **a large arena where the Scavenger Patriarch jumps down** ("Your money and your life"): a hammer, plus a shotgun arm at range. **A gate opens to the right of the arena after the fight.** [V Fextralife/Kihra]
15. Uphill: an enemy with **blade-like hands** (Piercing) and an open yard with loot in the side buildings → a **big dead tree** where **hooded humans fight blade-armed Necros**. A **Memory beside the tree** (Hardened Skin): "Sienna, they went to the cemetery, but none of them came back... Protect the [heart?] of the tree. Repel the Necros." [V; transcript wording uncertain]
16. *Left side path: the camp's sleeping man now makes Mud Balls next to a pile of pots (Iron Pot; trades Mud Balls for Noise Tape) → **a ladder you drop down = shortcut to Abandoned Houses**.* [V otoki/PowerPyx]
17. Gates → Disordered Fetus on a body → **egg-shaped spiky "urchin" traps** that spike out when you come close (one hit kills them). [V Neoseeker]
18. *The **Cemetery Key gate** (Frank sells the key; item memory: "those idiots want to lock Necros inside with a barred gate?"): right → ladder down through a thorn/spike-trap passage → circle a house (Breath of Life); up the stairs left → a Necro group (Adaptive Fragment) → **running jump across a street to a small arena among the tombs → Lost Blader #2** (Piercing; Corrupted Blader Greatsword, praised as the best early weapon); drop back to the main path.* [V]
19. The central path forks twice (left: Shriek Core; left: Necro flies, Tiny Resonance) → **up the slope; the Cemetery Branch sits in cover on the right** "after the long canyon area", just before the boss plaza. A good place to farm Crystals. [V PowerPyx/Neoseeker]

**E. Boss and exit**
20. **The top of the slope opens onto a plaza: cutscene, then the Panic Reaper** (floats; Piercing on every hit, even through a block; its scream causes Infection; grows a second pair of arms near 50%). Dark sepia dust in the arena. [V; C frame ubZLAZcWTVY_3]
21. **Through the door beyond: a monastery or church building, the Entryway Branch, and Stone hitting a corpse** (Ore Bell). [V Neoseeker] Delpha had pointed here: "you'll have to go to the **monastery in the north. There's an elevator to the city**." [V transcript] → **elevator → Church portal → Sunken City Overground** (Top Apron). [V al-gest]

### 3.3 Shortcuts and loops (Slums)
| Shortcut | Type | Connects |
|---|---|---|
| Double door in the building after the flamethrower fence (step 7) | door opened from the far side | → Temporary Campsite |
| Kick-down ladder under the sniper scaffold (step 8) | ladder you drop | → the same campsite side |
| Elevator loop (steps 11–13) | optional lower layer | → back up through the sewer stub into a building; a jumpable gate by Abandoned Houses |
| Ladder past the Iron Pot NPC (step 16) | ladder you drop | → Abandoned Houses Branch |
| Patriarch arena gate (step 14) | opens after the boss | → onward |
| Cemetery Key gate (step 18) | bought key | → optional cemetery + Lost Blader #2 |
| Wired door in the camp; manhole stub | locked | foreshadow the late-game Ancient Machine Works return |
[V]

### 3.4 Verticality and sightlines
```
HIGH  sniper tower(s) · rooftops (flamethrower robot) · Abandoned Houses Branch on a ladder platform · Entryway elevator up
MID   street slopes, bridges, plank crossings, title-card balcony (Pilgrimage), camp
LOW   Path of Pilgrimage (below the balcony) · campsite basin · canyon dig site via elevator · crystal cave · sewer stub
```
- **"Ranged enemies on the high points at the very start push the player to go up."** [C gcores] The sniper's laser is a moving sightline cue.
- The overall slope is up: camp → rooftops → Abandoned Houses (high) → drop → **uphill** past the tree → cemetery slope → boss plaza → monastery → elevator up → portal. [V route]
- Landmarks seen from many points: the **colossal outer wall** [V PCGamesN], **giant curved rib-like metal arches over sand-filled ruins** [C frames ke8Vh18hynE_1, PnDuel1rJjI_1], the sniper tower, the big dead tree, the monastery.

### 3.5 Enemies
Scavengers: scythe-men, gunmen and rifle snipers, grenadiers/firebomb throwers, explosive-charge shooters, dual-sword men, flamethrower men, **hat-wearing electric mages** (the Patriarch's gate men), a flamethrower robot. Necros: blade-handed Necro (first type) and a faster variant (Infection AoE, stabs), laser flies, a poison butterfly, **urchin/egg spike traps**. Lost Blader #2, Scavenger Patriarch, Panic Reaper. **Faction fights** at the dig site and the tree; the Necros win. [V Neoseeker/namu]

### 3.6 Look and mood (frames `img/sheet_slums1.jpg`, `sheet_slums2.jpg`, `sheet_trans.jpg`)
**Warm sepia and dusty sand**, sun haze, corrugated sheet metal, concrete tenement blocks, metal railings, candles and lanterns inside. Contrast pockets: the **blue crystal cave** (cold blue, dark water) and fire from the flamethrower fences. Later the slums turn darker and dustier around the cemetery and the boss plaza. [C frames]

---
## 4. Transition: Slums → Sunken City (Rooftop Street)
Monastery (Entryway) → elevator → **Church mud-portal** → Rooftop Street: arrive and "head for a portal that takes you to the Rooftop Street area proper". The world is stitched by portals here. [V al-gest/Fextralife]

---
## 5. The other areas (lighter map)

**Sunken City Overground – Rooftop Street.** [V Fextralife Rooftop walkthrough]
- **A vertical descent through flooded high-rises above a lake**: a covered road with hanging bodies, a wrecked bus, an elevator down to Top Apron (merchant Kyen).
- Stairs keep going down through apartment blocks; at the bottom are ladders, **ziplines between building fragments and broken road slices**, and vents and bent roof tiles you drop through.
- Fisherman gangs: poison swordsmen, gunmen, **jet-pack missile men**, spear brutes, **suicide drones**.
- **Gang skirmish set piece**: white-clad fighters zipline in to fight the red gang.
- The Lounge has a hidden side path to an **early portal into Hagios Patir Upper**, guarded by a lethal winged enemy. This is a deliberate early peek at the endgame.
- Ends in a hotel: Hotel Corridor Branch, then down the stairs to the **Three-Faced Pardoner**, then Viewing Balcony (Shirley) and an elevator down.

**Sunken City Overground – Flooded Street.** [V]
- Down an escalator into **waist-deep flooded streets and subway tunnels**. **Abandoned subway cars act as doors and bridges**.
- Swimming Necros, urchin growths, non-respawning "Charcoal-lookalike" beasts and a **six-armed giant Necro** guarding loot, and a red-tinted dead end.
- High Street hub fork: a train to the Withered Forest from Eastern Square, or the main path.
- **Pilgrims vs Necros battles**; a massive Necro lumbering in the distance as a backdrop.
- Hammer pilgrims at the stairs, then Aetherium Mansion, then the **Cleansing Knight**, then the Downward Elevator.

**Twilight Hill – Withered Forest (optional).** [V; C gcores]
- **A poison swamp under a petrified forest**, with plank walkways, trestles and bridges in the trees and **suspended ladders you kick down** as shortcuts.
- Hunter camps around campfires; a bridge that collapses under you.
- gcores: "like DS1 Blighttown plus Bloodborne's Forbidden Woods", with **segmented exploration; after the boss you loop back to the first Branch**.
- A **zipline drops you into the boss arena among thick trees** (Hunter Squad tag-team).
- The Arboretum's outer ring has a spiral ramp; its inner room opens only from Spirit Depths.

**Sunken City Underground – Underground Parish pt1.** [V]
- **Catwalks, pipes and suspended trams over an abyss**, with harpoon-wielders firing from above. You crawl through burst pipes and drop floor to floor, then take an elevator to a zipline.
- Parish Avenue (Millaire): descending ruined church streets with a bus and statues; casters and hammer guards; groups of pilgrims (Ore Bell → Stone).
- Mural Terrace sits at the end of a bridge; the **Saint** is fought on the main street; a portal goes up to the cathedral.
- gcores describes one underground map as "**symmetrical around a control room, an elevator on each side; you start left, finish right**". [C]

**Hagios Patir – Lower Level.** [V PowerPyx]
- Portal in, then an elevator up. Balconies of pilgrims (Shirley and Vikas); stairs crowded with hostile pilgrims.
- **One Branch only, right before the boss** (Cleansing Stairs) → **Choirmaster** → Inspector's Emblem; a pillar lowers stairs to a seal.
- The exit is a **large hole in the floor you jump into** (the cathedral is locked down), dropping you into the sewer.

**Sewer Town – North.** [V Fextralife]
- "An expansion of the initial sewer": a pipe, then **sedimentation silos you drop down in stages**. A Lore-like non-boss enemy, an inactive elevator, a control room with an elevator, and cracked big pipes you drop into.
- **Hunting Ground arena with giant exhaust fans** (gcores compares it to Bloodborne's Astral Clocktower) → **Hunter of Bladers**. **Your first death is scripted: you are abducted to the jail in the Ancient Machine Works.**
- After the fight: self-detonating crawlers, a gate shortcut, a Panic-Reaper-type Necro, and a scared woman by the Underground Rift Branch. A rift leads to Spirit Depths.

**Twilight Hill – Spirit Depths.** [V Fextralife; vgover; gcores]
- **A three-layer hollow cylinder with a floating Watch Tower in the middle.** **Red translucent platforms** serve as drop steps and as bridges.
- Giant rotating **eye structures ("Sauron's eye") spot you and call 5–6 lightning bolts**, so you must stay behind cover. A console inside the tower turns them off.
- **A triangular elevator inside the tower**. A wall of red mist hides an **invisible bridge** to the tower's lower floor. A platform under the elevator leads to a rift to the Arboretum.
- Former bosses (Panic Reaper vs Cleansing Knight) fight each other as a set piece. Persephone waits at the bottom; a rift leads onward.
- Colour: **red-dominant**. gcores likens it to Black Myth's pagoda in shape, with Elden Ring catacomb-style hidden jumps and an invisible path like a mage tower. [C]

**Underground Parish pt2.** [V]
- **The boss is at the start**: the Winged Colossaint on a **wind-swept bridge** where you follow Stone, who shields you with his coffin.
- Hidden drops below Parish Station lead to the **Wanderer of Undersea, a Shadow-of-the-Colossus climb**.
- Below lies the **Living Pond**: a poison pond in a cavern with growths, an elevator to narrow bridges patrolled by Saints, and the Dawnfrost pedestal. Stone's arc ends here. A subway runs onward.

**Sewer Town – Center → Courtyard of the Tree.** [V]
- Train → Central Station (a subway hub of open train cars and a vending machine) → Hidden Platform (train to the Ancient Machine Works).
- **Underground Shaft: a free descent of platform drops down beams with lanterns as waypoints.** There is a butterfly on a midway platform and an optional green-light door midway.
- Pipe → the Gate of the Tree (a giant door, an Asteria cutscene, a Memory) → the Guardians (with Millaire) → jump off the platform toward the **Tree** → Central Garden (Charon).

**Outer-Wall Ruins – Ancient Machine Works (+ Parish pt3).** [V PowerPyx/Neoseeker]
- Train → container yard and warehouse (Factory Bypass).
- **Assembly Hall: a giant laser robot as a room puzzle.** You break 4 power tubes on the upper paths while it fires, and you can turn its laser on big Sewer Cleaners.
- **A long bridge over the abyss** → the prison block and Shirley's Room. A hidden **pipe-drop from the bridge** leads to the Research Center and **Ursula**.
- Then a train → Living Pond → Trial Hall (Eunomia & Dike) → Bishop's Passage portal.
- It **returns the player to the Slums area late in the game**. [C gcores; namu: escaping the jail leads to the Slums]

**Hagios Patir – Upper Level.** [V]
- A white-gold sci-fi cathedral of **floating stairs**, balconies, statues and gold-faced passages; floating loot cubes; **halo/crown enemies that light up the floor**; triangle-faced ambushers set in the walls.
- A **shortcut elevator with a midway floor you reach by jumping off mid-ride** leads to the Mud-Drawing Room, which joins the Rooftop Street early-portal area.
- Then the Seraphim Absolver → a portal to the **Uncharted Realm**, a hub platform with three portal bosses → Path of Epitome (Vikas) → Welkin (Loskid; the point of no return) → The Altar.
- gcores: the last two chapters "have no hakoniwa (compact interconnected level) exploration", and the penultimate map is "a boss rush". [C]

**The Sphere – Elysium.** [V]
- A bright pastel VR paradise: Celestial Tree Garden (fountain, gazebo) → Gate of the Sphere, where Aether is fought (and Charon on the true-ending route).
- Two Branches; a short garden path, not a level.

**DLC – Northern Parish / Furnace.** [V notes]
- Reached through the Sewer Gate at Sewer Town North.
- Roguelite floors, not a hand-built level.

---
## 6. Patterns the game uses across areas
1. **Branch placement**: a Branch is almost always **right before the boss door** (Large Reservoir, Cemetery, Hotel Corridor, Aetherium Mansion, Mural Terrace, Cleansing Stairs, Hunting Ground, Depths' Bottom) and **right after it** (Before Upward Elevator, Entryway, Viewing Balcony, Downward Elevator, Underground Rift, Collapsed Cavern). The 1–2 Branches in between come after a shortcut opens: about **4–6 Branches per area and 3–14 minutes of collect-run time between them**. A Memory or ability orb is often placed next to a Branch. [V PowerPyx branch list; TurboAchiever timelines]
2. **Shortcut kit**: "Must be opened from the other side" double doors; a **green light above a door means a shortcut, a red light means locked/key**; **kick-down ladders**; jumpable gates; elevators (stand on the centre plate; one waiting on another floor is a death drop); breakable crates and planks hiding passages; floor hatches. **Each Branch segment usually has one shortcut that loops back to that segment's Branch.** [V]
3. **Gating**: a NPC permission (the Seal of Pilgrim gatekeeper), a **purchased key** for an optional area (Cemetery Key), a **key from destroying an environmental machine** (Reservoir Key), a **one-way drop into the boss arena** (Lore) or a **cutscene plaza** (Panic Reaper), and gates that open after the boss (Patriarch). [V]
4. **Area stitching**: elevators (Upward Elevator, Downward Elevator), **Church mud-portals** (Entryway → Rooftop; Mural Terrace → Hagios Lower; Bishop's Passage → Upper), **trains with tickets or passes** (Eastern Square → Withered Forest; Living Pond ↔ Central Station ↔ AMW), **rifts** (North → Spirit Depths → Sewer North stub), and **holes you jump into** (Hagios Lower → Sewer North; the Sewer Center shaft). [V]
5. **Set pieces**: an environmental giant machine (the sewer laser mech; the AMW laser robot), a sniper that dominates an open zone and must be climbed to, **faction battles you can exploit** (robot vs Void; Necro vs Scavenger; gang vs gang; pilgrims vs Necros; ex-bosses vs each other), **non-respawning "treasure guardian" monsters**, and **blue crystal caves with a Dew-Essence butterfly** (Slums, Sewer Center shaft, Hagios Upper). [V]
6. **Platforming as secret-gating**: sprint-jumps over gaps, pipe and beam drops, invisible bridges, jumping off a moving elevator. Players praise the secrets and hate the clunky jumping and the "drop-down puzzles". [V; C Reddit 1uh6gdn]
7. **Foreshadowing / backtracking**: loot or doors seen but unreachable (the broken bridge, the Forged Steel Blade door, the camp's wired door, the manhole stub, the Arboretum interior), early peeks at late areas (the Lounge portal), and **late-game routes that re-enter early areas** (AMW → Slums; Sewer North and Center). [V; C FingerGuns]
8. **Vending machines** ("Opossum's") near Branches sell consumables plus one **cosmetic outfit each**. [V]

---
## 7. What players and critics said about the levels
**Praise**
- "Interconnected, secret-filled, shortcut-finding mazes... each level is a compelling maze." [FingerGuns https://fingerguns.net/reviews/2025/03/26/ai-limit-review-ps5-combatgpt/]
- "Areas lead to one another in ways the player wouldn't expect while still making sense." [RPGamer https://rpgamer.com/review/ai-limit-review/]
- "Closest competitor to DS1's map design... looping branches, vertical 3D feel, hidden middle layers." [gcores]
- Reddit: "multiple routes, secrets, verticality, circular design"; "similar to DS3, exploration without being a maze"; fans love the "osha-violation" architecture of buildings hanging over the abyss. [1ve2h7h, 1uh6gdn]
- "Environments larger than life" (GameRant https://gamerant.com/ai-limit-review/); "nailed the feeling of isolation" (GamingBible https://www.gamingbible.com/reviews/ai-limit-review-765648-20250327).

**Criticism**
- **Load-screen stitching** (rifts and metro stations) makes players doubt the places are physically connected. [C gcores; Reddit 1x54pxi]
- **Routes are simple and guessable**; **"ambush from a blind spot every few minutes"** is tiring; spaces are boxy, empty and right-angled, and textures repeat. [IGN China]
- "Umpteenth dingy dull brown tunnel"; long runbacks before the shortcut opens. [TheSixthAxis https://www.thesixthaxis.com/2025/03/26/ai-limit-review/]
- "Nothing but greys and browns." "Linear A→B→C." [Reddit 1ujk5lx/1ve2h7h]
- Clunky jumping; content hidden behind drop-down puzzles. [RPGamer; Reddit 1uh6gdn]
- Late game re-traverses old area types. [FingerGuns]
- The last two chapters lack compact level design. [gcores]
- Producer: "Most of the later levels follow a linear progression, but there will be two or three branching levels." [PCGamesN]

---
## 8. For our builders: replicate vs change
**Replicate (in feel)**
- Sewer: a **narrow → huge reveal** rhythm (tight corridors, then a **fog-swallowed cistern with a giant hostile machine** you cross between sandbag-cover pieces). One hub loop around the second checkpoint with **one shortcut door plus one key door plus one elevator loop back to the start**. A one-way drop into the boss arena. A checkpoint plus a memory right after the boss.
- Exit set piece: **elevator up → manhole → stairs → balcony vista of the wall-city → map pickup → checkpoint below**.
- Slums: a **safe hub with a fire** and the story NPCs, a **gatekeeper who needs a token**, **a sniper with a visible laser** you must climb to (and who stays dead), **rooftops, planks and kick-down ladders**, an **optional elevator into a lower canyon** with a **cold-blue crystal cave** that loops back through a sewer stub, then an **uphill climb where the monsters are winning** (staged faction fights), a key-gated optional graveyard duel, a boss plaza, and a monastery with an elevator out.
- Storytelling: **an overheard voice line on item pickup**, door signs, NPCs who comment on the world, foreshadowed locked doors.

**Change**
- **Seamless transitions**: we have no load screens, so let players see and walk the connections (the top complaint about the original).
- **Fewer cheap ambushes** (at most one per room cluster; telegraph them with sound or particles), and more set dressing in the boxy spaces (the Minecraft palette helps).
- **Keep platforming forgiving**: wide jump gaps, no precision drops on the critical path, and optional drop-puzzles signposted with lanterns (the original's own Underground Shaft trick).
- **Break up the colour**: blue-teal sewer vs warm sepia slums, plus one cold accent zone each, to avoid "grey/brown" fatigue.
- **Original names and designs** throughout (no "Sewer Confluence", Lore, Patriarch, or the Opossum's branding). Mirror only the structure.

---
## 9. Gaps / uncertain
- No fan or official top-down map exists (the in-game map shows only connections), so the vertical layer counts in §1.4/§3.4 are inferred. [?]
- NPC names from auto-captions ("Sienna") need checking in-game. [?]
- Enemy official names were not collected (Fextralife has no Enemies page, 404); descriptions are used instead.
- Absolute size in metres or blocks is unknown. Time is the only scale measure.
