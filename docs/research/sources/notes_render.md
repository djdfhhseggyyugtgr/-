# Rendering, Shaders & Performance — research notes (as of 2026-10-13)

Scope: best visuals at >=50 fps for a soulslike adventure map (mods + RP + datapacks) on Minecraft Java.
Legend: **[V]** = verified from primary/official source (release notes, GitHub, Mojang); **[S]** = secondary site/news (generally reliable, not primary); **[C]** = community report/opinion (Reddit/YouTube/Discord mirrors); **[?]** = uncertain / possibly synthetic / promo.
Raw search/fetch JSON: `research/render/`, YouTube transcripts: `research/youtube/`.

---

## 1. Platform status: Vulkan, Vibrant Visuals, Sodium/Iris per version

### 1.1 Mojang's Vulkan transition
- [V] 18 Feb 2026 Mojang blog: Java will switch OpenGL -> Vulkan as a step toward Vibrant Visuals; Vulkan ships side-by-side with OpenGL in snapshots/releases during testing; **OpenGL will be removed once Vulkan is stable**, players notified in advance; modders told to move off raw OpenGL and use internal rendering APIs. https://www.minecraft.net/en-us/article/another-step-towards-vibrant-visuals-for-java-edition
- [V/S] 26.2 (16 Jun 2026): experimental Vulkan backend + "Graphics API" option (Default / Prefer Vulkan / Prefer OpenGL). Min Vulkan 1.2; macOS via MoltenVK; reversed depth buffer; Vulkan prefers dGPU. https://speaway.com/articles/minecraft-java-opengl-to-vulkan , https://syntaxmine.com/articles/minecraft-26-4-snapshot-1
- [V] 26.4 Snapshot 1 (22 Sep 2026): **Default now = Prefer Vulkan**; automatic crash fallback to OpenGL removed; OpenGL still selectable by hand. OIT (order-independent transparency, new in 26.3, replaced Improved Transparency) reworked; defines renamed (`OIT_COEFF_COUNT`->`OIT_NUMBER_OF_DEPTH_BINS` etc.) -> shader packs/core shaders need updates for 26.4. https://www.minecraft.net/en-us/article/minecraft-26-4-snapshot-1 , https://syntaxmine.com/articles/minecraft-26-4-snapshot-1
- [S] 26.3 also added `/posteffect` (add/remove resource-pack post-processing effects per player) and `/compute`. Post effects are client-side resource-pack assets. https://minecraft.wiki/w/Commands/posteffect , https://syntaxmine.com/articles/compute-posteffect-commands-26-3
- Vanilla Vulkan performance (no shaders):
  - [C] Dave Computes (YouTube, ~Sep 2026): 12 chunks, Fancy. RTX 5070: OpenGL 753 avg / 227 1% -> Vulkan 1279 / 396; RTX 5060 526 -> 774; Pascal +10-15%; Maxwell ~0%. All AMD/Intel GPUs he tried **failed to launch Vulkan** at that time. https://www.youtube.com/watch?v=uU0tiniGzlg
  - [C] Counter-reports: r/Minecraft "Vulkan is worse than OpenGL" (26.4-snap1: 236-310 OpenGL vs 158-174 Vulkan); a 9070 XT user: 1800-1900 OpenGL vs 1400-1600 Vulkan on 26.3. https://www.reddit.com/r/Minecraft/comments/1wnx7ys/
  - [V] Mojira: MC-307452 (Vulkan perf regression, fixed), MC-308887 (26.2 OpenGL perf regression, Won't Fix). https://mojira.dev/MC-307452 , https://mojira.dev/MC-308887
  - Takeaway: Vulkan speeds up *vanilla* on newer NVIDIA, is inconsistent elsewhere, and is irrelevant to Iris (OpenGL-only).

### 1.2 Vibrant Visuals on Java
- [V] Not in any Java development version as of late Sep 2026 (wiki updated 25 Sep 2026: "planned... has not appeared in any development versions yet"). Minecraft Live (26 Sep 2026) announced VV for Switch 2 Bedrock (27 Oct 2026), nothing dated for Java. https://theminecraftwiki.com/wiki/vibrant-visuals/ , https://theminecraftwiki.com/wiki/minecraft-live-september-2026/ , https://www.minecraft.net/en-us/article/mclive_sept2026_recap
- [V] Oct 2025 dev update: render-thread extraction mostly done for entities/particles/UI, chunks next. https://www.minecraft.net/en-us/article/the-road-to-vibrant-visuals-on-java
- **Verdict:** not a viable option for this project now; no date. Fan look-alikes: Visual Vibrance (Iris pack, archived Feb 2026), Vivid Visuals (Iris, 26.x), "Natural Visuals" Fabric mod (26.2 test, Iris not compatible). https://github.com/jbritain/visual-vibrance , https://www.curseforge.com/minecraft/shaders/vivid-visuals , https://www.reddit.com/r/Minecraft/comments/1x4bsx5/
- [S] Note: VV uses MERS (Bedrock) PBR format, not LabPBR (MineGraph docs). https://docs.minegraph.cn/labpbrmaterialstandard.html

### 1.3 Sodium / Iris / Embeddium / Oculus status by version
| MC version | Loader | Renderer | Shader loader | Status notes |
|---|---|---|---|---|
| 1.20.1 | Forge | Embeddium 0.3.31 (Sodium 0.5.8 fork) | Oculus 1.8.0 | [S/V] Both effectively frozen. Embeddium newest build overall 2025-01-24; no Forge builds past 1.20.2. Oculus issues still being filed on 1.8.0 in 2026 (#848, Jan 2026). Embeddium marks "tainted" when Oculus present. https://minecrafthub.io/articles/sodium-vs-embeddium , https://github.com/Asek3/Oculus/issues/848 , https://github.com/FiniteReality/embeddium/issues/529 |
| 1.20.1 | Fabric | Sodium 0.5.x | Iris 1.6/1.7.x | old but stable |
| 1.21.1 | NeoForge/Fabric | **Sodium 0.8.12 / 0.8.13 backport** (6 Jul 2026: "up to +115%" world render perf, better translucency, less micro-stutter, faster entity rendering) | **Iris 1.8.13+** (1.8.14-beta.1, 13 Jun 2026) | [V] Sodium 0.8.12 notes: "Iris works as of 1.8.13"; incompatible with unofficial "Sodium Options API" and dependents. Sodium 0.9.x does NOT exist for 1.21.1. https://github.com/CaffeineMC/sodium/releases/tag/mc1.21.1-0.8.12 , https://github.com/IrisShaders/Iris/issues/3243 |
| 1.21.11 (last 1.x) | Fabric/NeoForge | Sodium 0.8.14 (0.8.15-beta) | Iris 1.10.8 | [S] androidhire table (3 Oct 2026). https://www.androidhire.com/best-minecraft-shaders-high-fps |
| 26.1.x / 26.2 | Fabric/NeoForge | Sodium 0.9.2 | Iris 1.11.4 | [V] Sodium 0.9.0 (16 Jun 2026) moved all rendering to Blaze3D; first *experimental* Vulkan support. https://github.com/CaffeineMC/sodium/releases/tag/mc26.2-0.9.0 , https://github.com/CaffeineMC/sodium/pull/3735 |
| 26.3 (current) | Fabric/NeoForge | Sodium 0.9.2 (0.9.3-alpha) | **Iris 1.11.7** (NeoForge since 30 Sep) | [V/S] https://syntaxmine.com/articles/what-breaks-in-minecraft-26-3 , https://github.com/CaffeineMC/sodium/releases |
| 26.4 snapshots | — | — | — | Vulkan default; Iris requires switching to "Prefer OpenGL"; OIT define renames will need pack updates. |

- [V/S] **Iris does not support Vulkan**: Iris 1.11.0 (26.2) note "Vulkan is not supported"; nothing changed for 26.3. https://rockstarshaders.com/iris-shaders-mac , https://www.androidhire.com/best-minecraft-shaders-high-fps
- [S/?] **Aperture** = Iris team's next-gen shader mod (TypeScript pipeline -> now Slang) built for Vulkan; example pack exists; not publicly released as of Oct 2026. Fabulously Optimized issue (May 2026) states "once Vulkan becomes default, Iris will be discontinued" — maintainer's expectation, unconfirmed. https://shaders.properties/aperture/migration/ , https://github.com/IrisShaders/Aperture-Example-Pack , https://github.com/Fabulously-Optimized/fabulously-optimized/issues/1122 , https://github.com/ambrosia13/Amaryllis-Shaders
- Vulkan-native shader/RT alternatives (all early/experimental):
  - [V] **Vitrail Shaders** (beta, 26.2/26.3, Fabric+NeoForge): runs unmodified OptiFine-format packs on the Vulkan backend (Bliss, BSL, Complementary, Euphoria, Photon, Solas…), has Render Scale slider; author: "if you want a finished picture today use Iris on OpenGL"; AI-assisted development disclosed. https://www.modpackindex.com/mod/172368/vitrail-shaders , https://github.com/avpbynf/Vitrail-Shaders/blob/main/docs/why.md
  - [V] **Sulkan** (Fabric, Sodium-based, own pack format, 26.2/26.3). Promo video claims "5-10x FPS" [?]. Reddit: "Sulkan… works much less efficient than Vitrail" [C]. https://sulkan.org/ , https://www.youtube.com/watch?v=DQh1s2ChpJA , https://www.reddit.com/r/minecraftshaders/comments/1t20e0t/
  - [V] **Caustica** (26.2 Fabric, Vulkan HW path tracing, DLSS Ray Reconstruction + FG, NVIDIA RTX; LabPBR materials). Early. https://github.com/ComfyFluffy/Caustica
  - [V] **Radiance** 0.1.6-alpha (30 Sep 2026): own Vulkan C++ renderer w/ HW RT, DLSS/FSR upscaling + frame gen, ray-traced DH terrain, Create/Flywheel; **MC 1.20.1, 1.21.1, 1.21.4 on Fabric/Forge/NeoForge** (Win/Linux). RTX 5090 4K ~120 fps RD16 with DLSS [C]. https://github.com/Minecraft-Radiance/Radiance/releases , https://www.youtube.com/watch?v=BIw9cJRraNs
  - [C] Other hobby Vulkan RT mods posted on r/minecraftshaders (Oct 2026). https://www.reddit.com/r/minecraftshaders/comments/1x1svu0/
- **Implication:** For a map shipping now, lock to a version where Iris on OpenGL works (1.21.1 NeoForge or 26.3) and tell players to keep Graphics API = OpenGL (26.x). Do not target 26.4+ until Iris/Aperture story is clear.

---

## 2. Shader packs (2026 landscape) & cost

### 2.1 Pack status (authors' listings, 3 Oct 2026, androidhire) [S]
| Pack | Author rating | Latest | Newest MC | Notes |
|---|---|---|---|---|
| Complementary Reimagined / Unbound | Potato–High(Ultra) | r5.9.3 (15 Sep 2026), r5.10 dev on Patreon | 26.3 | r5.8 (May 2026) added Voxy + DH improvements; r5.9 "improved FPS, rebalanced profiles"; integrated PBR + LabPBR. https://www.complementary.dev/changelogs/ |
| Euphoria Patches (Complementary add-on) | — | 1.10.x for r5.9.x (15 Sep 2026) | 26.3 | default "clean canvas"; extra fog/darkness desaturation/seasons, block-emission intensity, best modded-block material support; Photonics support (1.9.0+). https://www.euphoriapatches.com/features/ |
| Photon | Low–High (Ultra) | v1.3b (14 Apr 2026) | 26.1.2 (likely still works) | voxel colored lights only on Ultra; optional temporal upscaling; not Apple GPUs. Profile matrix: Low=1024 shadow, no VL; Medium +VL; High +entity shadows, GTAO, SSR, colored shadows; Ultra +block-entity shadows, caustics, colored lights. https://deepwiki.com/sixthsurge/photon/2-configuration-system |
| BSL | Low | 10.1.8 (21 Sep 2026) | 26.3 | cheap, huge settings menu; Photonics-patchable. |
| Bliss | Low–High +Screenshot | 2.1.2 (23 Nov 2025) | 26.3 | fantasy look, strong fog/volumetrics; floodfill colored light WIP bugs (#576); dense-foliage FPS drops (#634). |
| Eclipse (Bliss edit) | — | GitHub "Unstable" | — | community favourite for landscapes/atmosphere [C]. https://github.com/Merlin1809/Eclipse-Shader |
| Solas | Low–High | 3.7b (23 Aug 2026) | 26.2 | colored block light, volumetric clouds, moderate cost. |
| Rethinking Voxels | Medium–High | r0.1-beta (last Jun 2025) | 1.21.10 | voxel RT colored block light + sharp shadows (Complementary fork). Very heavy. |
| Sildur's Vibrant / Enhanced Default | Potato–High | 2.02 / 1.20 (15 Sep 2026) | 26.3 | runs on anything incl. Macs. |
| MakeUp Ultra Fast, Mellow, Miniature | Potato | Sep 2026 | 26.3 | low-end fallbacks; Mellow supports DH + Voxy. |
| Kappa, Nostalgia | High / Medium | Feb 2025 | 1.21.4 | stale. |
| SEUS PTGI HRR 3 | — | old | — | loads in Iris; motion-blur issues; uses oldPBR not LabPBR. |
| Spooklementary (Complementary edit by SpacEagle17) | — | v2.0.4 (Dec 2025) | 26.3 | "spooky, very moody" — good dark-fantasy base. https://www.curseforge.com/minecraft/shaders/spooklementary |
| Path-traced/RT newcomers | — | 2026 | — | PathMax, Phoxel PT, Serie, Lyrae, Alpha Piscium (ReSTIR GI), Trace; IterationRP/IterationT (Bilibili; controversy over code origin + paid) [C]. |
| Horror/dark niche | — | 2026 | — | Rakoun DarkFantasy Visuals, Gravemist (26.2 horror fog), LostTape — small projects. |

### 2.2 Photonics (Iris add-on, software voxel ray tracing)
- [V] Fabric, latest builds for 1.21.11 (0.3.x "ReSTIR update"); soft block-light shadows, GI, colored glass light, 20-100 lights/chunk; supported by Euphoria Patches 1.9.0+, Photon (GitHub), Eclipse, Shrimple; BSL patched. Alpha; not NeoForge per listing. https://www.modpackindex.com/mod/115341/photonics-a-raytracing-engine , https://modrinth.com/mod/photonics/version/0.2.9+1.21.11

### 2.3 Measured / reported FPS (mixed reliability)
- [C, good] zWORMz, RTX 5090 + 9800X3D, **4K, 20 chunks, all settings maxed**, Iris (Feb 2025): BSL Ultra ~300 fps; Complementary Unbound Ultra ~170 fps (night); SEUS PTGI E12 ~120; **Rethinking Voxels ~60-64 fps** (heaviest tested). https://www.youtube.com/watch?v=lCk9zMC34co
- [V/C] Iris #3241 (RTX 3060 Laptop, 1080p, Complementary Reimagined r5.8.1, RD 25, shadow dist 15, cap 140): 26.1.2 = 138 fps; 26.2 = 84 fps (shadow pass selects ~2x sections; open). https://github.com/IrisShaders/Iris/issues/3241
- [V] Iris #2818/#2940: shader FPS 1.21.1 ~110-130 vs ~70 on 1.21.4+ (RTX 4060 laptop); root cause HorizonRenderer, fixed by PR #2941 (Dec 2025). https://github.com/IrisShaders/Iris/issues/2940
- [C] r/minecraftshaders comments (Dec 2025–Oct 2026):
  - "3060: Complementary Unbound med-high @1440p ~75 fps"; another "Complementary drops to 40-45 on a 3060; Bliss/Photon run better". https://www.reddit.com/r/minecraftshaders/comments/1oqhfqm/ , https://www.reddit.com/r/minecraftshaders/comments/1ph195s/
  - "Bliss & Photon ~20% higher FPS than Complementary at default tier; 300+ mod pack + DH: ~100 avg Bliss/Photon vs ~70 Complementary; Complementary struggles in forests". https://www.reddit.com/r/minecraftshaders/comments/1q4rmqp/
  - "GTX 1080 Ti + R5 3600: Photon/Bliss/BSL Ultra 70-100 fps". https://www.reddit.com/r/minecraftshaders/comments/1pwp2xe/
  - "4070 Super, 400+ mods, Bliss BSPT: 110-150 typical". https://www.reddit.com/r/minecraftshaders/comments/1sph249/
  - "4070 mobile 60+ fps with ~1.5-1.7x FSR + Voxy". https://www.reddit.com/r/minecraftshaders/comments/1sriihi/
  - "4070: IterationRP 40-60 fps". https://www.reddit.com/r/minecraftshaders/comments/1u1usg0/
  - Rethinking Voxels: "maxed RT settings 14 fps on 9070 XT"; "even with 4090 performance is horrible". https://www.reddit.com/r/minecraftshaders/comments/1wwi5r3/ , /1wryah0/
  - Opinion summary: Photon "best looks/perf"; Bliss/Eclipse "best atmosphere"; Rethinking Voxels "best indoor/cave lighting if PC is good enough"; Euphoria+Photonics as RT alternative. https://www.reddit.com/r/minecraftshaders/comments/1q2i231/ , /1x38b8p/
- [?] mctoolbox.net "benchmarks" (GTX 1660 Super @1440p/12 chunks: BSL default 104 fps; Rethinking Voxels default 64 fps) — identical vanilla baselines across pages and RV number implausible vs RTX 5090 data -> treat as **unreliable/synthetic**. https://mctoolbox.net/shader/bsl-shaders , https://mctoolbox.net/shader/rethinking-voxels
- [?] fpscalculator/theframecoach/fpsbench style "estimated FPS" pages — synthetic, ignored.
- YouTube benchmark videos exist per GPU (mostly no-commentary; numbers on-screen only — not extractable): RTX 3060 11 shaders on 26.1.2 (Adurite, O43IPzbpqZk), RTX 3060 20 shaders 1080p/1440p/4K (Hueemann, 2l5ijNwvTbg), GTX 1660 Super 10 shaders (369 Benchmarks, v6GkniztLcQ), GTX 1660S + DH + Photon (DP0DA5Yu9yo), RTX 4070 11 shaders (AesthetiTech, mXaC4Oh8OXo), RTX 4070 Super 8 shaders 1440p (XImarvXI, 3MmotrhCzqw). Useful for the user to eyeball on their GPU.

### 2.4 Fit for dark-fantasy soulslike mood (opinion + feature reasoning)
- **Complementary Unbound + Euphoria Patches** (or Spooklementary as a starting preset): deep nights, darkness desaturation, configurable fog, aurora/block-emission controls, best modded-block support, Voxy/DH support, Photonics optional. Safest all-rounder and best mod compatibility. Cost: medium; community says heavier than Photon/Bliss in dense foliage.
- **Bliss / Eclipse**: best volumetric fog & atmosphere for moody exteriors; cheaper than Complementary per community; NeoForge invisible-player caveat (see §5).
- **Photon (Ultra)**: semi-realistic, colored voxel lights for torch/lantern/soul-fire mood; efficient; Photonics support; last release Apr 2026 (26.1.2).
- **Rethinking Voxels / Photonics**: torch-lit dungeon interiors with true colored shadows — spectacular for boss arenas but expensive (RTX 4080/4090-class for 60 fps at 1440p+, per community).
- Vanilla fog via **environment attributes** is NOT honored by shader packs (see §5) — the mood must be built in the shader pack settings.

---

## 3. PBR / LabPBR / emissives

- [V] **LabPBR 1.3** (shaderLABS): `_n` normal (DirectX Y-), B = material AO, A = height (use >=1, 0 breaks some POM). `_s`: R = perceptual smoothness; G = F0 0-229 linear, 230-237 predefined metals (iron, gold, Al, Cr, Cu, Pb, Pt, Ag), 255 = albedo-as-F0 metal; B = porosity 0-64 / subsurface 65-255; **A = emission 0-254 (255 = none)**, emitted colour = albedo. https://shaderlabs.org/wiki/LabPBR_Material_Standard
- [V] Iris: `_n`/`_s` atlases; declare `format=lab-pbr/1.3` in `texture.properties` -> `MC_TEXTURE_FORMAT_LAB_PBR(_1_3)` defines; only 1.3 supported. oldPBR/seusPBR only for SEUS. https://shaders.properties/current/how-to/pbr_standards/
- Support: Complementary (RP Support: IntegratedPBR vs labPBR; integrated PBR covers vanilla textures procedurally — custom textures need real maps), Photon, BSL, Bliss/Eclipse, Rethinking Voxels, Radiance/Caustica (LabPBR-style). [S]
- Cost: normal+specular adds 2 extra atlases (VRAM + sampling); **POM** is the expensive part, scaling with texture resolution and step count; [C] users report 256x/512x PBR packs (e.g., PIXLLI) needing lower res on AMD due to VRAM. Popular base packs: Patrix (32x basic … 128x, made for shaders, tiling/randomization; updated for 26.3 on 2 Oct 2026), Stratum. https://www.curseforge.com/minecraft/texture-packs/patrix-32x , https://www.reddit.com/r/minecraftshaders/comments/1wf7h42/
- Recommendation (reasoning): author custom textures at 32x with LabPBR `_n`/`_s`; ship POM-friendly height but tell players to disable POM on low tiers; use specular alpha for emissive runes/eyes/embers.
- Tools [S]: Blockbench has PBR texture-set support (4.12+, aimed at Bedrock MER) and a PBR preview plugin; LabPBR channel packing still manual/external. https://github.com/jannisx11/blockbench-plugins/pull/545
- Emissive entities: GeckoLib 5 has built-in emissive/glowmask layers (fullbright texture parts). https://github.com/bernie-g/geckolib/wiki — shader packs may treat these differently; Iris supports `entity.properties` custom entity IDs and `block.properties` IDs that packs use for emission/colored light (editing a pack’s properties is possible but check redistribution license). https://github.com/IrisShaders/ShaderDoc/blob/master/iris-features.md
- [V] Iris #3053 (open): **block_display entities render as entities, not blocks → emissive blocks shown via displays look dimmer than real blocks in all packs tested** (Complementary). Affects Animated Java/display-entity props. https://github.com/IrisShaders/Iris/issues/3053
- [V] Iris ignores custom **core shaders** from resource packs while a shader pack is active (custom armor shaders, text/HUD tricks). https://github.com/IrisShaders/Iris/blob/26.1/docs/usage/limitations.md , https://github.com/IrisShaders/Iris/blob/1.20-new/docs/development/compatibility/core-shaders.md

---

## 4. Performance mods & entity rendering

### 4.1 Core stack (version availability)
- Fabric/NeoForge 26.3: Sodium 0.9.2, Lithium 0.26.2, Entity Culling 1.11.2, ImmediatelyFast 1.17.1, FerriteCore, ModernFix (official builds to 1.21.x; "ModernFix-mVUS" fork for 26.x), MoreCulling 1.8.x (Forge 1.20.1 port "More Culling Reforged"). [S] https://syntaxmine.com/articles/what-breaks-in-minecraft-26-3 , https://www.curseforge.com/minecraft/mc-mods/moreculling
- 1.21.1 NeoForge: Sodium 0.8.12/0.8.13, ModernFix 5.27.x, FerriteCore 7.0.x, Entity Culling 1.10.x, ImmediatelyFast 1.6.x. [S]
- 1.20.1 Forge: Embeddium + ModernFix + FerriteCore + Entity Culling; Canary (stale) for logic. https://www.switchbladegaming.com/minecraft/performance-mods/
- **Nvidium**: NVIDIA-only, Fabric, up to 26.2 (0.4.4-beta3); **disables itself while shaders are on** → irrelevant for a shader map. https://mcmodwiki.com/nvidium/26.2 , https://www.androidhire.com/best-minecraft-shaders-high-fps
- **C2ME**: chunk gen/IO concurrency; for a pre-built map the gain is mainly loading/IO; low priority. https://github.com/RelativityMC/C2ME-fabric/
- [S] 26.1 raised default launcher RAM 2→4 GB and moved to ZGC; third-party launchers may not apply. https://www.androidhire.com/best-minecraft-shaders-high-fps

### 4.2 LOD (vistas)
- [V] **Distant Horizons 3.3.x** (3.3.0 ~Sep 2026): MC 26.3 support, AA/TAA for LODs, fixed Iris shadow maps & depth texture issues, reverse-Z, shader devs can access DH textures; Fabric+NeoForge (+Forge for old versions). Blaze3D render path that runs on GL and Vulkan in dev since May 2026. https://gitlab.com/distant-horizons-team/distant-horizons/-/releases , https://gitlab.com/distant-horizons-team/distant-horizons/-/commit/a14a558f0d7be28450266ca4ba386e8fcbf05818
- [S] DH shader compatibility DB (to Dec 2025): Compatible — Complementary, Photon, Bliss, Solas, Rethinking Voxels, Nostalgia, Shrimple, Iterationᵀ, AstraLex; Partial — SEUS, Kappa; Incompatible — Sildur's Vibrant. https://distanthorizonsguide.com/shaders
- [C] DH + Oculus (Forge 1.20.1): "may work but unexpected results; prefer Iris on Fabric/NeoForge" (DH Discord bot); many crash threads. https://www.answeroverflow.com/m/1309626086799446087
- [S/V] **Voxy**: Fabric-only, needs Sodium + OpenGL 4.6, newest 0.2.19-beta (29 Aug 2026) up to 26.2; 26.3/Vulkan support open (#679/#684). Packs must explicitly support Voxy (Complementary r5.8+, Mellow, Photon per users). **LODs break with shader render scale <100%** (#350). https://minecrafthub.io/mods/voxy , https://github.com/MCRcortex/voxy/issues/684 , https://github.com/MCRcortex/voxy/issues/350
- [C] DH/Voxy with shaders cost: "+DH ~100→70 fps class drops", stutter on transitions reported even on RTX 4080. Good for scripted vista points, keep LOD distance modest. https://www.answeroverflow.com/m/1354510773371797677

### 4.3 Animated entities / boss fights
- **Epic Fight** (1.20.1 Forge / 1.21.1 NeoForge):
  - [V] 2024 "animation shader" GPU skinning: 50 ender dragons 50-60 → 80-100 fps; it had to rewrite shader-pack programs; if the pack failed to parse it fell back to vanilla pipeline with a chat warning. https://www.patreon.com/yessman/posts/epic-fight-based-109048971
  - [V] Later replaced by a **"compute shader"** path (needs newer OpenGL/GPU); users ask to re-add animation shader (#2080). Nightfall modpack tweak mod notes compute shader "may help performance, can sometimes cause rendering problems". https://github.com/Epic-Fight/epicfight/issues/2080 , https://www.modpackindex.com/mod/168637/ts-epic-fight-nightfall-tweaks
  - [V] **Epic Fight FPS Optimizer** (unofficial, client, Sep 2026; 1.20.1 Forge & 1.21.1 NeoForge): full animation within 12 blocks, distant pose calc capped at 20 fps, vanilla model beyond 32 blocks, trail/afterimage distance caps, **boss whitelist protection**. https://www.curseforge.com/minecraft/mc-mods/epic-fight-fps-optimizer
  - [V] Epic Fight issue #1921: entities using `epicfight:custom` render type have texture bugs under Complementary and Bliss (1.20.1, open). Bliss #551: Berserker red skin with Epic Fight (closed). "Epic Fight Mod Fixes" addon claims an animation-shader fix tested with Bliss only. https://github.com/Epic-Fight/epicfight/issues/1921 , https://github.com/X0nk/Bliss-Shader/issues/551 , https://mcmodshub.com/mod/479282
- **GeckoLib**: cost scales with bones; fewer bones, merge decorative parts; "GeckoLib Animation Optimizer" / "Geckolib Betterfps" client mods exist [S]. Old Iris+entity-shadow frozen-animation bug (2023) fixed. https://github.com/bernie-g/geckolib/issues/512
- **Animated Java** (supports 1.20.4 → 26.3): every bone is a display entity updated per frame; use few bones (groups without cubes are free; E: counter), Excluded Nodes, turn off Auto Update Rig Orientation on static rigs, keep Animation System = Functions, don't animate unseen rigs. https://animated-java.dev/docs/resources/faq
- Display entities: large `shadow_radius` caused perf issues (MC-259879, fixed 23w12a). https://bugs.mojang.com/browse/MC/issues/MC-259879
- [V] Iris #3149 (open feature request): first-time shader/entity encounter causes 0.5-1 s spikes (160 → 27-50 fps). Practical mitigation (reasoning): pre-spawn boss model/particles/water briefly out of sight before the arena. https://github.com/IrisShaders/Iris/issues/3149
- Iris translucent entities cost (#2599) and Bliss "separate entity draws" removal → keep boss models mostly opaque; use emissive instead of translucency where possible.

---

## 5. Compatibility gotchas (Iris/Oculus × mods)
1. [V] Iris/Oculus = OpenGL only → on 26.x keep Graphics API = Prefer OpenGL. 
2. [V] Custom core shaders from RP ignored with shader pack on (HUD/text/armor shader tricks break). Vanilla `/posteffect` interplay with Iris not documented → test.
3. [V] **Environment attributes** (data-driven fog distance/colour, block-light colour) are NOT respected under Iris + Complementary (#3065, 26.1); sky colour is. Datapack-driven fog is lost when a shader pack is active. https://github.com/IrisShaders/Iris/issues/3065
4. [V] Custom dimension types with nether/end effects used wrong pack programs — fixed (PR #2853, Sep 2025). Keep custom dimensions on standard effects or test. https://github.com/IrisShaders/Iris/pull/2853
5. [V] Bliss/Eclipse on NeoForge: invisible player/entity models from Iris separateEntityDraws → disable TRANSLUCENT_ENTITIES in pack debug settings; X0nk says not reproduced on 1.21.1 (seen on 1.21.6/1.21.8). https://github.com/X0nk/Bliss-Shader/issues/514
6. [V] Veil-based mods (e.g., Create Aeronautics) need "Iris Veil Compat". https://github.com/leon-o/iris-veil-compat
7. [V] Epic Fight custom render types + Complementary/Bliss texture bugs (#1921); Epic Fight compute shader may cause artifacts → test toggle per pack.
8. [V] block_display emission dimmer under shaders (#3053).
9. [V] Voxy requires pack support; breaks at render scale <100%.
10. [V] Nvidium off with shaders; Sodium 0.8.12 (1.21.1) breaks "Sodium Options API" dependents.
11. [V] Iris on macOS: Apple Silicon unsupported, Intel Macs deprecated. https://rockstarshaders.com/iris-shaders-mac

---

## 6. Practical "≥50 fps" guidance for a curated map

### 6.1 Upscaling options
- Iris has no built-in render-scale/DLSS (feature request #757 open since 2021). https://github.com/IrisShaders/Iris/issues/757
- Photon: optional temporal upscaling mode. Vitrail (Vulkan): Render Scale slider. Radiance/Caustica: DLSS/FSR (+FG).
- **FSR Reloaded** (Fabric; 1.21.11, 26.1.2, 26.2): FSR 1/2/3/3-FG/4(Win); "most shaders work, experimental, expect bugs"; OpenGL 4.3. https://modrinth.com/project/gFl0kYvv
- **MC FSR** (1.20.1 Forge, Iris/Oculus support claimed, 3 days old, 37 downloads) [?]. https://www.curseforge.com/minecraft/mc-mods/mc-fsr
- PFG (frame-gen mod, 1.20.1/1.21.1/26.1.2) [?]; Lossless Scaling (external, windowed) [C] — adds latency; bad for parry timing in soulslike combat.
- Reasoning: frame generation increases input latency → do not count FG frames toward the 50-fps target for combat.

### 6.2 Settings levers (most → least impact)
1. Shader profile (one step down first). 2. Shadow map resolution & shadow distance (shadow pass re-renders the world; Iris shadow distance 64-128 blocks). 3. Volumetric light/fog quality (keep fog — it's the mood — but lower steps). 4. Reflections (SSR) & GTAO. 5. Colored/voxel lighting (Ultra-only in Photon). 6. DOF/motion blur off. 7. Render distance (8-10 chunks in dungeons, 12 outdoors; vistas via DH/Voxy). 8. Entity & block-entity shadows off in crowded areas. 9. POM off on low tiers. https://www.androidhire.com/best-minecraft-shaders-high-fps , https://deepwiki.com/sixthsurge/photon/2-configuration-system
- Map-design levers (reasoning): enclosed arenas + fog walls cap draw distance; limit simultaneous emissive/colored light sources per chunk for voxel/Photonics packs (Photonics default 20 lights/chunk); avoid translucent boss geometry; pre-warm shaders; keep particle counts bounded during boss phases; prefer GeckoLib/Epic Fight mobs over 50-bone Animated Java rigs for bosses.
- Licensing (reasoning + Vitrail note): shader packs generally can't be redistributed inside the map download → ship a settings preset `.txt` + instructions.

### 6.3 GPU tier table (estimates synthesized from data points above; verify on target PC)
| Tier | Resolution | Pack & profile | RD / LOD | PBR | Expected |
|---|---|---|---|---|---|
| GTX 1060 6GB / RX 580 / GTX 1650S | 1080p | Complementary Reimagined Low–Medium (or BSL Low, MakeUp UF fallback); shadows 1024, VL low | 8 chunks, no LOD | 16-32x normals+spec, POM off | ~50-70 |
| GTX 1660S / RX 6600 / RTX 2060 | 1080p | Complementary Unbound Medium + Euphoria, Photon Medium, Bliss default-ish | 10 chunks; LOD off or small | 32x, POM off/low | ~60-90 |
| RTX 3060 / 4060 / RX 6700 XT | 1080p High / 1440p Medium | Complementary/Euphoria High, Photon High, Bliss/Eclipse | 12 chunks; DH 64-128 only at vistas | 32x LabPBR, POM low | ~60-100 (1080p) |
| RTX 4070 / 4070S / RX 7800 XT | 1440p High-Ultra | Photon Ultra (colored light), Complementary Ultra+Euphoria, Bliss; Photonics optional | 12-16; DH/Voxy vistas | 32-64x, POM medium | ~70-120 |
| RTX 4090 / 5080+ / RX 7900 XTX | 1440p–4K Ultra | any; Rethinking Voxels at 1440p, Euphoria+Photonics; experimental HW RT (Radiance on 1.21.1) | 16+; LOD 256 | 64-128x POM | 4K Complementary Ultra ~150+, RV ~45-60 at 4K |
Basis: 5090 4K data (zWORMz), 3060 laptop data (#3241), Reddit reports; scale factors are reasoning, flagged as estimates.

### 6.4 Version recommendation (rendering perspective)
- If Epic Fight (or other 1.21.1 content) is required → **1.21.1 NeoForge + Sodium 0.8.12/13 + Iris 1.8.13+** is the best-maintained shader stack on an Epic-Fight-capable version (modern Sodium backport July 2026; DH works; all major packs list 1.21.x).
- 1.20.1 Forge (Embeddium/Oculus) works but both are frozen; more bugs, no Photonics/Voxy; DH+Oculus fragile.
- 26.3 has the newest shaders/LOD support but Vulkan transition risk (Iris OpenGL-only; 26.4 default Vulkan; shadow-pass regression report on 26.2+).
