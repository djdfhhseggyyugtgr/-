# Soulslike adventure map: gameplay mods, map-making tools, version and loader choice

Research date: 2026-10-13. Searches went through the Ollama web_search/web_fetch helper (`tools/osearch.py`). Reddit (Arctic Shift) and YouTube (search plus transcripts) went through `tools/social.py`. Raw JSON and text are in `research/gameplay/` and `research/gameplay/social/`.

Labels used below:
- **[V]** verified on a primary page: CurseForge, Modrinth, GitHub or official documentation.
- **[C]** community opinion: Reddit, YouTube or modpack descriptions.
- **[?]** uncertain or inferred.

---

## 0. Headline findings

1. **[V] There is no released Epic Fight build for 26.x.** The newest releases are `21.17.3.1-mc1.21.1-neoforge` and `20.14.17-mc1.20.1-forge`, both dated May 2026 on CurseForge (https://www.curseforge.com/minecraft/mc-mods/epic-fight-mod/files).
   - A **`26.2` branch** is active. Its last commit was on 2026-10-13, and its CHANGELOG reads "26.2.0 – Unreleased: Rebuilt on the Akythera engine for Minecraft 26.2 (NeoForge & Fabric); Epic Fight is now All Rights Reserved". `release_type=alpha`. Sources: https://github.com/Antikythera-Studios/epicfight/blob/26.2/CHANGELOG.md, https://github.com/Antikythera-Studios/epicfight/commits/26.2, https://github.com/Antikythera-Studios/epicfight/blob/26.2/gradle.properties
   - The new LICENSE (ARR) still allows inclusion in modpacks "in its original and unmodified form… provided that the modpack does not charge a fee for access to the Mod itself and that attribution… is preserved" (https://github.com/Antikythera-Studios/epicfight/blob/26.2/LICENSE). The 1.20.1 and 1.21.1 releases remain GPLv3.
   - In July 2026 maintainer guivnf wrote: "our team is already working on a fabric port… Beginning on 26.1, Epic Fight will contain multi loader support" (https://github.com/Antikythera-Studios/epicfight/issues/2590).
   - The 26.x branch is a rebuild with breaking API changes (issues #2372, #2460, #2449). **Every addon (WOM, Nightfall, Dawn Day, Indestructible, compat packs) will need its own port.** Expect the addon ecosystem to lag the core release by months [?].
   - Antikythera Studios is based in South Korea (https://github.com/Antikythera-Studios). Its Discord is "ATK Studios" (https://discord.com/servers/atk-studios-955784714264932362). This may help a Korean creator.
2. **[V] Almost every soulslike content mod stops at 1.20.1 Forge or 1.21.1 NeoForge.**
   - Cataclysm, Mowzie's, Bosses'Rise, Born in Chaos, Iron's Spells, WOM, Nightfall, CustomNPCs-Unofficial and Heracles have no 26.x build.
   - These do have 26.x builds: Better Combat, Combat Roll, Corpse, Waystones, Pufferfish's Skills, Easy NPC, FTB Quests, KubeJS (beta), GeckoLib, Director's Camera, YAWP, WorldEdit and Axiom.
3. **[V] The acclaimed soulslike packs are still on 1.20.1 Forge or 1.21.1 NeoForge** (section 4).
   - The only big 26.x pack is ATM11 (kitchen-sink tech), still an alpha on 26.1.2 NeoForge.
   - NeoForge's Technici4n: "strong indications that 26.1 will be the next stable modding version… personal educated guess" (https://neoforged.net/news/26.1release/).
4. **[C] Recommended base: NeoForge 1.21.1 + Epic Fight 21.17.x.** This matches Ashen Vow, VALERIA (a soulslike adventure map) and most new Epic Fight addons. Keep map logic in datapacks and KubeJS so it can be ported later to Epic Fight 26.x.

---

## 1. Combat core: Epic Fight and its ecosystem

### Epic Fight itself
- **[V]** CurseForge: 29.9M downloads, GPLv3. Files:
  - `21.17.3.1-mc1.21.1-neoforge` (May 31, 2026)
  - `20.14.17-mc1.20.1-forge` (May 6, 2026)
  - 1.19.2 is legacy.
  - https://www.curseforge.com/minecraft/mc-mods/epic-fight-mod/files
- **[V]** Modrinth lists 1.21.1 and older only, Forge/NeoForge (https://modrinth.com/mod/epic-fight/versions).
- **[V]** GitHub branches (https://github.com/Antikythera-Studios/epicfight/branches):
  - `1.21.1` (default, updated May 27, 2026)
  - `26.2` (updated Oct 13, 2026)
  - `1.21.1-fabric` (updated Aug 30, 2026)
- **[V]** Open PR "21.17.4 Fix #2572 + Enchantments" from June 2026 (https://github.com/Antikythera-Studios/epicfight/pull/2573). A 1.21.1 maintenance release is still pending.
- **[V]** The README says there are no plans to backport new features to older MC versions.
- **[V]** Built-in data-driven tools: a weapon-type editor, item capabilities and a **Mob Capabilities editor** (in-game GUI that writes a datapack: model, armature, factions, stun armor, living and combat animations).
  - Docs: https://epicfight-docs.readthedocs.io/Guides/Entities/page1/, https://epicfight-docs.readthedocs.io/ko/Guides/Entities/page2/ (Korean page)
  - Official tutorial video by Yesman: https://www.youtube.com/watch?v=iXsATy1xNNw (transcript in `social/yt_iXsATy1xNNw.txt`)
  - Blender JSON exporter for custom animations: https://github.com/Epic-Fight/blender-json-addon
  - Example datapacks and Blender files: https://github.com/Antikythera-Studios/atk-resources (GPLv3)
- **[V]** Known issue: incompatible with SPBR, Fresh Animations and Bray's Zombie Overhaul (#2581, planned). Rendering issues with Iron's Spells addons (#2456).

### Main addons (verified on their CurseForge pages)

| Addon | 1.20.1 Forge | 1.21.1 NeoForge | Notes |
|---|---|---|---|
| Weapons of Miracles (WOM) | 2.0.171 (Aug 12, 2026) | 2.0.178 (Sep 7, 2026) | ARR, 12.4M downloads. https://www.curseforge.com/minecraft/mc-mods/weapons-of-miracles-epicfight |
| EpicFight-Nightfall | 3.4.2 (Sep 30, 2026) | 3.4.0 (Aug 4, 2026) | ARR. https://www.curseforge.com/minecraft/mc-mods/epicfight-nightfall |
| Epic Fight: Skill Tree (official) | 20.2.9 (Aug 17, 2026) | Apr 12, 2026 | GPLv3; replaces random skill books with a tree. https://www.curseforge.com/minecraft/mc-mods/epic-fight-skill-tree |
| Epic Fight – Indestructible (original, namelesslk) | 20.12.0 (Aug 2025) | – | Datapack-driven monster AI: guard, stamina, stun shield. https://www.curseforge.com/minecraft/mc-mods/epic-fight-indestructible |
| Epic Fight: Indestructible (fork, Unitei) | – | 21.16.3 (Apr 2026) | LGPLv3. https://www.curseforge.com/minecraft/mc-mods/epic-fight-indestructible-fork |
| Epic Fight: Impactful (fork) | – | Apr 2026 | Hit-stop and screen shake. https://www.curseforge.com/minecraft/mc-mods/epic-fight-impactful-fork |
| Epic Fight – Better Lock On | 2.0.14 (Oct 1, 2026) | May 12, 2026 | Client-side, ARR. https://www.curseforge.com/minecraft/mc-mods/better-lock-on |
| EF x Better Lock On: Movement & Camera Fixes | Forge 1.20.1 | NeoForge 1.21.1 | 360° lock-on movement. https://www.curseforge.com/minecraft/mc-mods/epic-fight-x-better-lock-on-better-third-person-qol-fixes |
| Epic Fight: Dawn Day | Forge | NeoForge 1.1.0 | Handcrafted weapon and death animations. https://www.curseforge.com/minecraft/mc-mods/epic-fight-dawn-day |
| Epic Fight – Mod Compat (payangar_dev) | – | 1.1.0 (Aug 2026) | Third-party downloads disabled (see section 5). https://www.curseforge.com/minecraft/mc-mods/epic-fight-mod-compat |
| Epic Fight Weapons Compat (sho09) | – | Jul 2026 | Movesets for 500+ weapons (Cataclysm, Epic Knights, Simply Swords). https://www.curseforge.com/minecraft/mc-mods/epic-fight-weapons-compat |
| CNPC-EpicFight-Integration (unofficial) | Forge (EF 20.14.10) | – | CustomNPCs NPCs using Epic Fight datapacks. https://www.curseforge.com/minecraft/mc-mods/cnpc-epicfight-integration-unofficial |
| SLM: Epic Fight | | | Skill and event utilities, 524K downloads. https://www.curseforge.com/minecraft/mc-mods/slm-epic-fight |

- **[C]** YouTube "Top 30 Minecraft Epic Fight Mods made in 2026" by ItsArenZ (https://www.youtube.com/watch?v=Ac1JsjcfGWw, transcript in `social/yt_Ac1JsjcfGWw.txt`) lists addons that add bosses with Epic Fight movesets:
  - Leonidas, Vergil ("Bosses of Miracle"), Arachne, Azrath
  - Awakened Mobs: vanilla mobs that block, parry and counter
  - Epic Foes, Epic ParCool, Mobs Plus, Weapons of Harmony
  - A first-person Epic Fight mod

  Most of these are 1.20.1 Forge or 1.21.1 NeoForge.

### Alternative combat stack (do not mix with Epic Fight)
- **[V] Better Combat** (ARR, 82.8M downloads) has the widest version coverage of any combat mod:
  - 3.2.2 for 26.1.2, 26.2 and 26.3 on both Fabric and NeoForge (Jul–Sep 2026)
  - `bettercombat-neoforge-2.4.0+1.21.1`
  - 1.20.1 Forge 1.8.x
  - https://www.curseforge.com/minecraft/mc-mods/better-combat-by-daedelus
  - GitHub release for 26.1.x: https://github.com/ZsoltMolnarrr/BetterCombat/releases/tag/3.2.1%2B26.1.2
- **[V] Combat Roll** (GPLv3): 3.0.1 for 26.1.2/26.2/26.3 on Fabric and NeoForge; 2.0.x for 1.21.1 NeoForge; also 1.20.1 Forge. https://www.curseforge.com/minecraft/mc-mods/combat-roll
- **[C] Ashen Vow** (1.21.1 NeoForge, Aug 2026) avoids mixing on purpose: "the pack deliberately contains no second combat or animation system: no Better Combat, no Combat Roll, no Not Enough Animations, no first-person model mod, and no second stamina bar. Two such systems fight each other on screen." https://www.curseforge.com/minecraft/modpacks/ashen-vow
- **[C]** LuluBelleMC on YouTube (82K views): "Epic Fight rebuilds combat. Better Combat polishes it." Epic Fight also reworks mob AI (windups, stagger, parry), but you have to curate addons. https://www.youtube.com/watch?v=cp7qqn2DGVQ
- **[C]** r/feedthebeast, "Anyone actually really prefer vanilla combat?" (Sep 2026, https://www.reddit.com/r/feedthebeast/comments/1w8peqb/). Top comments:
  - "Epic Fight is great but has to be properly implemented… If you're not gonna properly integrate Epic Fight, making all the mobs and weapons compatible, then just stick to vanilla" (+20)
  - "The epic fight mod completely overhauls the mob combat too" (+23)
  - Better Combat is "just Skyrim combat"
  - The lesson is that a complete "set" matters: mobs have to be designed for the combat system.
- **[C]** r/feedthebeast comment (Sep 2026): "almost all [Epic Fight packs]… make vanilla/non-combat gameplay feel bland". An adventure map that is all combat avoids this problem.
- **[C]** A common complaint is the Epic Fight lock-on camera ("HEINOUS", https://www.reddit.com/r/feedthebeast/comments/1wlyl51/). Better Lock On and the Movement & Camera Fixes addon are the usual fixes.

### Movement, stamina, lock-on, death, checkpoints, leveling
- **ParCool** (LGPLv3):
  - [V] Official builds: 1.20.1 Forge 4.0.1.4 (Oct 12, 2026), 1.21.1 3.3.1.0, betas up to 1.21.11 NeoForge. No official 26.x. https://www.curseforge.com/minecraft/mc-mods/parcool
  - [V] Unofficial "ParCool Reforged" for 26.1.1 NeoForge (142 downloads): https://www.curseforge.com/minecraft/mc-mods/parcool-reforged
  - [C] An "Epic ParCool" compat addon exists.
- **Stamina:** Epic Fight already has stamina for dodge and guard. Feathers (last update 2023) and Actions of Stamina (2023) are abandoned [V]. Ashen Vow advises against a second stamina bar [C].
- **Lock-on:**
  - [V] Lock On (tfarecnim): NeoForge 1.21.1, public domain. https://www.curseforge.com/minecraft/mc-mods/lock-on
  - [V] Camera Lock-on (Sep 2026, new) and Combat Focus: https://www.curseforge.com/minecraft/mc-mods/camera-lock-on, https://www.curseforge.com/minecraft/mc-mods/combat-focus
  - [V] Focus (JevenDev), NeoForge 1.21.1
  - For an Epic Fight setup, use Better Lock On.
- **Corpse / death run:**
  - [V] Corpse (henkelmax, ARR, 134M downloads): 1.20.1, 1.21.1, 26.1.x, 26.2 and 26.3 on NeoForge. https://www.curseforge.com/minecraft/mc-mods/corpse
  - [V] Smaller soul-drop mods: Death Penalty (lose max HP and XP, Soul Crystal), Soul Debt, Afterworld: Death (1.20.1 Forge). All have very few downloads. https://www.curseforge.com/minecraft/mc-mods/death-penalty
  - [?] A true "souls" currency dropped on death is probably best built yourself in KubeJS or a datapack.
- **Bonfires / checkpoints:**
  - [V] Bonfires (Wehavecookies56, LGPLv3): 1.21.1 NeoForge v1.2.20b (Nov 2025), 1.21.4. Teleport-focused. https://www.curseforge.com/minecraft/mc-mods/bonfires
  - [V] Waystones (ARR): every version, including 26.3 on NeoForge and Fabric. https://www.curseforge.com/minecraft/mc-mods/waystones
  - [C] Ashen Vow renames Waystones to "bonfires".
  - [V] Campfire Checkpoints exists as a Paper plugin and a Modrinth mod.
- **Estus flask:** [V] Only tiny or abandoned mods exist: EstusssZ (243 downloads, ARR), Estus Flask (2024). https://www.curseforge.com/minecraft/mc-mods/estusss
  - Recommendation: build it with KubeJS, or with a custom item using the 1.21.x `consumable` component (26.x).
  - Note: on 1.21.1 the `consumable` component does not exist (added in 1.21.2) [?, from knowledge]. Use KubeJS item events there.
- **Leveling and stats:**
  - [V] Pufferfish's Skills (custom license): 0.19.2 for 26.1/26.2/26.3 (NeoForge and Fabric, beta), plus 1.21.x and 1.20.1. Fully data-driven skill trees. https://www.curseforge.com/minecraft/mc-mods/puffish-skills
  - [V] Project MMO: 1.21.x and 26.3 NeoForge (modpacks.ch listing). https://www.curseforge.com/minecraft/mc-mods/project-mmo
  - [V] Passive Skill Tree: original is 1.20.1. Unofficial NeoForge 1.21.1 port (2K downloads, Sep 2026). https://www.curseforge.com/minecraft/mc-mods/passive-skill-tree-neoforge
  - [V] BK's Souls-Like Leveling (Oct 2026, 528 downloads): levels plus stat requirements on weapons. https://www.curseforge.com/minecraft/mc-mods/bks-souls-like-leveling
  - [C] Soulrend uses Passive Skill Tree and Just Leveling on 1.20.1.
- **Boss bars:** [V] Enhanced Boss Bars has a mod for 1.16.5–1.21.1 (Forge/NeoForge, Jan 2026) and a resource-pack version (31.8M downloads, Jun 2026). https://www.curseforge.com/minecraft/mc-mods/enhanced-boss-bars
- **Menus and loading screens:** [V] FancyMenu (3.8.6 for 26.1.x NeoForge) and Drippy Loading Screen (26.2, 1.21.1 and 1.20.1). Custom license DSMSLv3. https://www.curseforge.com/minecraft/mc-mods/drippy-loading-screen

---

## 2. Bosses and enemies (to use directly or study)

| Mod | 1.20.1 Forge | 1.21.1 NeoForge | 26.x | License | Notes |
|---|---|---|---|---|---|
| L_Ender's Cataclysm | 3.31 (Jun 2026) | 3.33 (Sep 20, 2026) | – | Custom; assets ARR | 117M downloads; bosses spawn in structures. https://www.curseforge.com/minecraft/mc-mods/lendercataclysm/files/all |
| Mowzie's Mobs | 1.8.2 (Mar 2026) | 1.8.2 (Mar 2026) | – | Custom | GeckoLib; config controls block-breaking. https://www.curseforge.com/minecraft/mc-mods/mowzies-mobs |
| Bosses'Rise | ✓ | 2.1.2 (May 2026) | – | ARR | 5 multi-phase soulslike bosses with arenas. https://www.curseforge.com/minecraft/mc-mods/bossesrise |
| Marium's Soulslike Weaponry | 1.4.10 Forge+Fabric (Sep 2026) | **Fabric only** (1.4.8) | – | CF says ARR, GitHub says CC0 | On 1.21.1 NeoForge it needs Sinytra Connector, and a user reported configs not applying (https://www.reddit.com/r/feedthebeast/comments/1uipsbc/). https://www.curseforge.com/minecraft/mc-mods/mariums-soulslike-weaponry/files/all |
| Born in Chaos | 1.7.5 | 1.7.6 (Jun 2026) | – | ARR | https://www.curseforge.com/minecraft/mc-mods/born-in-chaos/files/all |
| Souls like Bosses (Bananaph0ne) | 3.4 Forge/Fabric/Quilt (Apr 2026) | – | – | ARR | Soul of Cinder, Nightlord and others, with Epic Fight showcases. https://www.curseforge.com/minecraft/mc-mods/souls-like-bosses |
| Iron's Spells 'n Spellbooks | 3.16.3 | 3.16.3 (Aug 2026) | – | | https://iron.wiki/changelog/ |
| GeckoLib (shared dependency) | ✓ | ✓ | 26.1–26.3 NeoForge (5.5.x) | | https://www.curseforge.com/minecraft/mc-mods/geckolib |

- **[V]** New Epic Fight-native boss creation tools:
  - "Epic Fight: BK's Mob Attack Patterns" (https://www.curseforge.com/minecraft/mc-mods/epic-fight-bks-mob-attack-patterns)
  - Custom Mobs Framework (https://www.curseforge.com/minecraft/mc-mods/custom-mobs-framework)
  - Vitae, a datapack/KubeJS entity framework for NeoForge 1.21.1 (https://www.curseforge.com/minecraft/mc-mods/vitae)
- **[C]** A Sep 2026 r/feedthebeast post (+31) shows a mod that lets you "design monster attack patterns directly through a GUI and create mobs with Soulslike-style combat patterns". It supports Forge 1.20.1 and NeoForge 1.21.1 (https://www.reddit.com/r/feedthebeast/comments/1wdaijh/). The mod name was not captured [?].
- **Design note [V/C]:** For a handcrafted map, disable natural boss and structure generation and summon bosses with commands or KubeJS inside your own arenas. Cataclysm and Mowzie's both have block-breaking configs (https://wiki.9minecraft.net/mowzies-mobs-mod/configuration/) [?]. Also set `mobGriefing` and the per-mod configs so bosses cannot destroy the map.

---

## 3. Map-making and game-logic tools

### Logic layer: datapack vs KubeJS vs custom mod
- **Datapack / mcfunction:** works on any loader and outlives loader changes.
  - [V] Dialog screens: `/dialog` was added in **1.21.6** (https://minecraft.wiki/w/Commands/dialog). **It is not available on 1.21.1.**
  - [?, from knowledge, not verified] Other newer item components such as `consumable`, `equippable` and `item_model` are also missing on 1.21.1, since they came in 1.21.2–1.21.4.
  - [C] r/MinecraftCommands, Dark Souls adventure map thread: "HIGHLY recommend you learn how to make that a datapack" instead of command blocks (+9). https://www.reddit.com/r/MinecraftCommands/comments/1vgg2y5/
- **KubeJS** (LGPLv3):
  - [V] 1.21.1 NeoForge 2101.7.2 (Sep 2026)
  - [V] 1.20.1 Forge 2001.6.5 (May 2026)
  - [V] 26.1.2 NeoForge 8.0.6 beta (Sep 2026), changelog at https://github.com/kube-mods/kubejs/blob/2601/CHANGELOG.md
  - Good for event hooks (death, entity kill, item use, tick-based region checks) and custom items. https://www.curseforge.com/minecraft/mc-mods/kubejs
  - [V] Epic Fight skills can be registered from KubeJS (issue #2061).
- **Custom NeoForge mod:** best for estus, souls currency, a bonfire UI and HUD. Needs Java, and ports by hand on each MC version.

### NPCs, dialogue, quests
- [V] **Easy NPC** (Kaworru, custom license): actively updated.
  - 26.1.2, 26.2 and 26.3 on Forge, NeoForge and Fabric (7.14/7.15, Oct 2026)
  - 1.21.1 (NeoForge 7.x, Fabric 7.13)
  - 1.20.1 Forge 7.8
  - Dialogs, trading and actions, built for map makers. https://www.curseforge.com/minecraft/mc-mods/easy-npc
- [V] **CustomNPCs-Unofficial** (Goodbird, CC BY-NC 3.0): 1.20.1 Forge (Jul 2026), 1.21.1 NeoForge (Jan 2026) and Fabric (May 2026). No 26.x. https://www.curseforge.com/minecraft/mc-mods/customnpcs-unofficial
  - [C] Replay mods do not record CNPC + Epic Fight animations (https://www.reddit.com/r/feedthebeast/comments/1v9ggle/).
- [V] **FTB Quests** (ARR):
  - NeoForge 26.1.2.9 (Oct 7, 2026); Fabric 26.1.2.6
  - 1.21.1 NeoForge (Sep 15, 2026)
  - 1.20.1 Forge 2001.4.22
  - https://www.curseforge.com/minecraft/mc-mods/ftb-quests-forge
  - [C] Ashen Vow ships a 305-quest book with a build check that fails if any content mod is unused.
- [V] **Heracles / Odyssey Quests** (MIT): 1.20.1 (2024); 1.21.1 Fabric/NeoForge beta (Oct 5, 2026). https://www.curseforge.com/minecraft/mc-mods/odyssey-quests

### Cutscenes and camera
- [V] **Director's Camera** (MIT, Sep 2026): NeoForge 26.1.2 and 1.21.1.
  - Camera paths are defined in JSON, KubeJS or with an in-game camera tool.
  - Includes screen shake, timed sounds, hold-to-skip and keyframes.
  - The player is locked while it plays: "cannot walk, look around or break anything".
  - 40.8K downloads in its first month.
  - https://www.curseforge.com/minecraft/mc-mods/directors-camera
- [V] Other options:
  - Cutscene-API (thewinnt, MIT, branch 1.21.4): https://github.com/thewinnt/Cutscene-API
  - Lumiera (Jul 2026): https://www.curseforge.com/minecraft/mc-mods/lumiera
  - Cutscene-engine (mcfunction): https://github.com/Stepan1411/Cutscene-engine
- [C] Vanilla technique from a 201-upvote r/MinecraftCommands post: build camera moves in Blender and export them to mcfunction `tp` commands with a custom addon. Fade-to-black is "a title command that shows a custom font that contains a symbol that spans the entire screen". https://www.reddit.com/r/MinecraftCommands/comments/1o635jv/

### HUD and UI
- **Resource-pack font tricks (negative space glyphs, actionbar and bossbar overlays):** version-independent, apart from pack-format changes (26.1 resource pack format 84).
  - [V] Tools: Glyphsmith (https://github.com/SalyyS1/glyphsmith), HUDEngine (https://github.com/Nacvark/HUDEngine), guide at https://www.9minecraft.net/tools/guides/hud-customization-resource-pack/
  - [C] Alignment pain is common (https://www.reddit.com/r/MinecraftCommands/comments/1vy3wcm/).
- **Mod libraries:** FlexHUD (NeoForge, https://github.com/TT432/FlexHUD) and HudRendererLib (Fabric/NeoForge). For a polished soulslike HUD (souls counter, estus count), a small custom mod or KubeJS client script is cleaner [?].

### Regions, triggers, map protection
- [V] **YAWP** (server-side region protection):
  - Forge, NeoForge and Fabric for 1.20.1 and 1.21.1
  - Builds for 26.1.2 (0.6.3-beta3) and 26.2 (beta4)
  - https://z0rdak.github.io/yawp-docs/docs/getting-started/supported-versions, https://github.com/Z0rdak/Yet-Another-World-Protector/releases
- [V] **Loquat** (Snownee): area management for map makers, with scriptable areas and structure templates. Mostly 1.19–1.20.1. https://mineuniverse.net/mod/loquat-forge
- [V] Adventure-mode helpers:
  - Adventure mode plus `can_break` / `can_place_on` components (https://minecraft.wiki/w/Data_component_format/can_break)
  - adventure-protect (https://github.com/joel4848/adventure-protect)
  - adventure-zones (https://github.com/gimme/adventure-zones)
- [?] Region "enter" triggers on modded versions: a KubeJS tick or player-tick check against AABBs, or YAWP flags. A datapack predicate with `positioned`/`dx` checks also works.

### Building tools
- [V] **Axiom** (Moulberry, ARR + EULA):
  - **Fabric only.** Supports 1.20.x, 1.21.x, 26.1.x, 26.2 and 26.3 (6.1.3, Sep 25, 2026). https://modrinth.com/project/N6n5dqoA, https://www.curseforge.com/minecraft/mc-mods/axiomtool
  - **Commercial use needs a Commercial License**, which also unlocks multiplayer and history persistence (https://axiomdocs.moulberry.com/other/commerciallicense.html).
  - On NeoForge 1.21.1 it only runs through **Sinytra Connector**, which is fragile. Crashes reported Jan–Apr 2026 (https://github.com/Sinytra/Connector/issues/2190, #2100), and Moulberry traced one to a loom remapper regression.
  - Sinytra Connector: 2.0.0-beta.14 for 1.21.1; 3.0.0-beta.6 for 26.1.2 (Aug 2026). https://connector.sinytra.org/compatibility/archive
  - [C] A user asked whether the Axiom multiplayer plugin can run on modded NeoForge/Fabric servers; no answer (https://www.reddit.com/r/feedthebeast/comments/1weqxqk/).
  - **Workflow suggestion [C/?]:** sculpt terrain and vanilla-block architecture in a Fabric + Axiom instance on the same MC version (1.21.1), then open the world in the NeoForge pack to place modded blocks, NPCs and bosses. Or try Connector and accept the risk.
  - [C] YouTube "Mapmaking in 2026: A Terraforming Guide with Axiom" by Calven (61.7K views, https://www.youtube.com/watch?v=kGHzPIV6xbY, transcript in `social/yt_kGHzPIV6xbY.txt`):
    - start from a single-biome world to keep vanilla caves
    - set a world border and pregenerate
    - clear foliage with script brushes
    - flatten, then sculpt and paint
    - Part 2: https://www.youtube.com/watch?v=Y6kavdAkvqc
  - [C] Zeplington, "I started building my own Minecraft adventure map (using Axiom)", 60K views: https://www.youtube.com/watch?v=7z2_79oRXWk
- [V] **WorldEdit** (GPLv3):
  - NeoForge/Fabric 7.4.5 for 26.2; 7.4.6 beta for 26.3; 26.1.2 build
  - 7.3.8 for 1.21–1.21.1 NeoForge/Fabric
  - https://www.curseforge.com/minecraft/mc-mods/worldedit
- [V] **FastAsyncWorldEdit**: Paper/Bukkit only. 26.3 support merged Sep 30, 2026; 2.16.1 (Oct 9). https://github.com/IntellectualSites/FastAsyncWorldEdit/releases
- [V] **WorldPainter**:
  - 2.27.0 (Jun 27, 2026) added export, import and merge for the 26.1+ map format ("not yet new blocks")
  - 2.27.1 fixed the spawn point on 26.1+ (the changelog prints the year as "2027", a typo)
  - 1.21.x works fully
  - Issues: https://github.com/Captain-Chaos/WorldPainter/issues/524, #531; changelog https://www.pepsoft.org/worldpainter/CHANGELOG
- [V] **Amulet:** 0.10.54 added Java 26.1 (Mar 2026); 0.10.57 added J26.2 (Jun 2026, beta). https://github.com/Amulet-Team/Amulet-Map-Editor/releases/tag/0.10.57
- [V] Blender-to-schematic addon (Litematica .litematic, Axiom .bp, WorldEdit .schem): https://www.reddit.com/r/feedthebeast/comments/1x18gn9/

---

## 4. Which version and loader do acclaimed soulslike packs use (Oct 2026)?

| Pack | Version / loader | Evidence |
|---|---|---|
| Soulrend – Dark Fantasy RPG Soulslike (1.1M downloads, v8.5 Oct 9, 2026) | **1.20.1 Forge** | Epic Fight with 100+ custom movesets, Cataclysm, Mowzie's, Soulslike Weaponry, Passive Skill Tree, Just Leveling. https://www.curseforge.com/minecraft/modpacks/soulrend |
| Ashen Vow (Aug 2026) | **1.21.1 NeoForge** | Epic Fight + WOM + Nightfall + Dawn Day, Corpse run, Waystone bonfires, 305 quests. https://www.curseforge.com/minecraft/modpacks/ashen-vow |
| SoulsLikeLegacy (Sep 2026) | 1.20.1 Forge | Class-based, quest-gated, co-op. https://www.curseforge.com/minecraft/modpacks/soulslikelegacy |
| SULS – So U Like Soulslikes (10.7K) | 1.20.1 Forge | https://www.curseforge.com/minecraft/modpacks/so-u-like-soulslikes |
| Ashen RPG (Oct 2026) | 1.21.1 | https://www.curseforge.com/minecraft/modpacks/ashen-rpg-epic-rpg-dungeons-dark-conquest |
| Soul Veil (Aug 2026) | 1.21.1 NeoForge | https://www.curseforge.com/minecraft/modpacks/soul-veil |
| Age of Titans v2.0 (Oct 13, 2026, Reddit) | 1.20.1 | https://www.reddit.com/r/feedthebeast/comments/1x4vcqk/ |
| VALERIA (soulslike *adventure map*, demo updated Sep 22, 2026) | **NeoForge 1.21.1 + Epic Fight** | Ships a whole `.minecraft` folder. https://www.planetminecraft.com/project/valeria-6557226/ |
| Fool's Errand (vanilla soulslike adventure map) | 1.20.2, pure datapack | Stamina, parry, leveling, 7 levels, co-op. https://www.planetminecraft.com/project/fool-s-errand-the-curse-of-binding-a-soulslike-adventure-map/ |
| ATM11 (reference for 26.x uptake) | 26.1.2 NeoForge, "super early alpha" | https://www.curseforge.com/minecraft/modpacks/all-the-mods-11 |

### Community sentiment
r/feedthebeast thread "Which supported Minecraft versions should I ACTUALLY mod?" (Oct 12, 2026, https://www.reddit.com/r/feedthebeast/comments/1x4bsal/) [C]:
- Top answer "1.21.1" (+26).
- "1.20.1 is nowhere near obsolete. If you want the biggest ecosystem, use 1.20.1. If you want newer active development, 1.21.1 is probably the sweet spot."
- "New development is targeting 1.21.1… or 26.x if you're trying to future-proof."
- "26.3: You will have about 0 major content mods."
- "Whatever update we get the Sift in will probably be the next major modpacking version."
- "I'd aim for 26.1.2… 26+ versions really are the future and the codebase is a lot cleaner."
- One user downgraded their worlds from 26.1.2 to 1.21.1 "because I feel like it's going to take a solid chunk of time to get there".

**Interpretation [?]:** The 26.x anchor version is still unsettled. Possible anchors are 26.1.2 (ATM11, many ports), 26.2 (the Epic Fight branch) or a future drop. Do not start the map on 26.x unless you can do without Epic Fight addons and the boss mods.

### Support matrix: key mods (✓ = released build seen; β = beta/alpha; – = none found)

| Mod | 1.20.1 Forge | 1.21.1 NeoForge | 26.x NeoForge | 26.x Fabric |
|---|---|---|---|---|
| Epic Fight | ✓ 20.14.17 | ✓ 21.17.3.1 | β unreleased (26.2 branch, ARR) | β unreleased (same branch) |
| WOM / Nightfall / EF Skill Tree | ✓ | ✓ | – | – |
| Indestructible | ✓ (orig.) | ✓ (fork) | – | – |
| Better Combat | ✓ | ✓ | ✓ 26.1.2–26.3 | ✓ 26.1.2–26.3 |
| Combat Roll | ✓ | ✓ | ✓ | ✓ |
| ParCool | ✓ | ✓ (3.3.1) | unofficial (Reforged, 26.1.1) | – |
| Corpse | ✓ | ✓ | ✓ 26.1–26.3 | ? |
| Waystones | ✓ | ✓ | ✓ | ✓ |
| Pufferfish's Skills | ✓ | ✓ | β 26.1–26.3 | β 26.1–26.3 |
| Cataclysm | ✓ 3.31 | ✓ 3.33 | – | – |
| Mowzie's Mobs | ✓ | ✓ | – | – |
| Bosses'Rise | ✓ | ✓ | – | – |
| Soulslike Weaponry | ✓ (Forge+Fabric) | – (Fabric 1.21.1 only) | – | – |
| Born in Chaos | ✓ | ✓ | – | – |
| Iron's Spells | ✓ | ✓ | – | – |
| GeckoLib | ✓ | ✓ | ✓ | ✓ |
| KubeJS | ✓ | ✓ | β 26.1.2 | ? |
| Easy NPC | ✓ | ✓ | ✓ 26.1.2–26.3 | ✓ |
| CustomNPCs-Unofficial | ✓ | ✓ | – | – |
| FTB Quests | ✓ | ✓ | ✓ 26.1.2 | ✓ 26.1.2 |
| Heracles | ✓ (2024) | β | – | – |
| Director's Camera | – | ✓ | ✓ 26.1.2 | – |
| YAWP | ✓ | ✓ | β 26.1.2/26.2 | β? |
| Axiom | (Fabric 1.20.x) | Fabric 1.21.x only (Connector on NeoForge) | – (Connector 3.0 β) | ✓ 26.1–26.3 |
| WorldEdit | ✓ | ✓ 7.3.8 | ✓ 26.1.2/26.2, β 26.3 | ✓ |

---

## 5. Packaging and distribution

- **[V] CurseForge 3rd-party download toggle.** Some mods have third-party downloads disabled. The CurseForge app pauses and asks the player to download them by hand; Prism, MultiMC and ATLauncher often just fail.
  - Ashen Vow documents five such files, including Epic Fight – Smart Items, Epic Fight – Mod Compat and Entity Culling.
  - Launcher issues: https://github.com/PrismLauncher/PrismLauncher/issues/599, https://github.com/packwiz/packwiz-installer/issues/50
  - **Check the toggle on every mod before you commit to it.**
- **[V] Modrinth permissions.** An `.mrpack` references files hosted on Modrinth. For anything else in `overrides`, you need:
  1. an open-source license, or
  2. an explicit statement on the project page, or
  3. the author's written permission, sent as a screenshot to moderation.

  Otherwise it cannot be included. Sources: https://support.modrinth.com/en/articles/8797527-obtaining-modpack-permissions, https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack
  - Modrinth merged a "new modpack permissions system" in Jun 2026 (https://github.com/modrinth/code/pull/6005).
  - Epic Fight itself is on Modrinth (1.21.1). Many of its addons and compat packs are CurseForge-only, and a few useful mods are Modrinth-only; Ashen Vow lists three it could not include. [V/?] **CurseForge looks like the more practical host for an Epic Fight map pack, but some mods will be missing on either platform.**
- **[V] CurseForge modpack zip.** `manifest.json` references CurseForge files, and `overrides/` can carry configs, KubeJS scripts, datapacks and the **world save** (`overrides/saves/<MapName>`). Ashen Vow also ships resource and shader packs under their licenses with credits.
- **[V] Licenses that matter:**
  - Epic Fight 1.20.1/1.21.1 is GPLv3, so it can be redistributed.
  - Epic Fight 26.x is ARR, with modpack inclusion allowed if unmodified, free and attributed.
  - WOM, Nightfall, Bosses'Rise, Corpse, Waystones and Better Combat are ARR. Reference them through the platform manifest; never bundle the jars.
  - CustomNPCs-Unofficial is CC BY-NC.
  - Axiom-built content for a commercial product needs an Axiom Commercial License.
- **[C] Anti-pattern:** VALERIA distributes a whole `.minecraft` folder and tells users to empty their mods folder. That is a licensing risk and a poor experience.
- **[C] Server vs single-player.**
  - SoulsLikeLegacy is "primarily designed… for cooperative multiplayer on a dedicated server" and warns that single-player performance is worse.
  - Epic Fight multiplayer desyncs come up regularly with Essential-based hosting (https://www.reddit.com/r/feedthebeast/comments/1vbyscl/, /1wdq9wn/).
  - Ship a server pack (CurseForge supports server pack files; Soulrend ships one). `mrpack4server` exists for Modrinth (https://github.com/patbox/mrpack4server).

---

## 6. Recommendations (for the user)

1. **Target NeoForge 1.21.1** with Epic Fight 21.17.x, WOM and/or Nightfall/Dawn Day, Better Lock On, Indestructible (fork) and Impactful, Corpse, Easy NPC, FTB Quests, KubeJS, Director's Camera, YAWP, Cataclysm, Mowzie's, Bosses'Rise and Born in Chaos.
   - Drop Soulslike Weaponry, or accept Connector risk.
   - Do not add Better Combat or Combat Roll alongside Epic Fight.
2. **Keep logic portable.** Story flags, checkpoints and region triggers go in datapacks/mcfunction with scoreboards and storage. Event glue goes in KubeJS. Bespoke souls-currency, estus and bonfire UI go in a small custom NeoForge mod. This keeps a later move to 26.x Epic Fight manageable.
3. **Build pipeline:**
   - WorldPainter or Axiom (Fabric 1.21.1 instance) for terrain.
   - Axiom/WorldEdit for structures.
   - Then the NeoForge pack instance for modded dressing.
   - Pregenerate and lock the world: adventure mode, YAWP regions, `mobGriefing false`, and boss configs set to no block-breaking.
4. **Encounter design:** use the Epic Fight Mob Capabilities editor and datapacks so enemies and bosses fight with real Epic Fight movesets. Community consensus is that Epic Fight only shines when every mob is integrated.
5. **Distribute as a CurseForge modpack** with the world in `overrides`, plus a server pack. Audit third-party-download toggles and licenses first.
6. **Watch the Epic Fight `26.2` branch and the addon ports.** Re-evaluate around the first public 26.x beta [?].

## Coverage gaps
- **X/Twitter:** no search route exists, and no x.com status links turned up on the Epic Fight, Axiom, NeoForge or modpack pages harvested. No X posts were cited.
- **Reddit:** Arctic Shift full-text search often returned HTTP 422 (likely timeouts) for broad queries, so coverage relied on title searches and a few comment searches.
