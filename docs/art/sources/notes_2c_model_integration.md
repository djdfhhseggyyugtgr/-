# Round 2 / branch 2 (modeling) / part C — getting anime character models into gameplay, and AI-assisted character creation (2026-10-13)

Scope: MC Java 1.21.1 + NeoForge, Epic Fight (EF) 21.17.3.1, GeckoLib 4.9.3, Animated Java (AJ) 1.11, Blockbench 5.2.2.
Tags: **[V]** verified in a primary source (official docs, source code read in this session, mod pages / Modrinth API), **[C]** community claim / single report / vendor marketing, **[?]** inference or not verified, needs a test.
Raw data: `research/r2/2c/` (S_*.json searches, F_*.json pages). Source code read from shallow clones in `research/r2/2c/src/` (Epic-Fight/epicfight branch `1.21.1`, head a78aa24, 2026-05-26 = the 21.17.x line; Argorice/EpicYSM main, 2026-09-06).

Content rule applied: the child character (Daisy) gets age-appropriate designs only. Many community "anime girl" models (YSM packs, Sketchfab) are sexualised; do not use them as references. Only proportion and polygon counts are cited below.

---------------------------------------------------------------------
## 0. Summary of answers

| Question | Answer (short) | Tag |
|---|---|---|
| Can the player be a custom anime model while keeping EF animations? | **Yes, three working routes on 1.21.1 NeoForge.** (A) a custom EF skinned mesh that replaces EF's player mesh (our own mod + resource pack); (B) Yes Steve Model 2.6.5 + **EpicYSM 1.1.3** (MIT, client-only, Sep–Oct 2026), which converts a readable YSM/Bedrock cube model into an EF mesh at load time; (C) Figura + Figura ExtraFight/Fightura (not recommended). | [V] |
| Most realistic path | **Prototype with B in a day; ship A.** A needs no closed-source native mod, gives full control of texture, first-person arms, armor and versions. B depends on YSM (ARR, native C++ core, no macOS, removed from CurseForge, being rewritten) and on two 1-month-old bridge mods. | [V]/[?] |
| Can a GeckoLib boss use EF movesets? | **Not with its GeckoLib model.** An EF mob patch (`renderer: "epicfight:custom"`) draws an EF `SkinnedMesh` + EF armature instead; the GeckoLib geo/animations are unused while patched. Keep GeckoLib only for non-combat NPCs/props; bosses and combat NPCs become EF meshes (the same cube model converted). A code bridge that writes EF poses into a GeckoLib skeleton is possible (EpicYSM does this for encrypted YSM models) but is custom work. | [V] code |
| NPCs | Non-combat NPCs: GeckoLib entity in our mod, or **Easy NPC 7.15 + Easy Model Entities 2.5** (loads `.bbmodel` directly, no Java, MIT). Dialogue with portraits: **VNDialog 1.0.6** (MIT, NeoForge 1.21.1). | [V] |
| Cutscenes | In-engine with the same entities: `/epicfight animator play <targets> <animation>` + GeckoLib triggered animations + Director's Camera. Use AJ only for set pieces that are not one of the characters (or a stand-in). On 1.21.1, AJ texture-slot switching (faces, blinking) does not work, and cubes need legal 1.21.1 item-model rotations or their own bone. | [V] |
| One source model → many exports | Yes: one `.bbmodel` per character with a fixed bone-naming contract → (1) GeckoLib/EME export as is, (2) EF mesh by a converter (EpicYSM-style rigid binding, MIT reference code) or Blender + EF exporter, (3) AJ blueprint copy for set pieces, (4) portrait renders. | [V]/[?] |
| Performance budget | EF default player mesh = 472 triangles and 20 joints. Detailed Blockbench anime characters run about 3.9k–8.6k triangles (≈300–700 cubes). Suggested: player 250–400 cubes, NPC 150–300, boss 400–800; ≤20 biped joints + ≤20 physics/extra joints (EpicYSM's cap is 40). Measure in the G6 arena. | [V] counts / [?] budget |
| AI-assisted creation | Image-to-cube tools only produce blockouts (≈20–30 cuboids, silhouette IoU 0.57–0.68). Use AI for **turnaround sheets, 3D reference underlays and material swatches**, and have the agent build cubes and paint UV islands with deterministic checks. Pixel-art generators (PixelLab, Retro Diffusion) suit portraits/swatches, not UV atlases. Licenses: PixelLab outputs owned by the user; Meshy free = CC BY 4.0; Tripo free = non-commercial; **Hunyuan3D license excludes South Korea**; TRELLIS.2/TripoSR MIT. | [V] |

---------------------------------------------------------------------
## 1. Player character with Epic Fight

### 1.1 How EF draws the player (read from EF 1.21.1 source) [V]
- `PPlayerRenderer` draws `Meshes.BIPED`, or `Meshes.ALEX` for slim-arm skins (`getMeshProvider` checks `PlayerSkin.Model.SLIM`). Source: `client/renderer/patched/entity/PPlayerRenderer.java`.
- The meshes are JSON assets: `assets/epicfight/animmodels/entity/biped.json` and `biped_slim_arm.json` (`api/client/model/Meshes.java`, `MeshAccessor.create(EpicFightMod.MODID, "entity/biped", ...)`). Any resource pack can override them.
- `HumanoidMesh` looks up 12 named parts: `head, torso, leftArm, rightArm, leftLeg, rightLeg, hat, jacket, leftSleeve, rightSleeve, leftPants, rightPants` (`client/mesh/HumanoidMesh.java`). A replacement mesh must keep these part names. They control hiding (e.g., first person hides head/hat).
- The default biped mesh: 260 positions, **472 triangles**, armature with **20 joints**: `Root, Thigh_R, Leg_R, Knee_R, Thigh_L, Leg_L, Knee_L, Torso, Chest, Head, Shoulder_R, Arm_R, Hand_R, Tool_R, Elbow_R, Shoulder_L, Arm_L, Hand_L, Tool_L, Elbow_L` (measured from `biped.json`).
- Texture: the patched living renderer uses the vanilla render type from the entity, i.e. **the player's skin texture** (`PatchedLivingEntityRenderer`, `invokeGetRenderType`). The mesh JSON can declare `render_properties.texture_path` (`JsonAssetLoader.getRenderProperties`), but I did not find the player body path using it [?].
- **First person**: `FirstPersonRenderer` draws the same `Meshes.BIPED/ALEX`, hides everything except `leftArm, rightArm, leftSleeve, rightSleeve`, and plays EF first-person animations. So a replacement mesh automatically gives anime sleeves/gloves in first person if those four parts are modelled. [V] `client/renderer/FirstPersonRenderer.java`
- Mesh JSON format (`JsonAssetLoader.loadSkinnedMesh`): `vertices{positions, uvs, normals, vcounts, weights, vindices, parts{<name>{array}}}` + `armature{joints, hierarchy}`; optional `parent`, `render_properties{transparent, texture_path, color}`, **`cloth_info`** (cloth-simulated particles, constraints, mass, self-collision), and `mesh_loader: composite_mesh` with `meshes{static, cloth}`. Coordinates are Blender-space and converted at load. [V]
- EF has a GPU **compute-shader skinning** path with an Iris-specific init (`compat/iris/IRISCompat.java` → `ComputeShaderProvider.initIris()`). [V] code; performance not measured.
- Renderer registration order: EF puts `EntityType.PLAYER → PPlayerRenderer` and then posts `RegisterPatchedRenderersEvent.AddEntity` (EF's own event hooks, `EpicFightClientEventHooks.Registry.ADD_PATCHED_ENTITY`), followed by `ModifyEntity`. So a mod can replace the player's patched renderer with a subclass that returns its own mesh. The first-person renderer is created separately and still reads `Meshes.BIPED/ALEX` (override that asset, or mixin). [V] `client/events/engine/RenderEngine.java` lines ~735–758, 204.
  - Note: the docs (https://epicfight-docs.readthedocs.io/API/Starting/) still show the older `PatchedRenderersEvent.Add` on the MOD bus. The 1.21.1 branch uses `RegisterPatchedRenderersEvent` on EF's own event bus. Code against the 21.17.3.1 jar, not the wiki.

### 1.2 Route A — our own EF player mesh (recommended for shipping)
1. Model the protagonist in Blockbench (cubes, per-face UV, 32 px/block, one texture). Name bones by the contract in §6.
2. Convert to an EF mesh JSON with **rigid weights** (each cube bound 1.0 to one joint), splitting cubes into the 12 HumanoidMesh parts. Two ways:
   - **Blender path (official)**: Blockbench → OBJ/glTF → Blender → "Parent → Armature Deform With Empty Groups" to the EF biped rig → weight paint (rigid 1.0 per part) → EF Blender JSON exporter (tested on Blender 2.79–**5.0**, exports mesh, armature, animations, camera). https://epicfight-docs.readthedocs.io/Guides/Armor/3Darmor_page1/ , https://epicfight-docs.readthedocs.io/Guides/Armor/3Darmor_page3/ , https://github.com/Epic-Fight/blender-json-addon [V]
   - **Scripted path (agent-friendly, works in the cloud)**: a small Python converter from Bedrock geo / `.bbmodel` to EF mesh JSON, following EpicYSM's MIT `ModelConverter`/`JointMapper` logic (bone name → joint, cube centre → joint, armature re-proportioned to the model; physics chains for hair/skirt/cape bones). https://github.com/Argorice/EpicYSM (src/main/java/com/argorice/epicysm/client/convert/) [V code exists; our converter is [?] until built]
3. Ship it: resource pack overrides `epicfight:animmodels/entity/biped.json` and `biped_slim_arm.json` (covers third and first person), and our mod forces the texture (mixin `AbstractClientPlayer#getSkin` → our texture with model WIDE, or a `PPlayerRenderer` subclass registered via `AddEntity`). Without forcing the texture, the mesh would sample each classmate's own Mojang skin. [?] design, needs a prototype.
4. Side effects to handle: vanilla/EF armor meshes are fitted to the stock biped, so hide armor layers (the outfit is in the model); other EF users of `Meshes.BIPED` (the `player` preset renderer, Easy NPC [EF] humanoids) would also get the anime mesh — give them their own mesh ids. [?]
- Animations: EF animations are joint-space, so they play on any mesh bound to the biped armature. If the mesh has very different proportions (anime: big head, long legs), re-proportion the armature (EpicYSM does this) and check weapon contact points and colliders (`Tool_R`) in the G3/G5 gates. [V]/[?]
- Secondary motion: EF meshes support `cloth_info` (used for capes; "Cloth Simulator 2.0", Mar 2025: no stretching at low FPS, circular motion) https://www.patreon.com/yessman/posts/cloth-simulator-124329914 [V]. The authoring path for custom cloth (which exporter writes `cloth_info`) is undocumented [?]. Fallbacks: EpicYSM-style physics chains (code), or animate hair/skirt/coat-tail joints by hand.

### 1.3 Route B — Yes Steve Model + EpicYSM (fastest prototype)
- **Yes Steve Model 2.6.5** (2026-04-22; NeoForge 1.21.1 and 26.1.2, Forge 1.20.1, Fabric 1.20.1/1.21.1). Bedrock geometry + Bedrock animations + animation controllers, Blockbench `ysm-utils` plugin, GeckoLib-based core. **License ARR**; since 1.2.0 the core is **native C++** (Windows/Linux x64 only, no macOS); removed from CurseForge "due to review issues", Modrinth only (16.3M downloads). https://yesstevemodel.github.io/en/wiki/intro/ , https://modrinth.com/mod/yes-steve-model , https://ysm.cfpa.team/en/wiki/faq/ [V]
  - Commands useful for a map: `/ysm model set <model_id> <texture_id> true` (force a model, ignoring auth), `/ysm play <animation>` (force a player animation, usable in cutscenes), `/ysm model disable`. https://yesstevemodel.github.io/en/wiki/command/ [V]
  - Model folders: `config/yes_steve_model/custom` (readable folder/zip) vs `.ysm` (encrypted). https://yesstevemodel.github.io/en/wiki/type/ [V]
  - UV rule (2.6.0+): no zero-size UVs, UV positions/sizes must be integer multiples of the UV unit. https://yesstevemodel.github.io/wiki/ysm-uv-standard/ [V]
  - Status risk: an open-source rewrite (Apache-2.0, CC0 asset spec) started 2026-08-01 and warns that formats will break; first person and some mod integrations are not yet ported in the rewrite. The DRM was publicly reverse-engineered in 2026 (ysm.rip). Pin 2.6.5. https://github.com/YesSteveModel/YesSteveModel , https://www.ysm.rip/blog/openysm-technical-report [V]
- **EpicYSM 1.1.3** (Argorice; MIT; client-only; 1.21.1 NeoForge needs EF 21.15+ and YSM 2.6+; Modrinth 1.1.3 on 2026-10-03; ~6k downloads). Readable models are **converted on the fly into EF's own mesh + a skeleton with the model's proportions**, so EF draws them (weapons, trails, add-ons work); encrypted models are posed by writing EF's pose into YSM's skeleton. Per-model `epicysm.json` (bone→joint map, hide, pivots, physics add/remove). Joint cap 40 (20 biped + extra). Known limits: bones must be named `Head`, `LeftArm`, `RightLeg` etc.; shield hidden with two-handers; armor over converted models off by default; one open issue ("no ysm animations", 2026-10-13). https://www.curseforge.com/minecraft/mc-mods/epicysm , https://github.com/Argorice/EpicYSM [V]
- **YSM Epic Fight Compat 1.0.0** (sakuraimikoto33; MIT; client+server; 1.21.1 needs NeoForge 21.1.235+, EF ≥21.17.3.1 and <21.18, YSM 2.6.0+, **YSM Mapping API** 0.1.8+). First- and third-person EF rendering, Iris PBR bridge, ParCool/SWEM; it also **decrypts encrypted packages**, which we do not need. https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat , https://github.com/sakuraimikoto33/YSM-EpicFight-Compat [V]
- Before these bridges: YSM + EF crashed together (ClassCastException, 2025) and EF declined YSM support ("not planned", 2026-06). https://github.com/YesSteveModel/YSM-Wiki-Issues/issues/178 , https://github.com/Antikythera-Studios/epicfight/issues/2577 [V]
- Verdict [?]: good for a 1-day visual prototype of the protagonist (same Blockbench model, no Blender), and the YSM folder format is a convenient "source" export. For the shipped map, Route A avoids an ARR native mod, two reflection-based bridges (fragile to YSM updates), and the macOS gap.

### 1.4 Route C — Figura bridges (not recommended)
- Figura 0.1.6 has a 1.21.1 NeoForge build; **license PolyForm Noncommercial**. Bridges: **Figura ExtraFight** (custom license, ~11.8k DL, 1.21.1 NeoForge build `figura_extra_fight-0.0.41-neo`) and **Fightura** (MIT; now lists 1.21.1). Avatars are per-client Lua; a map cannot force them cleanly. https://www.curseforge.com/minecraft/mc-mods/figura-extrafight , https://www.curseforge.com/minecraft/mc-mods/fightura , Modrinth API [V]
- Customizable Player Models (MIT) has no EF bridge found. EMF/CEM player models do not apply while EF renders the player. [V]/[?]

### 1.5 Future note
- EF dev plan (#2460, Feb–Apr 2026): run EF animations through Player Animation Library + Bendable Cuboids for vanilla entities and players in 26.x, keeping skeletal meshes for EF-based bosses (WoM, Casket of Reveries). A custom player mesh may need rework on 26.x; not relevant for 1.21.1. https://github.com/Antikythera-Studios/epicfight/issues/2460 [V]

---------------------------------------------------------------------
## 2. NPCs and bosses

### 2.1 EF mob patch with a custom model [V code]
- Datapack: `data/<modid>/epicfight_mobpatch/<entity>.json` with `model`, `armature`, `renderer`, `isHumanoid`, `faction`, `attributes{impact, armor_negation, max_strikes, chasing_speed, scale}`, `default_livingmotions`, `stun_animations`, `combat_behavior[{weight, canBeInterrupted, looping, cooldown, behaviors[{conditions, animation}]}]`, `humanoid_weapon_motions`; conditions `random_chance, within_eye_height, within_distance, within_angle, within_angle_horizontal, health`. pack_format 48 for 1.21.1. https://epicfight-docs.readthedocs.io/Guides/Entities/page1/ [V]
- `renderer: "epicfight:custom"` → `PCustomEntityRenderer` / `PCustomHumanoidEntityRenderer` that draws `Meshes.getOrCreate(model)` with **the texture returned by the entity's original renderer** (`renderer.getTextureLocation(entity)`), render type `entityCutoutNoCull` (no translucency). Armature from `Armatures.getOrCreate(armature)` — any joint layout. Source: `client/events/engine/RenderEngine.java` (registerCustomEntityRenderer), `api/data/reloader/MobPatchReloadListener.java`. [V]
- Consequence: a **GeckoLib entity patched by EF is drawn as the EF mesh**; its GeckoLib model and animations do not show. Bosses that should fight in EF style must exist as an EF mesh + armature + Blender-made EF animations (or animations built by our converter/Blender scripts). The GeckoLib texture can be reused if the EF mesh keeps the same UVs (same source model). [V]/[?]
- Code-level patch for our own entities: `HumanoidMobPatch` subclass, `EntityPatchRegistryEvent`, `Armatures.registerEntityTypeArmature`, patched renderer via the register event. https://epicfight-docs.readthedocs.io/API/Starting/ [V]
- In-game Mob Capabilities editor and asset importer write the same datapack. https://epicfight-docs.readthedocs.io/hr/Guides/Entities/page2/ , https://epicfight-docs.readthedocs.io/Guides/page3/ [V]
- Shader risk: `epicfight:custom` entities showed broken textures under Complementary and Bliss on 1.20.1 (#1921, open). Re-test on 1.21.1 + Iris 1.8.13 in the benchmark arena. https://github.com/Epic-Fight/epicfight/issues/1921 [V]
- EF also ships GeckoLib/AzureLib **armor** transformers (`compat/geckolib/client/GeoModelTransformer.java`) — they bake GeckoLib armor cubes onto biped joints, i.e. EF itself already converts cube models to EF meshes for armor. [V]
- KubeJS: EF has a built-in KubeJS plugin (custom skills, `EFUtilsJS`). `compat/kubejs/` [V]

### 2.2 Non-combat NPCs
- **GeckoLib 4.9.3** (NeoForge 1.21.1, 2026-09-16) entity in our mod: the Blockbench model as is, triggerable animations, sound/particle keyframes. [V Modrinth API]
- **Easy NPC 7.15.0** (NeoForge 1.21.1, 2026-10-12; Modrinth license MIT, 1.22M DL): dialogs (trees, conditions, typewriter effect, button conditions since Jun 2026), trading, actions, objectives. NPC types include **Easy Model NPC** (renders an **Easy Model Entities** profile; pose editor matches bones named `head, body, left_arm, right_arm, left_leg, right_leg …`), Doppler NPC (renders another entity type), and `[EF]` Epic Fight NPCs (EF combat; skin-based biped). https://github-wiki-see.page/m/MarkusBordihn/BOs-Easy-NPC/wiki/Types , .../ModIntegration , .../CustomModels , https://github.com/MarkusBordihn/BOs-Easy-NPC/wiki/Skins [V]
- **Easy Model Entities 2.5.0** (Kaworru; MIT on Modrinth; NeoForge 1.21.1 build 2026-10-12; "early release, formats may change"): loads **`.bbmodel` directly** from resource packs, data-pack profiles, plays Blockbench clips named `idle/walk/attack/hurt/death/sit` automatically and others by command/API, Blockbench exporter plugin. https://github.com/MarkusBordihn/BOs-Easy-Model-Entities/blob/1.20.1/README.md , https://modrinth.com/mod/easy-model-entities [V]
- Touhou Little Maid (CC-BY-NC-SA-4.0; 1.21.1 build exists) uses data-driven Bedrock model packs and can render YSM models; its Epic Fight addon (EpicFight：TouhouLittleMaid 1.3.x) is **1.20.1 only**. The useful idea is the pattern (one Bedrock geo reused by player and NPC entities), not the mod. https://modrinth.com/mod/touhou-little-maid , https://mcmodshub.com/mod/257432 [V]
- Combat companion (e.g., Heather in a boss fight): our own EF-patched humanoid with an allied faction (code patch), not TLM. [?]

### 2.3 Dialogue portraits
- **VNDialog 1.0.6** (YourZi; MIT; 1.21/1.21.1 NeoForge + Forge; ~1M CurseForge DL): visual-novel dialog box, multiple standing portraits with entrance animation (`assets/dialog/textures/portraits`, auto-scaled to 0.7 of window height), branching options, voice audio, commands run per entry, background images, speaker entity. Data pack `data/dialog/dialogs/*.json`, command `/dialog show <id>` (a mod command; this is not the 1.21.6+ vanilla `/dialog`, but keep the naming clear in docs). https://modrinth.com/mod/nvdialog , https://github.com/Chakyl/SVDialog [V]
- Easy NPC dialogs have no portrait image (feature request #513 open). https://github.com/MarkusBordihn/BOs-Easy-NPC/issues/513 [V]
- Portrait source options: (a) render the actual in-game model at bust framing (bbmodel_render / Blockbench screenshot) + pixel paintover — consistent with the 3D model and no image-model licensing questions; (b) image-model illustration from the approved reference sheet (must match the model; disclose AI use). [?]

---------------------------------------------------------------------
## 3. Cutscenes and one source model across systems

| Runtime | Same character as gameplay? | 1.21.1 limits | Agent-authorable? |
|---|---|---|---|
| **EF entity** (player or patched NPC/boss) | Yes, same mesh | Animations made in Blender on the EF armature; `/epicfight animator play <targets> <animation> [transitionTimeModifier]`, `soft_pause`, `hard_pause` (perm 2) | Yes via bpy scripts + exporter; data-pack functions for timing [V command in `server/commands/AnimatorCommand.java`] |
| **GeckoLib entity** (non-combat NPC) | Yes, same `.bbmodel` | Needs our mod (renderer/model classes); triggerable animations | Yes: headless bbmodel MCP keyframes + validators [V] |
| **YSM player** (route B) | Yes | `/ysm play <animation>` forces player animations | Yes (Bedrock animation JSON) [V] |
| **Animated Java rig** | Copy of the model, separate export | Each bone with cubes = one `item_display`; cube rotations must obey 1.21.1 item-model rules or get their own bone; **texture-slot switching / keyframes need 1.21.4+** (on 1.21.1 only whole Variants switch); Iris glow weak (#3053) | Partly; AJ blueprints are not covered by the MCP tools [V docs: https://animated-java.dev/docs/core-concepts/texture-slots , https://animated-java.dev/docs/nodes/groups , FAQ: supports 1.20.4–26.3] |

- Recommendation [?]: cutscenes with characters run **in-engine on the real EF/GeckoLib entities**, camera by Director's Camera, timeline by data-pack functions. AJ only for set pieces that are not a main character (collapsing structures, giant props) or for a far-away stand-in. This keeps one look per character and avoids maintaining AJ copies.
- The EF Blender exporter also exports camera data (fork for 4.1 and the official addon) — runtime camera playback in 21.17 not verified [?]. https://github.com/sentwayfarer/ef-blender-4.1-json-exporter
- One-source rule (see §6): every export is generated from the approved `.bbmodel` by a script; never hand-edit an export.

---------------------------------------------------------------------
## 4. Performance (RTX 4060 / Ryzen 5 5600, Iris, ≥50 fps)

Facts:
- EF default player: 472 triangles, 20 joints (measured). [V]
- Detailed Blockbench anime characters on Sketchfab: "Anime girl minecraft style" 3.9k tris / 2.6k verts; "Anime Wuxia Girl" 4.4k tris / 2.9k verts; "Elf | Minecraft Girl" 7.1k tris; a simple "32x anime elf" 290 tris. A cube is 12 triangles, so ≈ 300–600 cubes for detailed ones. https://sketchfab.com/3d-models/anime-girl-minecraft-style-8eb0821c4e3943eba7b2a2b0d9b30c04 , https://sketchfab.com/3d-models/anime-wuxia-girl-blockbench-aca6550b20134308815e116f9139da4a , https://sketchfab.com/3d-models/elf-minecraft-girl-blockbench-75d561743b884ccbaba758deb42e165a [V counts]
- EF skins on the GPU via compute shaders, with an Iris init path; EF FPS Optimizer reduces distant animation cost (from round 1). [V]
- YSM preloads every model on the client (a server with ~1,000 models needed 24 GB) — irrelevant with a handful of models, but don't ship model collections. https://github.com/YesSteveModel/YSM-Wiki-Issues/issues/358 [V]
- EpicYSM caps extra joints so the armature is ≤40 joints. [V code]

Suggested budget [?, to confirm in the G6 arena]:
| Asset | Cubes | Joints/bones | Texture (32 px/block) |
|---|---|---|---|
| Player (EF mesh, always on screen, close camera) | 250–400 | 20 biped + ≤12 extra (hair, coat tails) | 256² |
| Story NPC (GeckoLib/EME) | 150–300 | ≤30 bones | 128²–256² |
| Combat NPC / rival Blader (EF mesh) | 250–400 | ≤32 | 256² |
| Boss (EF mesh) | 400–800 | ≤50 | 512² |
- Rough arithmetic: boss 800 + player 400 + 4 mobs × 150 = 1,800 cubes ≈ 21.6k triangles, ×2 with the shader shadow pass. That is small for an RTX 4060; the risk is CPU-side work per entity (bones × entities, vanilla-path layers, GeckoLib bone processing) and shader-pack entity shadows. Measure with spark + frame-time capture, then cut joints before cubes.

---------------------------------------------------------------------
## 5. AI-assisted character creation (evidence and tools)

### 5.1 Image/text → cube model tools
- **img2blockbench** (orca-gamedev, MIT, Jul 2026): three routes (image → external 3D mesh → cuboid rebuild; image → cuboid spec directly; image → img2threejs → cuboids), deterministic compiler, audits (UV-density outliers, "flat detail cuboids"), Claude/Codex skill. Benchmarks are animals at **≈20–28 cuboids**; silhouette **IoU 0.57–0.68** vs the source mesh; README: smooth character illustrations are "not a valid direct-route input" — restyle to a Minecraft concept first. https://github.com/orca-gamedev/img2blockbench [V]
- **BlockSmith** (gbusto, MIT, alpha v0.0.1, Gemini 2.5 Pro by default): text/image → block model, GLB↔bbmodel convert, animate. Write-up: all image-to-3D tools output watertight high-poly meshes, image models are poorly trained on blocky pixel style, nearest filtering matters, his texturing went from per-material tileable swatches to orthographic-view projection with ControlNet canny (2×2 view grid, LLM "texturing strategy" for hidden faces). https://github.com/gbusto/blocksmith , https://gbusto.github.io/blocksmithai.html [V]
- Commercial: Codella (text → .bbmodel, "first ninety percent"), Brikk (paused free tokens; ~$1.33/model per a commenter). https://codella.ai/blockbench-model-generator , https://brikk.lootvote.com/ [C]
- Agent skills on Blockbench MCP: pi-blockbench (procedural `model.js/texture.js/animation.js`, glowmask, checks; demo by DeepSeek V4 Flash), hairyf `minecraft-model` skill (image model makes design + three views, then MCP build, screenshot loop), mcpmodel `blockbench_build_from_reference` (blueprint, dry-run cube counts, mandatory four-view turntable). https://github.com/DexerMatters/pi-blockbench/blob/master/README.md , https://www.skills.sh/hairyf/skills/minecraft-model , https://glama.ai/mcp/servers/haotranq1234/mcpmodel/tools/blockbench_build_from_reference [V]
- Mesh → cubes: "Mesh to Cubes Voxelizer" Blockbench plugin (PR #863, merged Jul 2026), MrXiaoM convert-mesh-to-cube (MIT), PublicDark converter. Voxelized AI meshes are many small cubes, poor for rigging; use as a **reference underlay** (Blockbench 5.2 Reference Models), not as the asset. https://github.com/JannisX11/blockbench-plugins/pull/863 , https://github.com/MrXiaoM/blockbench-plugin-convert-mesh-to-cube [V]/[?]
- "gltf_to_minecraft" plugin: not found under that name; closest are gltf2mc (CC0) and the voxelizers above. https://github.com/keanzelgoh/gltf2mc [V]

### 5.2 Quality evidence for LLM/agent modelling
- YouTube demos (Oct 2026) build simple animals with Blockbench MCP; one creator: "make sure it's Minecraft-style, as complex things cannot be analyzed by your AI"; the player skin in his demo was not AI-made. https://www.youtube.com/watch?v=3Qql8yy7rzQ , https://www.youtube.com/watch?v=T4nUwow5CLk [C]
- 3DCodeBench (Google DeepMind, Jun 2026, 12 VLMs): failures are mostly API mismatches; successful renders still have **disconnected or floating parts**; more thinking and multi-turn refinement help. https://arxiv.org/abs/2606.01057 [V]
- P3D-Bench (Jun 2026): models recover global shape and identity but **fail precise geometry and part composition** in assemblies. https://arxiv.org/abs/2606.11152 [V]
- BLOCK (ShanghaiTech, arXiv 2603.03964): "current powerful MLLMs fail to generate Minecraft skin from character concept" one-stage; two-stage pipeline (Nano Banana Pro preview → fine-tuned FLUX.2 → 64×64 skin), weights on HF (AliceKJ/BLOCKv0.5). Only for vanilla 64×64 skins. https://arxiv.org/abs/2603.03964 [V]
- r/Blockbench is hostile to AI generators ("Ew", "results don't look good or useful"; Brikk posts removed). https://www.reddit.com/r/Blockbench/comments/1uq0ysy/ , https://www.reddit.com/r/Blockbench/comments/1v1p703/ , https://www.reddit.com/r/Blockbench/comments/1vrdfc5/ [C]
- Conclusion [?]: an agent can build a good anime cube character only with (1) an approved orthographic turnaround, (2) a bone/proportion template, (3) deterministic validators (floating parts, symmetry, UV density, budget), (4) render-compare loops against the turnaround (silhouette IoU per view, like img2blockbench's overlap audit), and (5) user review. Expect the face and hair to need the most iterations.

### 5.3 Reference sheets with image models
- PixelDojo test (2026-08-26): Seedream 5 was the only model of three that returned a real labelled front/side/back sheet with consistent identity; a "consistent characters" tool locked identity best but returned separate frames; Qwen Image Max cropped at the chest. https://pixeldojo.ai/best-ai-model-for-character-turnarounds [C, vendor]
- BLOCK found Nano Banana Pro the only model that consistently made Minecraft-style front/back previews. [V paper]
- The project pipeline already plans Codex image generation for concept art (pipeline §5.0). Use the image model for the 2D sheet; ask for orthographic A-pose, flat light, separate head close-up; then the user approves.

### 5.4 Image → 3D generators (for reference underlays only)
- TRELLIS.2 (Microsoft, MIT, 24 GB GPU, Linux) — not runnable on an RTX 4060 8 GB; use a hosted space. TripoSR (MIT, ~6 GB). **Hunyuan3D 2.x community license does not apply in the EU, UK and South Korea.** https://triposr.org/blog/hunyuan3d-vs-trellis , https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE [V]
- Meshy: free plan outputs CC BY 4.0 (credit "Model created with Meshy"); paid = owned. https://help.meshy.ai/en/articles/16102098-can-i-use-meshy-assets-commercially [V]
- Tripo: free plan "Public Models · Non-Commercial Use"; paid = full rights. https://www.tripo3d.ai/pricing [V]

### 5.5 Pixel-art texture generation
- **PixelLab** (ToS updated 2025-11-23): you own outputs, commercial use allowed, no training other models on outputs, Open RAIL-M terms; API + MCP; strengths are 4/8-direction sprites, animations, tilesets. https://www.pixellab.ai/termsofservice [V]
- **Retro Diffusion**: hosted MCP (`https://mcp.retrodiffusion.ai/mcp`, Claude Code plugin `pixel-art@retro-diffusion`), pay-per-image from ~$0.01, 90+ styles incl. "MC Texture" (flat block textures), tilesets; ToS page not retrieved — license terms [?] (aggregator says commercial use allowed [C]). https://github.com/Retro-Diffusion/retro-diffusion-mcp , https://retrodiffusion.ai/styles/mc-texture-rd-mini-mc-texture/ [V]/[?]
- Fit for 32 px entity atlases [?]: neither tool understands cube-face UV islands. Use them for (a) material swatches (cloth, leather, metal, hair strands) quantised to the art-bible palette, (b) dialogue portraits, (c) item icons. The agent places swatches into UV islands by script, then projects the turnaround for face/hair details (BlockSmith-style orthographic projection), then quantises to the palette, then touch-up.
- SkinMint (MIT, alpha): anime illustration → 64×64 skin → fixed box rig GLB; AI skin quality "fine, not great". Only useful for vanilla-skin extras. https://github.com/DohhhDo/SkinMint [V]

### 5.6 Distribution/AI policy reminders
- PixelLab/Retro Diffusion/Meshy outputs still fall under Modrinth AI disclosure and Planet Minecraft bans (round 1). Keep AI-use records (already in the pipeline).

---------------------------------------------------------------------
## 6. Recommended pipeline: one source model → player / NPC / boss / cutscene / portrait

**Source of truth**: `models/characters/<id>/<id>.bbmodel` (Blockbench 5.2.2, free/GeckoLib format, per-face UV, 32 px/block, one atlas, integer UVs). Bone-naming contract (so every converter is deterministic):
- Trunk: `root > body_lower(waist) > body_upper(chest) > head`; limbs `arm_upper_R/L > arm_lower_R/L > hand_R/L` (+ `tool_R/L` locator), `leg_upper_R/L > leg_lower_R/L > foot_R/L`; extras prefixed `phys_` (hair, skirt, coat tails, ribbons) or `prop_` (sheath, lantern).
- A rename table per target: EF joints (`Root, Torso, Chest, Head, Shoulder_R, Arm_R, Hand_R, Tool_R, Elbow_R, Thigh_R, Leg_R, Knee_R…`), YSM/EpicYSM names (`AllBody, UpBody, UpperBody, Head, RightArm, RightForeArm, RightHand, RightLeg, RightLowerLeg…`), EME pose names (`head, body, left_arm…`).
- Parts tag for EF HumanoidMesh: each cube labelled into one of the 12 parts (`head/hat/torso/jacket/leftArm/leftSleeve/...`); sleeves/gloves in `*Sleeve` so first person shows them.

**Exports (scripted, regenerated on every approved change)**:
1. Player → EF mesh JSON (rigid weights, re-proportioned biped armature, optional physics joints) → RP override of `epicfight:animmodels/entity/biped(.._slim_arm).json` + forced texture in our mod. Prototype first with YSM 2.6.5 + EpicYSM 1.1.3 using the YSM-name export.
2. Combat NPCs/bosses → EF mesh + armature (+ Blender EF animations made to the move sheet) → `epicfight_mobpatch` with `renderer: "epicfight:custom"`, same texture as the GeckoLib export.
3. Story NPCs → GeckoLib geo/animation export (our mod) or Easy Model Entities profile + Easy NPC (no Java).
4. Cutscenes → the same entities via `/epicfight animator play`, GeckoLib triggers, `/ysm play` (if route B), Director's Camera; AJ copies only for non-character set pieces.
5. Portraits → fixed-camera bust renders of the model + paintover → VNDialog portraits.

**Gates** (add to G3/G5/G6): bbmodel_validate (floating parts, symmetry), EF-mesh validator (12 part names present, every vertex weighted, joints ⊂ armature, ≤40 joints), per-target budget check, 6-view contact sheet vs turnaround IoU, in-game EF + Iris screenshot (Complementary/Photon) for #1921-type texture bugs, spark frame time in the boss arena.

**AI-assisted creation loop per character**:
1. Image model → turnaround (front/side/back + head close-up) and palette → user approves (G8 for the reference).
2. Optional 3D underlay (TripoSR/TRELLIS.2 hosted/Meshy paid; not Hunyuan3D in Korea) as a Blockbench reference model.
3. Agent builds cubes on the bone template via headless bbmodel MCP; validator + 6-view IoU loop.
4. UV/texture: per-face islands at 32 px; swatches (PixelLab/Retro Diffusion or scripted ramps) + orthographic projection of the turnaround for face/hair; palette quantisation; Blockbench paint touch-up on the PC.
5. Exports §6, in-game check, user review, iterate.

---------------------------------------------------------------------
## 7. Open questions / tests to run
1. Route A prototype: override `biped.json` with a 300-cube anime mesh (rigid weights) and force the texture; check third person, first person, weapon trails, `Tool_R` grip, and Iris + Complementary/Photon. Also check what else in EF uses `Meshes.BIPED`.
2. Does `epicfight:custom` still break textures under shaders on 1.21.1 (#1921)?
3. Which exporter writes `cloth_info` for custom meshes (capes/hair/skirts)?
4. Route B: does EpicYSM 1.1.3 work with EF 21.17.3.1 + Iris 1.8.13 + our other mods; how does `/ysm model set ... true` behave on a fresh single-player world (first-join function)?
5. Easy Model Entities on 1.21.1 NeoForge with GeckoLib 4.9.3 side by side; can an EME NPC be EF-patched?
6. Does `/epicfight animator play` work on the player in cutscenes without EF battle mode, and how do transitions back to living motions look?
7. Budget numbers in §4 against measured frame time in the benchmark arena.
