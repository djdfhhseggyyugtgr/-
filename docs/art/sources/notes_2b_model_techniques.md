# Anime-style female characters built from cubes: technique handbook (round 2, branch 2b)

Date: 2026-10-14. Scope: concrete, cube-level techniques for building original anime/subculture-style female NPCs and bosses in Blockbench for Minecraft Java 1.21.1 + NeoForge (GeckoLib 4.9.3, Epic Fight 21.17.3.1, Animated Java 1.11), at 32 px/block with per-face UV.

**Content rule (from CONTEXT.md):** body-shape techniques (section 5) apply to adult characters only. The child character Daisy gets an age-appropriate design: simple shapes, modest clothing, no body shaping. Everything here is non-sexual.

**Legend:** **[V]** checked against a primary source (official docs, source code, or a model/animation file I parsed). **[C]** community practice (tutorial video, Reddit, fan wiki). **[E]** my own synthesis or proposal, not sourced. **[?]** uncertain, needs a test.

**Raw data:** `research/r2/2b/` (Ollama search/fetch JSON), `research/r2/2b/yt/` (YouTube transcripts), `research/r2/2b/social/` (Reddit and YouTube search dumps), `research/r2/2b/tlm/` (parsed Touhou Little Maid model and animation), `research/r2/2b/ef/` (Epic Fight biped mesh), `research/r2/2b/gl/` (GeckoLib 1.21.1 source), `research/r2/2b/_raw_findings.md` (working log). Analysis scripts: `scripts2b/geo_stats.py`, `scripts2b/geo_detail.py`.

---------------------------------------------------------------------

## 0. Key findings and decisions to raise with the user

1. **The best reference is a professional anime cube model I parsed.** The Touhou Little Maid "winefox_elf" GeckoLib model has 225 bones and 513 cubes (including a second fox form and GUI parts). 359 of the cubes are rotated, 123 are inflated, 512 use per-face UV, and 87 have a dimension under 1 unit. The texture is 256×256 at about 1 texel per unit, and the model is rendered at 0.65–0.70 scale. It shows how professionals build eyes, blinking, expressions, skirts and hair in cubes, and most of sections 3, 4 and 6 build on it. [V data] Source: `https://raw.githubusercontent.com/TartaricAcid/TouhouLittleMaid/1.20/src/main/resources/assets/touhou_little_maid/tlm_custom_pack/touhou_little_maid-1.0.0/assets/geckolib/models/entity/winefox_elf.json` and `.../geckolib/animation/winefox_elf.main.animation.json`. This is reference only: TLM is CC-BY-NC-SA, so we copy techniques, never geometry or textures.
2. **The professional YSM/TLM look relies on mixels.** Pupils, highlights and mouth lines are cubes with negative inflate (−0.3 to −0.5) or 0.1-unit trims, which gives sub-pixel detail. Our `art-bible.yaml` forbids mixels. The house style therefore has to be "anime in a vanilla_plus grid": every facial feature is at least 1 texel (0.5 unit at 32 px/block) and sits on that grid. The first reference sheet should show this look to the user explicitly. [V data + contract]
3. **Proportions and face resolution trade off against each other.** At 32 px/block (2 texels per unit), a realistic anime adult of 5.5–6 heads at player height has a head about 5.5 units tall, so the face is only about 11 texels across. That is too small for anime eyes. Options for the user to decide [E]:
   - (a) A stylized "anime-lite" build of about 4.4–4.8 heads: head 7–7.5 units (face 14–15 texels), long legs. This is my recommendation.
   - (b) Build at 32 px per model unit and render at scale 0.75. The model stays mixel-free internally but is about 43 px/block in the world. This changes `hero_px_per_block`, so it is a contract proposal and needs approval. TLM uses the same trick, rendering at 0.65–0.70.
4. **Every cube face renders from both sides in GeckoLib 4.** The default render type is `RenderType.entityCutoutNoCull`. This has three consequences:
   - Hidden faces still cost fill and can show through gaps, so delete them.
   - A plane should have only one textured face. Two coplanar faces z-fight.
   - The "negative-size cube = inverted-hull outline" trick does not work by default.

   [V] `GeoModel.getRenderType` in `https://raw.githubusercontent.com/bernie-g/geckolib/1.21.1/common/src/main/java/software/bernie/geckolib/model/GeoModel.java`.
5. **GeckoLib 4 cubes support `inflate` and per-face UV, and skip missing faces.** A face set to null in per-face UV is not built, so deleting a face really saves geometry. Box UV floors cube sizes, which is where box-UV mixels come from. [V] `BakedModelFactory.java` (1.21.1 branch). GeckoLib 4 has no native mesh support. The GeckoMesh add-on ships builds for Forge 1.20.1–1.21.11, Fabric and NeoForge 26.x, but has no NeoForge 1.21.1 jar. **Use cubes only.** [V] `https://www.curseforge.com/minecraft/mc-mods/geckomesh`
6. **A cube model can feed Epic Fight.**
   - EF animations made on the EF player rig "can be applied to any biped (humanoid) entity". [V] `https://epicfight-docs.readthedocs.io/Guides/page1/`
   - The EF humanoid joints are verified from the 1.21.1 source and `biped.json` (section 8).
   - EpicYSM (Sep 2026, 1.21.1 NeoForge) converts readable YSM cube models into EF's format at runtime. [V] `https://www.curseforge.com/minecraft/mc-mods/epicysm`
   - So the plan of one Blockbench cube model, then GeckoLib export plus an EF mesh (via Blender, or via our own converter), is realistic. [E]
7. **Use geometry for blinking and expressions, not animated textures.**
   - GeckoLib 4 animated textures (`.png.mcmeta`) do not work with emissive glowmasks, and they animate every instance in sync. [V] `https://github.com/bernie-g/geckolib/wiki/Animated-Textures-(Geckolib4)`
   - In Animated Java 1.11, per-slot texture switching needs MC 1.21.4+, so on 1.21.1 only whole Variants can switch textures. [V] `https://animated-java.dev/docs/core-concepts/texture-slots`
   - So blink with bone scale or visibility. [E]
8. **NPCs have no budget line in `perf-budget.yaml`.** Proposal: main NPC ≤ 300 cubes (elite tier), hero boss ≤ 500, both after deleting hidden faces, with texture ≤ 256×256 at 32 px. The contract has to be changed by a human. [E]

---------------------------------------------------------------------

## 1. Ground rules for anime cube characters at 32 px/block

| Rule | Detail | Tag |
|---|---|---|
| Density | 32 px/block means 1 model unit (1/16 block) = 2 texels. In Blockbench, use Create Texture with Template and **resolution 32**. The generator maps 16 units to 32 px. | [V] `https://deepwiki.com/JannisX11/blockbench/6.5-texture-generation` |
| Grid | Cube sizes and positions go in multiples of **0.5 unit**, so 1 texel is the smallest feature. Offsets used only for anti-z-fighting (0.01–0.05) are the exception. | [E] from mixel rule |
| UV mode | Per-face UV, `box_uv: false`. Box UV floors non-integer sizes, which creates mixels. | [V] GeckoLib source; [C] r/Blockbench 1tmzhye, 1uxr7ra |
| Mixels | Do not use negative inflate for pupils or mouth lines, and no cubes under 0.5 unit. Small positive inflate on overlay layers (hair cap, sleeves) is acceptable up to about 1.1× stretch. Hytale allows 0.7–1.3× stretch for fixes; the Blockbench style guide allows "slightly inflated elements". | [V] Blockbench Minecraft Style Guide; [V] Hytale guide |
| Shape | The silhouette comes from cubes and the detail from texture. Use rotated cubes for slants rather than stair steps. Rings of rotated cubes forming curves are "not vanilla". YSM modelers do it heavily, so cap it (proposal: ≤ 30% rotated cubes). | [V] style guide; [C] Minto 0AKabk-2Ot8; [E] cap |
| Planes | Use a 0-thickness cube with only the north face UV'd. Because of NoCull it shows from both sides, mirrored. Never texture both faces of a plane. | [V] GeckoLib NoCull; [C] TLM troubleshooting `https://www.mcmod.cn/post/2603.html` |
| Hidden faces | Delete faces you can never see (under the hair cap, inside the torso, cube ends tucked into other cubes). With NoCull they cost fill and can flicker through. | [V]+[E] |
| Overlap instead of stitching | Let parts intersect rather than build edge loops, and float thin detail planes over the surface. | [C] blockbench-mcp skill `https://raw.githubusercontent.com/jasonjgardner/blockbench-mcp-project/refs/heads/main/skills/blockbench-modeling/SKILL.md` |
| Z-fighting | Separate coplanar faces by 0.01–0.05 unit. TLM eyes sit 0.01–0.05 in front of the face, and legacy TLM blink planes 0.001. The Bedrock wiki says to inflate one cube by ±0.01. TLM hair strands are 1.02 wide, so neighbours overlap without sharing a plane. | [V data]; [V] `https://wiki.bedrock.dev/visuals/bedrock-modeling.html` |
| Translucency | Avoid semi-transparent pixels and use 0 or 255 alpha (cutout). YSM docs warn of render errors with stacked translucent textures. | [V] `https://yesstevemodel.github.io/wiki/texture/` |
| Shared UV trap | In Create Texture, untick **"double_use"** (reuse identical faces) for anything you paint asymmetrically. Otherwise you get "I paint the hair and skirt at the same time". | [V] option list in Blockbench deepwiki; [C] r/Blockbench 1lrmpzq |

---------------------------------------------------------------------

## 2. Proportions and a unit sheet (adult female, proposal)

**Reference measurements** from the winefox model, measured in-file:
- Head 7×7×7 units.
- Legs from 0 to the hip pivot at about 19 units, which is about 49% of the 38.7-unit body height without hair.
- Total height is about 5.5 heads.
- Thigh 3.4×9×4, shin 3.35×8×4, upper arm 2.95×7×3.53.
- Rest-pose arms are rotated ±18° on Z (A-pose).

[V data]

**The vanilla player** is 32 units tall: head 8, torso 8×12×4, legs 12, arms 4 wide (3 for slim). [C, well known]

**Proposed house sheet [E].** All values are in model units at 32 px/block, with 1 unit = 2 texels.

| Part | Size (W×H×D) | Pivot / notes |
|---|---|---|
| Total height | ≈ 31–31.5 (≈1.95 blocks) without hair volume | Keep the neck at y≈24 so the EF head joint and the vanilla eye height stay close. |
| Head | 7 × 7.5 × 7 (front face 14×15 texels) | Pivot (0, 24, 0). Use 7×7×7 to copy TLM exactly. |
| Neck | 2 × 1.5 × 2, tucked 0.5 into the head and the chest | Child of chest, or of head with the bottom face deleted. |
| Shoulders / upper chest | top slab 7 wide | y 21.5–23.5 |
| Waist | 5 × 2.5 × 3 | y ≈ 17–19.5 |
| Hips | 6 × 3 × 3.5 | y ≈ 13.5–16.5. Hip pivot at y = 13.5. |
| Arms | 2.5–3 W × 3 D. Upper arm 5.5, forearm and hand 5.5 | Shoulder pivot (±4, 22.5, 0) |
| Legs | thigh 3 × 7 × 3.25, tapering via a 2.5-wide knee cube; shin 2.5 × 6.5 × 2.75; foot 2.5 × 1.5 × 4 | Hip pivot (±1.5, 13.5, 0). Knee pivot y ≈ 7. |

- Legs end up about 43% of height, a compromise between the anime look and EF biped compatibility (the vanilla hip is at 12).
- With the 7.5-unit head, the figure is about 4.2 heads tall; hair volume makes it read taller.
- **Daisy (child), age-appropriate:** about 22–24 units tall, head 7×7×7 (about 3.2 heads). Use one straight torso cube plus a dress or coat, with no waist or chest shaping and simple boots. Keep the same eye and blink system so she is equally expressive. [E]

---------------------------------------------------------------------

## 3. Head and face

### 3.1 Head shape
- **A single head cube is the professional default.** The winefox head is one 7×7×7 cube, and the legacy TLM Reimu head is one 8×8×8 cube. Hair adds the roundness. [V data]
- **Rounding:** Minto (YSM) rounds the head with "a lot of cubes, rotated bit by bit". To find the chin line, duplicate the head and scale it to half height. [C] `https://www.youtube.com/watch?v=0AKabk-2Ot8`
- **House recommendation [E]:**
  - One head cube.
  - Optionally one 6×1×6 "jaw" slab under it, inset 0.5 on each side, to soften the chin.
  - Optionally 4 cheek bevel cubes (0.5–1 wide, rotated ±22.5° on Y, inside the head bounds) only if the user wants a rounder face.
  - Hair hides the top corners, so do not round them.
- **Feature placement (anime):**
  - Winefox eyes span 1–3 units above the chin of a 7-unit head, so the centre sits at about 29% of head height. Brows sit about 0.5–1 unit above the eyes, and the mouth sits about 0.5 unit above the chin. [V data]
  - Bangs cover the upper half of the head.
  - On a 14×15-texel face: eyes on texel rows 8–12 from the top, brows on row 6–7, mouth on rows 13–14. [E]

### 3.2 Eyes: three proven constructions

**A. Painted eyes with a closed-eye overlay plane** (legacy TLM). An 8×8×0 "blink" plane sits 0.001 in front of the face. It carries the closed-eye texture and is shown at random. This is the cheapest method, with 1 cube. [V data, `research/r2/2b/tlm2`]

**B. A layered eye stack in front of a painted closed-lid line** (winefox, the professional method). [V data] Hierarchy:
```
Eyes
├─ EyeBrow ─ RightEyebrow (1.1×1×1 + 2×1×1), LeftEyebrow
└─ Eyelid
   └─ RightEyelid      2×2×1 cube, 0.01 in front of the face  (sclera + lash, "open eye")
      ├─ ysmGlowRightEyelidBase (emissive duplicate of the iris)
      └─ RightEyelidBase 1.4×2×1                              (iris)
         ├─ RightEyePublic 1.15×1.5×2, inflate −0.3            (pupil)
         └─ ysmGlowRightEyeDot 1.2×1×1, inflate −0.35          (highlight, emissive)
```
- Blink by scaling `RightEyelid` Y to 0. The pivot is about 0.5 unit above the eye bottom, so the whole stack collapses onto the closed-lid line painted on the head texture.
- Sleep is the same with Y scale 0. A sad face uses Y scale 0.78.
- Eye tracking moves the iris and pupil inside the white.

**C. Separate lash, sclera, pupil, brow and lid cubes** (Minto YSM tutorial). [C] `https://www.youtube.com/watch?v=8fs7yP0T21Q`
- The upper lash is curved with sharp, anime-style ends.
- The lower lash is a separate cube that hides when blinking.
- The sclera fits inside the lash. The pupil has rounded corners "so it looks nice when it moves".
- Push the middle eye cube forward while painting.
- Paint the iris dark at the top and light at the bottom, and add glow inside the iris.
- Extra lash detail goes on a see-through cube.

**House recommendation for 32 px with no mixels [E]:**
- Per eye, one open-eye plane of **2.5 × 2.5 units (5×5 texels)**, 0.02 in front of the face. Paint the upper lash, sclera, iris (3×4 texels), pupil (1–2 texels) and a 1-texel catchlight on it.
- Optional: a separate iris/pupil plane of 1.5 × 2 units (3×4 texels) 0.04 in front, for eye tracking. Move it only in 0.5-unit (1-texel) steps, clamped inside the white.
- Paint the closed-eye line (and the lower lash, if any) into the face texture under the plane.
- Blink: scale the open-eye plane's bone Y from 1 to 0, with the pivot on the painted lid line.
- Brows: a 2 × 0.5 unit plane (4×1 texels) on its own bone. Rotate it ±5–10° on Z and move it ±0.5 on Y for emotion.
- Emissive catchlight: only for magical or android characters (for example our android Aloe). Use a `_glowmask` texture (GeckoLib AutoGlowingGeoLayer). This is why blinks must use geometry and not `.mcmeta` (section 0, item 7).

### 3.3 Eye and expression painting rules
These come from pixeli eye rules, which are [C]: `https://pixeli.pebbly.space/knowledge/rules/33-eyes-and-expressions`
- Eyes are the last thing to lose pixels. Cut brows or nose first.
- The **whites are not white**. Use the lightest skin tone or a pale grey-blue. StrangeLifeKim adds that real whites are slightly pink. [C] `https://www.youtube.com/watch?v=bagRNBqCwUs`
- Use **one catchlight** in the same place on both eyes. Villains and blank stares get none.
- A **centred pupil on a camera-facing face reads as a dead stare.** Offset it 1 px, or set it low.
- **Brows carry the emotion with 1 px of tilt:**
  - inner end down = angry
  - inner end up = sad or worried
  - one brow 1 px higher = puzzled
  - Leave a 1-px gap between brow and eye, except for anger and determination.
- **Break symmetry by 1 px.** A perfectly symmetric expression reads as a mask.
- **The closed lid is darker than skin.** Lids never wobble and eye pixels never jitter.
- **Expression recipes at a 32 px head:**
  - happy = closed `^` arcs, mouth corners up, blush
  - angry = inner brow down touching the lid, top lid row hidden
  - sad = inner brow up, pupils low, mouth corners down
  - surprised = brows raised, white all round, small pupil, round O mouth
  - hurt = squeezed `> <`, grimace
  - determined = flat low brows, half lid
- r/Blockbench: "Mixels are evil. Try making the eye 3x3" (1vjx5qn) and "add some shines to those eyes so he looks less soulless" (1q3sgt4). [C]

### 3.4 Nose, mouth, blush
- **Nose:** "a cute spot", 1 texel of the skin shadow colour. [C] Minto
- **Blush:** 2–3 texels of pinkish skin highlight under the eyes. [C] Minto
- **Mouths:** winefox keeps the mouths as separate bone groups (`Mouth_chill`, `Mouth_surprise`, `Mouth_smile`, `weixiao`), built from inflate −0.5 cubes. Ours are 0.5-unit-thick or 0-thick planes painted at 1 texel per line. [V data / E]
  - Mouth set to model: closed line (3–5 px), small open, wide open, smile, frown, O. That covers dialogue beats.
  - Pixeli: swap on beats rather than letters, and hold each shape at least 2 frames (80–100 ms). [C]

### 3.5 How expressions switch, per runtime

| Runtime | Method | Tag |
|---|---|---|
| YSM | Blink in a `pre_parallel` animation (about 4 s). It has lower priority than the main animations, so the closed eyes in the sleep animation win. `parallel` overrides main animations and blends rotation additively, but not position or scale. Minto mirrors the keyframes for the second eye and uses "step" interpolation. | [V] `https://yesstevemodel.github.io/wiki/animation/parallel/`; [C] `https://www.youtube.com/watch?v=G_eLsOaeebE` |
| TLM / YSM (winefox) | `parallel5` uses Molang on the variable `v.exp`: `Expression {"scale": "(v.exp==0)?0:1"}` and `Expression_N {"position":[0,0,"(v.exp==N)?-1:0"]}`. The active expression is pushed 1 unit forward, in front of the neutral face, and the neutral `Mouth` is scaled to 0. Hunger state: brows rotate ±5°, eyelid scale 0.7, swapped mouth (`ysm.food_level<=6?…`). | [V data] |
| TLM legacy | A bone named `blink` is shown at random by the mod. `ahoge` follows the head and sways. `sinFloat`/`cosFloat` are ribbons that bob. `helmet` and `-helmet` show or hide by armour state. | [V] `https://www.mcmod.cn/post/2603.html` |
| GeckoLib 4 (ours) | (1) Scale keyframes (0 hides a bone) in a **separate face AnimationController** that never keys body bones. (2) Java: `FastBoneFilterGeoLayer` or `setCustomAnimations` calling `setHidden` on bones from synced entity data (expression id); reset when the condition ends. (3) Whole-texture swap with `GeoModel#getTextureResource(animatable)` per state; each variant needs its own `_glowmask` if emissive. (4) Not recommended: `.mcmeta` animated textures (global sync, no glowmask). | [V] GeckoLib wiki Render Layers and Geo Models; [E] controller split |
| Epic Fight (bosses) | EF meshes have named `parts` (vanilla biped: head, hat, torso, jacket, rightArm, rightSleeve…), and the EF API can hide parts. Face expressions on an EF-rendered mob would need custom renderer code. Proposal: EF bosses keep open eyes in combat, and expressions happen in GeckoLib or Animated Java cutscenes. | [V] parts in `biped.json`; [?] runtime toggling |
| Animated Java (cutscenes) | On 1.21.1, use **Variant** keyframes (whole variant) or bone scale. Texture Slot keyframes need 1.21.4+. The AJ 1.11 default target version is 26.2, so it must be set to 1.21.1. Stay within the contract's ≤ 40 bone groups with cubes, so put the eyes in one bone. | [V] `https://animated-java.dev/docs/core-concepts/texture-slots`, `/docs/resources/upgrading-to-1-11` |
| Figura (reference only) | `ModelPart:setUV` shifts a whole cube's UV over frames on a strip. Split the face into its own cube first. | [C] `https://manuel-3.github.io/animated-texture/` |

### 3.6 Blink and eye-life timing
- **Winefox** `pre_parallel3`, a 7.04 s loop:
  - Eyelid scale Y goes 1 → 0 at 0.083 s, holds to 0.167 s, and returns to 1 at 0.25 s (catmullrom). The brows dip 1.5 units at the same time.
  - A second blink comes at about 4.1 s.
  - After each blink the highlight wobbles and decays: `math.lerp(0, math.sin(q.anim_time*1440)*1, math.exp(-q.anim_time*5))`.

  [V data]
- **Pixeli:** at ≥ 24 px heads, half → closed → half for 50/80/50 ms. Blink every 2–4 s, on a different period from breathing. [C]
- **OutLandishly Crafted:**
  - Blink is "just a scale" with the **pivot at the top**. Alternatively, pop the lid in and out on Z.
  - "Don't do it exact", so vary the numbers.
  - Swap mouths by visibility.
  - Add random look-away idles, because staring NPCs feel unnatural.

  [C] `https://www.youtube.com/watch?v=Wi3Isin7Hjo`
- **Eye tracking (winefox `parallel1`):** pupil position x = `head_yaw/360`, y = `head_pitch/360`; iris base yaw/180, pitch/720. [V data] In GeckoLib, drive it from `query.head_y_rotation` and `query.head_x_rotation` and clamp to 0.5–1 unit (1–2 texels). [V] Molang list in `https://github.com/bernie-g/geckolib/wiki/Molang-(Geckolib4)`; [E] clamp
- **House default [E]:**
  - Blink loop 6.4 s with blinks at 0.0 s and 3.9 s.
  - Closing takes 0.05 s, closed 0.08–0.1 s, opening 0.07 s.
  - Brows dip 0.5 during the blink.
  - Breathing runs on a 4.0 s loop, so the two never sync.

---------------------------------------------------------------------

## 4. Hair

### 4.1 Building blocks (winefox measurements) [V data]

| Piece | Winefox build |
|---|---|
| Base / cap | `BaseHair`, 30 cubes, made of **plates** rather than an inflated head: back 8×7×1, top 8×1×8, 6×1×7, side and edge strips 1×1×5, plus small rotated tufts 1.02×3×1. |
| Bangs | 8 cubes in `MBangs/Bangs`: 2×2×1 and 1×2.05×1.05. All rotated about **−7.5° X** (tilted forward off the forehead) and fanned with **Z −9° to +12°**, with a few tips at 57° and 120°. |
| Side locks | 10 cubes per side, 1.02 × (1–4) × (1–2), each slightly rotated (X −1 to −7°, Z −10° to +15°). Wrapper bones `MRightSideHair` / `MLeftSideHair`. |
| Long back hair | Chain `FLongHair > MLongHair > LongHair (2×6×1, 2×6×1, 8×6×1 at X 10°) > LongHair2 (3×6×1, 3×6×1, 9×7×1)`. Side curtains `FLongRight/LeftHair` are rotated **Y ±50°**, two segments each. |
| Accessories | A flower cluster of 15 cubes on its own rotated bone. Ears are 11 cubes per side. |

- **Legacy chibi (TLM Reimu):** a back curtain made of a row of 1×10×1 strands, side locks 1×5×1. [V data]

### 4.2 Strands: cubes, planes or meshes
- **Planes** (2-face quads) are good for tufts and fans: "use flat planes and angle them like a fan" (r/Blockbench 1tt534a, 13 upvotes). For long hair they look thin from the side: "I'd want the hair to have some volume so it creates a good silhouette from all angles" (1wzlcjt). [C]
- **Thin cubes**, 1 unit deep (2 texels at 32 px), keep volume from every angle. Winefox uses them almost everywhere. [V data]
- **Meshes:** extrude, knife and Shift+F (ArtDanPol, Reddit). They are not usable here: GeckoLib 4 has no native mesh support and GeckoMesh has no NeoForge 1.21.1 build. [C]+[V]
- **House rule [E]:**
  - Cubes ≥ 1 unit thick for bangs, locks and back curtains.
  - 0-thick planes only for small tufts, ahoge leaves and ribbon tails.
  - Delete the hidden back faces of strands that touch the cap. McHorse deletes the left, right and down faces of strand cubes and switches to per-face UV. [C] `https://www.youtube.com/watch?v=q1bHozBf0_M`

### 4.3 Recipes [E unless tagged]

**Cap**
- Plates 0.5–1 thick, 0.25–0.5 off the head surface, never coplanar with it.
- Alternative: duplicate the head and inflate it by +0.25. The stretch from 7 to 7.5 units is about 7%, which is acceptable.
- Delete the head's top and back faces under the cap.

**Bangs**
- 5–9 cubes, 1–2 wide × 2–4 long × 1 deep.
- Rotate X −5° to −10° and fan Z ±5–30°.
- Make widths 1.02 so neighbours overlap without z-fighting.
- Their bottom edge stops 1 texel above the brow line.
- Paint a 1-texel shadow strip on the forehead under the bangs.

**Side locks**
- 2–3 segments, 1 × (2–4) × 1–2, taper toward the tip.
- Bone pivot at the temple.
- Second segment is a child bone so it can sway.

**Back hair**
- Curtain plates 1 thick (8–9 wide), plus side plates rotated Y ±40–50°.
- Two segments as bones (LongHair → LongHair2).
- Clipping fix: either counter-rotate (4.4) or parent the long curtain to the chest instead of the head, following head yaw ×0.5.

**Ahoge**
- 1–2 cubes 0.5–1 wide on top of the head, with its own bone pivoted at the base.
- TLM's `ahoge` bone follows the head and swings during "beg". [V]

**Ponytail and twin-tails**
- A tie cube (scrunchie or ribbon) plus a 3–4 segment chain.
- Segments 2–3 units long, tapering 2 → 1.5 → 1 wide.
- Each segment overlaps the previous by 0.5 so rotation does not open a gap; the pivot is at the top of each segment.

**Braids**
- Option 1: 1.5-unit segments alternately rotated ±12–15° Z (zigzag) with a braid pattern painted.
- Option 2 (cheaper): one cube per braid half with the plait painted in.

### 4.4 Hair motion and clipping
- **Long hair stabbing into the body when looking up (YSM).** Back-hair rotation X = `(ysm.head_pitch > 0) ? -ysm.head_pitch : 0`. When the head looks up, the hair cancels the head rotation and hangs straight; when it looks down, the hair follows the head. [V] `https://www.mcmod.cn/post/2955.html`; [V] `https://www.mcmod.cn/post/4125.html`
  - In GeckoLib, the head look is usually set in Java (`setCustomAnimations`). Apply the counter-rotation there, or use `query.head_x_rotation`. **Check the sign in game**, because MC pitch is positive when looking down. [?]
- **Speed-driven lift.** Winefox jump: `clothe` rotation X = `-7.5-math.clamp(query.ground_speed*3,0,30)`. The same works for hair, and `query.ground_speed` exists in GeckoLib. [V data]
- **Spring physics in Molang (YSM community).** Variables F (response), C (damping 0–1) and R (amplitude), driven by vertical speed, horizontal speed and angular speed, at 100 fps animations. Winefox `pre_parallel2`: `MLongHair rotation = ["-v.L1_P0+v.L2_P0", 0, "0.1*v.L3_P0"]`. [V data]; [C] `https://www.mcmod.cn/post/3772.html`
  - GeckoLib supports variables in Molang, but the YSM physics script uses YSM-only queries. Port it as a Java damped spring per entity instead. [E]
- **Figura hair physics:** a "physbone" group plus a `collider` cube the size of the torso keeps hair out of the body, but it bounces too much. [C] `https://www.youtube.com/watch?v=ZsXbkcPar_g`
- **Keyframed follow-through [E]:** each chain link lags its parent by 0.08–0.12 s, and amplitude grows about ×1.3 per link toward the tip. Match the loop to the walk cycle (winefox walk is 1.0 s).

---------------------------------------------------------------------

## 5. Body (adult characters only)

### 5.1 Torso
- **Slab stacking (winefox).** The upper chest is made of horizontal slabs that widen toward the shoulders: 8×3.1×4.9, then 8.2×2×5.1, then 8.6×1×5.7 and 8.8×1×5.7 with inflate −0.2. The waist (`UpBody`) is 1-unit-tall slabs 6 and 7 wide, with side bevel cubes 3.73×1×4.17 rotated **Z ±19.75°** to taper the waist. [V data]
- **Minto (YSM).** Start with a flat torso and add cubes later. Joining rotated side pieces is hard, so put a filler cube inside the torso to cover the seams. Shoulder-to-chest joins need more cubes. "I use the vertex snap tool a lot." The bottom of the torso goes inward, and the back gets a little shape. [C] `https://www.youtube.com/watch?v=0AKabk-2Ot8`
- **House recipe [E].** 4–6 slabs on the 0.5 grid:
  - shoulder slab 7 wide
  - chest 6.5
  - under-chest 5.5
  - waist 5
  - hip 6
  - Depth 3–3.5. Two side bevels rotated ±15–20° Z at the waist, plus one hidden filler.
  - Budget: 8–12 cubes.

### 5.2 Chest shaping (tasteful, non-sexual)
- Treat the chest as **part of the clothing silhouette**: bodice, vest, breastplate or coat front. Do not treat it as anatomy. [E]
- Use 1 (at most 2) cubes across the upper chest. Protrusion is ≤ 1 unit (2 texels) beyond the torso front. Rotate the lower edge in by X −15° to −25° so it reads as a soft slope instead of a shelf. Shade it with the clothing ramp. [E]
- Put it on the **`chest` bone**, which also carries breathing. Never give it an independent bone, jiggle or physics. [E]
- The child character gets none of this: a straight torso only. [E]

### 5.3 Arms and hands
- **Slim arms:** 2.5–3 units wide (5–6 texels) × 3 deep. Winefox upper arm is 2.95×7×3.53. [V data]
- **Split at the elbow.** The forearm group is a child of the upper-arm group, with its pivot at the elbow (YSM V2). [C] `https://www.youtube.com/watch?v=tEodmX-VpZo`
- Minto adds "a sort of elbow so the arm bends a bit softer". [C] For a 32 px build, use a 2×1.5×2 elbow filler cube, centred on the joint, weighted to EF `Elbow_*`. [E]
- **Hands:** Minto uses "small and stubby fingers". Winefox uses 2 cubes per hand. For NPCs, use a mitten hand plus an optional thumb cube (2–3 cubes). [C]/[V data]
- **Sleeves:** a separate inflated (+0.25) cube per arm segment, or extra cubes (winefox upper arm has 1 arm cube + 6 sleeve cubes, forearm 1 + 8). [V data]

### 5.4 Legs and feet
- **Winefox:**
  - thigh 3.4×9×4
  - a `guanjie` ("joint") filler cube 3.17×2×2 rotated X 30° at the knee
  - shin 3.35×8×4 plus a cuff 3.62×3.1×4.08
  - foot 3 cubes, shoe 11 cubes

  [V data]
- **Minto:**
  - The front of the leg is flat and the back is rounded.
  - **Flatten the top of the shin** so no cubes go through the leg when it bends a lot.
  - Round the top of the thigh so it looks connected to the torso when animated.

  [C]
- **Thigh-highs and boots [E]:**
  - At 32 px, paint thigh-highs and stockings in texture (a 1–2 texel band at the top hem).
  - Make boots from cubes: a cuff inflated +0.25 over the shin plus a sole 0.5 thick, extended 0.5 forward.
  - Armoured greaves are separate plates (6.4).

---------------------------------------------------------------------

## 6. Clothing and accessories

### 6.1 Skirts
- **Stepped tiers (legacy TLM).** `sittingRotationSkirt` stacks 10×2×10, 9×2×9, 8×2×8, 7×1×7 and 6×1×6, and the whole skirt rotates when sitting. It is cheap but stiff. [V data]
- **Panel ring (winefox, professional).**
  - The `clothe` group sits under the upper body, not the legs.
  - It splits into Right, Left, Back and Front panel groups. Side groups are rotated Z ±7.5°, the back X +11.25°, the front X −8.75°.
  - Each group has 2–3 sub-panels (RM, RB, RF / FL, FR, FM / BR, BM), made of plates 1 thick (for example 4.25×4×1 at Y 90° Z 15°), and each is a **2-segment chain** (waistband pivot at about y 22.8 → mid-thigh pivot at about y 19). The front trims are 0.1-thick ribbons.
  - Animation:
    - **walk:** BackClothe Y rotation swings ±12.5° in a 1 s loop; Left and Right panels alternate in sync with the legs.
    - **run:** bigger catmullrom swings.
    - **sit:** side panels rotate about −104° on X and scale to 0.8 so they fold onto the thighs; the front rotates −45° and scales Y to 0.7.
    - **jump:** the whole skirt lifts with ground speed.

  [V data]
- **Minto (YSM V2, from the transcripts):** groups are needed for everything that animates, and pivots matter. [C]
- **Principles from a skirt-physics plugin (Unreal KawaiiPhysics, used here as concepts).** Skirts have many chains and suffer leg penetration. Solutions:
  - a **sync bone**, so the skirt follows the thigh
  - capsule limits around the thighs
  - pleated skirts: stiffer, limit angle 30–45°
  - flared skirts: softer, 60–90°
  - a hem softer than the waist

  [V doc, other engine] `https://github.com/pafuhana1213/KawaiiPhysics/wiki/Tutorial-Skirt-en`
- **House recipe [E]:**
  - 6–8 panel bones around the hips, each with its pivot on the waistband, angled 7.5–15° outward.
  - Inner radius at least 0.5 unit outside the thigh's outer surface.
  - Optional lower segment for flare.
  - Inside faces: plane panels have only one face, so they show from both sides. Panel cubes keep their inside face (it is visible under the hem) and delete only the top and bottom edges hidden by the waistband.
  - **GeckoLib:** in `setCustomAnimations`, set front-left panel X = min(0, thighL.rotX) × 0.6 (and so on for each panel), plus a small Y twist. The skirt then follows leg swing whatever animation plays.
  - **Epic Fight mesh:** weight hem vertices 50/50 between `Root` and the nearest `Thigh_*`, and waistband vertices to `Root`. This is the EF equivalent of a sync bone and needs no code.
  - For long robes, split the front with a slit, or attach the left and right halves to the thighs.
- **Reddit:** "how to do a dress without legs clipping when posing" (1q8xrwd). The only answer given was "move them by 0.00000001", which does not fix it. The panel method is the real fix. [C]

### 6.2 Coats and capes
- **Coat tails:** treat them like skirt panels (2 back plus 2 side), pivoted at the waist. Collars are rotated plates. [E]
- **Capes:** 1-unit-thick plates in 2–3 chained segments from the chest bone, with a speed-driven lift (4.4).
  - Epic Fight has a "Cloth Simulator 2.0" (Mar 2025, Patreon). It is fps-stable and adds circular motion so the cape intersects the body less. It is documented for Patreon capes and cosmetics only. [V existence] `https://www.patreon.com/yessman/posts/cloth-simulator-124329914`
  - Using it on custom mobs is [?].

### 6.3 Layered and inflated cubes
- **Clothing over body:** inflate +0.25 (1.07× on a 7-unit face), keep the same UV size, and delete the body faces underneath. Inflate is applied per cube; Blockbench shows a group's inflate only as a helper. [V] `https://github.com/JannisX11/blockbench/issues/3318`; [V] GeckoLib honours bone-level inflate as a fallback (`BakedModelFactory`)
- Do not stack two inflated layers on the same face. Make the outer one a separate thicker cube instead. [E]

### 6.4 Armour plates, ribbons, halos, headphones
- **Armour plates:** cubes 0.5–1 thick floating 0.25 off the body. Pauldrons go on the **shoulder** bone (EF `Shoulder_*`, the parent of `Arm_*`) so a raised arm does not swing them fully. [V] EF hierarchy; [E] placement
- **Ribbons and bows (winefox):** each bow loop is 2 cubes, and the tails are a 2-segment chain (bowL1 → bowL2). Small ribbons in our build: 0-thick planes, one textured face. [V data]/[E]
- **Halo:** a cutout plane ring (transparent centre) or a 4-cube frame on its own bone above the head.
  - Emissive via `_glowmask` (GeckoLib AutoGlowingGeoLayer).
  - Slow bob: position y = `math.sin(query.anim_time*90)*0.25`.
  - YSM convention: a bone name starting `ysmGlow` glows "under most shaders". [V] `https://ysm.cfpa.team/wiki/tph2yetr/`
  - Check under Iris and Complementary (render branch).
- **Headphones:** 2 ear-cup cubes (2.5×3×1.5) plus a band of 3 plates on the head bone. Do not inflate them through the hair cap; place them 0.25 outside it. [E]

### 6.5 Weapons and attach points
- **YSM locators** are empty groups placed by their pivot:
  - `LeftHandLocator` / `RightHandLocator`, inside `LeftHand` / `RightHand`
  - `LeftWaistLocator` / `RightWaistLocator` for sheathed blades
  - `BladeLocator`, `SheathLocator`, `BackpackLocator`
  - `ElytraLocator`, shoulder locators

  [V] `https://ysm.cfpa.team/wiki/tph2yetr/`
- **TLM:** `armLeftPositioningBone` must be an empty bone inside `armLeft`; its pivot is the held-item origin. [V]
- **GeckoLib:** render held items with `BlockAndItemGeoLayer#getStackForBone` on an empty bone. [V] GeckoLib wiki Render Layers
- **Epic Fight:**
  - held items at `Tool_R` / `Tool_L`
  - `backToolJoint()` = `Chest`
  - right- and left-hand joints = `Hand_*`

  [V] `HumanoidArmature.java` (1.21.1)
- **House naming [E]:**
  - `item_r` / `item_l`: empty bones under the hand, pivot at the grip centre
  - `back_weapon` under the chest
  - `waist_l` / `waist_r` under the hips

---------------------------------------------------------------------

## 7. Texturing at 32 px/block for an anime look

### 7.1 Palette and cel shading
- **Structure:**
  - The basic anime look is base + **shadow 1 (soft) + shadow 2 (darkest)** + one highlight + line art made from a darker version of the base, never black.
  - Skin shadows shift toward red or purple, not grey.

  [C] `https://paletadecolores.org/en/anime-color-palette.html`
- **Ready-made ramps (highlight / base / shadow 1 / shadow 2 / line)** [C]:

  | Material | Highlight | Base | Shadow 1 | Shadow 2 | Line |
  |---|---|---|---|---|---|
  | Skin, light | #FEECDF | #F8D5C2 | #E6A995 | #CA8273 | #5E403C |
  | Skin, fair | #FFF4EC | #FDE7DA | #EBBCAA | #D09587 | #5C4945 |
  | Hair, silver | #E6E8EE | #C9CDD6 | #9DAAC7 | #7888AE | #3F434A |
  | Hair, pink | #FFD3E4 | #F2A1C2 | #CD7F9F | #AB5C7F | #602440 |
  | Hair, black | #98969C | #2B2730 | #1E1725 | #130A1C | #08050B |

  The black-hair line colour (#08050B) is close to pure black, so lift it for our art bible.
- **Hue shift amounts:**
  - About 20° per step at most (Slynyrd).
  - 10–15° per step for skin and familiar materials. "A cool blue shadow on a face looks like frostbite."
  - Saturation peaks in the midtones. Never put maximum saturation and maximum value on the same swatch.

  [C] `https://the-pixel.art/articles/hue-shifting-pixel-art-shading/`
- **Blockbench style guide:**
  - Build each ramp from the midtone with one shadow and one highlight first.
  - Light comes from the top and front: the top and front faces are brighter than the bottom and back, per face and between faces.
  - No banding, pillow shading, pancake shading, noise or unnecessary dithering.

  [V] `https://www.blockbench.net/wiki/guides/minecraft-style-guide/`
- **Hytale:**
  - No pure white or black.
  - Shadows "never purely desaturated", for example a hint of purple.
  - Paint light, shadow and AO into the texture.
  - When previewing characters in Blockbench, turn off side shadows to avoid hard edges on organic shapes.

  [V] Hytale blog, Dec 2025
- **House cel rule [E]:**
  - Each material uses base + 2 shadows + 1 highlight, with hard edges and no gradient brushes.
  - Use the line colour only for the lash line, brows, mouth, hair strand separations and clothing seams.

### 7.2 Hair painting (Minecraft-skin practice)
- **Jingles (416k views):**
  - A 4-colour ramp where the first two colours are close and the step to the third is bigger.
  - Put dark "C" shapes on the four corners and the lightest colour in the middle.
  - Brows are darker than the darkest hair colour.
  - Bangs are darker on the outside and lighter in the middle.
  - An optional fifth highlight.

  [C] `https://www.youtube.com/watch?v=LLv7Kw2casE`
- **Anime additions [E]:**
  - A 1-texel highlight band (the "angel ring") across the cap at about one third from the top, broken by the strand gaps.
  - Strand tips one step darker.
  - A forehead shadow under the bangs.

### 7.3 Eyes, face and skin (painting order) [C+E]
1. Fill the face with base skin. Add shadow 1 under the bangs (1–2 rows), under the chin and nose, and a 1-texel blush.
2. Paint the closed-eye lid line (lash colour, 3–4 px, gently curved with the outer end 1 px lower) on the face.
3. On each open-eye plane:
   - upper lash: 1–2 px thick, darkest, extending 1 px past the outer corner
   - sclera: pale grey-blue
   - iris: dark at the top → light at the bottom (Minto)
   - pupil: 1–2 px
   - catchlight: 1 px, upper outer, identical on both eyes
4. Brow planes: lash colour, 4×1 px.
5. Mouth planes: line colour; the open mouth uses shadow 2 inside and an optional 1-px tongue tint.
6. Check at 1:1 in-game distance (3–6 blocks), not only zoomed in.

### 7.4 Outlines
- **Geometric outlines (inverted hull):**
  - Blockbench negative-size cubes render only the far faces, which gives a fake outline. [C] CPM issue `https://github.com/tom5454/CustomPlayerModels/issues/493`
  - With GeckoLib NoCull this does not work by default, and it doubles the cube cost.
  - **Do not use geometric outlines.** Use selective coloured line art in the texture and value contrast at the silhouette. [V NoCull]+[E]

### 7.5 UV packing for 32 px characters [E unless tagged]
- In Create Texture, set resolution 32, tick rearrange UV and padding, and untick double_use for faces painted asymmetrically. Then pack by hand. [V options]
- Mirror UVs only for symmetric limbs and plain sleeves. Never mirror the face, hair or anything asymmetric.
- Put the face front and the eye, brow and mouth planes in one corner block of the atlas (for example a 64×32 region), so expression edits stay local.
- Keep each bone's islands together and align islands to the 2-texel grid, so a 0.5-unit cube edge lands on a texel boundary.
- Size: one adult NPC of about 250–300 cubes with hidden faces removed fits in 256×256 at 32 px. Use 128×256 for simpler NPCs. The contract boss maximum is 512.
- The Hytale texture rule (multiples of 32) is a good discipline even though entities do not need it.

---------------------------------------------------------------------

## 8. Rig and animation readiness (GeckoLib and Epic Fight together)

### 8.1 Epic Fight humanoid joints (verified)
- **`HumanoidArmature` (1.21.1)** requires these joints: `Root`, `Thigh_R`, `Leg_R`, `Knee_R`, `Thigh_L`, `Leg_L`, `Knee_L`, `Torso`, `Chest`, `Head`, `Shoulder_R`, `Arm_R`, `Hand_R`, `Tool_R`, `Elbow_R`, `Shoulder_L`, `Arm_L`, `Hand_L`, `Tool_L`, `Elbow_L`. [V] `https://github.com/Antikythera-Studios/epicfight/blob/1.21.1/src/main/java/yesman/epicfight/model/armature/HumanoidArmature.java`
- **Hierarchy (from `assets/epicfight/animmodels/entity/biped.json`):**
  ```
  Root ─ Thigh_R ─ {Leg_R, Knee_R}        (Leg and Knee are siblings with the same offset)
       ─ Thigh_L ─ {Leg_L, Knee_L}
       ─ Torso ─ Chest ─ Head
                       ─ Shoulder_R ─ Arm_R ─ {Hand_R ─ Tool_R, Elbow_R}
                       ─ Shoulder_L ─ Arm_L ─ {Hand_L ─ Tool_L, Elbow_L}
  ```
  [V data] Elbow and Knee are helper joints for the bend region. EF docs describe bends as 3 stacked loop cuts at the elbow or knee, weighted between bones, with UV fixes in the bend. [V] EF Guides page 1
- **EF mesh JSON format:**
  - `positions`, `uvs` (0–1), `normals`
  - `vcounts`: influences per vertex
  - `weights`: a table of weight values
  - `vindices`: (joint, weight) index pairs
  - `parts`: named triangle lists of (pos, uv, normal) triples

  [V data] A cube-to-EF converter is therefore a small script. EpicYSM does this at runtime for YSM cube models. [V existence]/[E]

### 8.2 Recommended GeckoLib bone tree with its EF mapping [E]
```
root                         → Root (pivot 0,13.5,0)
├─ hips   (skirt_* panels, waist_l/r)             → Root
├─ leg_l (Thigh_L) ─ knee_fill_l (Knee_L) ─ shin_l (Leg_L) ─ foot_l
├─ leg_r ...
└─ torso (Torso, pivot ~y14)
   └─ chest (Chest, pivot ~y18; breathing scale here; back_weapon, cape_*)
      ├─ head (Head, pivot 0,24,0)
      │   ├─ face_m → face (eyes_m/eyes, brow_l/r, mouth_* planes)
      │   └─ hair_m → hair (cap, bangs, side_l_1→side_l_2, ahoge, tail_1→tail_2→tail_3)
      ├─ shoulder_l (Shoulder_L) ─ arm_l (Arm_L) ─ {elbow_fill_l (Elbow_L), forearm_l (Hand_L) ─ hand_l ─ item_l (Tool_L)}
      └─ shoulder_r ...
```
- **Double bones (winefox "M" prefix).** Winefox wraps parts in pairs (`MRoot/Root`, `MHead/Head`, `MBangs/Bangs`, `MLongHair/LongHair`). The outer bone takes keyframe animations and the inner one takes procedural or physics motion, so two animation sources never key the same bone. Use `*_m` wrappers on the head, hair chains, skirt panels and face. [V data]+[E]
- **Names.** YSM's convention is UpperCamelCase adjective + noun (`LeftArm`, `AllHead`); helper groups are parent + number (`Mouth1`). For our project, pick lowercase snake_case once (GeckoLib does not care) and keep a mapping table to EF joint names in the ticket. [V] `https://www.mcmod.cn/post/2955.html`; [E]
- **Pivots.** Put them on joint centres on the 0.5 grid. "Groups are the bones, pivots are the joints, cubes are the flesh." Only groups animate, so put every cube in a group under one root. [V] `https://github.com/bernie-g/geckolib/wiki/Making-Your-Models-(Blockbench)`
- **Rest pose.** Arms straight down, as in vanilla and the EF rig. Winefox rests in an 18° A-pose, which complicates EF binding. Do an A-pose in the idle animation, not in the rest pose. [V data]+[E]
- **Rebuilding the body is fine.** "You don't have to use the default vanilla poor layout"; add a waist bend. [C] OutLandishly `Wi3Isin7Hjo`
- **Proportions and EF [?].** EF animations are made on its own rig. If our hips are 1.5 units higher than vanilla, the poses should still work, but test early: in-game stance, foot sliding, hitbox. EpicYSM working on arbitrary YSM proportions is encouraging evidence.

### 8.3 Paths into Epic Fight
- **(A) Documented path:**
  1. Blockbench (Generic) → OBJ or glTF.
  2. Blender with the EF Animation Rig (`EpicFight Animation Rig.blend`).
  3. Parent and weight: rigid per cube, with filler cubes on `Elbow_*` / `Knee_*`.
  4. Export with the EF JSON exporter (mesh + armature).
  5. Write the mobpatch datapack (`data/<modid>/epicfight_mobpatch/<entity>.json`, `pack_format` 48 for 1.21.1).

  [V] `https://epicfight-docs.readthedocs.io/Guides/Armor/3Darmor_page3/`, `/Guides/Entities/page1/`
- **(B) Proposed:** a `bbmodel → EF mesh JSON` converter in `tools/` that maps bone names to joints, with rigid weights plus blended hem weights for skirts. This avoids Blender for meshes, which suits the cloud agents. [E]

### 8.4 Idle breathing and secondary motion
- **Breathing:** "scaling on the chest… in and out… the whole body doesn't move when you breathe". [C] OutLandishly
  - House values: chest scale Y 1 → 1.015 and Z 1 → 1.02.
  - Shoulder and arm bones +0.15 Y.
  - Head counter −0.1 Y.
  - Sine loop of 4.0 s.

  [E]
- **Seamless sine loops (Bedrock wiki):** `Math.sin((q.life_time+offset)*speed)*pitch`. The loop pairs are speed 150 ↔ 2.4 s and speed 100 ↔ 3.6 s, and multiples. [V] `https://github.com/Bedrock-OSS/bedrock-wiki/blob/wiki/docs/visuals/bedrock-modeling.md`
- **Secondary motion menu:**
  1. Keyframed follow-through (4.4).
  2. Molang sine chains with a per-link phase delay.
  3. Speed-driven lift: `query.ground_speed`.
  4. Head-pitch counter for long hair.
  5. A Java damped spring in `setCustomAnimations` for bosses.
  6. EF meshes: blended hem weights, plus EF Cloth Simulator for capes [?].

  [E]
- **YSM priorities as a model:** `pre_parallel` (blink, idle extras) sits under the main animations, and `parallel` (overrides, additive rotation) sits over them. Copy this in GeckoLib with three controllers: body, face, secondary. Each controller keys only its own bones. [V YSM wiki]+[E]

---------------------------------------------------------------------

## 9. Common mistakes and how professionals fix them

| Mistake | Fix | Tag |
|---|---|---|
| Mixels from tiny or negatively inflated cubes, or box UV on non-integer cubes | 0.5-unit grid, per-face UV, Auto UV on all faces before creating the texture | [V] style guide; [C] r/Blockbench 1tmzhye |
| Shared UVs paint two parts at once | Untick double_use, or give each face its own UV island | [C] 1lrmpzq |
| Coplanar faces flicker (hair on head, eye planes on face, double-faced planes) | Offset 0.01–0.05, widen strands to 1.02, give planes one textured face, inflate ±0.01 | [V data, Bedrock wiki, TLM wiki] |
| Long hair goes through the chest when looking up | Counter-rotate with head pitch, or parent the hair to the chest | [V] YSM guide |
| Skirt clips through the legs | Waist-anchored panel bones, with leg-driven rotation (code) or blended weights (EF); sit pose folds panels and scales them to 0.8 | [V data]+[E] |
| Gaps or poking cubes at bent elbows and knees | Filler (`guanjie`) cube at the joint; flatten the shin top; round the thigh top | [V data]; [C] Minto |
| Staring, lifeless NPCs | Blink every 2–4 s with irregular timing; random look-away idles; eye tracking ±1 texel; catchlights | [C] OutLandishly, pixeli; [V data] winefox |
| Uncanny or dead face | Pupils 1 px off centre; whites not white; break symmetry by 1 px; brows 1 px from the eyes; no realistic nose or mouth geometry | [C] pixeli |
| Grey or muddy shading | Hue-shift ramps (skin toward red or purple); saturation peaks in midtones; no black | [C] the-pixel.art, Linky Playz `cR7De_c6N_8`; [V] Hytale |
| Too many cubes or rotated rings | Shape with few cubes, detail in texture, delete hidden faces; prototype one hair section before multiplying it | [V] style guide; [C] mcp skill |
| Blink via `.mcmeta` animated texture | Geometry blink (scale or visibility); `.mcmeta` is global and breaks glowmasks | [V] GeckoLib wiki |
| Resizing a finished cube stretches its texture | Rescale UVs with UV Size (5.1 "UV Size Editor") or re-run Auto UV | [V] Blockbench 5.1 release; [C] |
| Translucent pixels sort wrongly | Cutout only | [V] YSM texture docs |

---------------------------------------------------------------------

## 10. Build order for one adult character (agent checklist) [E, built from the sources above]

0. **Ticket and reference sheet approved by the user.** It shows front, side and back silhouettes, the palette as hex ramps (skin, hair, eyes, 2–3 cloth materials), and key details. Mark the proportion choice from section 0 item 3 and the "1-texel minimum feature" face style.
1. **Project.** GeckoLib Animated Model, per-face UV (`box_uv: false`), units on the 0.5 grid. Load a vanilla player and the previous approved character as scale references.
2. **Blockout (≤ 40 cubes).** Head, neck, torso slabs, hips, arms (upper / fore / hand), legs (thigh / shin / foot), hair masses as 3–4 big blocks, skirt cylinder. Check the silhouette from 6 views and against the reference sheet.
3. **Bones and pivots now, before detail.** Build the section 8.2 tree with `*_m` wrappers, the EF mapping table and empty locator bones (`item_r/l`, `back_weapon`, `waist_l/r`). Test-rotate every joint for gaps. Add knee and elbow fillers.
4. **Body pass.**
   - Torso slabs and bevels.
   - Adults only: the chest slab, tasteful, on the `chest` bone.
   - Arms 2.5–3 wide, legs with a flat shin top, boots.
   - Target 50–70 cubes.
5. **Face pass.**
   - Head cube plus an optional jaw slab.
   - Eye planes (2.5×2.5 each) 0.02 in front, an optional iris plane 0.04, brow planes, the mouth-plane set in `mouth_*` bones.
   - Paint the closed-eye line on the face texture first.
6. **Hair pass.**
   - Cap plates 0.25–0.5 off the head.
   - Bangs (5–9 fanned cubes, X −5° to −10°).
   - Side locks (2–3 segment chains).
   - Back curtain (2 segments) and ahoge.
   - Ponytail or twin-tail chains with 0.5 overlaps.
   - Target 40–80 cubes.
7. **Clothing pass.**
   - Skirt panel ring (6–8 panels × 1–2 segments, waist pivots).
   - Sleeves and coat inflated +0.25.
   - Armour plates on shoulder and chest bones; ribbons as planes; halo or headphones.
   - Running total ≤ 300 cubes (proposal).
8. **Cleanup.**
   - Delete hidden faces.
   - Check coplanar faces (offsets, 1.02 widths).
   - Run `bbmodel_validate`.
   - Confirm every cube dimension is ≥ 0.5 and on the 0.5 grid. Allowed exceptions: 0-thick planes and ±0.01–0.05 z-offsets.
9. **UV and texture.**
   - Create Texture at resolution 32, rearrange UV, padding, double_use off.
   - Hand-pack with the face and expression atlas in one corner.
   - Paint flats → shadow 1 → shadow 2 → highlights → line accents. Hue-shifted ramps from the reference palette; top and front faces brighter.
   - Eyes last, following 7.3.
   - Optional `_glowmask` for magical eyes or halo.
10. **Animation-readiness tests.**
    - Blink (6.4 s loop) in a face controller.
    - Breathing (4.0 s) on the chest.
    - Walk with skirt and hair follow-through.
    - Sit pose (skirt fold).
    - Head pitch ±60° (hair counter-rotation).
    - Arm raise 170° (pauldrons, sleeves).
    - Leg kick 90° (skirt clipping).
11. **Review loop (AGENTS.md 5.0).**
    - Render a 6-view contact sheet plus a close-up face sheet (neutral, blink, happy, angry, sad, surprised).
    - Check against section 9.
    - Send the Blockbench web link to the user and record their feedback in the ticket `note`.
12. **Export.**
    - GeckoLib `.geo.json` and animations.
    - For combat characters: OBJ → Blender → EF rig, or the proposed converter. Smoke-test in game with an EF longsword moveset.
    - Animated Java copy for cutscenes, with target 1.21.1 and blink via variants or scale.

---------------------------------------------------------------------

## 11. Open questions and tests
1. **[?] EF with non-vanilla proportions.** Do EF biped animations look right on a mesh whose hip joint is 1.5 units higher and whose limbs are slimmer? Spike test with one character before committing to the unit sheet.
2. **[?] EF expressions.** Can a custom EF mob renderer toggle mesh `parts` or swap textures per frame for blink and expressions? Read the EF 21.17 source during mod-skeleton work.
3. **[?] Back-hair counter-rotation sign** for `query.head_x_rotation` in GeckoLib 4.9.3.
4. **[?] Emissive eyes and halos under Iris** with Complementary, Photon and Bliss. GeckoLib glowmask and LabPBR `_s` alpha (render branch).
5. **[?] EF Cloth Simulator** on custom mob capes: API or patron-only?
6. **[E] Contract proposals for the user:**
   - NPC cube budget (≤ 300; hero boss ≤ 500).
   - Optional render-scale 0.75 variant for a larger face resolution (changes in-world px/block).
   - Rotated-cube cap (≤ 30%).
   - The 1-texel minimum face feature rule.

---------------------------------------------------------------------

## 12. Sources (all fetched 2026-10-13/14)

**Primary data and docs [V]**
- Touhou Little Maid winefox_elf GeckoLib model and animation (TLM 1.20 branch), parsed: URLs in section 0.
- Legacy TLM Reimu model (`.../touhou_little_maid/models/entity/hakurei_reimu.json`) and pack manifests.
- TLM custom pack guide with preset bones and z-fighting tips: https://www.mcmod.cn/post/2603.html
- YSM wiki:
  - model groups: https://ysm.cfpa.team/wiki/tph2yetr/
  - parallel animations: https://yesstevemodel.github.io/wiki/animation/parallel/
  - textures: https://yesstevemodel.github.io/wiki/texture/
- YSM old full guide (naming, hide via scale 0, long-hair counter-rotation): https://www.mcmod.cn/post/2955.html. Variables and physics posts: https://www.mcmod.cn/post/4125.html, https://www.mcmod.cn/post/3772.html
- GeckoLib 1.21.1 source: `GeoModel.java` (entityCutoutNoCull), `BakedModelFactory.java` (inflate, null faces, box-UV floor), `Cube.java`. GeckoLib wiki: Animated Textures (Geckolib4), Emissive Textures (Geckolib4), Render Layers (Geckolib4), Geo Models (Geckolib4), Molang (Geckolib4), Making Your Models (Blockbench).
- Epic Fight 1.21.1: `HumanoidArmature.java`; `assets/epicfight/animmodels/entity/biped.json`; docs Guides page 1 (bends, weight paint); Custom entity datapack; Blockbench Armor Model Remake.
- EpicYSM https://www.curseforge.com/minecraft/mc-mods/epicysm; YSM Epic Fight Compat https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat
- Animated Java docs: texture slots, upgrading to 1.11.
- Blockbench Minecraft Style Guide (stored in `research/modeling/`); Blockbench texture generation (deepwiki); Blockbench issue #3318 (inflate).
- Hytale "An Introduction to Making Models for Hytale" (Dec 2025, in `research/modeling/`); doctale NPC attachments https://doctale.dev/asset-development/npcs/attachments/
- Bedrock wiki modeling page (z-fight, sine loops).
- GeckoMesh https://www.curseforge.com/minecraft/mc-mods/geckomesh
- Epic Fight Cloth Simulator 2.0 Patreon post.
- KawaiiPhysics skirt tutorial (concepts only).

**Videos [C]** (transcripts in `research/r2/2b/yt/`; most are short, so no timestamps were needed except where noted)
- Minto (YSM):
  - Eyes and Face Creation https://www.youtube.com/watch?v=8fs7yP0T21Q (1:43)
  - How I Make Models From Scratch https://www.youtube.com/watch?v=0AKabk-2Ot8 (3:24)
  - V2 Part 3 https://www.youtube.com/watch?v=tEodmX-VpZo
  - V2 Part 4 Animating (4:41; the blink walkthrough is in the second half of the transcript, exact timestamp not captured) https://www.youtube.com/watch?v=G_eLsOaeebE
  - Texturing https://www.youtube.com/watch?v=9Q5TiKiOWJg
  - Armor/Morph https://www.youtube.com/watch?v=tU5KkZ-xHNQ
- OutLandishly Crafted, 3D eyelids and blinking https://www.youtube.com/watch?v=Wi3Isin7Hjo; Hytale blink https://www.youtube.com/watch?v=zWbq4Ufv0fk
- notsparkskye, expressive faces (chapters 01:54 facial components, 06:00 painting) https://www.youtube.com/watch?v=hTFKQrj8ZV4
- Josillia, blinking with an animated-texture eyelid plane https://www.youtube.com/watch?v=r9LfbkgG4u0
- StrangeLifeKim, HD eyes https://www.youtube.com/watch?v=bagRNBqCwUs
- McHorse, hair strands and physics https://www.youtube.com/watch?v=q1bHozBf0_M
- Hiro, Figura ponytail physics with collider https://www.youtube.com/watch?v=ZsXbkcPar_g
- Jingles, hair shading https://www.youtube.com/watch?v=LLv7Kw2casE
- Linky Playz, hue shifting https://www.youtube.com/watch?v=cR7De_c6N_8
- FayeTale, Blockbench and Figura basics https://www.youtube.com/watch?v=fO-eYNQ1dC4
- ArtDanPol, mesh hair and faces (not usable for GeckoLib 4): https://www.youtube.com/watch?v=9Cmsi2MeyG8, https://www.youtube.com/watch?v=VffhIfb5yvc, https://www.youtube.com/watch?v=MhcZGpxHOjM

**Reddit r/Blockbench [C]** (via Arctic Shift)
- 1wzlcjt long hair (planes vs volume)
- 1tt534a tuft fan
- 1um3i3m mesh hair
- 1wejrlm fluffy hair (X planes plus filler cubes)
- 1q8xrwd dress clipping
- 1lrmpzq shared UVs in GeckoLib
- 1tq8h5v face planes moved out of the head
- 1vjx5qn, 1q3sgt4, 1mdu0nw (mixels on eyes)

**Pixel art [C]**
- pixeli eyes and expressions https://pixeli.pebbly.space/knowledge/rules/33-eyes-and-expressions
- Sandro Maglione, pixel eyes https://www.sandromaglione.com/articles/pixel-art-eyes-techniques-and-styles
- the-pixel.art, hue shifting https://the-pixel.art/articles/hue-shifting-pixel-art-shading/
- paletadecolores anime palettes https://paletadecolores.org/en/anime-color-palette.html
