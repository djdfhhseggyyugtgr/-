# ANIMATION research notes — soulslike adventure map (MC Java, mods + RP + DP)
Date of research: 2026-10-13. Raw search/fetch JSON: `research/animation/` (+ YouTube transcripts in `research/youtube/`).
Legend: **[V]** = verified from primary/official source (project page, repo, docs, changelog); **[C]** = community opinion (Reddit/YouTube/X); **[?]** = uncertain / inferred / single source.

---------------------------------------------------------------------------------------------------
## 0. TL;DR / decision drivers

1. **Epic Fight (EF) decides your Minecraft version.** EF's newest release is 21.17.3.1 for **1.21.1 NeoForge only** (dated **31 May 2026**, not Sep 2026), plus 20.14.17 for 1.20.1 Forge (6 May 2026). No Fabric build, no 26.x build. [V] https://www.curseforge.com/minecraft/mc-mods/epic-fight-mod , https://modrinth.com/mod/epic-fight/versions , https://minecrafthub.io/articles/epic-fight-vs-better-combat
   - GitHub shows active branches **`26.2` (updated 13 Oct 2026)** and **`1.21.1-fabric` (30 Aug 2026)** → a 26.x / Fabric port is in progress but unreleased. [V] https://github.com/Epic-Fight/epicfight/branches
   - Planned 26.x architecture change: EF will run vanilla-entity/player animations through **Player Animation Library (PAL) + Bendable Cuboids** (keeps skeletal meshes only for EF-specific entities like WoM bosses). Tested by Yesman on a private 26.1 build. Expected side effects: lose Y/Z-axis bending and body bending; addons will need porting. [V] https://github.com/Antikythera-Studios/epicfight/issues/2460
   - ⇒ If you build now on 1.21.1 NeoForge, expect an API break when you later move to 26.x.
2. **Best soulslike feel today = 1.21.1 NeoForge + Epic Fight ecosystem** (skeletal animation, attack phases, colliders, stamina, dodge i-frames, stun/guard, lock-on, datapack-driven mob AI movesets, hit-stop addon). Better Combat (26.3-ready) is lighter and more compatible but lacks soulslike depth. [V]+[C]
3. **Animated Java (AJ)** is version-agnostic for map-making (1.20.4 → 26.3, pure datapack+RP via display entities) and also works inside modded worlds → great for **bosses with bespoke shapes, set-pieces, cutscene cameras**. [V] https://animated-java.dev/docs/resources/faq
4. **Blockbench 5.2.2** (Oct 2026) is the main authoring tool for GeckoLib/AzureLib/AJ/PAL; **Blender** (2.79→5.0) is required for Epic Fight animations. [V]

---------------------------------------------------------------------------------------------------
## 1. Runtime comparison

### 1.1 Version / loader support table (as of 2026-10-13)

| Library / tool | Latest seen | MC versions & loaders | Maintenance | Source |
|---|---|---|---|---|
| **Epic Fight** | 21.17.3.1 (31 May 2026) | 1.21.1 NeoForge; 20.14.17 for 1.20.1 Forge; older 1.19.2/1.18.2 Forge. No Fabric, no 26.x (branches `26.2`, `1.21.1-fabric` WIP) | Active dev, releases slowed since May | CF page, GitHub branches |
| **GeckoLib** | 5.5.7 (22 Sep 2026) | 26.3 NeoForge/Forge/Fabric; 26.2 = 5.5.6; 26.1.2 = 5.5.2; **1.21.1 NeoForge = 4.9.3 (16 Sep 2026)**; **1.20.1 Forge = 4.8.4 (Jun 2026)** | Very active (Tslat) | https://www.curseforge.com/minecraft/mc-mods/geckolib , https://modpacks.ch/mods/minecraft/388172/geckolib/versions/8893490 , https://mvnrepository.com/artifact/software.bernie.geckolib/geckolib-forge-1.20.1/versions |
| **AzureLib** | 4.0.11 (12 Oct 2026) | 26.3/26.2/26.1.2 NeoForge+Fabric (4.0.x); **1.21.1 NeoForge 3.1.18 (8 Oct 2026)**; **1.20.1 3.1.19 (8 Oct 2026)** | Very active (several builds/week) | https://www.curseforge.com/minecraft/mc-mods/azurelib , https://modpacks.ch/mods/minecraft/817423/azurelib/versions/9095629 |
| **Animated Java** (Blockbench plugin → vanilla DP+RP) | v1.11.0 (9 Oct 2026) | Targets Java 1.20.4 → 26.3 (any loader, or vanilla) | Active (SnaveSutit) | https://github.com/Animated-Java/animated-java/releases , FAQ |
| **Player Animation Library (PAL)** | 1.2.8 (6 Oct 2026; 26.3 = beta, 26.2 = release) | 26.3, 26.2, 26.1.x, 1.21.7–1.21.11, **1.21.1** (older builds 1.0.14 NeoForge / 1.1.1 Fabric); Fabric + NeoForge only (no Forge) | Active; official successor of playerAnimator | https://modrinth.com/mod/player-animation-library/versions , https://docs.zigythebird.com/pal/intro |
| **playerAnimator (KosmX)** | last update 14 Jul 2025 | up to 1.21.7; Fabric/Forge/NeoForge | **Discontinued** → PAL | https://www.curseforge.com/minecraft/mc-mods/playeranimator , https://github.com/KosmX/minecraftPlayerAnimator/issues/174 |
| **Bendable Cuboids** (PAL add-on) | 2.1.0+26.3 (Oct 2026) | 26.x, 1.21.11; client | Active | https://www.curseforge.com/minecraft/mc-mods/bendable-cuboids |
| **bendy-lib (KosmX)** | May 2023 | old Fabric/Forge | **Abandoned** | https://www.curseforge.com/minecraft/mc-mods/bendy-lib |
| **Emotecraft** | 3.5.0-alpha (1 Oct 2026) | 26.x Fabric/NeoForge (+Paper plugin); 1.21.x older | Active | https://www.curseforge.com/minecraft/mc-mods/emotecraft |
| **Better Combat** | 3.2.2 (17 Sep 2026) | 26.3/26.2/26.1.2 Fabric+NeoForge; 1.21.1 NeoForge 2.4.0; 1.20.1 Forge 1.9.0 (Dec 2025) | Active; newer builds depend on **PAL** | https://www.curseforge.com/minecraft/mc-mods/better-combat-by-daedelus , https://github.com/ZsoltMolnarrr/BetterCombat/commit/80335b2de37d66dbcaa29771fce10704059f1830 |
| **Combat Roll** | Sep 2026 | up to 26.3, Fabric/Forge/NeoForge | Active | https://www.curseforge.com/minecraft/mc-mods/combat-roll |
| **EMF / ETF** (OptiFine CEM format) | EMF 3.3.11 (5 Oct 2026) | 26.3…1.20.x; Fabric/Forge/NeoForge | Active | https://www.curseforge.com/minecraft/mc-mods/entity-model-features |
| **Fresh Animations** (RP) | FA 1.10.5 (beta for 26.3) | 26.3 … 1.13 (needs EMF+ETF or OptiFine); Player Extension (Jun 2026) EMF-only | Active | https://modrinth.com/project/50dA9Sha , https://fresh-animations.com/player/ |
| **Veil** (FoundryMC) | 4.5.2 (10 Oct 2026) | **1.21.1 only**, Fabric+NeoForge; 26.1 port requested (issue #131 open) | Active | https://github.com/FoundryMC/Veil/releases , https://github.com/FoundryMC/Veil/issues/131 |
| **Figura** | 0.1.6 (19 Jun 2026) | up to 1.21.4 (Fabric/Forge/NeoForge) | Slower | https://www.curseforge.com/minecraft/mc-mods/figura |
| **Blockbench** | 5.2.2 (8 Oct 2026) | — | Active | https://github.com/JannisX11/blockbench/releases |
| **EF Blender JSON exporter** | tested on Blender 2.79, 2.8, 3.6, 4.1, **5.0** | — | Maintained by EF team | https://github.com/Antikythera-Studios/blender-json-addon |

### 1.2 Feature notes per runtime

**GeckoLib** [V]
- Keyframe animation from Blockbench (GeckoLib plugin), 30+ easings, concurrent animation controllers (one animation per controller, many controllers per animatable), sound / particle / custom-instruction keyframes, Molang math in keyframes, server-triggerable animations, resource-pack overridable assets, entities/blocks/items/armor. https://github.com/bernie-g/geckolib , https://github.com/bernie-g/geckolib/wiki/Triggerable-Animations-(Geckolib4) , https://github.com/bernie-g/geckolib/wiki/Keyframe-Triggers-(Geckolib4)
- 5.x = render-state refactor (since 1.21.5), breaking API vs 4.x; v5.5.7 changelog: fixes reverse animations, easing override, "some animation performance improvements". https://github.com/bernie-g/geckolib/blob/main/changelog.md
- No runtime IK, no mesh skinning; procedural motion = code (bone manipulation). Root motion: visual only (entity movement is AI/code). [?] inferred from docs (no feature listed).
- Requires Java code per entity (renderer/model classes). Data-driven alternatives on 1.21.1: **Vitae** (NeoForge 1.21.1, datapack + optional KubeJS custom animated mobs/bosses) — young project, unvetted. [?] https://modrinth.com/project/UgpbVFch
- Used by: Mowzie's Mobs (partly), countless boss mods. L_Ender's Cataclysm does NOT use GeckoLib — it uses LionfishAPI animation + vanilla `AnimationState` internally. [V] https://deepwiki.com/lender544/new1.20.1/2.1-animation-systems
- Performance: CPU cost per animated bone per frame → keep bone count low (generic advice; 9minecraft wiki is low-quality source [?]). Third-party "GeckoLib Animation Optimizer"/"Geckolib Betterfps" exist (unvetted) [?].

**AzureLib** [V]
- Fork lineage of GeckoLib (AzureDoom), Bedrock-format models; 3.x introduced a new API (`AzEntityAnimator`, `AzCommand` dispatch, procedural animation docs) — different from GeckoLib code. https://moddedmc.wiki/en/project/azurelib/latest/docs/updating/entities , https://moddedmc.wiki/en/project/azurelib/latest/docs/misc/animating/azcommands_101 , https://moddedmc.wiki/uk/project/azurelib/latest/docs/misc/animating/procedural_animation
- Only matters if a mod you install depends on it; no reason to choose over GeckoLib for new work unless you prefer its API.

**Epic Fight** [V]
- True skeletal animation (armature + skinned mesh with weight paint, limb bends) authored in **Blender** with the EF JSON exporter (mesh, armature, animations, **camera** data). https://epicfight-docs.readthedocs.io/Guides/page1/ , https://github.com/Antikythera-Studios/blender-json-addon , fork w/ camera export for Blender 4.1: https://github.com/sentwayfarer/ef-blender-4.1-json-exporter
- In-game **datapack editor** (Mods → Epic Fight → Config): Weapon Types (styles, conditions, combos, innate skills, colliders, living motions, swing/hit sounds & particles), Item Capabilities, Mob Capabilities (mesh, armature, renderer, factions, stun animations, combat AI movesets with weights and conditions), Asset import (drag-drop JSON from Blender). Output = datapack. https://epicfight-docs.readthedocs.io/Guides/Weapons/page2/ , https://epicfight-docs.readthedocs.io/Guides/page3/ , https://epicfight-docs.readthedocs.io/Guides/Entities/page1/
  - YouTube (official, Yesman): "Creating a Weapon Type" iysWR_dSic4 (22k views), "Importing Assets" bslcU82UoK0, "Mob Capabilities" iXsATy1xNNw. Transcript confirms: **4 animation layers (base + lowest/middle/highest composite with joint masks)**; attack animations have **phases (anticipation → pre-delay → contact → recovery → end)**, each phase can strike with a collider bound to a joint; **mob combat AI = weighted movesets with conditions, interceptable chains**. https://www.youtube.com/watch?v=bslcU82UoK0 , https://www.youtube.com/watch?v=iXsATy1xNNw , https://www.youtube.com/watch?v=iysWR_dSic4
- Dodge skills: Roll (4 directions, immune to physical attacks during the move, 4 stamina) / Step. https://epicfight-docs.readthedocs.io/ko/Misc/Gameplay/skills/
- Gamerules useful for a map: `stiffComboAttacks`, `globalStun` (simple stun for unpatched modded mobs), `hasFallAnimation`, `canSwitchCombat`, `keepSkills`… https://epicfight-docs.readthedocs.io/Misc/Gameplay/
- First-person: EF can play dedicated first-person animations (samples: bow, crossbow, falling; special Blender rig provided for custom ones) (Patreon, Apr 2025). Add-on "Epic Fight – First Person Model" renders EF's animated body in 1st person (1.21.1 NeoForge / 1.20.1 Forge, small project, 8.6k DL). https://www.patreon.com/yessman/posts/quality-of-life-126135803 , https://www.curseforge.com/minecraft/mc-mods/epic-fight-first-person-model
- Rendering/perf: EF does GPU skinning; the 2024 "animation shader" (Patreon: ~50 Ender dragons 50–60 fps → 80–100 fps) was replaced by a **compute-shader** path; users on old GPUs/OpenGL ask for the old shader back (issue #2080). EF rewrites shader-pack shaders to animate its models; if parsing fails it falls back to the vanilla pipeline with a chat warning. https://www.patreon.com/yessman/posts/epic-fight-based-109048971 , https://github.com/Epic-Fight/epicfight/issues/2080
- **EF FPS Optimizer** (client addon, 1.21.1 NeoForge / 1.20.1 Forge, Sep 2026): full quality ≤12 blocks, distant pose updates capped to 20 fps, vanilla renderer beyond 32 blocks, protects bosses/crosshair target. Good for ≥50 fps target. https://www.curseforge.com/minecraft/mc-mods/epic-fight-fps-optimizer
- Root motion: EF attack/dash animations displace the entity (dash attacks etc.) — [?] not explicitly documented in sources read.

**Animated Java** [V]
- Blockbench plugin exports a **datapack + resource pack**; each Group (bone) that contains cubes becomes **one `item_display` entity**; groups without cubes ("Structure Groups") are free. FAQ perf tips: fewest bones possible, watch the **E: entity counter**, use Excluded Nodes, disable Auto Update Rig Orientation for static rigs, keep Animation System on Functions, don't animate unseen rigs. https://animated-java.dev/docs/resources/faq , https://animated-java.dev/docs/nodes/groups
- Animation is driven per server tick (20 Hz) by functions; smoothness comes from **display-entity client interpolation** (`interpolation_duration`, `teleport_duration` 0–59 ticks). https://elkonia.com/datapack_codex/display-entities.html
- Locators/Cameras/Interactions are teleported every tick with `teleport_duration` 2; **cameras track pitch/yaw only (no roll)**; Camera nodes require Blockbench's Cameras plugin; use `as_camera` + `spectate`. https://animated-java.dev/docs/nodes/cameras , https://animated-java.dev/docs/nodes/locators
- Tweening between animations; several animations at once if they move different nodes; Variants + (1.11) Texture Slots and texture-slot keyframes (1.21.4+); stacking rigs on locators (e.g., head that looks at player). FAQ + https://animated-java.dev/docs/guides/stacking-rigs
- v1.10 (Jun 2026): removed `data` entity → faster score-indexed storage; Interaction elements; support for 1.21.11 removal of item-model rotation limits; experimental Plugin-mode JSON; updated to Blockbench 5.1.4. v1.11 (Oct 2026): 26.3 support, Texture Slots, custom pivot for item/block/text displays, removed entity display names for perf, faster exports. https://github.com/Animated-Java/animated-java/releases/tag/v1.10.0 , https://github.com/Animated-Java/animated-java/releases
- Server-side consumers of AJ/Blockbench models (Fabric/Paper, Polymer) — relevant only if running a server: blockbench-import-library (tomalbrc), nylon, BetterModel (26.1.1 support). https://github.com/tomalbrc/blockbench-import-library , https://github.com/Provim-Gaming/nylon , https://github.com/toxicity188/bettermodel
- Typical boss architecture [C]: invisible vanilla mob (e.g., zombie) for pathfinding/hitbox + AJ rig teleported to it every tick; damage/health logic in datapack. Reddit r/MinecraftCommands (boss made for a *modded* 1.20.1 server entirely with DP+RP: 104 upvotes) https://www.reddit.com/r/MinecraftCommands/comments/1r0pnrk/ ; explanation comment in post 1t4xqb5.
- [C] "Most YouTube tutorials are outdated; use official docs + Discord" (r/MinecraftCommands 1oec8d2). In Oct 2025 AJ didn't work with Blockbench 5.0 (later fixed by AJ 1.10 → BB 5.1.4). BDEngine vs AJ thread: AJ = more complex, more optimized, steep learning curve. https://www.reddit.com/r/MinecraftCommands/comments/1lvjpsn/

**Player Animation Library (PAL)** [V]
- Plays JSON animations from **Blockbench and Blender** on the player; smooth transitions; priority system for multi-mod conflicts; near-full Molang via "mochafloats"; loads old playerAnimator format; 1.1.1 added particle keyframes for Blender animations and per-axis disabling. https://docs.zigythebird.com/pal/intro , https://www.curseforge.com/minecraft/mc-mods/player-animation-library/files/7281224
- Bendable Cuboids add-on gives MC-Story-Mode-style bent limbs; **known, unfixed conflict with EMF player-animation resource packs** (FA Player Extension). https://github.com/PlayerAnimationLibrary/BendableCuboids/issues/18
- Extension "PAL More Rotation" (26.2 Fabric) adds rotation/bend/sync APIs. https://www.curseforge.com/minecraft/mc-mods/player-animation-library-more-rotation/files/8871905

**Better Combat (+ Combat Roll)** [V]
- JSON weapon attributes (presets, combos, upswing/"feint", OBB+SAT swing collision, dual wield, two-handed). No parry (listed as "under consideration"), weapon trails planned. https://github.com/ZsoltMolnarrr/BetterCombat/blob/26.2/README.md
- [C] r/feedthebeast 2026: "Better Combat is just Skyrim combat"; "EF is great but has to be properly implemented"; "EF too buggy and clunky / BC compatible with everything"; "EF compat is terrible visually but one of the best". Threads 1w8peqb, 1vw49z1, 1vk2awe, 1vn97vb (see §7).

**EMF/ETF + Fresh Animations** [V]
- Resource-pack-only animation for vanilla-model entities (OptiFine CEM `.jem` + expression animations). EMF added `is_player_first_person` etc. https://github.com/Traben-0/Entity_Model_Features/blob/master/CHANGELOG.MD
- Conflicts with EF on mobs EF patches (EF renderer replaces them) → strip those FA files or use "Fresh Animations X Epic Fight Compat" RP (listed up to 1.21.8, last update Jul 2025 [?] check 1.21.1 build). https://www.curseforge.com/minecraft/texture-packs/freshepic-compat , https://github.com/Epic-Fight/epicfight/issues/977 ; Reddit complaints 1mbzpoo / 1mbvshi.
- Single perf report: ETF+EMF(+Punchy) big FPS loss (issue #489, open) [?]. https://github.com/Traben-0/Entity_Texture_Features/issues/489

**Veil (FoundryMC)** [V] — dev library (code), 1.21.1 only: **Necromancer** bone-based animated models (skeleton, keyframed animations, constraints package), Quasar particles (hot reload 4.5.2), post-processing pipeline, custom shaders, **screen-shake module (4.5.0)**. Only useful if you (or a commissioned dev) write a custom mod. https://github.com/FoundryMC/Veil/blob/1.21/README.md , https://foundrymc.github.io/Veil/

**Figura** [V] — client-side Lua-scripted player avatars; up to 1.21.4; not a map-authoring runtime. Fightura bridges Figura + EF on 1.20.1 Forge. https://www.modpackindex.com/mod/105553/fightura

**Other new/minor libs seen (unvetted [?])**: BlockbenchLib (free-form BB models), BlendLib (GLB models+animation from Blender into Fabric, Oct 2026), SimpleBedrockModel (TartaricAcid, Bedrock models in Java), VoxelFX (client display-entity keyframes, 26.1.2), player-animation-core (NeoForge 26.1.2), Mathimations. https://www.curseforge.com/minecraft/mc-mods/blendlib , https://github.com/TartaricAcid/SimpleBedrockModel , https://github.com/StainlessStasis/VoxelFX

---------------------------------------------------------------------------------------------------
## 2. Best combination for soulslike feel

### Recommended stack A (primary): **MC 1.21.1 + NeoForge**
| Need | Pick | Notes / source |
|---|---|---|
| Core combat + player/weapon animation | **Epic Fight 21.17.3.1** | stamina, dodge i-frames, guard/parry skills, stun, lock-on, weapon colliders [V] |
| Weapon movesets content | **Weapons of Miracles 2.0.178** (Sep 2026), **EpicFight-Extra 1.2.2**, **Dawn Day** (≈20 souls-inspired weapons, 18 player + 16 mob death animations), Epic Fight Weapons Compat (500+ weapons incl. Cataclysm) | https://www.curseforge.com/minecraft/mc-mods/weapons-of-miracles-epicfight , https://www.curseforge.com/minecraft/mc-mods/epicfight-extra , https://www.curseforge.com/minecraft/mc-mods/epic-fight-dawn-day , https://www.curseforge.com/minecraft/mc-mods/epic-fight-weapons-compat |
| Hit-stop, screen shake, radial blur | **Epic Fight: Impactful (Unitei fork) for 1.21.1** (original namelesslk build is 1.20.1-only). Per-weapon-category or per-animation JSON (RP for visuals, DP+RP for hit-stop) | https://www.curseforge.com/minecraft/mc-mods/epic-fight-impactful-fork , https://www.curseforge.com/minecraft/mc-mods/epic-fight-impactful |
| Mob/boss AI behaviours via datapack | EF Mob Capabilities editor; **Indestructible fork (Unitei) 1.21.1**; Combat Evolution (executions, mob AI) [? verify 1.21.1 build] | https://www.curseforge.com/minecraft/mc-mods/epic-fight-indestructible-fork , https://www.curseforge.com/minecraft/mc-mods/combat-evolution/files/7765635 |
| Extended datapack hooks | EF – EDP Extended Datapacks 2.4 (1.21.1) | https://www.curseforge.com/minecraft/mc-mods/epic-fight-edp/files/8487777 |
| Compat glue | **Epic Fight Compat Suite** (fixes GeckoLib/AzureLib armor, playerAnimator spell anims, Essential cosmetics, Cataclysm movesets) | https://www.curseforge.com/minecraft/mc-mods/epic-fight-compat-suite |
| Third-person camera / lock-on | Shoulder Surfing Reloaded (EF compat improved Dec 2025 by EF contributor) + **EF x Better Lock On movement/camera fixes** (458k DL) or ssr-camera-fixes | https://github.com/Exopandora/ShoulderSurfing/issues/359 , https://www.curseforge.com/minecraft/mc-mods/epic-fight-x-better-lock-on-better-third-person-qol-fixes , https://github.com/Seramicx/ssr-camera-fixes |
| Camera feel | CameraOverhaul (tilt/smoothing; 26.1+ and older) | https://github.com/Mirsario/Minecraft-CameraOverhaul/releases |
| First-person | EF first-person animations + "Epic Fight – First Person Model" | see §1.2 |
| Performance | **EF FPS Optimizer** | see §1.2 |
| Bespoke bosses | (a) EF-patched custom boss (Blender mesh+armature → mob capability) = best combat integration; (b) GeckoLib 4.9.3 boss in a small custom mod (Blockbench); (c) **Animated Java rig + datapack logic** | see §1.2 |
| Ambient vanilla-mob life | Fresh Animations + EMF/ETF only for mobs EF doesn't patch | conflicts noted |
| Ragdolls (optional) | Ragdollified (1.21.1 + 26.x) | https://www.curseforge.com/minecraft/mc-mods/ragdollified/files/8819960 |

Acclaimed Souls-like content references: Casket of Reveries modpack + "TheCasketOfRrveriesBosses" (EF-patched bosses, 1.20.1, ~1M DL) [V] https://www.modpackindex.com/mod/99875/thecasketofrrveriesbosses ; [C] "casket of reveries is still the best there is" (r/feedthebeast 2026-09-11). Soulrend (1.20.1 Forge, 1.09M DL), Ashen Vow (EF-based, bonfires/corpse run). Showcases: K.Overlegen EF boss videos (e.g., KW0tBPaVp9E "Souls Like Bosses ALL FIGHTS", 13k views) — souls-like boss mods often too easy without tuning [C].

### Stack B (alternative): **MC 26.3 (Fabric or NeoForge)** — Better Combat 3.2.2 + Combat Roll + PAL + GeckoLib 5.5.7 + AJ 1.11 + EMF/FA. Pros: newest vanilla (26.3 `/posteffect` & `minecraft:end_of_frame` post effects for datapack-driven screen FX; Vulkan path), all libs current. Cons: no EF; BC has no parry/stamina/stun; and **26.3 entity interpolation regression MC-311974** ("Confirmed", Mojang priority "Important", still open 10 Oct 2026) makes entity/player movement stutter — X post by @inteledits (459 likes) shows melee feeling "awful". https://mojira.dev/MC-311974 , https://x.com/inteledits/status/2101032339170296194 , https://minecraft.wiki/w/Java_Edition_26.3 , https://syntaxmine.com/articles/compute-posteffect-commands-26-3
Also: Kingdom Come Combat (directional combat, 1.21.1 NeoForge / 1.21.11 Fabric, early test) [V] https://www.curseforge.com/minecraft/mc-mods/kingdomcome-combat

### Design guidance for weight / telegraphs [V for EF mechanics, general craft otherwise]
- Build each boss attack as anticipation (readable silhouette, hold pose) → contact (explicit hit window = EF "contact" phase) → recovery (punish window = EF "recovery" phase). Prefer holding key poses over adding frames; VFX must not hide the tell. https://www.framesprite.com/guides/enemy-attack-telegraph-anticipation-recovery
- Blocky-rig craft [C, Racewizard]: move legs → body → arms (momentum chain), keep planted foot fixed, reduce root rotations to avoid contact jitter, act motions yourself as reference. https://www.youtube.com/watch?v=hQcaWc2lPoY
- Minecraft-native animation style talk (Minecraft Legends, Eric Luhta, Develop 2023). https://www.gameanim.com/2024/09/25/minecraft-legends-building-a-unique-animation-style-true-to-minecraft/

---------------------------------------------------------------------------------------------------
## 3. Authoring workflow

### Blockbench (5.2.2) [V]
- 5.0 (Oct 2025): **Armatures + Weight Brush** (mesh deformation), animation groups, expanded Molang editor, default interpolation setting, quaternion interpolation (generic models), graph-editor keyboard nudging. https://github.com/JannisX11/blockbench/releases/tag/v5.0.0
- 5.1 (Mar 2026): **Mirror Animating** (L/R naming), Copy Animation Pose, named/draggable timeline markers, round keyframes, keyframe-column creation. https://github.com/JannisX11/blockbench/releases/tag/v5.1.0
- 5.2 (Sep 2026): **IK upgrades — IK poles, IK with armatures, better perf**; variable placeholders; particle effects respect hold-on-last-frame. https://github.com/JannisX11/blockbench/releases/tag/v5.2.0
- Bezier keyframes + graph editor exist (keyframe bezier handles API). https://web.blockbench.net/docs/interfaces/custom_keyframe.KeyframeOptions.html
- IK is an **editor-time tool baked into keyframes on export**; Minecraft runtimes don't solve IK. [?] inferred.
- Format matrix: GeckoLib format supports bone rotations, Molang, sound/particle/custom keyframes; armature/mesh skinning is not listed for Java runtimes (Generic format only) → don't rely on BB armatures for GeckoLib/AJ. [V table / ? inference] https://blockbench.net/wiki/blockbench/formats/
- Bug: armature animation FPS drops in editor (closed Aug 2026). https://github.com/JannisX11/blockbench/issues/3701
- [C] Racewizard "(OUTDATED) Why is Animating in Blockbench Like… That?" (25k views): BB animation is FK-on-groups; old IK lacked poles/joint limits; Molang-based transitions are Bedrock-specific. Much of that addressed by 5.0–5.2. https://www.youtube.com/watch?v=XT06xMs0mH0
- MCP/AI-assist: blockbench-mcp-plugin (307★) lets an AI agent drive Blockbench (modeling/animation). https://github.com/jasonjgardner/blockbench-mcp-plugin/

### Blender → Minecraft
- **Epic Fight**: Blender (2.79 → 5.0 tested) + EF JSON exporter → drag-drop into EF in-game editor → datapack. Visual vs normal keyframes matter for constraints (bake constraints as visual keys). https://epicfight-docs.readthedocs.io/Guides/page1/
- **Bedrock-format runtimes (GeckoLib/AzureLib/PAL)**: **mcblend** (Blender 4.5 addon; exports Bedrock geometry + animations, NLA-based; also camera/FOV animation export as JS for Bedrock). https://github.com/Nusiq/mcblend/ , https://mcblend.readthedocs.io/en/latest/animations/exporting_animations/
- PAL loads Blender animations natively (with particle keyframes). [V]
- blender_geckolib_exporter: ChatGPT-written; author warns not to use (Reddit 475 upvotes, Feb 2026). [C] https://www.reddit.com/r/feedthebeast/comments/1qtv0tf/ , https://github.com/yellowcake3d/blender_geckolib_exporter

### Mocap / AI video-to-animation
- Generic pipeline [V tools exist, ? quality on blocky rigs]: Rokoko Video (free AI mocap) or GVHMR-based tools → Blender retarget to EF biped armature / mcblend rig → clean-up (exaggerate anticipation, add holds, remove foot slide) → export. https://www.rokoko.com/insights/tutorial-start-animating-with-our-free-ai-mocap-tool-rokoko-video , https://www.rokoko.com/insights/ace-retargeting-in-blender-with-this-simple-workflow-i-the-ultimate-retargeting-guide , https://github.com/wenshensong/mixamo-llm-mocap (experimental, 2026), https://mocap.plus/ (commercial)
- No dedicated mocap→Minecraft tool found besides "EF Mocap" (records EF player animations in-game and replays on clones; 1.20.1, 269 DL) — not a video mocap tool. https://www.curseforge.com/minecraft/mc-mods/efmocap
- [C] Mocap on 4-cube limbs reads "floaty"; stylised keyframing generally preferred (Polylusion low-poly article: realistic subtle motion looks like "pudding"). https://polylusion.com/blog/low-poly-animation

### Procedural / IK references (only if writing code)
- FABRIK (Aristidou & Lasenby 2011) — simple iterative IK, suits blocky chains. https://andreasaristidou.com/FABRIK
- Procedural spider legs with display entities (YouTube Hc9x1e85L0w); vanilla IK datapack (artefox1). https://www.youtube.com/watch?v=Hc9x1e85L0w , https://github.com/artefox1/vanilla-inverse-kinematics
- AzureLib procedural animation docs; Veil Necromancer constraints.

---------------------------------------------------------------------------------------------------
## 4. Cutscenes / cinematics

| Tool | Type | Versions | Notes |
|---|---|---|---|
| **Animated Java Cameras** | DP (vanilla) | 1.20.4–26.3 | camera keyed in BB alongside boss rig → perfect sync for boss intros; pitch/yaw only, no roll; `spectate`. https://animated-java.dev/docs/nodes/cameras |
| Vanilla display-entity camera | DP | 1.20.2+ | invisible `item_display` + `teleport_duration` (≤59 ticks) + spectator `spectate`; "Smooth Cutscene Cameras with 1 Command" (Cloud Wolf, 37k views). https://www.youtube.com/watch?v=STaEfUoygig |
| 26.3 `/posteffect` + `minecraft:end_of_frame` | vanilla | 26.3 only | per-player post shaders (blur/invert/outline/custom from RP) from functions → stun/vision/dream FX. https://syntaxmine.com/articles/compute-posteffect-commands-26-3 |
| **Director's Camera** | mod | NeoForge **1.21.1** & 26.1.2 | server-driven paths via JSON/KubeJS/in-game camera tool; screen shake, timed sounds, hold-to-skip, keyframes, anchors; new (≈41k DL, Sep 2026). https://www.curseforge.com/minecraft/mc-mods/directors-camera |
| ImmersiveCinematics | mod | Forge (versions unclear) | 6-DOF incl. roll/FOV, Bézier paths, letterbox, subtitles, 23 trigger types — **README says code is AI-agent generated** [?]. https://github.com/SanZiNEO/ImmersiveCinematics |
| CMDCam (CreativeMD) | mod | up to 26.3 Forge/NeoForge | waypoint paths, roll/zoom, follow target, server scenes `/cam-server`. https://www.feed-the-mods.com/cmdcam-mod/ |
| Lumiera, Sandbox Cutscenes, Cutscene API | mods | various | small projects [?]. https://www.curseforge.com/minecraft/mc-mods/lumiera , https://github.com/thewinnt/Cutscene-API |
| Cinemalya | DP library | 26.2–26.3 | spline camera moves, easing, title cards. https://smithed.net/packs/cinemalya |
| Flashback / Replay Mod / BBS | recording/machinima | Flashback (Fabric); BBS Fabric 1.20.1/1.20.4 ("1.7.7 possibly last official update") | trailers only, not in-game cutscenes. https://github.com/Moulberry/Flashback , https://github.com/mchorse/bbs-mod-wiki/wiki/Change-log/ |
| EF Blender exporter camera data | mod pipeline | EF | EF exporter supports camera export (fork) — EF-side cinematic camera use [?]. |

---------------------------------------------------------------------------------------------------
## 5. Known compatibility issues

- **EF vs other renderers (root cause)**: Yesman: "99% of EF incompatibility comes from the independent EF renderers" (vanilla/GeckoLib/AzureLib armors, first person, 3D skin layers, Curios). [V] issue #2460.
- **EF + GeckoLib/AzureLib armor & playerAnimator anims**: GeckoLib armor baked static, AzureLib armor purple-black, Iron's Spellbooks casting anims not playing → **Epic Fight Compat Suite** (client). [V] https://www.curseforge.com/minecraft/mc-mods/epic-fight-compat-suite ; EF PR #1901 (merged Mar 2025) fixed playerAnimator emotes not playing. https://github.com/Epic-Fight/epicfightmod/pull/1901
- **EF + GeckoLib mobs**: EF doesn't animate unpatched modded mobs (they keep their own animations; `globalStun` gives them basic stun). To make a GeckoLib mob fight "EF-style", you must patch it with an EF mesh+armature via datapack (`epicfight_mobpatch`, `epicfight:custom` renderer). [V] docs. [C] "any modded mob that isn't patched for EF really sucks to fight against" (r/feedthebeast 1w8peqb).
- **EF + Iris/Oculus shaders**: generally usable; EF adapts shader-pack programs (fallback to vanilla path if it fails). Open issues: `epicfight:custom` render type textures broken with Complementary/Bliss (#1921, 1.20.1); Bliss translucent armor in battle mode (Bliss #512); deformed textures (#2580, 1.21.1, open). Edited Complementary "Epic Fight Glowing Light Trail" shader for EF trails. [V] https://github.com/Epic-Fight/epicfight/issues/1921 , https://github.com/X0nk/Bliss-Shader/issues/512 , https://github.com/Antikythera-Studios/epicfight/issues/2580 , https://www.mc-mod.net/epic-fight-glowing-light-trail-shader-pack/
- **Iris + Sodium on 1.21.1 NeoForge**: latest builds reportedly don't work together → third-party "Iris-Sodium Compat" (Aug 2026). [V page exists / ? severity] https://www.curseforge.com/minecraft/mc-mods/iris-sodium-compat/files/8585108 ; crash report Iris #3126.
- **GeckoLib + Iris**: 2023 bug (entity shadows froze animations, GeckoLib 4.2.4) fixed; "Iris/Oculus & GeckoLib Compat" mod deprecated (older versions only). [V] https://github.com/bernie-g/geckolib/issues/512 , https://www.curseforge.com/minecraft/mc-mods/geckoanimfix
- **Animated Java / display entities + Iris**: display entities render/light like entities (no block emissive behaviour, Iris #3053, open), text displays can hide entities behind them (Iris #2756). No AJ-specific breakage found. [V] https://github.com/IrisShaders/Iris/issues/3053 , https://github.com/IrisShaders/Iris/issues/2756
- **EF + Fresh Animations**: EF overrides patched vanilla mobs → FA animations lost; compat RP / delete overlapping files. [V]+[C]
- **Bendable Cuboids (PAL) + EMF player packs**: known, no fix. [V]
- **Better Combat + Epic Fight**: not designed together; an auto-switch compat mod exists (1.20.1 Forge). Treat as untested. [V] https://www.modpackindex.com/mod/170142/better-combat-epic-fight-compat , minecrafthub article.
- **Better Combat + First-person Model**: dynamic-mode incompat (open issue). [V] https://github.com/tr7zw/FirstPersonModel/issues/453
- **26.3 entity interpolation stutter** (MC-311974) — affects all entity motion on 26.3. [V]
- Sodium/Embeddium + animation libs: only old reports (GeckoLib #26, 2020; Botania animations w/ Sodium 1.20.1). No current blocker found. [?]

---------------------------------------------------------------------------------------------------
## 6. Performance notes (for ≥50 fps target; PC specs unknown)
- EF: GPU (compute-shader) skinning; heavy with many patched mobs + trails; use EF FPS Optimizer distances; keep arenas' mob counts modest. Compute-shader path needs a modern OpenGL GPU (issue #2080). [V]
- AJ: cost = (#bones-with-cubes entities) × (#rigs) on client + per-tick function cost on the server thread (single-player = same PC). Keep each boss rig small (watch E: counter), pause offscreen rigs, use 1.10+ storage system. [V FAQ] Quantitative benchmarks: none found [?].
- GeckoLib: CPU per bone per frame; 5.5.7 perf improvements; keep bone count low. [V/?]
- EMF/FA: one open report of large FPS loss with ETF/EMF+Punchy. [?]
- Shaders multiply entity cost (shadow pass renders entities again). [general knowledge, ?]

---------------------------------------------------------------------------------------------------
## 7. Community opinion log (Reddit / YouTube / X) [C]
- r/feedthebeast (2026, via Arctic Shift comment search "epic fight better combat"):
  - "Epic Fight is great but has to be properly implemented… If you're not gonna properly integrate EF, making all mobs and weapons compatible, then just stick to vanilla" (score 20, post 1w8peqb).
  - "Better Combat and Epic Fight are good when paired with other mods… fighting Cataclysm bosses with vanilla combat feels equally [underwhelming]" (8, 1w8peqb).
  - "Vanilla combat lacks variety… epic fight is too buggy and clunky, better combat is good enough and compatible with basically everything" (11, 1vw49z1).
  - "EF compat is terrible visual wise, one of the best (with Photon)… Better combat… visual wise kinda shit" (1vk2awe).
  - "EF is too anime/hype… endlag too long" for a grounded pack (1wufyr5).
  - "EF used to be unusable in first person… BC hasn't improved in years" (17, 1v7upb6).
  - "no EF modpacks know how to balance hype moments with everything else" (5, 1wfjq7t).
- r/MinecraftCommands: AJ boss on modded 1.20.1 server (104 upvotes, 1r0pnrk); AJ = "each bone becomes an item display" (1rlz75k); boss = zombie + AJ model teleported each tick (1t4xqb5); AJ docs > outdated YouTube (1oec8d2); BDEngine vs AJ (1lvjpsn).
- r/feedthebeast: Blender→GeckoLib AI exporter (475 upvotes, 1qtv0tf); GeckoLib 4→5 migration confusion (1vma3zr).
- YouTube: Yesman official EF editor series (iysWR_dSic4, bslcU82UoK0, iXsATy1xNNw); Racewizard Blockbench craft (hQcaWc2lPoY, XT06xMs0mH0); Cloud Wolf camera (STaEfUoygig); K.Overlegen EF boss showcases (KW0tBPaVp9E); EF vs BC explainer (cp7qqn2DGVQ).
- X: @inteledits on 26.3 interpolation (https://x.com/inteledits/status/2101032339170296194); @Fresh_LX FA player-extension progress posts (2132 & 2786 likes): https://x.com/Fresh_LX/status/1998329280472752150 , https://x.com/Fresh_LX/status/2002520750511763777

---------------------------------------------------------------------------------------------------
## 8. Open questions / to verify before committing
- Exact 1.21.1 builds of: Combat Evolution, FA×EF compat RP, Better Combat-on-PAL for 1.21.1, ImmersiveCinematics.
- Whether EF 26.x port lands before the map ships (watch `26.2` branch).
- AJ rig + EF interplay: EF player attacks should damage the AJ boss's *hitbox mob* (vanilla/patched entity); confirm EF colliders hit invisible base mob as expected (should, as it's a normal LivingEntity) [?].
- Real fps numbers on the user's PC: test an arena with EF + Iris + 1 AJ/GeckoLib boss + N mobs.
