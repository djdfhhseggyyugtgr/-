# R2 / 3b — Soulslike level design translated to Minecraft (scale, flow, case studies)

Date: 2026-10-13. Researcher: branch 3 part B. Raw fetches: `research/r2/3b/` (S_*.json searches, F_*.json pages), YouTube transcripts in `research/youtube/`.
Tags: **[V]** primary source / official doc / game code / major wiki · **[C]** community, analysis blog, single reviewer · **[?]** my derivation or unverified; must be checked in a metrics zoo (see §6).
Scope reminder: Minecraft Java 1.21.1 + NeoForge, Epic Fight 21.17.3.1, contract `perf-budget.yaml` says render distance 8–12 chunks and `boss_arena: enclosed`.
Not repeated here: what is already in `docs/research/README.md` (tool list, YAWP, Axiom) and `docs/design/sources/notes_ailimit.md` (area list, Branch counts, bosses).

---------------------------------------------------------------------
## 0. Headline findings

1. **[V] The player is the ruler.** Hitbox 0.6×1.8, eye 1.62, step 0.6, jump 1.2522, sprint-jump gap ≈4.2, walk 4.317 b/s, sprint 5.612 b/s, safe fall 3 blocks, lethal fall ≈23.5 at 20 HP, fence collision 1.5. Vanilla third-person camera sits **4 blocks** behind the eye and is pulled in by a block raycast. Epic Fight lock-on range default **20 blocks** (config 5–25) and needs line of sight. → These numbers, not real-world architecture, set corridor, ceiling and arena sizes.
2. **[C/?] A third-person melee camera needs ~30 % more room than a body.** Real 1 m corridors become 3+ blocks; for Epic Fight combat with a 4-block camera, use 5-block-wide combat corridors and 4-block interior air height as the default; 3×3 only for deliberate tension squeezes.
3. **[V] Soulslike level grammar to copy:** critical path + short optional loops that feed back; one-way doors/drops that open shortcuts back to the checkpoint; "teach → test → twist" ambush escalation; enemies as breadcrumbs; landmarks seen long before reached; a Branch near each boss (modern Elden Ring / Lies of P norm) or a short, *meaningful* runback (Dark Souls argument).
4. **[V] Things that failed in recent soulslikes:** Lords of the Fallen launched with too many gank squads/ambushes and had to cut enemy density (up to 30 %) and tighten enemy leashing; its lifts could not be "sent back", which players hated. AI LIMIT was criticised for samey grey corridors and for having no memorable vista. → Our remake should add vistas and keep density moderate.
5. **[V] Minecraft-specific traps:** carpets/trapdoors on top of fences let players jump them; adventure mode still lets players open wooden doors/trapdoors/fence gates and press buttons; `camera_distance` attribute does **not** exist in 1.21.1 (added 1.21.6); in 1.21.1 attributes still use the `generic.` prefix (`generic.safe_fall_distance`, `generic.follow_range`, `generic.step_height`, `generic.scale`, `player.entity_interaction_range`).
6. **[C] Minecraft case studies:** soulslike maps that worked (The Way of Kings, Fool's Errand) are compact, level-based, use fog walls and a bonfire/checkpoint system, and needed post-launch fixes for checkpoint softlocks and telegraphs. VALERIA (NeoForge 1.21.1 + Epic Fight) is open-world and admits mechanics lag behind the world. Big recreations (Stormveil ~400×600 blocks) are "adapted in size for gameplay" and planned with coloured wool blockouts first.

---------------------------------------------------------------------
## 1. Soulslike level-design principles (with sources)

### 1.1 Structure: critical path, loops, shortcuts, one-way doors
- **[V] Dark Souls world = branching + looping maze, "accordion" structure** (linear acts alternate with open acts). Shortcuts are often doors that only open from one side; you see the locked side early and open it later from the other side, so the world gets more connected over time without overwhelming the player at the start. Elevator from Undead Parish back to Firelink is the archetypal "aha". Bonfires get scarcer deeper in. — Mark Brown, *The World Design of Dark Souls* (Boss Keys), transcript https://www.youtube.com/watch?v=QhWdBhc3Wjc
- **[V] Upper Undead Burg = 3 areas, each a critical path plus short optional side paths that loop back.** One-way drops "enforce a one-way flow with no backtracking" and drop you on a landmark (the start stairs). Most of the area is optional on purpose: encourages exploration, supports repeat runs after death (you can skip explored side areas), and enemies act as breadcrumbs. Level Design Book, https://book.leveldesignbook.com/studies/sp/undead-burg
- **[V] Ambush escalation (teach/test/twist):** 1 enemy in a suspicious doorway → 2 hidden ledge enemies → 4 visible-but-hanging enemies that can be pre-empted ("ambushes are fair if you're smart enough"). Same source.
- **[V] Encounter recipe:** melee pair from behind breakables + an archer elevated on a tower (height leashes it) + a late joiner at the back; a long flat walkway lets the player back-pedal and funnel melee enemies out of the archer's line. "A less generous approach would've been a one-way drop without space to back away." Same source.
- **[V] Fog gate as psychological beat:** after 10–20 kills and half the potions used, an empty room behind the fog, then the dragon. Same source. (Useful: fog gates create anticipation even with nothing behind them.)
- **[V] Useful NPCs can sit mid-dungeon near the checkpoint** (Undead Merchant) because respawning there makes them convenient. Same source.
- **[C] Bloodborne:** multiple routes, no markers; distant cathedrals pull you; narrow alleys slow you (anything around the corner); walkways that cross explored areas remind you how far you came. https://mikebarclay.co.uk/bloodborne-to-run/
- **[V] Lords of the Fallen (2023):** permanent vestiges + one player-planted seed vestige at a time; NG+ removing vestiges was reverted to gradual removal after backlash. https://www.pcgamer.com/lords-of-the-fallen-will-tone-down-infamous-gank-squads-and-restore-checkpoints-to-new-game-in-its-second-week-of-patches/
- **[V] LotF one-way commitment:** some routes force you into Umbral one-way until another effigy, to create vulnerability; used "sparingly". https://www.gamedeveloper.com/design/creating-_lords-of-the-fallen-s_-parallel-world-of-umbral

### 1.2 Checkpoint spacing and runbacks
- **[C] Case for "annoying" checkpoints (Dan Felder):** `Checkpoint ——— Boss — Checkpoint` (DS1) forces mastery of the run; `Checkpoint ——— Checkpoint — Boss` lets players barely survive a section once and never master it. But runbacks only add value if the run itself is engaging: "30–60 seconds of engaging gameplay", not mindless walking. https://danfelder.net/2017/12/31/designing-for-mastery-the-case-for-annoying-checkpoints/
- **[V] Elden Ring deliberately shortened runbacks** ("more mindful of this distance between Sites of Grace and Stakes of Marika in each boss fight… to reduce the stress"). https://www.gamesradar.com/elden-ring-bosses-wont-require-a-trek-to-get-back-to/
- **[C] Lies of P:** Stargazer usually "mere steps away" from main bosses; occasional short straight runs with ignorable weak mobs; "the only soulslike that has the elevator waiting for you at your level every respawn". https://steamcommunity.com/app/1627720/discussions/0/806832194048938018/
- **[C] Lords of the Fallen:** many players felt save points were "way too far apart" while trash enemies kept respawning. https://steamcommunity.com/app/1501750/discussions/0/3873718561385105395/
- **[V] DS1 bonfire density falls over the game** (generous early, zero in New Londo, one at the top of Sen's Fortress). Boss Keys transcript above.
- **AI LIMIT reference [V, already in notes_ailimit]:** 60 Branches over ~19 h main path; Sewer Town–SW has 4, Slums 5; boss Branches are named after the boss location (Large Reservoir, Abandoned Houses, Cemetery). PowerPyx walkthroughs https://www.powerpyx.com/ai-limit-sewer-town-southwest-walkthrough/ , https://www.powerpyx.com/ai-limit-outer-wall-ruins-slums-walkthrough/ (Slums: sniper on a tall platform you can reach by ladder and kill permanently; optional elevator down to a sniper platform; ladder shortcut back to the previous Branch after the Necro; key-locked Cemetery gate side path to a Lost Blader.)

### 1.3 Enemy placement, density and leashing
- **[V] LotF post-launch fixes:** improved "leashing" ("further limiting how far enemies will pursue players from their spawn point"), AI less likely to dogpile, fewer enemies "in areas where players most struggle" on the first playthrough but kept in NG+. PC Gamer link above. Density later reduced "by up to 30 percent". Game Developer Umbral link above.
- **[V] Dark Souls designers "mess with you":** snipers, burst-from-wall ambushes, firebomb bridges into crowds, enemies hiding behind corners, rolling traps, tower shooters; the ideal is 1v1 with room to move and the level fights that with thin walkways, archers, traps, narrow corridors. Boss Keys transcript.
- **[V] AI LIMIT is "punishing mostly via falls/ambush level design"** (notes_ailimit §8).

### 1.4 Landmarks, sightlines, vistas, guiding light/colour
- **[V] Dark Souls shows distant areas as cheap LOD models / 2D skybox textures** (Great Hollow is a 2D texture from Firelink; Firelink from Blighttown is a simplified LOD; Duke's Archives shown repeatedly as the ominous destination). This is exactly the role Distant Horizons LOD or a hand-built low-detail silhouette can play. https://illusorywall.tumblr.com/post/132589360859/dark-souls-1-distant-views-explained-part-1
- **[V] Level Design Book, Composition:** hierarchy by contrast (height, density, orientation, shape); a **vista** is a deep view that previews the next area and lets the player plan; an **approach** is a path with a vista; "leading lines" are a myth — use real sightlines (empty space) and landmarks that are *useful*. https://book.leveldesignbook.com/process/blockout/massing/composition
- **[V] Wayfinding aids by reliability** (LDB estimate of % of players who notice): sound 15 %, typology (e.g. "this room looks like an arena") 20 %, composition/sightlines 35 %, **lighting/colour 40 %**, in-world signs 40 %, environmental storytelling 50 %, ground composition 55 %, repetition 60 %, scripted sequence 70 %, **items/breadcrumbs 80 %**, cutscene 90 %, **active threats 93 %**, deep wide barriers 95 %, hard walls 98 %. Players don't look up unless something draws the eye; they look where they move; they notice contrast. https://book.leveldesignbook.com/process/blockout/wayfinding.md
- **[V] Light as guidance (Valve, Left 4 Dead):** too many light sources give no navigation cue; after simplifying, playtesters "instinctively moved towards well-lit areas"; light sources placed at intersections where they wanted players to go; light-coloured fog made enemy silhouettes readable at mid-distance. https://www.l4d.com/blog/post.php?id=2129
- **[C] AI LIMIT review:** "fails to conjure a single exciting or unpredictable vista"; levels feel like Dark Souls covers (fire-raining causeway, firebomb shanty town, poison swamp). https://www.pcgamesn.com/ai-limit/review → our remake's cheapest quality win is landmark + vista design.

### 1.5 Verticality and proportion
- **[V] Dark Souls verticality = strata (going down = history/dread, going up = ascension/heroism).** Boss Keys transcript.
- **[C] DS jumps only cross gaps horizontally; ascent is controlled by stairs/ladders; falls are the main vertical move** (death or treasure). Big-enemy reveals use framing so scale is hidden until close. https://gamemanifesto.net/2012/06/03/little-things-in-a-big-world-terrain-proportion-and-mobility-in-dark-souls/

### 1.6 Pacing
- **[V] LDB pacing tools:** beat sheet, flowchart, intensity graph (Valve L4D/HL2 beat types: explore, combat, choreo, puzzle); teach-test-twist; set pieces need an arena typology and hero props; "pile of beats" — prototype many encounters separately, then arrange. https://book.leveldesignbook.com/process/preproduction/pacing.md
- **[C] Dan Taylor (GDC 2013) ten principles** incl. "fun to navigate", "tells the player what to do, not how", "constantly teaches something new", "surprising", "lets the player control the difficulty", "efficient (modularity, bi-directional gameplay)". https://www.gamedeveloper.com/design/ten-principles-of-good-level-design-part-1- and part 2.

### 1.7 Boss arena design
- **[V] Itay Keren, GDC 2018 "Boss Up":** small open arena encourages confrontation and prevents hiding (Cyberdemon); wide space tailored to the boss; phased layout and lighting as a layout tool; telegraph everything; design attacks around a safe "negative space"; phases for rule changes, not padding. https://media.gdcvault.com/gdc2018/presentations/Keren_Itay_BossUp.pdf
- **[V] How FromSoft implements bosses (DS3 Iudex Gundyr, map + event scripts):** boss entity placed with an AI "think param" (aggro range, give-up distance, navigable area) and NPC param; event scripts gate everything — region triggers, fog wall appears after death, health bar, music, phase change; **event flags**: some persist in the save (boss killed), others reset (phase state); events can be set to **reset when resting at a bonfire**. Two Gundyrs share one map with different params (reuse). https://www.soulsmodding.com/doku.php?id=tutorial%3Aboss-iudex-gundyr → our datapack/KubeJS/mod logic should copy this flag model.
- **[C] Common complaint:** camera gets lost against big bosses near walls/at close range (Elden Ring Fire Giant / Elden Beast threads; No Rest for the Wicked arena rafters). https://steamcommunity.com/app/1245620/discussions/0/6982351509014127458/ , https://forum.norestforthewicked.com/t/walls-of-the-arena-get-in-the-way-of-being-able-to-see-whats-going-on/21426
- **[C] Arena size reference points (Elden Ring, measured in the map editor):** Placidusax playable disc 285 m diameter; Radahn's Wailing Dunes >1 km × 700 m. These are dragon/horse-scale, *not* our model. https://www.youtube.com/watch?v=XWQtJiQ1Sm4 (transcript)

---------------------------------------------------------------------
## 2. Minecraft facts that drive scale (all 1.21.1 unless noted)

| Fact | Value | Tag / source |
|---|---|---|
| Player hitbox | 0.6 w × 1.8 h; sneak 1.5; crawl/swim 0.6 | [V] https://minecraft.wiki/w/Player |
| Eye height | 1.62 (1.27 sneaking) | [V] same |
| Model height | player model 2 blocks × 0.9375 = **1.875 visual** (0.9375 wide); anime heroines built on this rig read ~1.85–1.9 with hair | [V] same |
| Walk / sprint | 4.317 / 5.612 blocks/s | [V] same |
| Max sprint-jump gap | ≈4.225 blocks (wiki player page); >9 only with ice tricks | [V] same; https://minecraft.wiki/w/Jumping |
| Jump height | 1.2522 blocks | [V] https://minecraft.wiki/w/Jumping |
| Step height | 0.6 (`generic.step_height`) | [V] https://minecraft.wiki/w/Attribute |
| Fence/wall collision | 1.5 tall → not jumpable; **carpet/trapdoor/moss carpet on top lets players jump it** | [V] https://minecraft.wiki/w/Fence |
| Fall damage | `max(0, floor((fall − safe_fall_distance) × fall_damage_multiplier))`; default safe 3; 23.5 blocks kills at 20 HP | [V] https://minecraft.wiki/w/Fall_damage |
| Tunable attributes in 1.21.1 | `generic.safe_fall_distance`, `generic.fall_damage_multiplier`, `generic.jump_strength`, `generic.gravity`, `generic.step_height`, `generic.scale`, `generic.follow_range` (default 32), `player.entity_interaction_range` (3), `player.block_interaction_range` | [V] Attribute history (added 1.20.5) |
| `camera_distance` attribute | **not in 1.21.1** (added 1.21.6) | [V] Attribute history |
| Vanilla 3rd-person camera | 4 blocks behind eye; 8 raycasts (±0.1 offsets) pull it closer when blocked | [V] decompiled code in https://mojira.dev/MC-255151 |
| Shoulder Surfing Reloaded defaults | x −0.75, y 0, z 4.0; dynamic offset adjustment in tight spaces | [V] config gist https://gist.github.com/EchoEllet/232f77cdc5c9f6171402ff0e12c4abee |
| Epic Fight camera | own TPS camera API; config `camera.horizontal_location` −5 (−10..10), `vertical_location` 0 (−2..5), `zoom`, `lock_on_range` **20 (5..25)**; lock-on candidates need `canBeSeen` line of sight | [V] EF source on the 1.21.1 default branch (`config/ClientConfig.java`, `api/client/camera/EpicFightCameraAPI.java`, via GitHub code search); exact match to 21.17.3.1 [?] |
| Epic Fight gamerules | `noMobsInBossfight` (default true), `hasFallAnimation`, `stiffComboAttacks` | [V] https://epicfight-docs.readthedocs.io/Misc/Gameplay/ |
| Epic Fight dodge distances | Roll = long dodge, Step = short dash; **no published block distances** | [V/?] https://wiki.9minecraft.net/epic-fight-mod/guides/epic-fight-skills/ — measure |
| Simulation distance | singleplayer default 12 chunks (5–32); entities outside it are not ticked | [V] https://minecraft.wiki/w/Simulation_distance |
| Adventure mode | can't place/break without `can_place_on`/`can_break`; **can** open wooden/copper doors, trapdoors, fence gates, press buttons/levers/plates; explosions still break blocks | [V] https://minecraft.wiki/w/Adventure |
| Interaction entity | detects left/right clicks in an area (1.19.4+) → "touch the fog gate", "rest at Branch", levers | [V] https://datapack.wiki/guide/right-click/interaction |
| Block model limit | elements −16..32 → 3×3×3 block max per model; Potomy's Yharnam had to build big pieces "piece-by-piece, like Lego" | [V] AGENTS.md rule; [C] https://www.gamesradar.com/meet-the-minecraft-modder-rebuilding-bloodborne-block-by-block/ |

### 2.1 Generic level-design metrics translated (1 block ≈ 1 m for a 1.8 m figure)
- **[V] LDB metrics:** minimum hallway ≥ 2× player width "and even then it feels narrow"; Unreal defaults 150 cm hall, 110×220 cm doors; build a **metrics zoo** test map with grid textures; decide camera height early. https://book.leveldesignbook.com/process/blockout/metrics
- **[C] Numivo scale reference:** comfortable corridor 2 m, tight 1.2 m; games widen circulation ~30 % "because a camera needs more room than a body"; third-person corridors want **≥3 m**; doors 2.2–2.4 m so the camera doesn't clip. https://www.numivo.org/tools/scale-reference (2026 tool page; treat as practitioner rule of thumb)
- **[C] MineSpecs Minecraft heights:** 2 = tunnel/claustrophobic, 3 = domestic, 4 = comfortable/grand, 5–6 = public halls, 8+ = monumental; corridor 1 passable / 2 comfortable / 3 reads as a main hall; break flat walls every 5–7 blocks; give big builds a plinth and human-scale objects at the foot; check silhouettes from 150 blocks. https://minespecs.com/blog/scale-and-proportion/ (2026 blog; heights are for walking, not third-person combat)

### 2.2 Derived camera geometry [?] (verify in the metrics zoo)
- Camera height ≈ 1.62 + 4·sin(pitch). At a typical 15–30° downward pitch the camera sits ~2.7–3.6 blocks above the floor → **4 blocks of interior air** keeps it free; 3 blocks pushes it into the player's head during combat.
- Lateral camera swing ≈ 4·sin(angle between view and corridor axis): 30° → 2 blocks each side → a **5-wide** corridor fights without camera pull-in; a 3-wide corridor only works when you look straight down it.
- Lock-on 20 blocks with LOS: an arena radius ≤ ~18 never drops lock from the centre; pillars break lock-on by design (good for casters, bad for duels).
- Wall clearance: a 4-block camera means the player should rarely fight with <4 blocks of open space behind them → keep arena props/pillars ≥5 blocks from the walls and avoid low overhangs over the fighting floor.

---------------------------------------------------------------------
## 3. Case studies (Minecraft)

| Map | Platform / tools | Size / length | What it did well | Lessons / problems | Source |
|---|---|---|---|---|---|
| **VALERIA (Demo)** by zoraL1NK | NeoForge 1.21.1; Epic Fight + Soulslike Universe, L_Ender's Cataclysm, Mowzie's, Epic Knights, Waystones, JourneyMap, Sodium; custom soundtrack + resource pack "valoror" | Open-world; demo = first of 7 regions ("Firone"); "multilayered castles, isolated places, dungeons" | Same stack as ours; strong world-building focus | Author: "I focused more on building an interesting world" — teleport, levelling, quest systems not done; ships whole `.minecraft` (licensing/UX anti-pattern, see research README); switching resource pack mid-session breaks mob animations | [C] https://www.planetminecraft.com/project/valeria-6557226/ |
| **The Way of Kings + Kingsgaol** (Benjelder) | Vanilla 1.19.4, single player | 15 interconnected areas + DLC; ~50 enemy types; 13+3 bosses; **10–12 h + 4 h DLC** | Interconnected "maze-like kingdom"; fog walls; bonfire = level up + spawnpoint; jump-over attacks by checking player Y above a detection plane | v2.1 fixed "a game-breaking bug with fog walls"; a player broke the campfire system by re-pressing the bonfire pressure plate rapidly → **debounce checkpoint triggers** | [C] https://www.planetminecraft.com/project/the-way-of-kings-a-minecraft-souls-like-adventure/ |
| **Fool's Errand: The Curse of Binding** (uz_buz) | Vanilla 1.20.2 datapack, co-op up to 3 | 7 levels, "dozens" of bosses, multiple endings, noteblock OST | Stamina, parry, levelling, upgrades, hub between levels | Update #1 fixed: dying in tutorial sent you to hub early; softlock on early death; multiplayer cutscene bugs; **improved boss telegraphs** | [C] https://www.planetminecraft.com/project/fool-s-errand-the-curse-of-binding-a-soulslike-adventure-map/ |
| **Stormveil Castle recreation** (Iwanfix) | Axiom + WorldEdit; decoration mods (XK's Decoration, Dawn of Time, Create, Derelict) | ≈**400×600 blocks** | Full interiors, same paths as the original | "Adapting its size and terrain for better gameplay"; "plan everything with **colored wool** before actually start to build"; server-only, never released | [C] https://www.planetminecraft.com/project/minecraft-recreation-of-elden-ring-stormveil-castle/ |
| **Bloodborne × Minecraft** (Potomy + team of 9) | Texture/model pack + mods; Patreon-funded | Yharnam, Cathedral Ward, part of Old Yharnam (alpha 0.13) | Like-for-like city; creature models with ~5 → planned 20–30 animations each | 3×3-block model limit forces piece-by-piece kits; recreation of copyrighted world (we must not do this) | [C] https://www.gamesradar.com/meet-the-minecraft-modder-rebuilding-bloodborne-block-by-block/ ; https://www.patreon.com/posts/bloodborne-x-0-7-75284627 |
| **Elden Block v2** (Lerfing) | Patreon map | "1:1 scale" Lands Between incl. Leyndell | Scale showcase, not gameplay | Paywalled recreation | [C] https://www.patreon.com/Lerfing/posts/elden-block-v2-1-122296650 |
| **Across The Time II – Definitive Edition** (Adventquest) | 100 % vanilla, 1.21.11 | **12 km²** hand-built, 43 regions, 40 h main / 100 h full, **440 checkpoints**, **44 panoramas**, 40 auto-travel landmarks, 37 bosses, 777 k command lines, 7,433 command blocks, GPS quest pointer | Scale of a polished vanilla RPG; dedicated vistas ("panoramas") as collectibles | Open-world density (≈0.12 km²/h) is far sparser than a soulslike | [V/C] https://adventquest.com/across-the-time-ii-time-for-regrets |
| **Herobrine's Mansion** (Hypixel, 2012) | Vanilla + MCEdit | 6 boss fights, co-op | Classic acclaimed adventure map | Old advice still valid: hide spawners/redstone, one mission must not be visible from another, make out-of-map impossible, mobs despawn unless persistent | [C] https://www.planetminecraft.com/blog/adventure-map-creating-how-the-pros-do-it/ |

Gap: Noxcrew's design write-up (Adventurer's Dream) returned 404; no first-party Noxcrew/Hypixel level-metric document found.

---------------------------------------------------------------------
## 4. Map-making UX: how to build the soulslike devices in 1.21.1

### 4.1 Fog gates
- Souls model [V]: boss AI disabled until a region trigger; fog wall appears on entry and after death; you "walk through" deliberately; flags decide whether the fog stays after the boss dies (soulsmodding link).
- Implementation options:
  - **Custom block in our NeoForge mod** (translucent animated texture, collision on, opened by a flag) — most robust with shaders. [?]
  - Barrier blocks + particles / block display: cheap; note research README: datapack fog/colour is ignored by Iris+Complementary (#3065) and display-entity emission is weak under Iris (#3053) → don't rely on vanilla fog or display glow for the "wall". [V for the bugs]
  - **Interaction entity** in the doorway to require a deliberate right-click "enter" (souls feel, prevents accidental entry), then teleport 2 blocks through + close behind. [V for the entity; design ?]
- Keep the fog gate **inside the 30–60 s runback** and put the Branch on the near side when the boss is hard.

### 4.2 Invisible walls vs natural boundaries
- [V] LDB: deep wide barriers (pits, rivers, lava) and hard walls are the most trusted "you can't go here" signals; global UI is a fallback.
- Minecraft rules [V]: walls ≥2 blocks of collision height (jump 1.25); fences/walls (1.5) are fine **unless decorated with carpet/trapdoor on top**; gaps ≥5 blocks are unjumpable by sprint-jump (4.2) — **test Epic Fight roll/step and our dash ("Thunder Step"-like) across gaps**; use barrier blocks only above railings/roofs where art can't make a natural edge.
- Void/kill volumes: under-map pits with a datapack/mod kill or "fall → respawn at Branch" handler.

### 4.3 Elevators and lifts
- **Create 6.0.10 (1.21.1 NeoForge) Elevator Pulley** [V]: multi-floor, Elevator Contacts can be powered to call the cabin (call buttons at both ends), floor names, door control, synchronised pulleys. Known open bug: other players' positions render wrong on a moving cabin in MP (#10271). Cost: adds Create + Flywheel; contraptions are entities (shader/Epic Fight interaction untested [?]). https://create.fandom.com/wiki/Elevator_Pulley , https://github.com/Creators-of-Create/Create/issues/10271
- Datapack: fade + teleport "ride" (robust, no physics), or display-entity cabin with `teleport_duration` interpolation (visual only) while the player is moved by commands [?].
- Custom mod lift entity with boat/shulker-style collision [?] — most control.
- Souls UX requirements [V/C]: call lever at both ends; allow "send back" (step on plate, step off) — LotF removed it and was criticised (https://gamerant.com/lords-fallen-fromsoftware-soulslike-trend-elevators-run-back-shortcut-lotf/); Lies of P resets lifts to the player's level on respawn (Steam thread) → **on death/rest, park each lift at the side nearest the last Branch**. Ride ≤10–15 s.

### 4.4 One-way shortcut doors
- Locked side shows a clear message ("Opens from the other side"); interaction entity or iron/custom door on the open side; **persistent flag** (scoreboard/world SavedData), never reset by rest/death. Use **iron or custom doors**, since adventure mode lets players open wooden/copper doors and fence gates. [V for adventure rules]
- Dark Souls pattern: show the locked side early on the critical path so the later opening "clicks". [V Boss Keys]

### 4.5 Checkpoint (Branch) flow and enemy reset
- Copy FromSoft's flag model [V soulsmodding]: three flag classes — **persistent** (boss killed, door opened, item taken, NPC state), **reset-on-rest/death** (trash enemies, lift positions, temporary fogs), **session** (phase state).
- Enemies: `minecraft:marker` (or mod data) per spawn point holding the mob type/equipment; on rest or death, kill tagged trash + mark all markers "alive"; spawn lazily when a player is within ~32–48 blocks so unloaded chunks don't matter; set `PersistenceRequired` so mobs don't despawn; cap chase with `generic.follow_range` 16–24 and a return-home goal (LotF leashing lesson). [?] design, [V] for attribute names.
- Debounce the rest trigger (Way of Kings bug); handle death during tutorial/cutscenes (Fool's Errand softlocks). [C]
- Respawn at last rested Branch via spawnpoint; refill potions; Epic Fight `noMobsInBossfight` default true may suppress spawns near boss fights — check it doesn't stop scripted adds. [V gamerule exists; interaction ?]

### 4.6 Sequence-break prevention checklist
Adventure mode + `mobGriefing false` + YAWP regions; no wooden doors where locks matter; wall/gap metrics above; tune falls with `generic.safe_fall_distance`/`fall_damage_multiplier` instead of building tall walls everywhere; test Epic Fight jump attacks, rolls, our dash, and standing on mobs; keep key items/levers unreachable from the wrong side (interaction range 3). [V for mechanics]

---------------------------------------------------------------------
## 5. Render distance, occlusion and vistas
- Contract: render 8–12 chunks (128–192 blocks) and enclosed boss arenas. [V repo]
- Make each 20–40 min area fit comfortably inside one render radius (≤ ~12 chunks across) and wall it with cliffs/buildings so the next area is hidden until a framed reveal ("one mission must not be visible from another", Hypixel-era advice). [?/C]
- **Distant Horizons** [V]: 3.1.0-b exists for 1.21.1 NeoForge/Fabric (https://www.curseforge.com/minecraft/mc-mods/distant-horizons/files/8263048); works with pre-made worlds; LODs stored in the world save (`saves/<world>/data/DistantHorizons.sqlite`) → can be pre-generated and shipped; with Iris only on Iris 1.7+ and DH-aware shader packs, and the shader takes control of DH fog. https://gitlab.com/distant-horizons-team/distant-horizons/-/wikis/1-user-guide/1-frequently-asked-questions/1-general/General ; https://www.answeroverflow.com/m/1380959985952882791
- Use DH only for a few **vista balconies** (research README already says "전망 지점에만") — the Dark Souls trick is that distant views are cheap LODs anyway (illusorywall). Landmarks for distant views must be **blocks**, not entities (entities don't render at LOD distance). [?]
- Simulation distance 12 by default: anything >12 chunks away is frozen; good for perf, but scripted encounters must start only when chunks are ticking. [V]

---------------------------------------------------------------------
## 6. Recommended block-scale spec (draft for a `level-metrics` contract — propose, don't commit)

Assumptions: heroines at player scale (1.8 hitbox; tall NPCs ≈2.1–2.3 via model or `generic.scale`), Epic Fight third-person combat, 4-block camera, lock-on 20.

| Element | Spec (blocks) | Why |
|---|---|---|
| Interior air height, normal path | **4** (3 only for short tension squeezes ≤8 long) | camera at ~2.7–3.6 during combat pitch [?]; MineSpecs 4 = comfortable [C] |
| Combat rooms / halls | ceiling **6–8** | room for jump attacks, big weapons, camera rise |
| Corridor width: traversal only | **3** | ≥2× player width + camera margin [V LDB/C Numivo] |
| Corridor width: 1v1 combat | **5** | ±30° camera swing without pull-in [?] |
| Corridor/room: 1v2–3 or large weapons | **7–9** | room to circle and funnel (Undead Burg walkway) [V] |
| Main-path doors | **2 w × 3 h** (gates 3–4 w × 4–5 h) | camera and silhouettes pass; 1×2 vanilla doors only for secrets [C] |
| Stairs | stair blocks 1:1, landings every 4–6 rise; 2–3 wide on main path | step 0.6 [V]; LDB landings every 12–16 real steps [V] |
| Unjumpable wall / railing | ≥2 solid, or 1.5 fence/wall **with nothing on top** | jump 1.25, fence 1.5 rule [V] |
| Deliberate jump gap | ≤3 flat (forgiving) | sprint-jump 4.2 max [V] |
| Uncrossable gap | ≥6 (after testing roll/step/dash) | 4.2 + dodge margin [?] |
| Free drop / painful drop / lethal one-way drop | ≤3 / 6–10 / ≥24 (default HP; retune with `generic.safe_fall_distance`) | fall formula [V] |
| Humanoid duel arena (Blader/rival, 1.8–2.5 tall) | Ø **24–32**, ceiling ≥10 or open | radius ≤18 keeps lock-on; boss reach + 2 dodges + 4 camera ≈ 12 radius minimum [?]; "small open arena prevents hiding" [V Keren] |
| Large boss (3–5 tall: Sewer Cleaner robot, Panic Reaper) | Ø **32–40**, ceiling ≥2×boss height+4 (≥12) | camera must frame the boss; big-boss camera complaints [C] |
| Huge boss (≥6 tall) | Ø **40–56**, open sky | still ≤ ~2× lock range for melee [?] |
| Caster / ranged boss (Saint type) | Ø **32–44** + 2–4 LOS pillars ≥5 from walls | pillars break LOS and lock-on by design [V code] |
| Group / gank fight (Hunter Squad) | Ø **36–48** | room to separate targets |
| Branch → boss fog gate | **≤30 s** run (~80–150 blocks), ≤2 skippable mobs; for the school demo put a Branch on the near side of every main boss | Elden Ring/Lies of P norm [V/C]; runback only worth it if engaging [C Felder] |
| Branch spacing on the critical path | every **8–15 min** of first-time play (~120–250 blocks of path); always open a shortcut back to the previous Branch before reaching the next one | AI LIMIT SW 4 / Slums 5 Branches [V]; DS generous-early pattern [V] [?] |
| Encounter density | 1 group per **1.5–3 min** (Undead Burg: 10–20 kills in ~15–30 min); mostly 1–3 enemies; ambushes in teach-test-twist order | [V LDB Undead Burg] [?] |
| Enemy leash | `generic.follow_range` 16–24 + return home | LotF fix [V] |
| Area for 20–40 min | critical path **200–400** blocks; footprint **~128×128 to 192×192**; vertical span 24–64 in 3–5 layers; 10–20 encounters, 1–2 Branches, 2–4 shortcuts, 1 boss, ≥1 vista | triangulated from encounter density, Stormveil ~400×600 for a 2–4 h legacy dungeon, Across The Time II 12 km²/100 h (open world) [?] |
| Visibility | whole area within one 12-chunk radius; next area hidden until a framed reveal; DH only at vista points | contract + perf [V repo] |

Validation plan: build a **metrics zoo** (grid-textured corridors 3/4/5/7 wide, ceilings 3/4/6/8, doors 1×2/2×3, gaps 3–7, drops 3/6/10/24, arenas Ø24/32/40/48 with and without pillars) and record, with Epic Fight + Iris on the target PC: camera pull-in, lock-on drops, roll/step/dash distances, time-per-block of a first-time tester. Replace every [?] with the measured value before writing `level-metrics.yaml` (human-approved contract).

---------------------------------------------------------------------
## 7. Applying it to the milestone areas (Sewer Town–SW, Outer-Wall Ruins–Slums)
- Sewer Town–SW is the tutorial: mostly linear, 4 Branches, first boss before the first Branch, a laser robot tunnel, a key-locked room, a ladder shortcut back to Maintenance Access, then Lore at the Large Reservoir and an upward elevator. [V PowerPyx] → good place for the "teach" beats: 3-wide sewer pipes (tension), 5-wide combat galleries, one 32-Ø reservoir arena, the elevator as the act transition.
- Slums: hub camp, a sniper on a tall reachable platform (kill permanently), optional elevator down, crystal cave side path, ladder shortcut back, key-gated cemetery side path. [V PowerPyx] → layered shanty town with 3–5 vertical layers, the hub Branch visible from several points (landmark), a vista over the outer wall to show later areas (fixes AI LIMIT's "no vista" criticism).
- Keep original names/layouts out: copy structure (loops, shortcut counts, Branch rhythm), not maps. [V AGENTS.md]

## Coverage gaps
- No measured Epic Fight roll/step/lock-on behaviour for 21.17.3.1 specifically (code read from the 1.21.1 dev branch only).
- No first-party Noxcrew/Hypixel design metrics; no measured Souls humanoid arena diameters (only dragon-scale ones).
- Reddit (Arctic Shift) title search returned 422/empty for most single-word queries this session; Reddit coverage is thin.
- Several 2026 blogs (Numivo, MineSpecs, consolepulse, asidehouse) may be AI-written; used only as [C] rules of thumb.
