# Dark anime sci-fi ruins in Minecraft: Chinese, Japanese, and Korean research

Research date: 2026-10-13. Target: Java 1.21.1 + NeoForge; first milestone is the sewer and outer-wall slums. This report adds atmosphere and map-design evidence to the existing project research rather than repeating the stack survey.

Evidence labels: **[V]** verified creator/maintainer/official primary source; **[C]** community interpretation, walkthrough, translation, or archive whose original could not be authenticated; **[?]** inference, proposed settings, or unresolved compatibility. Verification here means reading the source, **not running Minecraft or benchmarking**. Every proposed number below is explicitly [?]. Source-code snapshots are current branch files retrieved on the research date, not promises about every released ZIP.

Read first: `research/r2/CONTEXT.md` and the four existing documents named there, including their relevant art, scope, performance, and originality requirements. Research artifacts are under `research/r2/codex_raw/`. No key file was opened. No map internals were downloaded or reverse-engineered.

## 1. Most useful regional discoveries

### 1.1 Chinese ruin builders: distinguish the actual build from the promotional render

- **[V] Kaiwen Liu 刘铠闻 / cogco, *Dawn Elegy 黎明挽歌*.** The creator describes overgrown high-rises, an abandoned factory, a stranded cargo ship, collapsed bridges, and towers. The original release explicitly credits **ITT3, SEUS HRR3, XEHD textures, and C4D rendering**, with a Minecraft 1.18+ world. This is strong evidence for a ruin-building reference, but its screenshots do not establish achievable gameplay on our RTX 4060. Sources: [Chinese/English creator portfolio](https://kaiwenliu.work/projects/dawn-elegy), [original map publication and credits](https://www.planetminecraft.com/project/wasteland-dawn-elegy/).
- **[?] Visual observation from an inspected creator image:** repetition of vertical window bays establishes an intact architectural order; missing windows, interrupted rooflines, and concentrated vegetation break it locally. Large damage shapes remain readable before fine detail. For our setting, replace most living vegetation with stains, cables, collapsed panels, or dead growth rather than importing the reference's ecological recovery. Image: [overgrown high-rises](https://kaiwenliu.work/images/mc-dawn-2.jpg).
- **[V] The same creator's *Automata's Heart 人偶之心*** layers airship docks, cranes, and industrial waterfronts into a steam mountain-city described as Hong Kong mixed with London. It specifies **3000 × 3000 blocks**, about **20% completion**, and a hold due to technical issues. Useful evidence for stacked industrial city composition and the cost of enormous scope—not evidence that our playable milestone needs that size. [Creator's bilingual account](https://kaiwenliu.work/projects/automata-heart), [original development announcement](https://www.planetminecraft.com/project/new-project-automata-s-heart-20-progress/).
- **[C] SSSP26, *紊乱（绿地废墟）*.** An MCBBS archive preserves the creator recommending volumetric light and strong light/dark contrast, specifically **Bliss or SEUS Renewed**. The description says the initial world arose from a failed Bedrock-to-Java conversion, leaving fragments of structures. This is an unusual Chinese ruin-design reference, but no numeric preset survived in the inspected text. [Readable archive](https://t.me/s/mcbbsss/415095), [original thread URL](https://www.mcbbs.net/thread-1471291-1-1.html). The direct archive mirror tried during this run returned 404; treat attribution conservatively.

### 1.2 Chinese townscape tools are unusually relevant to anime slums

- **[V] Yuushya 方块小镇's Chinese official site** supplies demo worlds *微缩社区* and *六分街*. The latter is a detailed street scene based on *Zenless Zone Zero*, credited to 世隐. The site says it uses **Townscape plus 方块建模**, including moved/rotated block models; the demo depends on both mods. Its lightweight pack includes Complementary shaders. Special resource-pack effects may require **OptiFine or Continuity**. [Chinese download/demo descriptions](https://yuushya.com/townscape/download.html).
- **[V] A concrete target-version file exists:** `yuushya-1.21.0-neoforge-2.2.3.jar` is listed for **1.21.1 NeoForge**. The filename's 1.21.0 alone is not a reason to reject it; use the publication's compatibility metadata. [Creator's version-filtered files](https://www.curseforge.com/minecraft/mc-mods/yuushya-townscape/files/all?page=1&version=1.21.1).
- **[?] Transfer:** use the official demo to study how storefronts, signage, pipes, counters, and narrow frontage create inhabited streets. Make original worn versions in our resource pack/mod. A shader cannot supply this density of everyday objects. Test CTM and moved-block collision on the actual NeoForge client before adopting the demo's visual workflow. The demo documents construction possibilities; it does not prove Epic Fight camera, collision, or performance compatibility. Sources: the [official demo page](https://yuushya.com/townscape/download.html) and [target file listing](https://www.curseforge.com/minecraft/mc-mods/yuushya-townscape/files/all?page=1&version=1.21.1).

### 1.3 Japanese ruin building: small modules and presentation boundaries

- **[V] SOU's Minecraft-log, “廃墟の作り方,” 16×16 No.12** explicitly works at **one chunk**, using **Complementary Unbound r5.6** and **Continuity**, with vanilla materials as of 1.21.10. This is a concrete manageable module size and a disclosed visual stack; material availability must be checked back against 1.21.1. [Creator's video description](https://www.youtube.com/watch?v=Grur6B8ummc).
- **[C] The Japanese *水没廃墟都市* reference** is documented as a Tokyo-like flooded city with submerged roads, vegetation, tilted towers, and a Tokyo Tower-like landmark. The creator's mirrored video description says CustomSteve/MMD was used for its PV and interiors were mostly absent. It therefore illustrates skyline/presentation work rather than a complete adventure level. [Japanese description](https://minecraft.ologies.net/2015/02/), [mirrored creator description](https://www.nicozon.net/search/%E5%BB%83%E5%A2%9F%E9%83%BD%E5%B8%82/v/d), [original Nicovideo video](https://www.nicovideo.jp/watch/sm25620005).
- **[?] Transfer:** author one 16×16 damaged-facade module, one playable room behind it, and one skyline shell. Keep separate complexity budgets for spaces the player enters and distant silhouettes. This combines SOU's small module scale with the flooded-city reference's explicit distinction between presentation and interiors. Sources above.

### 1.4 Korean builders' observations: mist, bloom, and time of day are different decisions

- **[C] DC Inside's Steve gallery shader comparison** describes Bliss as having heavy mist that can make distant views oppressive, and prefers Complementary Unbound for clarity. It specifically recommends **11500 ticks** for Unbound's orange sunset when building. This is a person's scene preference, not a universal fog measurement or performance test. [Korean builder comparison, 2026-06-08](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=380424).
- **[C] Velo's Korean Complementary tutorial** separates **Bloom Strength**, **Cave Lighting**, **Border Fog**, **Cave Fog**, and **Atmospheric Fog**; its cave-lighting examples use deliberately extreme settings to expose the difference. Its UI is from 2023 and should not be used as a current numeric-key reference. [Korean illustrated settings walkthrough](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=240222).
- **[?] Transfer:** judge fog at the intended combat distance, bloom at the light source, and cave lighting on the enemy silhouette. Do not increase bloom to simulate depth fog. For repeatable slum screenshots, test `/time set 11500`; choose a separate fixed gameplay time after checking enemy visibility. Community sources above; current control definitions are verified below.

## 2. Concrete shader controls, with source-checked trial presets

### 2.1 Complementary: best first prototype because regional examples disclose it

**[V] Current primary definitions** expose `ATM_FOG_MULT`, `ATM_FOG_DISTANCE`, `ATM_FOG_ALTITUDE`, `CAVE_LIGHTING`, `LIGHTSHAFT_BEHAVIOUR`, `BLOOM_STRENGTH`, `TM_CONTRAST`, and `T_SATURATION`. Fog settings are under Atmosphere/Fog; cave lighting is under Lighting; tone controls are in the image/tonemap settings. `LIGHTSHAFT_BEHAVIOUR=1` means **Scene Aware**, `2` Regular, and `3` Extreme. The author's tooltip discourages Extreme for general play and flags its performance cost. Cave lighting also depends on the video Brightness slider; atmospheric fog distance also depends on render distance. Sources: [option definitions](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lib/common.glsl), [UI layout](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/shaders.properties), [maintainer's labels/tooltips](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lang/en_US.lang).

**[?] Trial presets:** these numbers are selected from verified allowed values, **not presets published by a Chinese/Japanese/Korean creator**. Check the installed Unbound/Euphoria build because source branch menus can differ from releases. Begin from the chosen shader's Medium profile; export settings after visual calibration.

| Setting | Sewer trial | Slum trial | White-gold church trial | Evidence |
| --- | --- | --- | --- | --- |
| `ATM_FOG_MULT` | [?] 0.95 | [?] 0.80 | [?] 0.65 | [Primary options](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lib/common.glsl) |
| `ATM_FOG_DISTANCE` | [?] 60 | [?] 80 | [?] 100 | Same source; this is the shader slider, **not a guaranteed block distance** |
| `ATM_FOG_ALTITUDE` | [?] match the district's dominant height; initial 40 if built there | [?] initial 70 if built there | [?] match nave height | Same source; world elevation must be chosen first |
| `CAVE_FOG` | [?] on | [?] on for buried routes | [?] on only if useful underground | [Primary tooltip](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lang/en_US.lang) |
| `CAVE_LIGHTING` | [?] 70 | [?] 80 | [?] 100 | [Primary options](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lib/common.glsl) |
| `LIGHTSHAFT_BEHAVIOUR` | [?] 1 | [?] 1 | [?] 1 | [Mode labels](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lang/en_US.lang) |
| `BLOOM_STRENGTH` | [?] 0.09 | [?] 0.09 | [?] 0.12 | [Primary options](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lib/common.glsl) |
| `T_SATURATION` | [?] 0.80 | [?] 0.85 | [?] 0.90 | Same source |
| `TM_CONTRAST` | [?] 1.05 | [?] 1.10 | [?] 1.05 | Same source |

**[V] Colored Light Fog is separate from ordinary atmospheric/cave fog.** Its tooltip requires Advanced Color Tracing and supporting hardware, and warns of substantial cost. Border Fog is discouraged below **8 render chunks**. [Maintainer tooltips](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lang/en_US.lang).

**[?] First performance pass:** 1080p, 8–10 render chunks, Medium profile; retain atmospheric depth while testing **Colored Light Fog off**, motion blur off, and depth of field off. Hold video Brightness constant during comparisons. If an emitter blooms so strongly that its shape disappears, lower bloom/emission before darkening the entire map. These are trial decisions, not an FPS guarantee. Sources: [maintainer control definitions](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lib/common.glsl) and the [Korean builder's visibility observations](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=380424).

**[C] Useful Chinese UI vocabulary:** Surisen's maintained Complementary translation maps Border Fog to the fog at loaded-world edges and separately explains Colored Light Fog's dependency/cost. The article is labeled r5.8 and dated September 2026; it intermittently returned a captcha during this run. Use it for Chinese terminology, with primary files above as the technical authority. [Bilibili translation](https://www.bilibili.com/opus/839255129542623241), [alternate article URL](https://www.bilibili.com/read/cv26414719).

### 2.2 Photon shader: a good alternative for controlled teal grading

**[V] The shader's own files** expose global fog intensity, separate Mie densities for time of day, teal/orange saturation boosts, cave brightness, bloom, and exposure modes. The Medium profile uses **2048 shadow resolution**, disables entity/block-entity shadows, and retains `VL`. These are published settings, not hardware measurements. [Profiles/UI](https://github.com/sixthsurge/photon/blob/main/shaders/shaders.properties), [values](https://github.com/sixthsurge/photon/blob/main/shaders/settings.glsl), [labels](https://github.com/sixthsurge/photon/blob/main/shaders/lang/en_US.lang).

**[?] Compact shader trial**, using current source-allowed values:

```properties
# Proposed, not benchmarked. Apply through the installed shader UI/export.
shadowMapResolution=2048
shadowDistance=96.0
GRADE_CONTRAST=1.05
GRADE_SATURATION=0.85
GRADE_TEAL_SAT_BOOST=0.15
GRADE_ORANGE_SAT_BOOST=0.05
CAVE_LIGHTING_I=0.70
OVERWORLD_FOG_INTENSITY=1.20
BLOOM_INTENSITY=0.60
AUTO_EXPOSURE=0
```

**[?] Rationale:** a small selective teal boost preserves the district cue after moderate global desaturation. Fixed exposure makes a bright shrine or doorway less likely to change the readability of nearby combat. Leave Mie time-of-day densities at defaults on the first pass; global intensity is easier to compare. Keep POM, motion blur, and DOF off initially. Source for the available controls/enum: [Photon settings](https://github.com/sixthsurge/photon/blob/main/shaders/settings.glsl). This does not imply the published defaults are unsuitable.

### 2.3 Bliss: strongest explicit cave-fog color controls in the inspected source

**[V] Bliss exposes** `VL_SAMPLES`, `FOG_START_HEIGHT`, `TOD_Fog_mult`, separate morning/noon/evening fog densities, `CAVE_FOG`, `CaveFogFallOff`, and RGB cave-fog controls. Current defaults include **8 fog samples**, **start height 60**, **falloff 1.0**, and cave fog RGB **0.1 / 0.2 / 0.5**. “Falloff” changes how quickly the gradient reaches its brightest part. [Maintainer settings](https://github.com/X0nk/Bliss-Shader/blob/main/shaders/lib/settings.glsl), [menu layout](https://github.com/X0nk/Bliss-Shader/blob/main/shaders/shaders.properties), [tooltip](https://github.com/X0nk/Bliss-Shader/blob/main/shaders/lang/en_us.lang).

**[?] Sewer experiment:** `VL_SAMPLES=8`, `CAVE_FOG` on, `CaveFogFallOff=0.8`, `CaveFogColor_R=0.10`, `_G=0.18`, `_B=0.20`. This moves the bright part of the cave gradient toward muted teal; it is not a linear sRGB paint swatch. For the slums, begin with `TOD_Fog_mult=0.75` if the default mist obscures the route. Check fixed world time and elevation before touching per-day weather controls. [Allowed values](https://github.com/X0nk/Bliss-Shader/blob/main/shaders/lib/settings.glsl).

**[?] Decide on one shader for the shipped milestone.** Shader settings are generally client-wide; the presets above are A/B comparison recipes, not a verified mechanism for silently switching shader settings between districts. A shared preset plus geometry, materials, physical lights, and local particles should create the district transitions. Automatic regional shader control remains a separate engineering question. Sources: the client shader [menu definitions](https://github.com/X0nk/Bliss-Shader/blob/main/shaders/shaders.properties), [Complementary UI](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/shaders.properties).

## 3. Resource-pack and material choices

| Candidate/workflow | What the source actually establishes | Use for this project |
| --- | --- | --- |
| Yuushya + Townscape | [V] Chinese official demos, small-town details, moved/rotated blocks; target NeoForge file exists | [?] Study prop vocabulary for slums. Test its CTM and model behavior before dependency adoption. [Official demo](https://yuushya.com/townscape/download.html), [files](https://www.curseforge.com/minecraft/mc-mods/yuushya-townscape/files/all?page=1&version=1.21.1) |
| XEHD / ITT3 / SEUS HRR3 in Dawn Elegy | [V] Explicit screenshot/render credits | [?] Visual reference only; no verified 1.21.1 runtime preset, redistribution permission, or performance result collected. [Creator credits](https://www.planetminecraft.com/project/wasteland-dawn-elegy/) |
| Original 16px environment pack | [?] Project-specific proposal | [?] Grey structural modules, teal fixtures, restrained gold landmarks; use the creator references for composition rather than copying their assets. [Dawn reference](https://kaiwenliu.work/projects/dawn-elegy), [Yuushya example](https://yuushya.com/townscape/download.html) |
| Bedrock RTX material tutorials | [V] NVIDIA's Chinese guide explicitly concerns Bedrock RTX | [?] Material-thinking reference; its file/channel conventions are not a Java LabPBR implementation guide. [Chinese official guide](https://www.nvidia.cn/geforce/guides/gfecnt/minecraft-rtx-texturing-guide/) |

**[?] Original material brief:** use three readable grey families—dry concrete, wet concrete, painted metal—before adding more colors. Keep cracks, streaks, and seams clustered around plausible damage. Give gold a consistent role: sacred machinery and distant objectives. Use teal for utility infrastructure and checkpoint-adjacent cues, with different silhouettes for each function. Neither color should be the sole identifier. This is a proposal informed by the [inspected Dawn image](https://kaiwenliu.work/images/mc-dawn-2.jpg) and [Chinese detailed-street workflow](https://yuushya.com/townscape/download.html).

**[?] Church materials:** off-white structural panels, pale grey recesses, thin gold framing, and teal maintenance light behind service grilles. A dark substructure and deep recesses preserve contrast around white surfaces. Repeated ribs, concentric apertures, and a suspended machine altar convey sci-fi ritual more specifically than covering an ordinary cathedral in gold blocks. No inspected regional source documented this exact white-gold sci-fi recipe; it is an original art-direction proposal, grounded only in the project's brief and the general [layered machinery reference](https://kaiwenliu.work/projects/automata-heart).

## 4. Custom particles and local atmosphere

### 4.1 Chinese Photon VFX is a different project from Photon shaders

**[V] KilaBash's original Bilibili introduction** describes a Unity-inspired Minecraft particle/trail editor, with effects usable through commands. This establishes Chinese creator provenance. [Original 2023 introduction](https://www.bilibili.com/video/BV12c41137G2/).

**[V] Current Photon2 documentation** lists Minecraft **1.21.1**, NeoForge **21.1+**, particle emitters, trails, beams, timelines, and exportable FX packs. The repository's current getting-started section uses **LDLib2**. Do not install the old LDLib version mentioned in the 2023 video merely because it was correct then. [Current toolkit requirements](https://low-drag-mc.github.io/LowDragMC-Doc/en/photon2/), [maintainer README](https://github.com/Low-Drag-MC/Photon/blob/1.21/README.md).

**[V] Current Chinese command documentation** says the editor opens only in singleplayer. It supports block/entity binding, `allowMulti=false` by default, forced removal, and block-state checks. [Chinese command reference](https://low-drag-mc.github.io/LowDragMC-Doc/zh/photon2/commands.html).

```mcfunction
# [V] Existing documented demonstration effect, not one of our original assets:
/photon_editor
/photon fx photon:fire block ~ ~-1 ~
/photon fx remove block ~ ~-1 ~ true
```

**[?] Use a lifecycle owner for ambient FX:** spawn once when the player enters a district, permit one equivalent FX per anchor, stop on district exit, and forcibly clear encounter FX on death/reset. The toolkit itself recommends Java integration when the mod owns lifecycle. Test Photon2's post-processing with Iris before enabling any additional bloom/color pass. [Lifecycle/commands](https://low-drag-mc.github.io/LowDragMC-Doc/en/photon2/commands.html).

### 4.2 Japanese particle vocabulary worth translating into original effects

**[V] “自作パーティクル&アニメーション配布 v1.23”** is a Japanese **Bedrock** resource/addon project made with **Snowstorm**. It distinguishes ground smoke, inward-moving illusionist smoke, abyss aura, digital flash, gold slashes, and shockwaves. The author permits use in distributed worlds and creating new particles from its code while forbidding separate redistribution. It supplies useful naming/shape distinctions; these are not Java resources to drop into NeoForge. [Creator's pack, examples, and terms](https://minecraft-mcworld.com/158592/).

**[V] Java 1.21.1 has a different pipeline:** custom particle types/providers and particle texture definitions are documented by NeoForge. [Version-specific particle documentation](https://docs.neoforged.net/docs/1.21.1/resources/client/particles/).

**[?] Original emitter budget for the first playtest**—all values are trial limits, not creator measurements:

| Effect | Concrete starting recipe | Placement/purpose |
| --- | --- | --- |
| Sewer drip | [?] 1–2 particles/sec; 0.5–1.5 sec life; downward velocity; collision only where needed | Cracked pipe joints; occasional drip sound |
| Sewer vent mist | [?] 2–4/sec; 2–3 sec life; 0.3–0.8 block size; soft alpha; no collision | Local low vents, away from melee sightlines |
| Slum dust | [?] 1–2/sec per visible pocket; 3–5 sec life; slow drift | Shafts of sky light and broken windows |
| Checkpoint mote | [?] 4–6/sec; 1–2 sec life; slow rise; compact 1–2 block radius | A shape distinct from enemy attacks |
| Church gold mote | [?] 1–2/sec near altar; 3–4 sec life; restrained emission | Adds suspended-machine ritual without filling the room |
| Attack telegraph | [?] brief burst/defined ring; short fade; highest visibility priority | Reduce ambient emitters during intense boss patterns |

**[?] Budget interpretation:** steady live count is approximately emission rate × lifetime before bursts/sub-emitters. Start below **200 live ambient particles visible at once** and measure; transparent coverage can still dominate cost even at low count. Use world-space mist pockets instead of attaching a dense haze to the camera. The effect shapes are inspired by the [Japanese particle taxonomy](https://minecraft-mcworld.com/158592/) and implemented through [Photon's emitter workflow](https://low-drag-mc.github.io/LowDragMC-Doc/en/photon2/).

## 5. Music, sound, and encounter cleanup

### 5.1 Regional map makers expose useful implementation decisions

- **[V] Keeema's Japanese map-making article** documents replacing music-disc OGGs and invoking them with `/playsound`; it recommends the **`record` category** so players adjust custom music via the Jukebox/Note Blocks slider while setting vanilla BGM to zero. The article is explicitly based on **Java 1.21.3**, so confirm examples on our 1.21.1 instance. [Author's practical tips](https://qiita.com/Keeema-1/items/d9002459b0a9066ad0e2).
- **[V] 青空ソラマメ's Fillusioner boss map**, Java **1.21.5**, specifies **Master 100%, vanilla BGM off, Weather off, Hostile 50%, Player 100%, Voice 50%**. Its battle BGM uses the **Player** category. It credits MusMus and provides a full encounter reset function. This proves creators make deliberate mix/category choices; it is not the only appropriate category assignment. [Creator's boss demonstration and settings](https://minecraft-mcworld.com/151471/).
- **[V] *Angel of Abyss*'s creator** says BGM is commissioned or free material, and acknowledges that BGM can fail to change between areas, requiring relogging. [Creator's map/support page](https://minecraft-mcworld.com/32951/).
- **[C] A Chinese walkthrough** describes an explicit music reload button in *Angel of Abyss*'s preparation hub. [Chinese player walkthrough](https://klpbbs.com/thread-98290-1-1.html).

### 5.2 Version-correct custom audio foundation

**[V] NeoForge 1.21.1 documents OGG files and namespace `sounds.json`.** Mono audio can attenuate spatially; stereo does not behave as a point source and suits background music. `stream=true` is recommended for files longer than a few seconds. Multiple sound entries can be randomly selected. [Official version-specific sound documentation](https://docs.neoforged.net/docs/1.21.1/resources/client/sounds/).

**[?] Minimal original pack example**, based on that documented schema; not executed:

```json
{
  "ambience.sewer": {
    "sounds": [{"name": "ruinmap:ambience/sewer", "stream": true}]
  },
  "music.boss_01": {
    "sounds": [{"name": "ruinmap:music/boss_01", "stream": true}]
  },
  "pipe.drip": {
    "subtitle": "subtitles.ruinmap.pipe_drip",
    "sounds": ["ruinmap:pipe/drip_01", "ruinmap:pipe/drip_02"]
  }
}
```

**[?] Layout:** `assets/ruinmap/sounds.json`; stereo beds/music in `assets/ruinmap/sounds/ambience/` and `/music/`; mono drips/vent noises in `/pipe/`. Begin custom BGM in `record`, environmental emitters in `ambient`, and attack cues in `hostile` or the mod's chosen combat channel. The category is supplied by playback, not this JSON. Keep local machinery outside the music bed so position remains meaningful. Source: [NeoForge sounds](https://docs.neoforged.net/docs/1.21.1/resources/client/sounds/), [Japanese category example](https://qiita.com/Keeema-1/items/d9002459b0a9066ad0e2).

```mcfunction
# [?] Command-only prototype; each custom event requires the corresponding asset.
execute as @a[tag=in_sewer] at @s run playsound ruinmap:ambience.sewer ambient @s ~ ~ ~ 0.35 1
execute as @a[tag=in_boss_01] at @s run playsound ruinmap:music.boss_01 record @s ~ ~ ~ 0.60 1
stopsound @a[tag=in_boss_01] record ruinmap:music.boss_01
```

**[?] Run starts on state transition, never every tick.** The commands above neither loop nor crossfade by themselves. In the custom mod, keep per-player district/encounter audio state, crossfade beds over **2–4 sec**, duck music **3–6 dB** during critical attacks/dialogue, and cancel scheduled sounds on death, save reload, teleport, and boss victory. These are original mix targets, with the need for cleanup motivated by [Angel's documented BGM problem](https://minecraft-mcworld.com/32951/) and [regional player reports](https://klpbbs.com/thread-98290-1-1.html).

### 5.3 Sound palettes for the actual milestone

| Space/state | [?] Proposed original sound design | Mix function |
| --- | --- | --- |
| Sewer traversal | Low ventilation drone, intermittent drips, distant metal movement, occasional electrical pulse; sparse pitched motif | Leave gaps for enemy footsteps |
| Sewer checkpoint | Two or three clear glass/bell notes over a softened drone | Audible place of relief |
| Slum traversal | Wind through broken sheets, cable rattles, distant mechanical work; brief muted melodic fragments | Implies inhabitants beyond visible NPCs |
| Safe camp | A related motif with less dissonance and no combat percussion | Recognizable hub identity |
| White-gold church | Synthetic choir-like vowels, high resonant metal, servo undertone; longer tails in the music production | Beautiful but artificial institution |
| Boss entrance / phase change | Brief silence or bed reduction, unique entrance cue, then layered percussion/synth pulse | Marks commitment and phase change |

**[?] These are new composition briefs, not a request to reuse AI LIMIT, NieR, anime, or another map's soundtrack.** Regional evidence supports custom/commissioned music and deliberate channel control; it does not establish a canonical anime-ruin orchestration. Sources: [Angel creator's commissioned/free BGM statement](https://minecraft-mcworld.com/32951/), [Fillusioner creator's mix](https://minecraft-mcworld.com/151471/).

### 5.4 Optional acoustic mods: avoid layering everything at once

- **[C] MC百科 documents** footsteps, material/armor variation, splashes, and additional ambient layers in Dynamic Surroundings, including old-version processing/compatibility details. Those old sections must not be assumed to describe every new port. [Chinese overview](https://www.mcmod.cn/class/1083.html), [dated translated sound-overlay explanation](https://www.mcmod.cn/post/605.html).
- **[V] AmbientSounds has an explicit 1.21.1 NeoForge file**, for example `AmbientSounds_NEOFORGE_v6.1.10_mc1.21.1.jar`; use a pinned target-version file rather than a latest-version download. [Primary file page](https://www.curseforge.com/minecraft/mc-mods/ambientsounds/files/6525171). **[?]** Its natural biome ambience is an optional reference; authoring district beds directly avoids accidental cheerful nature sounds in machine ruins. [Chinese discovery entry](https://www.mcmod.cn/class/2947.html).
- **[V] Sound Physics Remastered's maintainer** documents attenuation, block absorption, reverberation, configurable reflectivity/occlusion, and debug rendering. [Primary repository](https://github.com/henkelmax/sound-physics-remastered). **[?]** Evaluate one acoustic processor with mono emitters before adding additional sound mods; this run did not test its 1.21.1 build or boss-cue readability.
- **[C] An easily missed NeoForge Presence Footsteps fork exists** in MC百科, including **1.21.1** and an explicit warning that it is unofficial. Do not conclude the whole feature is Fabric-only from the original project's entry. [Chinese fork entry](https://www.mcmod.cn/class/23371.html). **[?]** Exact fork binaries and shader/client compatibility remain unverified.

## 6. Soulslike adventure maps: what their creators and players actually show

### 6.1 Japanese *Angel of Abyss*, cross-checked with Chinese reports

**[V] Creator れる / れるにゃ** calls it a singleplayer Bedrock action RPG, estimates **4–6 hours**, and disallows viewing/reusing modified map internals. The public page acknowledges disappearing bosses and cutscene teleport problems under lag. Creator replies recommend Normal, with Easy for less confident players. This report studies public descriptions/comments, not the prohibited internals. [Creator release and comments](https://minecraft-mcworld.com/32951/).

**[C] Chinese walkthrough findings**—this is a player account, not a measured level-design specification:

- Preparation hub links weapon selection, upgrades, buffs, and stage selection; tutorial precedes ordinary encounters and the first boss.
- Several early sections are linear, with small groups; later routes include a window drop, an alternate longer route, and optional NPC rewards.
- One boss's marked danger zone can be escaped behind columns; another fast boss has an unobstructed arena and little breathing space.
- Low-end performance/cutscene failures and awkward camera behavior are reported.

Source: [detailed Chinese walkthrough](https://klpbbs.com/thread-98290-1-1.html). Exact arena widths, shortcut lengths, and checkpoint spacing were **not verified**.

**[C] Japanese release-page comments** report getting lost after a story segment, bypassing a barrier and skipping the first boss, attack audio continuing after an enemy was killed, and duplicate bosses/state damage after recovery. **[V]** The creator acknowledges the barrier escape and says the severe boss lag bug was being addressed. [Public comments on original release](https://minecraft-mcworld.com/32951/).

**[?] Transfer to our map:** attach gates to durable quest/boss flags, not merely a low barrier; clear all encounter-owned audio, particles, temporary entities, lock tags, and timers on reset; use a landmark plus explicit opened-route feedback after a boss. Keep a preparation area where players can change equipment without pressure. These lessons follow from the public support record above; they are not claims about the creator's internal code.

### 6.2 Chinese *欧米伽：PVE打怪* by 回声工作室

**[V] Echo Studio's original publication** identifies a Bedrock **1.20.x/1.21.x** PVE map, explicitly organized around **dodge → block → counterattack**, with credited contributors and authorized resource-pack contributors. [Original publication](https://klpbbs.com/thread-163262-1-1.html), [creator-linked trailer](https://www.bilibili.com/video/BV1Ct3EzKEDE/).

**[C] Replies report** a tutorial softlock when the enemy is killed before the third task is completed and truncated hints on desktop. Later comments describe a soulslike encounter and a way to bypass a phase using a fire weapon. [Same forum discussion](https://klpbbs.com/thread-163262-1-1.html).

**[?] Transfer:** tutorial encounters must recover when a player achieves an objective early or kills the demonstration enemy. Set hint safe margins for the actual GUI scale; build encounter completion around facts such as boss dead and objective satisfied, not one expected animation sequence. No shader preset, block-scale specification, or checkpoint interval was found in this publication.

### 6.3 Korean map lead: useful but not enough evidence for design claims

**[C] Marple's March 2026 “누가 마크로 다크소울 만듦” video description** points to a map on Naver and a full playthrough. It is evidence that a Korean map/player community lead exists. [Preserved video description](https://video.korea.com/view/?id=5xpY14dQcNA), [video](https://www.youtube.com/watch?v=5xpY14dQcNA), [full playthrough](https://www.youtube.com/live/QaxaETeuNsk), [Naver map post](https://cafe.naver.com/marplecafe/42414).

**[?] The Naver post and direct video fetch were inaccessible in this run.** Creator identity, engine/version, checkpoint logic, route topology, boss dimensions, and whether listed music credits belong to video editing or map audio remain unverified. Do not use an automated video summary as proof of the map maker's implementation.

### 6.4 English fallback where regional evidence is missing

**[V] LGSC team's *Year of Blood*** publicly describes opening shortcuts inspired by Bloodborne/Dark Souls, **1–4 players**, **6–10 hours**, and Minecraft **1.19.2**. This supplies a direct Minecraft map-maker example of unlockable shortcut design. It does not supply arena measurements or a target-version dependency. [Creator-attributed map publication](https://www.minecraftmaps.com/48937-year-of-blood).

**[?] Finding:** the inspected sources support linear combat stages, hubs, alternate routes, blocked passages, and unlockable shortcuts. They do **not** justify claiming that Chinese/Japanese/Korean soulslike makers follow a standard numeric checkpoint formula. The dimensions and retry times below are proposals to validate on our combat stack.

## 7. Concrete district and level-flow brief for the first playtest

### 7.1 Greybox before decorative damage

**[?] Proposed player-scale starting dimensions:** combat passages **4–6 blocks wide**, quiet squeeze passages **2–3**, ordinary rooms **10–16 across**, combat headroom **5–8**, first boss arena **24×24 clear floor with about 10 blocks headroom**, larger mobile boss **32×32 with 12–16 headroom**. Dimensions are for prototyping—not measurements from a regional map. Check third-person Epic Fight camera and attack displacement at walls, doorframes, steps, and pillars. Use the [Angel arena contrast described by the Chinese walkthrough](https://klpbbs.com/thread-98290-1-1.html) as a reason to test obstacle layout, not as a dimension source.

**[?] Trial checkpoint goals:** a new route should take **3–5 minutes** to explore between meaningful safe points; after opening a shortcut, boss retries should take **10–25 seconds** without mandatory repeat trash combat. Observe actual times and revise. Keep shortcut state permanent through death; regenerate encounter enemies without re-locking exploration doors. Source inspiration: [Year of Blood's explicit shortcuts](https://www.minecraftmaps.com/48937-year-of-blood), [Angel's preparation hub/flow reports](https://klpbbs.com/thread-98290-1-1.html).

**[?] Proposed route graph**—original topology, not a reconstruction of another creator's map:

```text
Sewer checkpoint A
  → dry service passage → flooded machine room → upper maintenance walk
  → unlock lift/ladder back to A
  → checkpoint B → reservoir boss
  → exterior reveal → slum camp checkpoint C
  → stacked homes → scrap market → unlock gate back to C
  → workshop boss → elevated crossing → burial/courtyard boss
```

**[?] Architecture and logic should agree:** show a shortcut before it opens, then reach its far side naturally; keep a recognizable pipe tower, lift shaft, or white-gold distant structure visible across several viewpoints. Mark essential exits with silhouettes/light rather than cluttering every junction with identical signs. Inspiration: [Chinese layered-city composition](https://kaiwenliu.work/projects/automata-heart), [regional navigation problems](https://minecraft-mcworld.com/32951/), [explicit Minecraft shortcuts](https://www.minecraftmaps.com/48937-year-of-blood).

### 7.2 Scene recipes

| District | [?] Build and lighting recipe | [?] Gameplay/sound role |
| --- | --- | --- |
| Sewer town | Grey ribs and concrete panels; exposed teal conduits; water below dry fighting routes; larger pump silhouette above smaller housing; light haze beyond combat floor | Drips and ventilation; one brighter exit per chamber; lower routes reconnect through maintenance stairs |
| Outer-wall slums | Staggered facade modules; patched sheet roofs; cables crossing above head; tall wall as persistent backdrop; warm camp/gold salvage against muted teal distance | Wind/rattle; stacked paths with visible returns; safe camp receives reduced tension |
| White-gold sci-fi church | Pale ribs and broad negative space; gold structural accents; recessed machine rails; suspended altar; a controlled light shaft and sparse motes | Synthetic choir/servo contrast; symmetric processional approach broken by one maintenance route; readable isolated arena |

**[?] Reference basis:** repeated ruin structure from [Dawn's inspected image](https://kaiwenliu.work/images/mc-dawn-2.jpg), industrial layering from [Automata's Heart](https://kaiwenliu.work/projects/automata-heart), street details from [Yuushya's Chinese demos](https://yuushya.com/townscape/download.html), and small authorable modules from [SOU's one-chunk ruin](https://www.youtube.com/watch?v=Grur6B8ummc). The exact church recipe is original synthesis and has the weakest direct regional precedent.

### 7.3 Required review views and tests

**[?] Produce six repeatable views:** sewer checkpoint, sewer machine-room fight, reservoir arena, slum street, camp, church prototype. Fix camera/FOV, time, weather, resolution, and video brightness; record shader name/version and exported options with each screenshot. Add a no-shader view of the same geometry to check whether the map itself communicates route and scale. The need to separate screenshot treatment from runtime follows directly from [Dawn's C4D/shader credits](https://www.planetminecraft.com/project/wasteland-dawn-elegy/).

**[?] Playtest criteria:** enemy silhouette and attack cue remain visible at **8–12 blocks**; local mist does not hide floor hazards; arena perimeter does not trap the camera; save/reload and death stop boss music/FX; tutorial survives out-of-order actions; shortcuts retain their state; longest district transition does not duplicate audio. Measure actual boss performance against the project's **≥50 fps** target—none of the web sources establishes that result on the specified PC. Failure cases are motivated by [Angel support comments](https://minecraft-mcworld.com/32951/) and [Omega tutorial reports](https://klpbbs.com/thread-163262-1-1.html).

## 8. Search coverage, limitations, and reproducibility

**[V] Strongest inspected primary regional material:** Chinese bilingual builder portfolios and original releases; Yuushya's Chinese official demos; KilaBash's Bilibili video and Chinese Photon docs; Echo Studio's release; Japanese creator pages, commands, mix instructions, particle packs, and their comments. **[C]** Chinese walkthroughs, MCBBS archive, Chinese shader translation, and Korean DC Inside builder discussions supplement them. URLs appear beside the findings above.

**[?] Coverage gaps:** targeted searches in Tieba, NGA, Zhihu, Arca Live, Ruliweb, and Namu did not yield a stronger attributable Minecraft creator technique than the sources retained here. BOOTH surfaced a Minecraft builder anthology, not usable public ruin/preset instructions; Pixiv/Fanbox/X and Nicovideo access was uneven. Naver's identified map post could not be read. These are retrieval limits, not evidence that those communities lack relevant work. [BOOTH discovery lead](https://booth.pm/en/items/6651894), [Naver lead](https://cafe.naver.com/marplecafe/42414), [original Japanese ruin PV](https://www.nicovideo.jp/watch/sm25620005).

**[?] Bilibili comment limit:** public video pages and descriptions were searchable, but the metadata API returned HTTP 412. A comment response whose video association could not be verified was discarded. No claims in this report depend on those unassociated comments. Bilibili search-related suggestions, auto-generated forum summaries, and translated third-party download pages were not treated as creator evidence.

**[?] Practical evidence missing:** no verified regional “post-apocalyptic preset” with all three of shader release, full settings export, and matching hardware benchmark; no trustworthy published block dimensions or numerical checkpoint spacing for the regional soulslike examples; no complete NeoForge/Iris/Epic Fight integration test. Proposed recipes explicitly preserve those gaps.

**[V] Local primary snapshots:** `complementary_common.glsl`, `complementary_properties.txt`, `complementary_en_US.lang`; `photon_shader_settings.glsl`, `photon_shader_properties.txt`, `photon_shader_en_US.lang`; `bliss_settings.glsl`, `bliss_shader_properties.txt`, `bliss_en_us.lang`; `photon_vfx_README.md`; creator HTML and selected readable page captures. They are in `research/r2/codex_raw/` and were retrieved from the linked primary URLs. Branch contents may move; re-export the settings from the exact release eventually pinned by the project.

## Summary

**[V] The most useful discoveries are Chinese Yuushya's detailed street demos, Chinese ruin builder cogco/Kaiwen Liu's disclosed rendering workflow, Japanese Angel of Abyss's public support record, Japanese map makers' explicit audio-channel choices, and KilaBash's current Chinese Photon VFX documentation.** Sources: [Yuushya](https://yuushya.com/townscape/download.html), [Dawn Elegy](https://www.planetminecraft.com/project/wasteland-dawn-elegy/), [Angel](https://minecraft-mcworld.com/32951/), [Fillusioner](https://minecraft-mcworld.com/151471/), [Photon commands](https://low-drag-mc.github.io/LowDragMC-Doc/zh/photon2/commands.html).

**[C] Regional atmosphere advice favors volumetric depth and strong contrast for ruins, while Korean builders also warn that heavy mist obscures distant detail.** The preserved MCBBS recommendation names Bliss/SEUS Renewed; DC Inside supplies a concrete Unbound sunset reference at 11500 ticks. Neither is a complete gameplay preset. [MCBBS archive](https://t.me/s/mcbbsss/415095), [Korean comparison](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=380424).

**[?] Start with one shared Complementary preset:** Medium profile, controlled bloom around 0.09, saturation around 0.80–0.85, Scene Aware shafts, and moderate cave lighting. Tune fog altitude to the district's actual elevation. Distinguish sewers, slums, and church through original materials, local emitters, lights, and sound rather than assuming automatic regional shader switching. All proposed values need the actual 1.21.1 client and boss benchmark. [Verified controls](https://github.com/ComplementaryDevelopment/ComplementaryReimagined/blob/main/shaders/lib/common.glsl).

**[?] Build atmosphere at three scales:** repeated structural order and large damage shapes; original street/industrial props; sparse particles and spatial sounds. Use 16×16 authoring modules, but greybox the playable interiors and boss floors first. The white-gold machine church is an original synthesis, not a verified regional builder's recipe. [Small Japanese module](https://www.youtube.com/watch?v=Grur6B8ummc), [layered industrial city](https://kaiwenliu.work/projects/automata-heart).

**[V] Custom audio can use streamed OGGs; mono supports positional attenuation, stereo suits beds/music. [?] Give each district its own original sound identity and separate local machinery from background music.** Use one audio/FX lifecycle owner and clear it on death, reload, teleport, and victory. [NeoForge audio](https://docs.neoforged.net/docs/1.21.1/resources/client/sounds/).

**[C] Regional map reports expose navigation confusion, barrier bypass, tutorial softlocks, persistent attack audio, and boss/reset problems. [?] These are actionable design tests:** durable progression flags, recoverable tutorial states, visible opened routes, and reliable cleanup. Trial arena sizes of 24×24 or 32×32 and 10–25-second boss retries are proposed starting points, not measurements from those creators. [Angel comments](https://minecraft-mcworld.com/32951/), [Omega discussion](https://klpbbs.com/thread-163262-1-1.html).

**[?] Korean creator implementation evidence remains limited because the identified Naver post was inaccessible; exact regional checkpoint formulas and RTX 4060 performance remain unverified.** The report separates these limits from source-checked capabilities and original design proposals. [Korean map lead](https://cafe.naver.com/marplecafe/42414).
