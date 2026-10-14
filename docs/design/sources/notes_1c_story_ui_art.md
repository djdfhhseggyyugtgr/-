# AI LIMIT — story delivery, NPCs, items/lore, UI, art direction, sound (round 2, branch 1c)

Date: 2026-10-13. Researcher: branch 1 part C.
Tags: **[V]** primary source, official interview, major wiki/guide, or seen directly in game footage frames · **[C]** community/fan/single reviewer, or my reading of a low-res frame · **[?]** uncertain.
Raw files: `research/r2/1c/` (S_*/F_* JSON). Downloaded frames and contact sheets: `research/r2/1c/img/` (Steam store `ss0-4.jpg`, community `u*.jpg`, YouTube auto-frames `y*_maxres*.jpg`, sheets `sheetA..J.jpg`, HUD crops `hudcrop.jpg` and `bossbar.jpg`, music map `bgm1.png` and `bgm2.png`).
Cutscene transcript: `research/youtube/F_https_www_youtube_com_watch_v_xJeiu_kw8_I_*.json` (65k chars, "All Cutscenes" video).
Earlier facts are in `docs/design/sources/notes_ailimit.md`. They are not repeated here.

**Copyright note:** everything below is summary and paraphrase for structural study. Do not reuse any original line, name, or design in our work.

---------------------------------------------------------------------
## 0. Key sources

| Source | Used for |
|---|---|
| All-cutscenes transcript https://www.youtube.com/watch?v=xJeiu-kw8_I (Gamer's Little Playground) | Order and content of every slice dialogue scene [V] |
| namu 스토리/등장인물 (round 1 `namu_main.txt`, `F_..EB_93_B1..e39304.json`) https://namu.moe/w/AI%20LIMIT | Dialogue summaries, NPC events, alternate outcomes [V] |
| PowerPyx Endings & NPC Questlines https://www.powerpyx.com/ai-limit-endings-npc-questlines-guide/ | Step lists per NPC, plus the comments that report missable bugs [V]/[C] |
| PowerPyx Sewer SW and Slums walkthroughs https://www.powerpyx.com/ai-limit-sewer-town-southwest-walkthrough/ , https://www.powerpyx.com/ai-limit-outer-wall-ruins-slums-walkthrough/ | Slice item and NPC placement [V] |
| Fextralife Slums Walkthrough https://ailimit.wiki.fextralife.com/Slums+Walkthrough , item pages (Ore Bell, Seal of Pilgrim, Void/Turbid/Elite Necro's Nucleus, Life Dew, Old Notepad, Shepherd's Tag) | Slice flow, item text format, "Item Memories" [V] |
| Dev diary (May 2024) https://www-ali.gamer.dog/news/html/2024-5/839117.html ; 17173 https://news.17173.com/content/06202024/133621973.shtml ; 3DM https://www.3dmgame.com/original/3744667.html ; BB姬 https://www.163.com/dy/article/J61UHIHP0526FP3N.html ; GamingBolt https://gamingbolt.com/ai-limit-interview-bosses-level-design-art-style-and-more ; GameRant https://gamerant.com/ai-limit-soulslike-game-experience-developer-interview/ (round-1 file) | Art direction straight from the producer, Yang Bin [V] |
| 游研社 hands-on https://news.qq.com/rain/a/20240720A00GOO00 | Cel-shading description [C] |
| IGN China review https://www.ign.com.cn/wu-xian-ji-bing/53484/review/... ; douban review https://www.douban.com/review/16655155/ | HUD, environment criticism, music opinion [C] |
| Rushdown Radio review https://rushdownradio.net/ai-limit-review-accessible-ambitious-and-rough-around-the-edges/ ; Fextralife review (round 1) ; TheSixthAxis https://www.thesixthaxis.com/2025/03/26/ai-limit-review/ | Sound and UI likes and dislikes [C] |
| Moga sponsored beginner video https://www.youtube.com/watch?v=5JBVecZ3fxw (transcript) | Consumables, storage, Nucleus numbers, first-hour feel [C] |
| OST: Vanguard Sound official upload https://www.youtube.com/watch?v=TQgrFZj4P9Y ; Deezer https://www.deezer.com/sv/album/734388451 ; Bangumi (M€I) https://chii.in/person/85790 | Track list and composer per track [V] |
| BGM-replacement mod tables https://ayakamods.com/mods/bgm-replacement-with-nier-automata.308/ (`img/bgm1.png`, `img/bgm2.png`) | The game's internal BGM file name per area and per boss (modder OCR) [C, strong] |
| Bangumi credits https://bangumi.tv/subject/475990 | Art staff [V] |
| Frames: Steam store, Steam community, YouTube auto-frames (Shirrako uPISl8qMZBk, Raizen tv0fynxQXM0, All-About-Boss-Fights lM110855OI0 / zJW0T_ORTlI, SpookyFairy AG4gY1xQiIU, Katsune KMBDtQ-__yU, Optinoob WXDEJSisteQ / vTPNwbbl16k, SEtou59EXQ8, p8dbbyFsd_g) | HUD layout, menus, palettes [V for what is visible; C for interpretation] |

Not usable: ludo.guide "UI overview" and "Branch system" pages are AI-generated filler; their claims ("skill trees", "fast-travel fees") are wrong. Fextralife NPC pages return 404 or empty through the fetch API.

---------------------------------------------------------------------
## 1. Slice story beats: start → end of Outer-Wall Ruins–Slums

The order follows the cutscene video plus the walkthroughs. "Scene type": CUT = non-interactive cutscene; TALK = NPC conversation (camera reframes over the shoulder, subtitles, Confirm to advance); BARK = ambient line when walking past; MEM = "Memory" interactable (glowing echo) that plays a voice fragment and gives an item or ability; ITEM = lore in a description.

### 1A. Sewer Town – Southwest (tutorial, about 1–2 h)

| # | Where | Type | What happens / what the player learns | Gives / flags |
|---|---|---|---|---|
| 1 | — | CUT | Narration over a ruined megacity: after an age of war and calamity, life withered; a black mud crept over the land; survivors fight over food, hide from mud-born monsters, and crowd into the last city. Ends on the great wall with a shanty town outside it. [V transcript, namu §7] | — |
| 2 | Sewer start | CUT | A Blader lies face-down in a pool of black mud, rises, has no memory ("where is this?"). [V] Note: the player avatar is born from the same stuff as the enemies (mud). | — |
| 3 | Corridors | tutorial | Rusty Longsword on a corpse; tutorials for attack, Weapon Skill, backstab, throwables. The **Old Notepad** key item stores every tutorial tip; its description is a worn notebook of combat basics, and its "memory" line is a muttered *must… keep… in mind*. [V Fextralife Old Notepad] | Old Notepad |
| 4 | Gate room | mini-boss | **Sewer Cleaner** (Old-World robot, flashes red, explodes on death) → drops the **Railgun** spell. Teaches the rule "**enemy weapons become your spells**". [V; producer: "scavenging is the core fun; weapons and spells are world objects, many used by enemies first" 17173] | Railgun |
| 5 | Side room | TALK | **Old man** (Asteria's attendant) calls her a newborn Blader, thanks her for fighting the Void, assumes she seeks Branches, and urges her to meet the Branchweaver: "there isn't much time left for her lordship". Foreshadows Asteria fading. [V transcript] | — |
| 6 | Sewer Confluence | TALK + event | **Asteria** greets the "seeker of the Branch"; says this is an ancient drainage tunnel under south Havenswell; asks her to restore a long-damaged Branch → **repair** (kneel in the mud pool, touch the sapling) → **vision** (underwater; something huge glowing in the distance) → Asteria: perhaps a memory stored in the Branch; keep seeking Branches to recover your past; go to the city to understand everything → gives **Life Dew** (refills at Branches) and a **"parting gift": choose 1 of 3 Blader weapons** → final charge: meet humans, find and restore the scattered Branches, the only salvation of this broken world. She then dissolves into mud (only memory recordings afterward). Trophy "Journey Begins = bid farewell to Asteria". [V transcript, PowerPyx, Lorebrarians] | Life Dew ×3, starter weapon, Branch menu unlocked; flag `asteria_farewell` |
| 7 | Near Confluence | BARK | Sewer dwellers: Lord Asteria warned that the Void infests this level; someone scolds a friend wounded by a Void beast; a hostile local tells the new face to keep away; "stay away from the mud". A Mud Ball maker NPC lives further in. [V transcript; PowerPyx] | — |
| 8 | Maintenance Access | MEM | A Memory beside the Branch: a fragment about releasing the force field to counter → **Counter Field** (parry). Learning a move = recovering a memory. [V] | Counter Field |
| 9 | Long tunnel | set piece | A giant laser robot fires down the corridor (sandbag cover; later you topple it via its hand → Reservoir Key) → snail → **Dew Essence**; floating enemy → **Partial Reconstruction** heal spell; **Shield** frame ability lies on a corpse. [V PowerPyx] | Reservoir Key, Dew Essence, Shield |
| 10 | Before reservoir | mini-boss | **Lost Blader #1** (a Blader who lost herself) → Ragged Hood. Foreshadows that Bladers can fall. [V namu §16.2] | Ragged Hood |
| 11 | Near reservoir | TALK/BARK | A fleeing local ("too much for me"). A bitter old man: once her lordship perished, her ungrateful followers fled toward the surface and were all killed by Lore; up there the weak are prey; he would rather die collecting mud. **The world reacts to Asteria's death.** [V transcript] | — |
| 12 | Large Reservoir | BOSS | **Lore, the Lost Lancer**: phase 1 lance (an improvised giant pipe-lance [C frame]); at 50% throws the lance away and rampages like a beast (Necro/Void power released) [V namu]. Its own two-part music (MX_Lore 01/02) [C]. Rewards: **Arboretum Key** (opens a door much later) and **Void Nucleus**. | Void Nucleus, Arboretum Key; trophy "The Lost" |
| 13 | Before Upward Elevator | MEM | Asteria's recorded voice mourns Lore: it could have become a Blader like you, but a desire for destruction built up over years of war consumed it. The Void are beings born from consciousness flowing in the mud that go mad when overwhelmed by emotion. She thanks you for giving it final redemption ("may the Branch guide your path" is her sign-off line). Teaches what the Void is. [V transcript; seal Metastability at this Memory per PowerPyx; pairing of voice ↔ Memory is C] | Metastability seal |
| 14 | Exit ladder | CUT | Climb into harsh sunlight: reveal shot of the Slums against the immense outer wall. A body holds the **City/Ancient Map**; from now on the map fills in at each repaired Branch. [V Fextralife Slums walkthrough] | map |

### 1B. Outer-Wall Ruins – Slums (about 2–3 h; hub = Temporary Campsite)

| # | Where | Type | What happens / learns | Gives / flags |
|---|---|---|---|---|
| 15 | Path of Pilgrimage | combat | Scavengers with rifles; rock-throwers on bridges; snipers on high ground pull the player upward (douban). [C] | Branch |
| 16 | **Temporary Campsite** (hub; small campfire, tents, Branch; **barrier keeps Necros out**; own music `BGM_Scenes_Campsite`) | TALK | **Delpha** (botanist) is calibrating a survey tripod; startled, he calls the player "Ursula?" because of her eyes, then apologises: a head injury has erased much of his memory. He has never seen a living plant (they went extinct before his birth) and has studied soil for 20 years. Light and water are solvable (rainwater evaporates clean); **soil** is the problem: it is laced with mud crystals. He admits he eats a little when starving. Gives **Purified Soil** "in case it has another use". [V transcript, namu] | Purified Soil → *Cultivate Branch* (+1 Life Dew); flag `delpha_met` |
| 17 | Campsite centre | TALK | **Shirley** waves the player over ("big sister!"), gives her **first sermon**: Elysium is a paradise without disease or hunger, made by the Father. Asks the Blader's name → none → horrified, decides it is a trial from the Father → explains why **a name matters** (people can call you, write about you, *remember* you) → names her after her **bunny doll**, the only gift from her grandpa, left at home because she is going to Elysium to find mom and dad and won't return. Elysium is "nowhere and everywhere"; only the chosen get in; pilgrims join the Church and walk to the city centre; monsters block the road ahead → the Blader offers to look → Shirley kneels her down and gives the **Seal of Pilgrim** with a blessing. The Blader notes she has no needle to rewrite seals (sets up the Seal Needle pickup). [V transcript, namu] | **Seal of Pilgrim** (required to pass); flags `named`, `shirley_1` |
| 18 | Campsite shop | TALK | **Frank** (merchant): just finished his apprenticeship and is stuck in this dump; scavengers haggle all afternoon and pocket Mud Balls. Teaches **trade as world-building**: the Crystal Nucleus you wear absorbs crystals; bring it near someone else's Nucleus and, once both agree, crystals transfer. Sells the Cemetery Key; takes a 5% fee vs. the later main merchant. [V transcript, namu] | Cemetery Key (2500) |
| 19 | Campsite | BARK | Pilgrims pray and fear a Necro attack on the camp; a robbed traveller says scavengers don't dare touch the Church, so they rob travellers instead, and vows revenge. [V transcript] | — |
| 20 | Camp exit | TALK | A Church **Shepherd** (Church-employed escort for pilgrims beyond Church territory; cf. Shepherd's Tag item) blocks the road: show the Pilgrim's Seal. [V] | gate opens if `seal_of_pilgrim` |
| 21 | Slums route | combat | Permanent-kill sniper; flamethrower robot → **Flame Jet** spell; Drizzle seal; optional elevator branch: crystal cave with a giant butterfly (Dew Essence) and Sacred Blood Crystal; Scavenger's Clothing. **Golden Seal Needle** lies among pilgrims before the next Branch (now seals can be rewritten). [V Fextralife, PowerPyx] | Seal Needle |
| 22 | Abandoned Houses | CUT + BOSS | Barrels rolled down at you. **Scavenger Patriarch** intro: his men refuse to flee and want to help; he orders them out ("you'd only get in my way; I'll hold it off; run"). **The bandit boss is a protector who sees you as the monster.** Hammer plus shotgun arm. [V transcript; PowerPyx] | Turbid Nucleus, Luminous Diamond |
| 23 | Abandoned Houses | ITEM | **Turbid Nucleus** memory: the Patriarch rehearsing his robbery line ("your money or your life"), unhappy it isn't menacing enough. Humour that humanises a boss. Description: nucleus of outer-wall Void entities, full of impurities from eating garbage. [V Fextralife] | — |
| 24 | By the big dead tree | MEM | Chant of the Tree's guardians: protect the heart of the Tree, repel the Necros, protect the Tree's courtyard → **Hardened Skin** seal. Foreshadows the hidden Courtyard and the Guardians boss. [V transcript; seal location V PowerPyx; speaker C] | Hardened Skin |
| 25 | Side path | NPC/ITEM | An NPC by a pile of pots (pick up the Iron Pot helmet); a shortcut ladder. [V] | Iron Pot |
| 26 | Cemetery Gate (optional) | BARK + mini-boss | Pilgrims beg a Blader (name heard as "Sienna" [?]) to help: their people went into the cemetery and never came back; "she can't hear us anymore" → **Lost Blader #2** (fast, Piercing) → Corrupted Blader Greatsword. Breath of Life seal on a backpack. [V transcript, PowerPyx] | weapon, seal |
| 27 | Slums (location [?]) | MEM | Asteria's recorded message: "since you found this you must be deep in Havenswell"; the Church and the Necros rule the city with superhuman power, but they are not unbeatable for Bladers; don't hold back. [V transcript; placement ?] | — |
| 28 | **Cemetery** | BOSS | **Necro, the Panic Reaper**: Piercing build-up (blocking still builds it), floating scream (Infection), second pair of arms, dash. [V] | **Piercing Claw**, Elite Necro's Nucleus; trophy |
| 29 | — | ITEM | **Elite Necro's Nucleus** memory reads like a machine log: *[executing command 776435…] [coordinates… cleared…] [contacts…]*. Description: contains received commands and fragments of the spells that form its body. **Lore twist delivered through an item: Necros are remote-controlled units.** [V Fextralife; namu §8] | — |
| 30 | Camp (return) | TALK/BARK | Pilgrims: the monsters are gone; was it you? Thanks. **Shirley** is ready to leave and blesses you (she moves to Rooftop Street). **Delpha**: was the soil useful? Bring other soils, he will purify them and give you some (mutual help). Asks what Branches are ("looks like metal but grows like a plant"); the Blader: restoring them may recover her memory → "we're alike, chasing far-fetched goals with broken memories". Then asks a favour: protect the girl; scavengers got rowdy and drew deadly Necros; the camp has a barrier; the way into Havenswell is the monastery to the north with an elevator to the city, where the Necro leader lurks → the Blader: already killed it. (A request you may have *already* fulfilled; the dialogue adapts.) Necros: monsters that appeared with the Church a century ago. [V transcript] | flags `shirley_1_done`, Delpha soil exchange opened |
| 31 | Entryway | TALK | **Stone** (giant old coffin-bearer) is stripping parts off pilgrim corpses ("just vessels; they didn't even fight back"). He recognises a Blader and calls killing hollow vessels his duty, "or rather my fascination"; you'll become one sooner or later, and then he'll take care of you too. A second exchange (**commission**): gives a crude **Ore Bell** signalling device; ring it where pilgrims gather for "weird rituals" and he'll come; easy crystals; don't ask questions. [V transcript, namu, Ore Bell desc] | **Ore Bell**; flag `stone_1` |
| 32 | Entryway | TALK [?] | An NPC (speaker unclear) says: follow the pilgrims into Havenswell to find Branches; beyond the wall lies the **Sunken City**, an Old-World city ruled by the Church where pilgrims are under its protection; hopes the girl stays safe. → **Church mud-portal** into the city. [V transcript; speaker ?] | slice end |

**What the player knows at the end of the slice** [V]: she is a nameless mud-born Blader; Branches hold her memories; Asteria made her and is gone; the Void are mud-consciousness gone mad; Necros appeared with the Church a century ago and follow commands; pilgrims seek Elysium through the Church; humans scrape by on Mud Balls; a botanist wants plants back; a girl gave her a name; a strange coffin-bearer kills "empty" pilgrims. Several **seeds** are planted for much later payoffs: "Ursula" (Delpha), the Arboretum Key (Lore), the Tree's courtyard chant, the bunny doll, "vessels" (Stone), Necro command logs.

### 1C. Delivery techniques visible in the slice (structure to copy, not text)
1. **Naming as the emotional hook**: the protagonist gets her name from the child NPC, and the name is tied to a lost object (the doll) that becomes a late quest item. [V]
2. **NPC dialogue carries the plot**: the main path is NPC talk plus two or three short cutscenes. The producer says the protagonist has no family goal, so the "thread is *making contact with humans and searching for Branches*" (GameRant interview, round-1 file). [V]
3. **Exhaust-dialogue pattern**: talking repeatedly yields new lines until the NPC loops; an important item comes at the end (Shirley's seal, Delpha's soil). Guides always say "exhaust dialogue". [V]
4. **Memories (glowing echoes)**: voice fragments of the dead or of Asteria, each paired with a reward (ability or seal). [V]
5. **Item "memories"**: boss Nuclei carry 2–4 overheard lines from the former owner (humour for the Patriarch, obsession for Lore, a machine log for the Necro). [V Fextralife]
6. **World reacts**: after Asteria's death, followers flee and die; after a boss dies, pilgrims and NPCs change lines and positions. [V]
7. **Request-after-fact** dialogue branches (Delpha's favour vs. "already done"). [V]
8. **Bosses with a human side** (the Patriarch protecting his gang). [V]
9. Notes on corpses scattered through levels ("notes to read", Moga; Rushdown: "scattered notes and brief NPC encounters add texture"). [C]
10. Dialogue choices are rare: Asteria's farewell (you can pick "give up the mission", which loops back citing Shirley and Delpha, namu fn8 [V] — that loop is at the ending, not here); Delpha's late truth-or-lie choice about Ursula; the final accept/decline. [V namu]

---------------------------------------------------------------------
## 2. Item and lore format (for our item JSON / lang files)

Every item tooltip has three layers [V Fextralife item pages, frames]:
1. **Function line** (one sentence, gameplay). E.g. Ore Bell: "Used to call Stone at pilgrim gatherings." Life Dew: "Repairs body damage and restores Life."
2. **Lore paragraph** (1–3 sentences, world fact). E.g. Life Dew = small green crystals condensed from dew that drips from Branches when a Blader is reconstructed. Ore Bell = modified signalling bell commissioned by Stone, crude factory work. Shepherd's Tag = proves identity of Church-employed escorts of pilgrims. Mechanical Part = general-purpose Old-World factory part that merchants like.
3. **Item Memories** (optional; Nuclei and some key items): quoted fragments of the former owner's mind, "read" from the crystal.

Stat items show numbers in the tooltip: Nuclei list Retention Rate / Absorption Rate / Energy Absorption (LOW/MEDIUM/HIGH). Seals show "▶ Max LP +70/+84/…" per level. [V]

Slice nuclei: Void Nucleus (Lore) 65% retention / 80% absorption / LOW; Turbid (Patriarch) 85/70/MED; Elite Necro's (Reaper) 60/90/MED; starter nucleus 75/75 (Moga) [C]. Swapping nuclei costs some carried Crystals (Moga) [C]. Boss nuclei can be traded to Assis for weapons (Lore → Scrap Lance + 5000; Reaper → Reapers + 6000). [V]

Pickup categories visible in the slice: consumables (Mud Ball, Mini Bomb, Portable Ignition/Electrification, Magnetic Surge), upgrade materials (Luminous Carbon/Diamond), sellables (Crystallized Remains, Stone, Mechanical Part, Shepherd's Tag), key items (purple glow on the ground = Soil Samples and key items, PGG), weapons, armour, headwear (in safes and chests), seals, spells, frame abilities. [V]

---------------------------------------------------------------------
## 3. NPC questline structures (for a data-driven quest system)

### 3.1 Common mechanics [V unless noted]
- **Step advance triggers**: (a) exhaust dialogue; (b) **rest at a Branch** (most NPC relocations happen on rest: Shirley moves after rest, Stone appears after ringing the bell *and resting without leaving the area*, Delpha moves after the Arboretum soil); (c) a boss killed (Shirley leaves camp after the Panic Reaper; Millaire moves after the Hunter of Bladers); (d) deliver a key item (soil, seed, doll, flower, Observation Record, Vessel Remains, Nutrition Cube); (e) another NPC's step (cross-dependency); (f) affinity/purchase threshold (Assis calls you "Stranger" until you buy a few items) [C, PowerPyx comments].
- **Location = Branch**: every step is anchored to a named Branch. Guides describe steps as "Branch X > walk Y". Good for us: the quest-marker unit is a checkpoint.
- **Missable gates**: the **point of no return** (taking the Golden Branch from Loskid / Path of Epitome) removes unfinished NPCs (Delpha leaves if the flowers aren't grown; Millaire leaves if the Tree gate isn't opened) [V namu fn5, fn13]. Ordering traps: talking to Sklarm before Vikas reaches Shirley permanently removes Vikas [C, PowerPyx comments]; Shirley stalls at location 3 without some Stone progress [C comment].
- **Alternate outcomes for ignored mercy requests**: if you don't kill crystallised Castina or the defeated Ursula and rest instead, a mutated Necro roams nearby; killing it still gives the reward (Ursula's Necro drops the Lab Key) [V namu fn17, fn20]. Adrammelech: attack him → badge; leave and rest → found dead [V namu fn22].
- **Ally summon steps**: Stone (Winged Colossaint), Feylia (Eunomia), Millaire (Guardians) join one specific boss if their chain is up to date. Feylia must survive for her last step (disputed) [C].
- **NG+ resets questlines**; upgrades are kept but delivery steps must be redone. [V]
- **Map annotation**: after meeting an NPC, the map shows their title ("Soil Researcher Delpha"). [V Fextralife]

### 3.2 Per-NPC step tables (original names, for structure only)

**Shirley (child pilgrim; true-ending key)** [V PowerPyx, namu]
| Step | Branch / place | Precondition | Content | Reward / flag |
|---|---|---|---|---|
| 1 | Slums – Temporary Campsite | — | sermon, naming, seal | Seal of Pilgrim (required) |
| — | moves | Panic Reaper dead + rest | — | — |
| 2 | Rooftop St – Viewing Balcony (beside Branch, after Pardoner) | — | her flying Necro guardian (sent by "grandpa", harmless); wants to see real flowers | flag |
| 3 | Underground Parish – Parish Avenue (hidden hanging train car) | Cleansing Knight dead | saw a pilgrim "become Blessed" and felt his consciousness leave; first link to Stone (if met) | Contemporary Resonance ×2 |
| 4 | Hagios Patir Lower – Cleansing Stairs | Vikas step 3 done | with wounded Vikas; her Necro was killed (by Vikas, if you know him) | — |
| 5 | same | Choirmaster dead + Sklarm step | alone; headache; points toward the Spirit Depths | — |
| 6 | Spirit Depths – Dormant Array | — | talking to the people "in Elysium"; **eyes turn blue → red**; message for Stone if he was sent | — |
| 7 | Spirit Depths – Watch Tower | — | crying: Elysium is a torture trap; will warn others | — |
| 8 | Hagios Patir Upper – Evolving Palace | — | nobody believed her | — |
| key | Ancient Machine Works – Shirley's Room | — | **Bunny Doll** (pickup) | — |
| 9 | Path of Epitome | doll | give doll → she returns it → you throw it into the void | trophy "Farewell to the Past" |
| 10 | same | Delpha flower | give **Nameless Flower** → she promises to build a home with you, hugs you | true-ending flag |

**Delpha (botanist; Life-Dew upgrades; good-ending key)** [V]
1 Campsite: Purified Soil (free) → 2..8 each **soil sample** (1 per main area, purple glow) → Purified Soil (+1 Life Dew; the Withered Forest soil is too contaminated and gives 10 Mud Balls instead [V namu fn4]) → Arboretum soil → **relocates to the Arboretum** (via a Spirit Depths rift) → recovers his memory of his lover Ursula → give **Living Seed** (from Ursula) → choose to tell the truth or lie about Ursula's fate → flowers bloom → **Azure Branch** (trophy "Blooming Life") → rest → **Nameless Flower** for Shirley. Missable: he vanishes if the Golden Branch is taken first.

**Stone (coffin-bearer; ally)** [V]
1 Entryway: talk → Ore Bell. 2–4 (optional, repeatable pattern): at a pilgrim gathering the protagonist comments ("the pilgrims… gathering"; "I should return to the Branch and wait a while") → ring the bell → rest → return → Stone has "dealt with" them → Crystals 3000 / 5000 + 5 Pure Crystal / 6000 → he decides to go to the Spirit Depths. 5 Watch Tower: busy searching for someone. 6 Parish Station: "the ore bell is ringing" popup → he hangs from a beam; drop the chain → **ally vs Winged Colossaint** (walk behind his coffin to block the wind) → 5 Luminous Silica. 7 Living Pond: find the Nutrition Cube → feed the giant flesh blob → it breaks a wall → Stone kills his old friend (the scholar who invented Mud Balls, turned into the Sinner by the Church) after 100 years of drug-extended life, dies asking you to bring down the self-proclaimed gods → 50,000 Crystals; rest → his followers mourn → Hereditary Resonance (trophy "Friends Reunited"). A note left elsewhere says the old coffin-bearer even killed a priest. [V namu]

**Millaire (Blader spell vendor; Courtyard key)** [V]
1 (opt) Flooded Street High Street; 2 (opt) Parish Avenue; 3 (opt) **jail cell** in the Ancient Machine Works after dying to the Hunter of Bladers (helps you escape; if you won the first try, at camp she grumbles that she was tricked) → 4 settles at the Campsite (spell shop: boss Nuclei/Adaptive Fragments + Crystals) → Seal of the Tree from the Memory at the Gate of the Tree → 5 show her → 6 she waits at the gate, opens it, **ally vs Guardians of the Tree** → Courtyard: she interrupts Charon and **breaks her own Branch link** → back at camp; 7 give **Vessel Remains** (from Eunomia) → a seal / Hereditary Resonance for 10 fragments. Says goodbye but never actually leaves. Missable via the point of no return.

**Feylia (small Blader, giant greatsword)** [V]
1 Rooftop Lounge (dozing in a room): scolds the makeshift look, gives the **Standard Seal of Bladers** → 2 Mural Terrace (dozing) → 3 Hagios Patir Lower, right wing (cathedral sealed; meet at the Trial Hall) → 4 Trial Hall: **ally vs Eunomia & Dike** (trophy "Fair Fight") → seal → 5 Welkin: wounded after losing to her master, says the master went to the Church of her own will, dissolves into mud → Sacred Blood Crystal.

**Vikas + Sklarm (human hunter)** [V PowerPyx/namu; ordering C]
1 Rooftop Top Apron → 2 Flooded St Eastern Square: legless, asks for **Mud Balls** (optional; gives status cures ×3) → 3 Withered Forest after the Hunter Squad boss: on new prosthetic legs, "four losing to one is on us" → 4 Cleansing Stairs: arm cut off, lying with Shirley → 5 Sklarm (guild master) asks where Vikas is; if step 4 is done he sends men to fetch him → 6/7 Faultage Corridor: Sklarm's secret Church deals exposed; Vikas throws him off a cliff, wants to be alone → 8 Uncharted Realm: "the Church are all monsters too" → 9 Path of Epitome: lost to the Church's champion, who wasn't human and spared him → challenges you (boss) → you talk him round → trophy "The Battlefield of Humanity".

**Adrammelech + Assis (mad scholar; robot nucleus trader)** [V]
1 Parish Mansion Ground Floor: Adrammelech sends Assis to the Campsite (time-limited: you must talk to Assis after this, before Hagios Patir [C]) → Assis trades boss Nuclei for weapons; with enough purchases he starts claiming he used to be human → **Observation Record** (Research Center) → show him → he realises he was built to *believe* he was human (trophy "A Deadly Joke"). Adrammelech closes a gate on the Sewer North detour; lab reveals Blader/human/Necro experiments and Shirley's origin; after Ursula, in his lab he panics and throws junk (tiny damage) → attack = badge, or he is later found dead. Recorded memories (timestamped transcripts of a secret-society meeting, giving him the codename) carry his backstory. [V namu]

**Kyen (main merchant)** [V]: introduces himself as a caravan merchant; worries about apprentice **Otto**, who went into the city when the Necro invasion began → bring 3 documents (2 covenants + Otto's hand-drawn **Merchant Map** of safe routes) → each expands stock (upgrade materials) and reveals Otto's death (trophy "Expanded Trade Routes").
**Frank** (camp merchant, 5% fee, Cemetery Key). **Church Tribute Priest** vendor speaks single words ("Tribute—", "Grace—", "Live—") [V namu §4]. **Vending machines** (e.g., one selling the Ponytail hairstyle for 1000, the maid outfit) buy at a lower rate than merchants [V/C].
**Castina (Necro researcher Blader)**: Flooded St survivors' stronghold (advice: find what you want to do; 20+ years in Havenswell; Necros named by pilgrims as "spirits of the dead", actually mud bodies run by complex spells; 80 years ago they wiped out the city's east) → Withered Forest entrance → Spirit Depths: crystallised to stop infection, asks to be killed so she revives elsewhere → seal; or a mutated Necro roams. [V namu, transcript]
**Ursula (twice-fought Blader)**: masked Hunter of Bladers (first death = abduction to jail = **death used as a story event**) → hidden boss → asks you to cut her Branch link and kill her → Living Seed + its use; or a Necro roams with the Lab Key. [V]
**Lost Bladers ×6**: fixed hostile Blader duels with your moveset family and their weapon's skill; drop that weapon/hood (trophy "The End of the Lost Ones"). [V]
**Loskid**: beaten, swears an oath, gives the Golden Branch = ending lock. **Charon**: optional conversation in the Courtyard reveals the Tree Project.

### 3.3 Proposed data model (our side; matches `.ai/` ticket style)
```yaml
npc: daisy                     # our Shirley-equivalent
steps:
  - id: daisy_01_naming
    anchor_branch: slums_campsite
    requires: { flags_all: [asteria_farewell] }
    dialogue: daisy_01            # pages; "exhaust" = until loop page
    on_exhaust: { give: [seal_pilgrim], set: [named, daisy_01] }
    relocate_after: { boss_dead: slums_boss, then: rest_at_branch }
  - id: daisy_02_balcony
    anchor_branch: rooftop_balcony
    requires: { flags_all: [daisy_01], boss_dead: [rooftop_boss] }
missable:
  - when: { flags_any: [golden_branch_taken] }
    remove_steps_after: daisy_09
variants:
  - if: { flags_all: [heather_met] }   # cross-NPC line swap
    dialogue_override: daisy_03_knows_heather
```
Rules worth copying: relocate on *rest*, not instantly; every step anchored to a Branch; cross-NPC flags change lines (Shirley knows Stone; Delpha's request is "already done"); one global point-of-no-return flag; ignored mercy requests turn into a roaming mutated enemy holding the reward.

---------------------------------------------------------------------
## 4. UI / HUD

### 4.1 In-combat HUD (from 1280×720 gameplay frames, `img/hudcrop.jpg`, `img/bossbar.jpg`, sheets C/D/E/I) [V visible; C interpretation]
- **Centre-bottom stack** (about 80–88% screen height, centred under the character):
  - **Sync bar** on top: a long thin line with **arrow/needle end caps**, about 1/3 screen wide; fill colour by tier (grey 0 → light blue I → blue II → purple III → red IV); **current % printed above the fill tip** ("31.9%", "100.0%"). IGN China calls it a "wavy energy bar above the white HP bar". [V]
  - **LP bar** below it: shorter, plain white fill on dark.
  - **Status/seal icons** in a row under the LP bar (seal buffs such as Clergies or Standard Seal threshold icons; Fextralife). [V]
  - Piercing build-up appears as a red meter above Sync when hit by Necros; on trigger, red spikes burst from the body and the LP bar border flashes red spikes. [V Fextralife Status Effects]
- **Bottom-left cluster** (thin silver circuit/root-like line art under it):
  - small top slot = **Life Dew** (green crystal icon, charge count);
  - a row of 3 quick-item slots (centre = selected, bigger; left/right = neighbours) with counts;
  - **Crystal icon + total**, with "+450"-style gain numbers stacking above it.
- **Bottom-right cluster** (angular **diamond frames with mud-drip / crack flourishes**):
  - top diamond = **active frame ability** (Counter Field / Shield / Claw / Thunder Step icon);
  - **two weapon icons drawn diagonally** (main in front, the other behind) with a small diamond for the weapon skill/swap;
  - big diamond = **spell slot** (cyan-glowing icon); it greys out when Sync is too low (NoobFeed). Since v1.2 (Mar 2026) there are 3 spell slots plus quick switch (round 1). [V]
- **Boss bar**: top-centre, about 70% of screen width, **very thin white bar** with **thorny crystal-branch end caps**, recent damage shown as a **red chip** that trails, **boss name in a serif font centred above**, damage number at the right end. Two-phase bosses refill or replace the bar (Persephone and Ursula have "two health bars"). [V frames; PowerPyx]
- **Normal enemies**: small thin floating bar over the head with an accumulating damage number. [V]
- **Backstab prompt**: yellow-orange cursor on the enemy. [V Fextralife Combat]
- No minimap; the map is a separate screen (D-pad down) that fills in per repaired Branch and lists met NPCs. [V IGN China, Fextralife]
- Semi-Void hard mode tints the UI with red spike strokes (round 1). Fan mods: No-HUD / No-Effects (Nexus #1), so screenshots without HUD are common. [V]

### 4.2 Pickups, tutorials, dialogue, cutscenes
- **Normal pickup toast**: a small dark horizontal plate right of centre (icon + name + ×count), e.g. "Pure Crystal ×1", stacking briefly. [V frames]
- **Key/unique pickup banner**: large mid-left banner, **colour brush-stroke header** (purple for a Main Seal) with icon and serif name, one lore line below on smoky dark, **category label right-aligned** ("MAIN SEAL"). [V frame `KMBDtQ-__yU_maxres1`]
- **Tutorial panel**: left-side panel with an illustration box, title, 2–3 short paragraphs, and **torn black brush edges** (e.g. "Cultivate Branches"). Tips are stored in the Old Notepad. [V frame]
- **Dialogue**: no dialogue box; the camera frames the speakers; **subtitle bottom-centre, small white serif, no backing**; "Ⓐ CONFIRM" bottom-right. Speaker name labels were not visible in frames [?]. [V]
- **Cutscene skip**: "Esc SKIP" / "OMITIR" small, bottom-right. [V]
- **Menus pause the game** (liked: "games should pause when you pause", Rushdown). [C]

### 4.3 Branch (checkpoint) flow [V Fextralife, PowerPyx, PSNProfiles; menu labels partly C]
1. **Unrepaired Branch** (dark crooked sapling in a mud pool) → interact "Repair" → kneel/touch animation → the cyan crystal lantern on its hooked tip lights → sometimes a **memory vision** → the map updates.
2. **Rest** (sits in the mud pool): LP + Sync + Life Dew restored; quick-slot consumables auto-refilled from **storage** (overflow pickups go to storage; used items are gone even if you die) [C Moga]; enemies respawn.
3. Menu: **Level Up** (Crystals; 5 attributes; derived stats preview) · **Enhance** (weapons +1…+10 with Luminous materials; Main Seals Lv0–5 with Resonance items) · **Teleport** (Branch list grouped by area; available from the 2nd Branch) · **Cultivate Branch** (Purified Soil → +1 max Life Dew; trophies "Branch Growth", "Gardener") · **Rewrite Seal** (needs the Seal Needle) · **Ability Reconstruction** (free respec once the Crystal Sprout item is owned) · **NG+** after clearing · Leave.
4. Death → respawn at the last rested Branch; lose a **% of carried Crystals = 100 − Nucleus Retention**, unrecoverable (no corpse run); bubbling-mud sound as the body re-forms (Rushdown, TheSixthAxis). **Death-screen text: not found [?].**

### 4.4 Menu visual language (Rewrite Seal screen, `img/ym_AG4gY1xQiIU_maxres3.jpg`) [V]
- Dark charcoal gradient background with faint texture; top bar = **title in small caps serif, top-left** ("REWRITE SEAL"), **currency top-right** (crystal icon + number); a hairline **dark-red rule** separates the top and bottom bars.
- **Three columns**: left = stats panel framed by a thin double silver line with corner filigree: PHYSICAL (LP x/y, Sync Rate %, plus a mini Sync tier bar showing the colour bands), PROWESS (Weapon 1, Weapon 2, Spell Power, Stability, Conversion), DEFENSE (Physical, Fire, Electricity, Shatter), RESISTANCE (Poison, Piercing, Infection). Centre = list of slanted tab cards (white line icon + name), the selected card glows white-silver with a diagonal sheen, a red corner tick marks the equipped/new one, slim scrollbar. Right = detail card (big icon, name, short effect text, then a separate lore box).
- Bottom bar: context hint bottom-left ("Replace your Main Seals and Normal Seals."), button prompts bottom-right (D-pad Switch slots · A Confirm · B Return).
- The Level-up screen uses the same stats-panel grouping (Physical/Prowess/Defense/Resistance) per Fextralife "listed on your upgrade menu as such". [V text; layout C]

### 4.5 Likes / dislikes
- Liked: "sleek and interesting UI" (IGN preview) [V]; parry/counter visual feedback (Fextralife review) [V]; menus pause [C]; partial Crystal loss is less stressful [C]; the Sync bar is readable once learned [C].
- Disliked: spell swap required the pause menu (fixed in v1.2 with 3 slots plus quick switch) [V]; sprint and dodge on one key (separate binds added Aug 2025) [V]; no sheathing animation, weapons pop in and out (fixed Aug 2025) [V douban + round 1]; black loading screens between areas make the world feel disconnected [C douban]; poor Korean/JP localisation and text layout [V namu]; camera lock-on fussiness [C]; tiny skill effect at Sync 0 confuses players [C].

---------------------------------------------------------------------
## 5. Art direction

### 5.1 Stated intent (producer Yang Bin) [V]
- **Cel-shaded anime characters + realistic environments**, deliberately combined to find an own style (3DM). Reasons: the team loves *BLAME!* (the 2017 3D-cel film showed cel style can carry a serious story); cel characters appeal to young players; and it was sensible on a small budget (GameRant, 17173, BB姬).
- BLAME! shows only in "**intricate level routes and pipes and cables everywhere**", plus "massive splicing and stacking of wasteland houses and wreckage" (BB姬). Other references: AKIRA, Battle Angel Alita, Borderlands, BioShock, The Last of Us, Fallout, Mad Max, Metro Exodus; **brutalist architecture** for the city: concrete facades and interiors that read "cold and deathly still" (dev diary).
- **"What if plants went extinct?"** is the core visual rule: **no vegetation as set dressing anywhere**; level art had to find other filler (dev diary/3DM). Dead petrified trees, crystals, mud, wreckage, cloth instead of foliage.
- Level layout is **level-based, not seamless**; "scene-changing-as-you-move": alternate surface and underground so a 10 km city feels crossed without noticing (GamingBolt).
- Art credits: art direction 侯一轩 and 张芮; concept art 侯一轩, 张芮, 杨淳一; character modelling 徐文浩; script 时眠 (Bangumi). [V]

### 5.2 Rendering style as seen [V frames + 游研社 C]
- Characters: **hard two-tone shadow blocks** (no soft gradient) on clothing, which gives a manga ink feel; thin dark outline; the shadow shapes flow across the cloth when moving. Skin and hair are flat-shaded with a subtle rim. Environments: PBR-ish realism, desaturated, heavy fog and atmospheric haze, volumetric shafts.
- **One saturated accent per scene**: the protagonist's **crimson crystalline left arm/hand** is the brightest red against grey and sepia; the Branch's **cyan crystal** is the "safe" colour; enemy cores and eyes are **red-orange**. 游研社 notes the red on the hands of both the protagonist and the lost Blader turns sickly against the monochrome. [C]
- Criticism to avoid: "dark grey corridors with minimal background detail" (Fextralife review), "flat, square rooms and slopes, few props, sparse and repetitive surface materials; looks empty; not on the same layer as the fine character design" (IGN China), "repetitive rough materials" (douban). Praised: area styles are coherent (Spirit Depths red-dominant; Church sci-fi floating stairs and statues; Underground Parish ruins with Necros) (douban). [C]

### 5.3 Per-area palette and materials (slice areas in detail)
Hex values are approximate medians from screenshots (`scripts1c/pal.py`); use them for mood only. [V measured; C interpretation]

| Area | Palette | Light | Materials / set dressing |
|---|---|---|---|
| **Sewer Town – SW** | cold blue-black: #0f1015 #191c23 #20252f #2b3544 #414653; highlight #7b859a; **cyan Branch glow** about #5c7f97 → near-white; rust accents #69292a–#a24f52 | dim moonlit blue fill, fog, rare amber/sodium lamps; some rooms flooded in **red caged lamps** (#c0 red) | black reflective mud water; wet concrete; huge riveted pipes and pipe elbows; corroded steel; diamond-plate catwalks with tube railings; grates; sandbags; **yellow hazard stripes** on floors; teal-painted louvred machinery; giant derelict robots (rusty gunmetal, gas-mask or cannon heads, red eyes, red cables) |
| **Outer-Wall Ruins – Slums / Campsite** | sun-bleached sepia and ochre: #f3e3d3 #c9b099 #b5977e #997761 #6d5044 #554039 #2d2120; red-brown rock #775045 #906c5f; shadows warm brown #271c1b | low overcast sun, haze, long hard shadows; dusty bloom; candles and fire barrels as warm points | pale sand ground; red-orange sandstone cliffs; **corrugated-metal and plank shanties**, cloth tents and tarps, tattered banners on poles, stacked concrete pipes, wooden crates, fire barrels, candles on graves; **leaning concrete monolith slabs** as gravestones; the giant outer wall looming |
| Sunken City Overground | grey concrete, overcast sky, lake | daylight haze | brutalist high-rises above a subsidence lake; elevated roads, rooftops, rope bridges, ziplines (dev diary); glass sky-bridges |
| Underground Parish | teal concrete with **graffiti**; church ruins | cold | ruins + Necros; hanging train cars |
| Hagios Patir (Church) | **white + gold**, warm sepia haze (#5a4d44–#a49182); royal blue cloth; deep red mantles | warm god-rays, gold dust motes | huge geometric white halls, gold V/X emblems, floating stairs, giant statues, giant hands |
| Spirit Depths | **red-dominant** | red laser and eye-beam light, neon red shards | server/data-bank architecture, red holographic grids |
| Ancient Machine Works | dark steel + red-lit doors | industrial | factory halls, cranes, lab rooms |
| Elysium | bright pastel garden (round 1) | high-key | — |

### 5.4 Character and faction design language [V frames/interviews; C wording]
- **Protagonist (the dev's own breakdown)**: not human → **cracks in the skin, a deep-crimson chitin left arm, glowing patterns in the pupils**. Hair was changed from long bright pink to **short pale pink ("not white!")**; outfits went from refined tailoring to **wasteland patchwork mix-and-match** (dev diary). Starting look = torn grey hooded half-cape, bandaged legs, heeled boots, rusty sword. Many cosmetic sets (maid, bunny, Blader light armour + visor, Church-white set). Proportions: slim anime teen-to-young-adult; reviewers noted she looks very young [C LootLevelChill]. PCGamesN: outfits "too ornate, lack a 2B-level silhouette" [V]. **Lesson: one strong silhouette beats many ornate sets.**
- **Bladers**: fitted bodysuit/skirt under light plate, visor or headgear, asymmetry, monochrome (white/black/grey) plus the **red Spell-Frame arm** that transforms per ability (claw, shield, field) [V GamingBolt: "it even shows visually with Arrisa's arm activating"]. Lost/corrupted Bladers: same silhouette, twisted posture, red crystal growths.
- **Church**: **white porcelain/ceramic plating with gold filigree trim**, **royal-blue** cloth panels, **deep-red** capes and mantles, halos and sunburst crowns, serene mask faces, multi-armed bishops, lances and censer-staffs, **golden-yellow electricity** (Church = Electricity damage). Knights are centaur-like quadruped frames. Inside: Mud-filled metal frames with crystal cores (round 1).
- **Pilgrims**: cream/beige hooded robes, rags, candles, kneeling groups; the Church seal is "engraved on the pilgrim's clothing by the clerics" (Seal of Pilgrim pickup text). **Shepherds**: Church-employed armed escorts.
- **Scavengers**: "guy in rags" (Rushdown), scrap armour, pot helmets (Iron Pot headwear), rifles and snipers, hammer + shotgun-arm boss, repurposed old robots.
- **Hunters**: humans with **prosthetic limbs** (Vikas).
- **Necros** (dev): "**spikes, blades, tentacles, silver shells, insect-like wings** — symbolising chaos and slaughter"; seen: pale translucent glassy/bony white bodies with **dark-red vein tendrils**, scythe-blade limbs, pink bulbous fleshy heads on some, a spiky red flying familiar. **Purple glow = Shatter damage** (Fextralife Stats). Piercing = red crystal spikes.
- **Void** (mud beasts): black mud bodies with **glowing red-orange magma cracks**, red crystal cores; a red crystal-armoured quadruped (probably Lore phase 2 [?]).
- **Old-World robots**: rusty gunmetal, gas-mask/cannon heads, red eyes, exposed red cables, self-destruct.
- **The Branch**: a thin, black, crooked metal-crystal sapling growing out of a round mud pool, with a hooked top that holds a **floating cyan crystal cluster** like a lantern. [V frames]

### 5.5 Weapon design language [V producer + names; C look]
- **Scavenged first** ("the core fun of a wasteland is picking up junk"): Rusty Longsword, Rusty Pipe, Pickaxe, Road Sign (greatsword), Scrap Lance, Impact Drill, Cast Iron Greatsword; **taken from enemies**: Church Knight's Lance, Holy Embrace claws, Necro Stygian Touch claws and Reapers, Pardoner scythe; **Blader-made**: sleek long black blades with white/red accents (Blader Longsword/Swords/Greatsword), Millaire's staff made from her own Branch.
- Corrupted variants get red crystal growth. Element read by colour: fire orange (#ee815b/#feb77a), electricity gold-white, Shatter purple, poison green.

---------------------------------------------------------------------
## 6. Sound and music

### 6.1 OST facts [V]
- Studio **Vanguard Sound** (Punishing: Gray Raven, Wuthering Waves CBT, Girls' Frontline). They did all sound design and music as a PlayStation China Hero Project partner (behind-the-scenes video 79IasFHDxSQ; no transcript available). Composers **M€I** (synth-heavy electronic/experimental; also led the SFX team, per Bangumi bio), **Haloweak**, **Rabbit J**.
- 27 tracks, 1h16m (Apr 3, 2025): 01 Ruins Overwatch (M€I) · 02 Solitude · 03 Approach of Silence · 04 Survivors of Havenswell (Haloweak) · 05 Disorder · 06 Wasteland (H) · 07 Extinguished Campfire (H) · 08 Scurry of Necros · 09 Dead City (RJ) · 10 Faith Illusion · 11 Pulsation Underwater (RJ) · 12 Chant of the Anointed · 13 Inverted Tomb (RJ) · 14 Salvation (RJ) · 15 Resonance of Rust (H) · 16 Shadow Strike · 17 Lingering Souls · 18 Styx (M€I; the "official" showcase track) · 19 Tragedy Prelude · 20 Fanatical Mutation · 21 Antigravity (H) · 22 Violent Delights (RJ) · 23 Lengthy Decay (RJ) · 24 Above the Sky · 25 Promised Land (RJ) · 26 Gaze From Stars · 27 Calculating Evolution. Unmarked = M€I.

### 6.2 How music is wired in game (internal file names from a BGM-replacement mod table; OCR by the modder) [C, strong]
- **One ambient track per area family**: Title `BGM_MenuStart`; Sewer SW `BGM_Scenes_Sewer`; Sewer North `…WaterWay`; Sewer Centre `…MidWaterWay`; Courtyard of the Tree `…Garden`; **all Outer-Wall Ruins exteriors (Path of Pilgrimage, Abandoned Houses, Cemetery, Entryway) share `…RuinsRes`**; **Temporary Campsite has its own `…Campsite`**; Machine Works `…MachineFactory`; Rooftop St `…SunkenCap`; Flooded St `…WaterStreet`; Underground Parish `…SubSunkenCap`; Hagios Patir `…Churches`; Spirit Depths `…Abyss`; Withered Forest `…Forest`; Elysium `…Pureland`; Credits.
- **Boss music = 4 shared "faction" themes + unique two-phase themes**:
  - `MX_Common_Battle_Human`: Scavenger Patriarch, Hunter Squad, (Guardians?)
  - `MX_Common_Battle_Death` (Necro): Panic Reaper, Wanderer of Undersea
  - `MX_Common_Battle_Church`: Three-Faced Pardoner, Saint, Winged Colossaint…
  - `MX_Common_Battle_Church 2`: Cleansing Knight, Choirmaster, …
  - Unique: **Lore 01/02**, **Hunter of Bladers (Ursula Mask)**, **Ursula 01/02**, **Persephone (Abyss) 01/02**, **Eunomia 01/02**, **Loskid 01/02**, **Charon**.
  - So Fextralife's claim that "all bosses share a single track" is wrong; the shared themes are what players remember. The DLC added character themes (Feylia, Millaire, Eirene, Prometheus, Eunomia simulacrum: fan uploads). [V YouTube titles]
- Mood (from track titles plus reviewers; not listened to) [?/C]: field tracks are "long-note ambient, not silent, never distracting" (douban); "foreboding soundtrack… nailed the isolation" (GamingBible); "couldn't name a single track; ambient and inoffensive" (Rushdown); "ambient so subtle I struggled to recall whether there was any" (Fextralife). Boss tracks "no memorable hook" (douban). Titles suggest choral or liturgical pieces for the Church ("Chant of the Anointed", "Faith Illusion"), a melancholic camp theme ("Extinguished Campfire" or "Survivors of Havenswell"), and synth-driven tension for Necros ("Scurry of Necros", "Fanatical Mutation").

### 6.3 SFX and voice [C unless marked]
- Praised: **weighty hits and a clear metallic "clang" on a successful parry** (Fextralife review [V]); metal-on-metal scrape; **bubbling mud on death and respawn**; **an audible warning cue just before a sniper shot** lets you dodge (Rushdown); Sekiro-like status-ailment sound (douban). Weak: explosions.
- Voice: English + Chinese VO; NPCs with questlines emote well; **the protagonist's monotone is the most criticised element**; her fall-death scream became a meme (namu). Church vendor speaks in single words; Necros "scream" (Infection).
- Interactive warning: the protagonist voices hints ("must be opened from the other side"; "the pilgrims are gathering"; "that energy density is dangerous, take cover!" before Persephone's nuke) (namu). **Diegetic voice hints replace UI markers.** [V]

---------------------------------------------------------------------
## 7. Gaps / uncertain
- Death-screen text and animation (not found in any source) [?].
- Exact Branch menu labels and order (assembled from guides) [C].
- Which Memory plays which Asteria recording in the Slums; the speaker of the "follow the pilgrims to the Sunken City" line [?].
- The "Sienna" name (auto-caption) [?]. Identity of the red crystal quadruped (probably Lore phase 2) [?].
- OST track ↔ in-game file mapping (titles vs. `BGM_Scenes_*`) is not documented [?].
- The behind-the-scenes sound video has no transcript (Chinese speech).

---------------------------------------------------------------------
## 8. For our designers (actionable; original content only)

**Story / NPC**
1. Keep the slice's scene skeleton: wake in mud → attendant points to the creator → creator repairs the first checkpoint with you, gives healing + a 1-of-3 weapon, then dissolves → a world-reaction bark (her followers fled and died) → the first boss → creator's recorded voice explains what the boss was → surface reveal of the wall → hub camp: the botanist (soil plus a memory seed), the child names the heroine and gives the pass, the merchant explains trade in-world, the escort gate → a sympathetic bandit boss → a necro boss whose core reads like a command log → the hub reacts, the child leaves → the coffin-bearer's commission → a portal into the city.
2. Model quests as Branch-anchored steps with triggers {exhaust dialogue, rest, boss dead, item delivered, other-NPC flag, purchase count}; relocate NPCs on rest; one global point-of-no-return flag; ignored mercy → a roaming mutated enemy holds the reward.
3. Every boss core gets 2–4 "echo" lines (one funny, one sad, one cryptic). Every item gets a function line + a lore line.
4. Use **diegetic voice hints** (the heroine comments at pilgrim gatherings or locked doors) instead of quest markers; the map lists met NPCs.
5. Our Daisy (child) gets an age-appropriate design. Give the protagonist a clearly young-adult read to avoid the "looks 13" criticism.

**UI (custom HUD in our mod)**
6. HUD: centre-bottom thin Sync line with arrow caps + % text, tier colours (grey → light blue → blue → purple → red), white LP bar below, status icons below that; bottom-left = healing flask count + 3 quick items + currency with +gain popups; bottom-right = diamond icons for frame ability / two weapons / spell. Boss bar = thin top-centre line with ornate caps, serif name, red trailing chip.
7. Pickups: a small toast for normal items; a big colour-banner for key items and seals. Tutorials go to a "notebook" item. Subtitles bottom-centre, no box; "skip" bottom-right. Menus pause the game.
8. Checkpoint menu: Level Up / Enhance / Teleport / Cultivate / Rewrite Seal / Respec / (NG+) / Leave; stats panel grouped Physical · Prowess · Defense · Resistance; three-column menus.
9. Avoid their dislikes: spell switching without a menu, separate sprint/dodge keys, sheathe animations, and no long black loading screens (Minecraft teleport → use a fade + vista).

**Art (Minecraft translation)**
10. Rule "no plants": fill detail with pipes, cables, crystals, wreckage, cloth, candles, mud. Brutalist concrete + corrugated shanties.
11. Characters: bake hard two-tone shadow blocks + thin dark outline into the 32 px textures; environments keep more material noise (realistic vs. cel contrast).
12. Palettes: Sewer = cold blue-black + cyan checkpoint + rust red; Slums = bleached sepia/ochre + red sandstone + warm candle points; one saturated accent per scene (heroine's crimson arm; cyan checkpoint; red-orange enemy cores).
13. Faction language: Church = white porcelain + gold trim + royal blue + deep-red mantles, halos, gold lightning; Necro = silver shells/spikes/blades/tentacles/insect wings, pale glassy bodies with dark-red veins, purple glow = their element; Void = black mud + magma-orange cracks; scavengers = rags + scrap + pot helmets; pilgrims = cream hooded robes. Weapons: scavenged junk → enemy parts → elegant Blader blades.
14. Checkpoint = crooked dark sapling in a mud pool with a floating cyan crystal lantern (design ours, but keep the "crystal lantern on a crook" readability).

**Sound**
15. Music plan: one ambient loop per area + a separate hub theme; boss music = 3–4 shared faction themes + unique 2-phase themes for story bosses (our slice: the Lore-equivalent gets a unique theme; the Patriarch- and Reaper-equivalents use the faction themes). Make field music long-note ambient; give boss themes a hook (their main criticism).
16. SFX priorities: a distinct metallic parry clang, a hit thud, a pre-shot sniper warning cue, mud bubbling on death and respawn, a distinct status-ailment sting.
