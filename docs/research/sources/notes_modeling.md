# Modeling / UV / Texturing pipeline — research notes (2026-10-13)

Scope: modeling, UV unwrapping and texturing of cube/block-built ("Minecraft-style") models for a soulslike adventure map on Minecraft Java (mods + resource packs + datapacks), at the highest quality that still runs at 50 fps or more.
Raw search and fetch JSON lives in `research/modeling/` (Ollama web_search and web_fetch). Reddit, YouTube and X dumps are in `research/modeling/social/` and `research/youtube/`.
Legend: **[V]** = checked against a primary or official source (release notes, wiki, docs, the vanilla jar as reported by a reference site). **[C]** = community opinion or practice. **[E]** = my own estimate or synthesis, not sourced. **[?]** = uncertain, conflicting or possibly out of date.

---------------------------------------------------------------------------------------------------

## 1. Blockbench: current version and features

### 1.1 Versions [V]
- **Latest stable: Blockbench 5.2.2 ("The Screen-Space Update", Patch 2), released 2026-10-08.** https://github.com/JannisX11/blockbench/releases
  - 5.2.2 adds support for **object texture references and the `force_translucent` field** in the Java block/item format (this matches the MC 26.1 model-format change, see §5). It also fixes glTF UV scaling with multiple materials and non-power-of-2 textures, and keeps vertex weights when merging meshes.
  - 5.2.0 came out 2026-09-18 and 5.2.1 on 2026-09-21. Pixelwolf recommends 5.2.1 or later for IK and glTF animation work: https://www.pixelwolf.net/blog/blockbench-5-2-screen-space-brush-low-poly-texturing/
- 5.1.0 "The Workflow Update" came out 2026-03-24, and its last patch was 5.1.6 on 2026-07-25. https://github.com/JannisX11/blockbench/releases/tag/v5.1.0
- 5.0.0 "The Element Update" came out 2025-10-12. https://github.com/JannisX11/blockbench/releases/tag/v5.0.0
- It is free and open source (GPL) and runs on Windows, macOS and Linux, plus a web app/PWA. The official channel videos: 5.2 at https://youtu.be/9MET5-wH5uw (about 166k views in 3 weeks) and 5.1 at https://youtu.be/OH82WjNwriE.

### 1.2 Features that matter for this project [V]
**5.2 (Sep 2026)**: release notes at https://github.com/JannisX11/blockbench/releases, transcript of the official video in `research/youtube/`.
- **Screen-Space Brush.** The stroke is projected from the camera instead of snapping to each face, which makes it easy to paint across cube edges and seams. You get it from a built-in preset or by toggling "Screen Space Brush Projection". The experimental settings expose a sample-interval option.
- **Brush lock** restricts painting to the first element, the first face or the selected faces. There is also a brush aspect-ratio slider.
- **Layer Groups.** Groups can be nested, folded and hidden.
- **Paint Bucket in the UV/2D editor** detects which face or element you clicked and fills it.
- **Presets for "Generate PBR Map"** (#3658).
- A new HSV color wheel. The color picker now works on locked elements, and face selections persist while painting.
- **3D-plane reference images** and video references with playback controls. Preview models can be moved and remember their position.
- IK poles, IK on armatures and faster IK.
- Mesh tools: icosphere, octahedron and dodecahedron primitives, even loop cut, proportional editing for resize and rotate, and Inset now computes new UVs.
- Minecraft-specific: better handling of generated Java item models, an option to resolve the whole parent chain, and the **Java "Shade Direction Override" cube property**, available in format version 26.3 or later.

**5.1 (Mar 2026)**: https://github.com/JannisX11/blockbench/releases/tag/v5.1.0
- **UV Size Editor** ("Edit UV Size" tool with live preview) and **Move UV to cursor**.
- **Texture wrap modes**: Restricted, Repeat (tiled, shown 3×3 in the UV editor) and Clamp Edge. "Move Texture with UV" now supports UV rotate and flip.
- Native PNG, TGA, JPEG and WebP support with live refresh. A **TGA workflow keeps color accurate at low-alpha pixels**: use "Split Alpha Channel into Layer". "Split RGB channels into Layer" now handles alpha too.
- A new **"Alpha Mask" layer blend mode** and a brightness slider in the Hue/Saturation tool.
- Better pen-tablet pressure support. On Windows, Windows Ink must be enabled.
- **Mirror Animating**, Preserve World Transform on reparenting, and Bounding Boxes.
- Per-flipbook FPS, and flipbooks sync to the animation timeline.

**5.0 (Oct 2025)**: https://github.com/JannisX11/blockbench/releases/tag/v5.0.0
- **Armatures** with weight painting, splines, billboards and mesh smooth shading.
- A **normal-map color picker** and darken/lighten blend modes.
- The "antialiasing bleeding fix" setting is now on by default. This fixes viewport bleeding only.
- An STL exporter and a GIF exporter.
- Breaking change: the keyframe direction fix inverts X position keyframes and X/Y rotation keyframes in pre-5.0 files when they are read by external tools. Check `format_version`. Source: https://elkonia.com/datapack_codex/bbmodel.html
- **5.0.5 (2025-12-10)**: "New Java block/item format version with no rotation limit (#3146)". https://github.com/JannisX11/blockbench/releases/tag/v5.0.5
- **5.0.6**: a setting for the default Java block/item format version.
- **4.12.5 (2025-06-17)** had already lifted the 22.5° snapping for the 1.21.6 format version and added a format version selector. https://github.com/JannisX11/blockbench/releases/tag/v4.12.5

**4.12 (Jan 2025)** added the native PBR "Materials" system as an extension of texture groups. It includes a Material Preview view mode, "generate PBR maps from existing textures" and texture_set.json import and export, but it is **"optimized for Bedrock; other formats planned"**. So for Java/LabPBR you still author the `_n`/`_s` maps yourself (see §4). https://github.com/JannisX11/blockbench/releases/tag/v4.12.0

### 1.3 Format feature matrix [V]
Source: https://blockbench.net/wiki/blockbench/formats/

| | Java Block/Item | Modded Entity | OptiFine Entity (EMF) | Generic | GeckoLib |
|---|---|---|---|---|---|
| Per-face UV | yes | **no (Box UV only)** | yes | yes | yes |
| UV face rotation | yes | no | no | yes | no |
| Multiple textures per model | yes | no | no | yes | **no (one texture per model)** |
| Cube rotation axes | 1 (wiki)\* | 3 | n/a (bones) | 3 | 3 |
| Size limit | 3×3×3 blocks (-16..32) | unlimited | unlimited | unlimited | unlimited |
| Non-integer cube sizes | yes | **no** | no | yes | yes |
| Double-sided faces | no | yes | yes | yes | yes |

\* [?] The wiki says Java Block/Item has a single rotation axis and "Unlimited⁵" angles, where note 5 is "Limited to multiples of 22.5° before 1.21.6". Vanilla supports per-axis x/y/z rotation since 1.21.11. Blockbench 5.0.5 added a "no rotation limit" format version, but I could not confirm that the editor exposes 3-axis rotation for Java Block/Item. The Elkonia codex (Oct 2026) says it is still one axis in the editor. Test this in 5.2.2.

---------------------------------------------------------------------------------------------------

## 2. UV: per-face vs Box UV, texel density, mixels, atlas packing

### 2.1 Box UV vs per-face UV [V + C]
- **Box UV** unwraps each cube automatically into the classic cross. All vanilla entities use it, and the **Modded Entity format requires it**. Faces take integer sizes, so non-integer cubes get rounded UVs, which causes mixels and wasted space. Box UV breaks when you rotate a cube 90°, and it cannot rotate faces. https://elkonia.com/datapack_codex/bbmodel.html , https://blockbench.net/wiki/guides/minecraft-style-guide/
- **Per-face UV** lets each face point anywhere, rotate (Java Block/Item and Generic) and reuse texture patches. It survives 90° rotations. It is the native form for Java block/item models and is supported in GeckoLib, Bedrock, OptiFine/EMF and Generic. https://mineassets.com/blog/uv-mapping-minecraft-models-explained
- **Use per-face UV when** you need maximum texture quality per pixel of texture budget: reused trims, mirrored limbs that share UVs, tight packing, rotated faces, faces at different texel density (avoid that), and inflated or non-integer cubes. **Use Box UV when** the target format requires it (Modded Entity), for quick blockouts, or for a vanilla-faithful entity look. [C] On r/Blockbench the common fix advice for stretched or mixel faces is "switch that cube to per-face UV, Auto UV, then resize the face's UV". See `social/r_comments_1.txt` (e.g., https://www.reddit.com/r/Blockbench/comments/1vqnkkm/ and https://www.reddit.com/r/Blockbench/comments/1uxr7ra/).
- To keep pixels square with per-face UV, select all faces, apply **Auto UV**, then use "Create texture" with **Rearrange UV** or the 5.1 **Edit UV Size** tool. A Reddit tip: Ctrl+A in face mode, then Auto UV, before generating the template (https://www.reddit.com/r/Blockbench/comments/1tmzhye/). Another: "Select All → Create new texture with Rearrange UV" removes unused faces from the texture (https://www.reddit.com/r/Blockbench/comments/1todojk/).

### 2.2 Texel density conventions [V + C]
- Vanilla: **1 texture pixel = 1 model unit = 1/16 block (6.25 cm)**. "It is very important that the ratio of pixels is preserved" (Blockbench Minecraft Style Guide, https://blockbench.net/wiki/guides/minecraft-style-guide/).
- **Mixels** (mixed pixel sizes) are elements smaller than 1 px, over-inflated elements, or textures that were upscaled and then detailed. The style guide says Minecraft art "generally does not allow mixels", with the exception of slightly inflated elements. Source: same style guide.
- [C] The community verdict on r/Blockbench is overwhelmingly negative: "Mixels (mixed pixel sizes) are evil", "mixels always look bad in Minecraft… I size up the model", and "Third is mixels". There is a minority view that small, grid-aligned mixels on eyes or mouth can work if done skillfully. Sources: https://www.reddit.com/r/Blockbench/comments/1vjx5qn/ , https://www.reddit.com/r/Blockbench/comments/1t61smv/ , https://www.reddit.com/r/Blockbench/comments/1mdu0nw/ ; dump in `social/r_comments_1.txt`.
- [C] Advice on 256² textures for blocks people place in large numbers: "an optimization nightmare… keep the original texture size" (https://www.reddit.com/r/Blockbench/comments/1vy9gyr/). Also "don't go below size 1… upscale the texture to get more pixels per cube" (https://www.reddit.com/r/Blockbench/comments/1wwzctv/).
- **"HD voxel" reference: the Hytale official style (Dec 2025).** Characters and attachments (weapons, tools, cosmetics) use **64 px per unit**, props and blocks use **32 px per unit**, and textures must be multiples of 32. Higher density goes on characters because faces are seen up close, they read better against the environment, and first-person weapons look better. Hytale allows stretching only from **0.7× to 1.3×** per axis. Its geometry is only cubes and quads (no spheres). It recommends a soft round brush with opacity pressure plus a pencil, light and AO **painted into textures**, no pure black or white, and colored shadows. Hytale does not use PBR. https://hytale.com/news/2025/12/an-introduction-to-making-models-for-hytale
- [E] Recommendation for a soulslike map: pick **one density per asset class and enforce it**. Two workable profiles:
  - (a) "Vanilla+": 16 px/block for everything. This blends with vanilla terrain and is the cheapest option.
  - (b) "HD-entity": 16 px/block for terrain and props, and **32 px/block for bosses, NPCs and held weapons only**, done uniformly per model (the Hytale logic at half its numbers).
  Do not mix densities inside one model. Test the boss in-world beside 16× terrain before committing.

### 2.3 Clean layouts and atlas packing [V + C]
- Mipmapping: Minecraft uses **mip level 4**, so block/item atlas textures should be **multiples of 16** in each dimension. One bad-sized texture lowers the mip level of the **whole atlas**. Fill the unused texture area with colors that match the visible region, because mips average it in. https://gist.github.com/HalbFettKaese/c193caeccc94b793b29981aa38170ea6
- Newer versions have a per-texture `.mcmeta` `"mipmap_strategy"` (values like `mean`, `cutout`, `strict_cutout`, `dark_cutout`; e.g. vanilla `poppy.png.mcmeta` in 26.2-snapshot-1 uses `strict_cutout`). https://mcasset.cloud/26.2-snapshot-1/assets/minecraft/textures/block/poppy.png.mcmeta ; bug reports MC-304400 and MC-304652 on mojira.
- Block-atlas overflow: the atlas can exceed GPU max texture size (16384² on many GPUs). Then Minecraft throws a "Caught error stitching, removing all assigned resourcepacks" and "Unable to fit… try a lower resolution" error, and the reporter of MC-135848 hit it on an **adventure map** with more than 450 models. https://mojira.dev/MC-135848 . MC-306532 (1.21.11) says the error message became unclear. The "Pages of Atlas" Fabric mod splits oversized atlases (https://www.modpackindex.com/mod/173938/pages-of-atlas). [E] Budget the item/block atlas, because Animated Java and ModelEngine rigs put every texture into it.
- 22w46a+ atlas JSON (`atlases/blocks.json`) controls which directories get stitched. https://mcmodels.net/guides/5-atlases
- Bleeding lines at UV edges: use **Plaster** (JannisX11), which shrinks UVs slightly. The Java wiki says behavior is "inconsistent if UV extends below 0 or above 16". https://minecraft.wiki/w/Model and MC-156088 (https://mojira.dev/MC-156088).
- Tools for packing UVs or combining textures: the **Texture Stitcher** plugin (McHorse v1.0.7, rewritten packing in 2024; PR https://github.com/jannisx11/blockbench-plugins/pull/539), the built-in **Rearrange UV / texture template generator**, and **Clear Unused Texture Space**. Built-in "auto pack UVs" was declined (issue #2236 closed "not planned": https://github.com/JannisX11/blockbench/issues/2236). [C] Mirrored limbs that share one UV island (Mickey Joe video: "it's the same UV mapping, saves time") save texture space.
- [E] Practical rules: keep islands on the pixel grid with integer UVs, use 1 px padding between islands of different materials (mip bleed), group islands by material for easier palette work, and put symmetrical parts on shared islands (mirror UV) unless asymmetric wear is needed. Pick texture sizes that are powers of two, or at least multiples of 16.

---------------------------------------------------------------------------------------------------

## 3. Blockbench plugins relevant to modeling, UV and texturing

Source of versions and compatibility: the official registry https://raw.githubusercontent.com/JannisX11/blockbench-plugins/master/plugins.json (fetched 2026-10-13, 146 plugins). "min" is the minimum Blockbench version and "max" the maximum. [V] facts come from the registry; the maintenance notes are mine.

| Plugin | Ver | Author | Notes / status |
|---|---|---|---|
| **GeckoLib Models & Animations** | 4.2.5 | Eliot Lash, Tslat, Gecko, McHorse | min 5.0.0, max 6.0.0. Replaces the old "GeckoLib Animation Utils" 4.1.3 (marked superseded). Actively maintained. |
| **Animated Java** | 1.11.0 (2026-10-09) | SnaveSutit | min 5.1.4, desktop only. Targets MC 1.20.4 to 26.3. Adds Texture Slots. https://github.com/Animated-Java/animated-java/releases , https://animated-java.dev/docs/resources/faq |
| **CEM Template Loader** | 9.2.0 | Ewan Howell | min 5.0.0. For OptiFine/EMF entity re-models (vanilla mob replacement). Plus **EMF Animation Addon** 1.0.5. |
| **Free Rotation** | 1.2.1 | Godlander & Ewan Howell | min 5.0.0, desktop. Java item models "without rotation limitations"; **requires MC 1.21.4+**. Models can't be re-imported, so keep the .bbmodel. Mostly superseded by vanilla free/multi-axis rotation in 1.21.6/1.21.11+, but still useful for item models that need more. https://cdn.jsdelivr.net/gh/jannisx11/blockbench-plugins@master/plugins/free_rotation/about.md |
| **Optimize** | 1.2.8 | Krozi | "Hide concealed faces for better performance". Old (min 2.0.2) but still listed. MCModels recommends it as the final step before export. https://mcmodels.net/guides/18-optimizations [?] Test on 5.2. |
| **Plaster** | 1.1.0 | JannisX11 | Fixes in-game texture-bleeding lines by shrinking UVs slightly. Old but simple. |
| **Texture Stitcher** | 1.0.7 | McHorse | Merges several textures into one and handles mixed resolutions. |
| **MTools** | 2.1.0 | Malik12tree | Mesh operators and generators (min 4.9.4). Meshes only matter if your runtime supports meshes (see §5). |
| **UV Locker** | 1.0.0 | nklbdev | Keeps UVs fixed while moving mesh vertices (like Blender's "Correct Face Attributes"). |
| **Mr Salmon's Baked Ambient Occlusion** | 1.0.0 | Kai Salmon | Bakes AO, edge highlights and a ground plane into textures. **Works on meshes**. Good for a painted-AO style. https://cdn.jsdelivr.net/gh/jannisx11/blockbench-plugins@master/plugins/baked_ambient_occlusion/about.md |
| **Colour Gradient Generator** | 3.0.0 | Ewan Howell | Builds hue-shifted ramps from one color (min 5.0.0). |
| **Palette Swap** | 2.2.0 | Cmetanochkaa | Recolors whole hue families while keeping shading. Good for boss variants. |
| **Let there Be Noise** (2026-03) / **Brush Plus** / **Brush Tuna** (min 5.1.4) | | | Noise and brush tooling. [C] r/Blockbench: noise is "easy to misuse" (https://www.reddit.com/r/Blockbench/comments/1wzx004/). |
| **Repeating Textures** 3.0.0, **Texture Downscaler** 1.0.0 (min 5.0.3), **Texture Filtering** 1.0.0, **Grayscale Preview** 1.0.0 | | 0x13F, JannisX11 | Grayscale preview helps check values (readability). |
| **Ambient Occlusion** (SSAO viewport) 1.0.4 | | JannisX11 | Preview only. |
| **Double Sided Cubes** 1.0.2, **Outline Creator** 1.2.0, **Simplify Models** 1.0.0 | | | Java-specific helpers. |
| **Resource Pack Utilities** 1.10.0, **Asset Browser** 1.2.2 | | Ewan Howell | Browse vanilla assets in Blockbench. |
| **Export to Blender** 2.0.0, **glTF Importer** 1.2.1, **Reference Models** 1.1.0 | | 0x13F, JannisX11 | Interop (§4). |
| **Java Display Animator** 1.0.0 (2026-08) | | rieyi | Frame-baked item animations plus a resource pack and datapack. |
| **glTF to Minecraft** 0.1.2 (2026-08) | | MopicMP | Converts glTF (including Sketchfab) into cubes for GeckoLib or CPM. Experimental. |
| **No Java Limits** 1.0.0 | | Rajdacz | Infinite-size models for display entities. |
| **PBR Tools (pbr_preview)** | 1.2.2 | Jason J. Gardner | **max 4.11.9, so it does NOT run on Blockbench 5.x.** Use the built-in materials and Generate PBR Map (5.2 presets) or external tools instead. |

Also relevant:
- **Blockbench MCP plugin** (jasonjgardner, about 512 stars) for AI-driven modeling. https://github.com/jasonjgardner/blockbench-mcp-plugin . [C] An r/Blockbench thread (Oct 2026) shows a chat-built frog: https://www.reddit.com/r/Blockbench/comments/1x1welt/
- The Hytale plugin 0.11.0 (needs 5.2.0) is irrelevant to Java but shows active development.

---------------------------------------------------------------------------------------------------

## 4. Blender interop and texturing tools

### 4.1 Blender: is it worth it? [V + C + E]
- Blockbench's recommended export paths: **DAE for Blender modeling, glTF for Blender rendering**, glTF for Godot, FBX for Unity and Unreal. https://www.blockbench.net/wiki/guides/export-formats/
- The **Export to Blender** plugin writes a .blend scene (desktop, v2.0.0, updated for the 5.0 beta: https://github.com/jannisx11/blockbench-plugins/pull/755). The **glTF Importer** plugin brings glTF/GLB into Blockbench.
- **MCprep 3.6.3** (2026-07-12) supports Blender 2.83 to 5.2. It refreshed resources up to MC 26.2, reworked the JSON model importer, and handles the 26.1+ JSON model changes. **MCprep 4.0** will require Blender 4.2+ (meta-issue https://github.com/Moo-Ack-Productions/MCprep/issues/713). MCprep is for **renders and animations of Minecraft content**, not for authoring game assets. https://github.com/Moo-Ack-Productions/MCprep/releases
- **Mcblend** (Nusiq) targets Blender 4.5, for **Bedrock** models and animations, with auto UV-mapping. It is Bedrock-only, but its geo output is structurally close to GeckoLib's. https://github.com/Nusiq/mcblend/ , https://mcblend.readthedocs.io/en/stable/
- Blender pixel-art UV addons: **Pixel-Unwrapper / PixPaint** (noio, 410 stars, last push Oct 2025) https://github.com/noio/PixPaint , and the **Texel Density Checker** addon https://extensions.blender.org/add-ons/texel-density-checker/
- [C] On r/Blockbench in 2026, Blender comes up almost only as the **render** step ("Made in Blockbench & rendered in Blender"), for spheres and organic forms, or as a career skill for commission work. Examples: https://www.reddit.com/r/Blockbench/comments/1vfzd6h/ , https://www.reddit.com/r/Blockbench/comments/1wo3wyt/ , `social/r_mixed_2.txt`. One artist says Blockbench is "easier… because the program works with pixels in mind… but if you set up Blender with the right scale and grid you can nearly replicate it" (https://www.reddit.com/r/Blockbench/comments/1wkhmrb/).
- [?] A Cookstation blog (May 2026) still repeats the "22.5° rotation rule". That is outdated for 1.21.6+ targets, so treat such SEO blogs as low reliability. https://www.cookstation.blog/blender-export-json-minecraft
- **Verdict [E]: use pure Blockbench for every asset that ships** (Java JSON, GeckoLib geo/animation, Animated Java, EMF .jem). Blender is worth it only for:
  - (a) concept sculpts or blockouts to trace as reference (use 3D-plane reference images or Reference Models in 5.2),
  - (b) promotional and trailer renders (glTF to Blender with MCprep lighting),
  - (c) baking AO or curvature from a high-poly proxy to paint over.
  Rigging in Blender and re-exporting to Minecraft formats is **not worth it**: Blockbench 5.x now has armatures, IK with poles, mirror animating and Bezier keyframes for GeckoLib, and the Blender path loses Molang, box UV and per-bone pivots.

### 4.2 Texturing tools [V + C]
- **Blockbench Paint** (5.2): screen-space brush, layer groups, alpha mask, pressure and a HSV wheel. With 5.2 it is good enough to be the main painting tool. [C] Mineassets: "Paint on the model rather than in an image editor for anything positional, then touch up the flat texture for detail." https://mineassets.com/blog/uv-mapping-minecraft-models-explained
- **Aseprite v1.3.18.6** (2026-09-22; 1.3.18 stable was 2026-07-22) is the standard pixel-art editor. Use it with Blockbench's "Edit externally", and Blockbench live-reloads the PNG. https://www.aseprite.org/release-notes/ , https://blog2.aseprite.org/aseprite-v1318/ . [C] An r/Blockbench user mentions a "noise brush I made in Aseprite" plus Brush Plus.
- Krita, Photoshop, Clip Studio and Procreate all appear in the Hytale guide. paint.net is used by Mickey Joe (texture-pack artist): https://youtu.be/4w_N8r4j2vc
- **Substance 3D Painter** suits PBR rather than pixel art. Community helpers exist: jasonjgardner/substance3d_minecraft (LabPBR presets) https://github.com/jasonjgardner/substance3d_minecraft and an 80.lv pixel-art generator for Painter https://80.lv/articles/creating-a-pixel-art-generator-for-substance-3d-painter . [E] Overkill for 16–32 px textures. Use it only if you go "HD-entity" at 32+ px/block and want to generate LabPBR maps.
- Normal and specular generation for pixel art:
  - **Laigter** (GPL, about 1.3k stars): normal, specular and parallax from sprites. https://github.com/azagaya/laigter
  - **Pixel Maps** (LunarBlank): pixel-art PBR maps that keep crisp pixels. https://lunarblank.itch.io/pixel-maps
  - **Bonemeal**: a LabPBR converter and auto-generator. https://bonemeal.io/labpbr
  - Blockbench's built-in **Generate PBR Map** (4.12+, presets in 5.2).

### 4.3 Shading style for "Minecraft-quality" textures [V + C]
- Style guide (https://blockbench.net/wiki/guides/minecraft-style-guide/):
  - Build ramps from the midtone outward and use **hue shifting** (straight ramps look dull).
  - Use pixel tools (pencil, shape, fill, eraser) and deliberate pixel placement.
  - Avoid **banding, pillow shading, pancake shading, unnecessary dithering, noise and jaggies**.
  - Item textures are lit from the top-left.
  - **Entity textures make the top and front brighter than the bottom and back**, both within each face and between faces.
  - Check block textures in a 3×3 tiling wall early.
- Hytale variant (HD): paint AO and highlights into the texture, use the soft brush plus opacity pencil, avoid noise, and add color in shadows (a hint of purple), never pure black or white. https://hytale.com/news/2025/12/an-introduction-to-making-models-for-hytale
- [C] Mickey Joe's "Science of Pixel Art" video:
  - Build a palette by sampling and blurring reference photos.
  - Think of shading as manual anti-aliasing with palette colors.
  - Use the light-from-top-left convention.
  - Texture one side and copy it.
  https://youtu.be/4w_N8r4j2vc (transcript in `research/youtube/`)
- The "Hue Shifting Tutorial" short (Linky Playz, about 288k views) shows the demand for the technique: https://youtu.be/cR7De_c6N_8

### 4.4 Emissive, normal and specular so models look good under shaders [V]
- **LabPBR 1.3** (shaderLABS): https://shaderlabs.org/wiki/LabPBR_Material_Standard
  - `_n.png`: RG = normal in **DirectX (Y−)** convention, B = material AO (linear, 0 means fully occluded), A = height (use a minimum of 1, not 0, or it breaks some shaders' parallax occlusion mapping).
  - `_s.png`: R = perceptual smoothness, G = F0 for values 0–229 and predefined metals for 230–254 (iron 230, gold 231, …, silver 237), with 255 meaning "albedo as F0"; B = porosity for 0–64 and subsurface scattering for 65–255; **A = emission for 0–254, while 255 is ignored**.
  - Declare it with `texture.properties` → `format=lab-pbr/1.3`. Iris defines `MC_TEXTURE_FORMAT_LAB_PBR_1_3`, and 1.3 is the only supported version. https://shaders.properties/current/how-to/pbr_standards/
- Iris uses `_n`/`_s` suffixes next to the base texture, provided as extra atlases (`normals`, `specular`). Entity PBR works when the resource pack is up to date. An Iris dev closed a 1.21.4 "entity PBR broken" report as "user error (non updated pack)". https://github.com/IrisShaders/Iris/issues/2506
- [C] LabPBR packs can cause purple or black-line artifacts (r/minecraftshaders 2025–26: https://www.reddit.com/r/minecraftshaders/comments/1s1y7rk/ , https://www.reddit.com/r/minecraftshaders/comments/1n06u1e/). Test with the shader packs you target.
- Emissive options:
  - **GeckoLib** has built-in emissive/glowmask layers (AutoGlowingGeoLayer and a `_glowmask` texture). Wiki: https://github.com/bernie-g/geckolib/wiki/Emissive-Textures-(Geckolib5) (moved to a new GeckoLib 5 wiki). [?] The GeckoLib 5.5.2 changelog says GeckoLib "patch[es] out custom emissivity if not on Windows" because of GL issues on Linux and Mac. https://github.com/bernie-g/geckolib/blob/main/changelog.md
  - **ETF** (Entity Texture Features; 7.0.10 supports 26.1) handles OptiFine-style emissive textures for vanilla/EMF entities (default `_e` suffix, configurable in `emissive.properties`). https://github.com/Traben-0/Entity_Texture_Features/blob/master/.github/README-assets/EMISSIVE_GUIDE.md , https://modrinth.com/mod/entitytexturefeatures/version/7.0.10-fabric-26.1
  - For block/item models: `light_emission` per element (1.21.2+), plus LabPBR specular alpha under shaders.
- 26.1 snapshot 7 changed block models: **any block model can use cutout or translucent textures**, chosen by the sprite's pixels. Texture entries can be objects `{ "sprite": ..., "force_translucent": true }`. https://github.com/misode/deepslate/issues/75 , https://minecraft.wiki/w/Model . Blockbench 5.2.2 supports this.
- 26.3 replaced "Improved Transparency" with **Order-Independent Transparency (OIT)**. Re-test translucent textures, shader packs and glass. https://syntaxmine.com/articles/what-breaks-in-minecraft-26-3

---------------------------------------------------------------------------------------------------

## 5. Performance constraints and budgets

### 5.1 Vanilla JSON (block/item) model rules [V]
Sources: https://minecraft.wiki/w/Model and https://elkonia.com/datapack_codex/bbmodel.html (counts measured on the 26.3 Snapshot 10 vanilla jar).
- `from`/`to` must be in **-16..32**, which gives a 3×3×3-block envelope. Out-of-range cubes are clamped silently. Minecraft checks the raw from/to values, not the rotated vertices, which can confuse users (Ewan Howell's issue: https://github.com/JannisX11/blockbench/issues/3492).
- Rotation history:
  - **Before 1.21.6**: one axis, angles limited to -45/-22.5/0/22.5/45.
  - **1.21.6 (25w16a)**: any angle from -45 to 45.
  - **1.21.11 (25w46a)**: per-axis `x`/`y`/`z` rotation (applied X, then Y, then Z) and no range limit. Face names (and so culling) still use the original directions. https://github.com/JannisX11/blockbench/issues/3146 , https://github.com/JannisX11/blockbench/issues/2754
- **26.3 snapshot 3**: `shade` was removed and `shade_direction_override` was added.
- **This matters for the loader choice.** On **1.20.1 Forge and 1.21.1 NeoForge, the old rules apply to block/item models**. Backport libraries exist (Bay4lly "1.21.11 Java Item Model Backport" for Fabric 1.20.1 https://github.com/Bay4lly/1.21.11-Java-Item-Model-Backport ; "Modern Model Format" https://www.curseforge.com/minecraft/mc-mods/modern-model-format) but they are small and new [?].
- ModelEngine-style server plugins still apply the pre-1.21.6 cube rule. Bones rotate freely.
- **Display entities / Animated Java**: "Groups (bones) can rotate freely, on any axis and at any angle, on every Minecraft version". Put the cubes that need odd rotations into their own group. https://animated-java.dev/docs/nodes/groups

### 5.2 What makes entity models slow [V + E]
- Vanilla entity and block-entity rendering transforms and uploads vertices **on the single render thread, on the CPU, every frame**. That is why scenes with many vertices are CPU-bound while the GPU sits idle. **Accelerated Rendering** (Argon4W, MIT; 1.20.1 Forge and 1.21.1 NeoForge; 3.4M downloads; OpenGL 4.6; Iris-compatible; "alpha") moves this onto GPU compute shaders. https://www.curseforge.com/minecraft/mc-mods/accelerated-rendering
  - [E] So **cost ≈ visible vertices × visible entities × passes**. Each cube is up to 6 quads (24 vertices) before culling. Shaders add a shadow pass, so roughly ×2 for entities (Iris shadow program: https://shaders.properties/current/reference/programs/shadow/ ; the per-pack options are on https://shaders.properties/current/reference/shadersproperties/ordering/).
- **GeckoLib**: every animated bone is processed each frame, so cutting bones helps CPU cost. Optimizer mods exist: "GeckoLib Animation Optimizer" (https://www.modpackindex.com/mod/164844/geckolib-animation-optimizer) and "Geckolib Betterfps" for 1.20.1 Forge. GeckoLib is **5.5.7** (2026-09-22) on NeoForge, Forge and Fabric for 1.21.11 to 26.3, with older lines on 1.20.1 and 1.21.1. https://www.curseforge.com/minecraft/mc-mods/geckolib/files/8945638
- **Meshes in GeckoLib**: not native. The **GeckoMesh** library (bay4lly; 1.20.1 to 1.21.11 on Forge, Fabric and NeoForge, plus 26.1–26.2) bakes Bedrock poly_mesh into GeoCubes at load time with no per-frame overhead claimed. It is very new (about 49k downloads). https://www.curseforge.com/minecraft/mc-mods/geckomesh
- **Animated Java / display entities** (datapack + resource pack, no mods): **every group that contains cubes = one `item_display` entity**. Groups without cubes are free. Keep the bone count low, use Excluded Nodes, turn off "Auto Update Rig Orientation" on static rigs, keep the animation system on "Functions", and don't animate unseen rigs. The outliner shows an "E:" entity counter. https://animated-java.dev/docs/resources/faq . v1.11.0 also removed entity display names "to improve in-game performance". https://github.com/Animated-Java/animated-java/releases
- ModelEngine: "Bone count is entity count… a model with sixty bones costs sixty entities per spawn". https://elkonia.com/datapack_codex/bbmodel.html
- Static props as block models are baked into chunk meshes, so they cost **memory and meshing, not per-frame CPU**. Vanilla's own models are lean: across 4,192 model files only 347 define elements, 1,204 elements in total. Prefer `parent` plus texture swaps.
- Hidden faces: delete faces you never see (Optimize plugin), use `cullface` on block models, and use Entity Culling (tr7zw; supports up to 26.3) to skip occluded entities. https://modrinth.com/project/NNAgCjsB
- objmc (Godlander) bypasses model limits by baking vertices into textures with core shaders. It is **incompatible with Sodium in practice** (closed "wontfix", https://github.com/Godlander/objmc/issues/47) and with shader packs (#52). **Avoid it in a modded + shaders setup.** https://github.com/Godlander/objmc

### 5.3 Texture size impact [V + C]
- [C] Every resolution step roughly multiplies memory by 4 (PackAnvil guide https://packanvil.com/en/guides/resolution-16x-32x-64x-128x). Entity textures are separate GPU textures and are not atlased in GeckoLib/EMF, while item and display-entity textures go into the block/item atlas (overflow risk in §2.3).
- [C] MCModels' performance guide: fewer cubes, 16× textures and the Optimize plugin. https://mcmodels.net/guides/18-optimizations

### 5.4 Recommended budgets [E — my synthesis, not an official standard]
These target ≥50 fps on a mid-range PC (for example a GTX 1660 or RTX 3060 with a 6-core CPU) with Iris and a medium shader. Tune them after profiling with F3 and Spark.

| Asset | Cubes (after culling) | Bones | Texture (16 px/blk / 32 px/blk HD) | Notes |
|---|---|---|---|---|
| Static prop (block/item JSON) | 1–40 | – | 16²–64² / 32²–128² | Use parent models, cullface, rotate cubes not "stairs". |
| Dungeon decoration rendered as entity/display | ≤60 | ≤5 | 64² | Prefer block models where possible. |
| Regular mob (GeckoLib) | 30–150 | 10–30 | 64²–128² / 128²–256² | Several on screen at once. |
| Elite/mini-boss | 150–300 | 25–50 | 128² / 256² | 1–3 on screen. |
| Main boss (GeckoLib) | 300–800 (hard ceiling about 1,500) | 40–80 | 256² / 512² (one texture, since GeckoLib allows one per model) | Alone in the arena. Phase-2 parts can be hidden bones. |
| Boss as Animated Java rig (vanilla) | cubes cheap-ish | **≤25–40 groups with cubes** | in atlas (watch 16384²) | Every bone is an entity. |

Reference point: a commercial Sketchfab "Custom Minecraft Boss/NPC" claims "over 1,800 elements… designed for high performance" at 10.9k triangles (https://sketchfab.com/3d-models/custom-minecraft-boss-npc-21800bedfd044681bae00610e85c1258). [E] Treat that as the upper end, not the norm.

---------------------------------------------------------------------------------------------------

## 6. Where quality models are shared, and the quality bar

### 6.1 Marketplaces and showcases [V]
- **MCModels** (https://mcmodels.net): a quality-controlled marketplace where vendors are vetted and every product is reviewed. It lists 200+ vendors (e.g., RuneFist Studios, Erocavontic, Endesman/E-Magination). Boss packs often ship with "30+ animations, VFX, sounds" for MythicMobs/ModelEngine. Examples:
  - The Fallen Defender | Ultra Boss: https://mcmodels.net/products/10425/the-fallen-defender-ultra-boss
  - Tesseract Boss (tested on Paper 1.21.4 with ModelEngine R4.0.5): https://mcmodels.net/products/16032/tesseract-boss
  - About page: https://mcmodels.net/information/about
- **BuiltByBit** Minecraft models: 675 or more ModelEngine-ready models, aimed at plugin servers (ItemsAdder, Oraxen, ModelEngine). https://builtbybit.com/resources/minecraft/models/modelengine/
- **Sketchfab** Blockbench artists. Soulslike-relevant: **kenddie** ("Lady Maria Bloodborne", "Abyss Watchers style armor", "Bone knight", "Nazgul") https://sketchfab.com/kenddie ; **Athinea** https://sketchfab.com/Athinea ; gammabyte (dragons).
- **BlockModels.com** (Java block models with JSON download) https://www.blockmodels.com/ . The Blockbench share service is temporary only.
- **BDEngine** (block-display.com), a web editor and library for display-entity models. Version 2027.1 came out 2026-10-07 and supports vanilla 1.19.4 to 26.3+. https://block-display.com/bdengine-updates
- Studios and commission prices (for orientation): ArtsByKev Studio charges from $500 per custom asset, $75–90/h for fixes (https://www.artsbykevstudio.com/services). Athinea's commission tiers are by mob size (https://athinea.carrd.co/).
- Mod references for a soulslike quality bar:
  - **L_Ender's Cataclysm** bosses (Ignis and others; artists Mangotastejuice, LegendNoob07 and others; CC-BY-NC-ND) https://lendercataclysm.wiki.gg/wiki/Ignis , https://en.namu.wiki/w/L_Ender's%20Cataclysm
  - **Mowzie's Mobs** (1.20.1/1.21.1) https://www.curseforge.com/minecraft/mc-mods/mowzies-mobs
  - **Fresh Animations** (FreshLX; vanilla+ re-animated mobs that keep 16× textures; 101M+ downloads; up to 26.3; needs OptiFine or EMF+ETF) https://fresh-animations.com/ , https://modrinth.com/project/50dA9Sha

### 6.2 "Vanilla+" vs "HD voxel" [C + E]
- Vanilla+ means 16 px/block, no mixels, low element count, shape from the model and detail from the texture. This is the official Blockbench Minecraft Style Guide's stance, which also calls for slants via rotation rather than stairs and planes with transparency instead of many tiny cubes. It is also the r/Blockbench consensus. Fresh Animations shows that motion, not resolution, carries "quality" in vanilla+.
- HD voxel (Hytale model, Minecraft Dungeons DLC art) means a consistent higher density (32–64 px/unit), painted AO and light, and stylized proportions. It looks premium but clashes with 16× terrain unless the whole map's resource pack is consistent.
- [E] For a soulslike map, use vanilla+ geometry rules and a single density per asset class. Spend the budget on silhouette, animation (GeckoLib or Animated Java), emissive accents and LabPBR maps rather than raw texture resolution.

---------------------------------------------------------------------------------------------------

## 7. Academic and technical write-ups (marginal relevance)
- **Voxify3D: Pixel Art Meets Volumetric Rendering** (CVPR 2026; arXiv 2512.07834). It turns meshes into stylized voxel art with pixel-art guidance and palette quantization (Gumbel-softmax). Possibly useful for concept blockouts. https://arxiv.org/html/2512.07834 , https://yichuanh.github.io/Voxify-3D/
- **Texel Splatting: Perspective-Stable 3D Pixel Art** (arXiv 2603.14587). It is about rendering, not asset authoring. https://arxiv.org/pdf/2603.14587
- **Dream Cubed** (Sakana AI/NYU, arXiv 2604.22847) and **Block3D** (arXiv 2608.19567) cover generative Minecraft-block and voxel structures. They are about world and structure generation, not entity models.
- Atlas packing: **TABI: Tight and Balanced Interactive Atlas Packing** (arXiv 2602.07782), **Box Cutter** (Limper et al., SIGGRAPH 2018), and **Atlas refinement with bounded packing efficiency** (TOG 2019). These target arbitrary charts. For axis-aligned, pixel-snapped cube faces a simple shelf or rect packer (like Texture Stitcher) is enough. https://arxiv.org/html/2602.07782 , https://www.cs.ubc.ca/labs/imager/tr/2018/BoxCutter/Limper2018_BoxCutter.pdf
- Conclusion: no paper changes the practical pipeline. The rules that matter come from the community (style guide, mipmapping gist, LabPBR).

---------------------------------------------------------------------------------------------------

## 8. Social sources (Reddit, YouTube, X)
- Reddit via Arctic Shift. Dumps are in `research/modeling/social/r_*.txt`. Key threads:
  - Mixels opinions: https://www.reddit.com/r/Blockbench/comments/1vjx5qn/ , /1t61smv/ , /1mdu0nw/ , /1gky5ih/ (Box UV with non-integer cubes leads to mixels, so use per-face UV).
  - Plugin wishlist (Oct 2026), where a noise brush was the most upvoted request: https://www.reddit.com/r/Blockbench/comments/1wzx004/
  - Blockbench 5.2 announcement: https://www.reddit.com/r/Blockbench/comments/1wjqyao/
  - BDEngine vs Animated Java (r/MinecraftCommands): Animated Java for custom models and resource packs, BDEngine for vanilla block displays. https://www.reddit.com/r/MinecraftCommands/comments/1lvjpsn/
  - An Animated Java boss on a modded 1.20.1 server: https://www.reddit.com/r/MinecraftCommands/comments/1r0pnrk/ . A commenter warns that "cubes shift by 0.02 pixels… you see gaps in game", so keep values on the grid.
- YouTube. Transcripts were read only for the first two videos below; the rest come from search results (title and views only), and the search dump is `social/yt_search_1.txt`:
  - Blockbench 5.2 official, https://youtu.be/9MET5-wH5uw
  - Mickey Joe "How to texture in the Minecraft Style – Science of Pixel Art" (20.8k views), https://youtu.be/4w_N8r4j2vc
  - Blockbench "How To Create PBR Textures for Vibrant Visuals" (36k views; Bedrock MERS but the same tool), https://youtu.be/IcZB4eXImIY
  - ArtsByKev "Blockbench for Beginners" (1.08M views), https://youtu.be/dsax5p4brN8
  - Brandon James Greer "Low-Poly Models with Pixel Texture" (535k views), https://youtu.be/GukhptdHlPk
- X/Twitter: there is no search route. The @blockbench profile was confirmed via fxtwitter (about 35.7k followers; "development updates"), but I could not harvest any relevant status links, because tweetlook mirrors returned 404 and no relevant x.com links appeared in the fetched pages. **No X posts are cited.**

---------------------------------------------------------------------------------------------------

## 9. Recommended pipeline [E]
1. **Pick the runtime per asset class first**, because it fixes the UV and rotation rules:
   - static props → Java block/item JSON
   - mobs and bosses → GeckoLib (per-face UV, 3-axis cubes, one texture per model)
   - vanilla mob re-skins → EMF/CEM
   - mod-free set pieces → Animated Java display rigs
2. Block out in Blockbench 5.2.2 with Reference Models or 3D-plane references. Keep every cube integer-sized and on the grid.
3. Run per-face UV with Auto UV on all faces, then Create Texture with Rearrange UV at a chosen density of 16 or 32 px/block. Then hand-pack: mirror shared limbs, put islands on the grid, keep sizes multiples of 16 or powers of two.
4. Run the Optimize plugin (hidden faces) before final texturing so you don't paint invisible faces.
5. Paint:
   - Base colors, ramps and hue shifting in Aseprite (or in Blockbench with the Colour Gradient Generator).
   - Seams with the 5.2 screen-space brush.
   - AO with the Baked-AO plugin (meshes) or by hand.
   - Check values with Grayscale Preview.
6. Make shader maps:
   - `_n`/`_s` LabPBR 1.3 via Generate PBR Map, Laigter or Bonemeal, then hand-fix.
   - Emissive through LabPBR specular alpha plus a GeckoLib glowmask or ETF `_e`.
7. Profile in-world (F3, Spark) with Iris and the target shader pack. Use Entity Culling, and Accelerated Rendering (1.20.1/1.21.1) for heavy scenes.
