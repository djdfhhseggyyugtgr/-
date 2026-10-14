# Notes 3A: visual and audio atmosphere (dark anime sci-fi ruin, AI LIMIT vibe)

Researched 2026-10-13/14 for the Minecraft **1.21.1 + NeoForge** soulslike map. Scope: shader look-dev, resource-pack look, particles and weather, sound, and reference builds. Shader choice and performance are already covered in `docs/research/README.md`, so they are not repeated here.

**Method.** I used the Ollama `web_search`/`web_fetch` API for web pages and for raw GitHub source files (shader `en_US.lang`, `shaders.properties`, LICENSE). Reddit came from Arctic Shift and YouTube from `tools/social.py`. I checked mod versions and dependencies through the public Modrinth REST API with `curl`/urllib (`api.modrinth.com/v2/project/<slug>/version?game_versions=["1.21.1"]&loaders=["neoforge"]`). I did not use the built-in WebSearch or WebFetch. Raw data is in `research/r2/3a/`. The Modrinth helper scripts are in `research/r2/3a_scripts/`.

**Tags:** [V] verified in an official doc, source code, or primary page · [C] community report or secondary source · [?] inference or untested; needs an in-game test on the user's PC.

---

## 0. Key findings (read first)

1. **Per-area mood under shaders cannot come from switching shader settings.** Shader options are compile-time `#define`s, so every change triggers a full pack reload [V Iris docs: https://shaders.properties/current/reference/shadersproperties/shader_settings/]. Mood per area has to come from things the pack already reads at runtime:
   - the biome uniforms
   - cave detection from altitude and skylight
   - the dimension type (`fixed_time`, `has_skylight`, the effects folder)
   - biome water color
   - world content: blocks, lights, particles
   - runtime shader patches through Supplemental Patches (§1.6)
2. **Datapack fog and sky colors are mostly ignored by shader packs. Biome *water* color is honored.** Complementary has `WATERCOLOR_MODE` = Biome Based. Photon has `BIOME_WATER_COLOR` ("water absorption takes the biome water colour into account") [V, both lang files]. So a custom sewer biome's `water_color`/`water_fog_color` reaches the shader.
3. **Complementary's cave mode fires only below camera Y = 5 with low skylight.** The rule is `isEyeInCave = … if(eyeAltitude < 5.0, eyeBrightness.y/240, 1.0)` [V `shaders.properties`, main branch]. Photon's `biome_cave` fires below Y = 63 with low skylight [V Photon `shaders.properties`]. **Build the Sewer Town walkable floor at Y below 0** so both packs switch to their cave fog and cave lighting.
4. **Iris biome detection only knows vanilla biome IDs.** The constants are `BIOME_*`/`CAT_*` [V https://shaders.properties/current/reference/uniforms/biome/]. Bliss has per-biome environments (Swamp, Jungle, Dark Forest …) and Photon has per-biome Rayleigh fog RGB (swamp, jungle, taiga, snowy, arid). Both key off vanilla biomes and categories [V]. Trick [?]: build an area with a **vanilla biome ID whose JSON you override in the map datapack**, for example `minecraft:swamp` re-themed as the Slums. The shader then sees "swamp" and applies its swamp fog, which you tune in the preset. Photon also reads `temperature`/`rainfall` of any biome, custom ones included, for its weather and fog variation [V].
5. **Licensing decides how far presets can go:**
   - **Complementary License 1.7:**
     - Modpacks may include the pack only unmodified, through the CurseForge/Modrinth systems.
     - Modified redistributions need a new name and must "look noticeably different". They also need "significant **human-written** code additions" (§1.3.f).
     - So agents cannot ship a Complementary edit. Shipping a settings `.txt` is fine because it does not modify the pack [V].
   - **Euphoria Patches** gets around this with a patcher mod, under an agreement with EminGT [V FAQ].
   - **Photon's license** allows redistributing modified or unmodified portions, except on monetized platforms (CurseForge/Modrinth) without permission. It allows modpack inclusion [V]. So a **map-specific Photon edit** (custom `dimension.properties` folders or biome fog) is legally possible if hosted on GitHub.
6. **Supplemental Patches** (MIT, NeoForge 1.21.1 v1.0.2, 2026-09-18) lets a *resource pack* do three things in Complementary + Euphoria at runtime:
   - inject **custom fog functions** into `mainFog.glsl`
   - inject **custom blocklight colors** for modded blocks into colored lighting (ACL)
   - detect **modded biomes** (`moddedBiome` + `MOD_BIOME_*`; needs one shader reload after joining)

   This is the cleanest way to get a teal sewer fog keyed to our own biome under Complementary [V docs]. Whether it is allowed under the Complementary license has not been confirmed [?].
7. **Version traps on 1.21.1** [V wiki histories]:
   - Model-element `light_emission` came in **1.21.2**.
   - The biome `music` field became a weighted list, with `music_volume`, in **1.21.4**.
   - The firefly, `tinted_leaves` and copper-torch particles are 1.21.5+.
   - Biome environment *attributes* came in **1.21.11**.
   - Do not use any of these.
8. **Continuity on NeoForge 1.21.1 needs Sinytra Connector + Forgified Fabric API** [V Modrinth deps]. Use **Fusion** (native NeoForge, connected and scrolling textures, emissive overlays, 1.3.16 on 2026-10-05) or **Athena** instead.
9. **Art direction rule from the AI LIMIT producer: "what would happen if plants went extinct?"** The team rejected the usual "nature reclaims the ruins" look [V GamingBolt interview]. So **no green moss or vines**. Use black-mud seepage, mineral streaks, rust and crystal instead. The glowing 묘목 saplings should be the only living green, which makes them a strong accent. Critics disliked AI LIMIT's "dingy dull brown subterranean tunnels" and "samey grey corridors" [V TheSixthAxis; notes_ailimit]. Plan landmarks and color accents so the areas do not repeat that.
10. **Flag outside this scope (stack pin):** Modrinth has **no Iris 1.8.13** at all. The 1.21.1 NeoForge builds are 1.8.12 (2025-06, Sodium 0.6) and **1.8.14-beta.1** (2026-06-13, "updates to Sodium 0.8") [V Modrinth API]. Iris #3114 ("Iris will need an update to work with Sodium 0.8.12 on 1.21.1") is still open. A third-party "Iris-Sodium Compat" mod exists for this gap [C modpackindex]. `versions.yaml` pins Iris 1.8.13 + Sodium 0.8.12, and that combination may not exist. Propose a contract review: either Iris 1.8.14-beta.1, which has the block-entity shadow bug #3283, or Sodium 0.6.x + Iris 1.8.12.

---

## 1. Shader look-dev

### 1.1 Ways to vary mood per area (what each pack actually reads)

| Lever | Complementary/Euphoria | Photon | Bliss/Eclipse | Notes |
|---|---|---|---|---|
| Below Y≈5 with low skylight ("cave") | cave fog, cave lighting, darker water [V] | cave below Y 63 [V] | Cave Fog, which is a darkness heuristic [V] | Put the Sewer floor at Y < 0 |
| Biome precipitation (none/rain/snow) | `inDry/inRainy/inSnowy` [V] | `biome_may_rain/snow` [V] | rain fog multiplier | Set per custom biome with `has_precipitation` |
| Vanilla biome ID or category | only Nether biomes and Pale Garden (1.21.4+) [V] | per-category fog color and density (swamp, jungle, taiga, snowy, arid) [V] | per-biome environments: swamp, jungle, dark forest … [V] | Override a vanilla biome's JSON to re-theme it [?] |
| Biome temperature/downfall | – | `biome_temperature/humidity` drive weather and fog variation [V] | – | Works for custom biomes |
| Biome `water_color` | WATERCOLOR_MODE = Biome Based [V] | BIOME_WATER_COLOR [V] | ? | Sewer sludge color |
| Dimension type | custom dims fall into the overworld program through wildcard entries [V PR #2853 discussion] | same | same | `fixed_time` (frozen sun angle), `has_skylight=false` (no rain, no sun shafts), `ambient_light` (Iris `ambientLight` uniform [V]) |
| Dimension with nether/end `effects` | Iris ≥ PR #2853 (Sep 2025) uses the nether/end programs [V]; whether the 1.21.1 builds include it is [?] | | | A "nether-effects" sewer dimension would get Complementary's biome-colored nether fog (soul-sand-valley teal, basalt grey) [?]. Risky |
| `minecraft:darkness`/blindness effect | `maxBlindnessDarkness` uniform [V] | | | Pulse darkness for boss intros through `/effect` |
| Runtime GLSL patch | **Supplemental Patches** custom fog and colors (§1.6) [V] | edit the pack, which the license allows off CF/Modrinth [V] | Bliss license not checked (it is a Chocapic13 edit) [?] | |

### 1.2 Complementary Unbound r5.9.x + Euphoria Patches: option names and a starting preset

The option IDs below were checked in the source (`shaders/lang/en_US.lang`, `shaders.properties`, main branch) [V]. **The values are my starting proposals [?]** and must be tuned on the RTX 4060 by looking at the result.

| Group | Option (ID) | Meaning [V] | Starting value for this map [?] |
|---|---|---|---|
| Base | `SHADER_STYLE` | 1 = Reimagined, 4 = Unbound | 4 |
| Base | `RP_MODE` | 0 Basic, 1 IntegratedPBR+, 2 seuspbr, 3 labPBR | 3 if our pack ships `_n/_s` for **every** block in view. Otherwise 1 plus `IPBR_EMISSIVE_MODE=3` ("labPBR > IPBR+") |
| Fog | `ATM_FOG_MULT` | altitude fog: 0.50 Very Subtle … 0.95 Intense | 0.95 (Slums) |
| Fog | `ATM_FOG_DISTANCE`, `ATM_FOG_ALTITUDE` | start distance; altitude where fog is densest | Altitude at the slum street level, so haze pools in the alleys |
| Fog | `CAVE_FOG`, `BORDER_FOG` | extra underground fog; chunk-edge fog | on, on |
| Light shafts | `LIGHTSHAFT_BEHAVIOUR` | 0 off, 1 Scene Aware, 2 Regular, 3 Extreme | 1. Use 2 for set pieces with sun through grates |
| Light shafts | `LIGHTSHAFT_SMOKE` | volumetric smoke ("severely impacts performance") | off; test it at boss arenas |
| Light shafts | `LIGHTSHAFT_NOON_I/SUNSET_I/NIGHT_I/RAIN_I`, `LIGHTSHAFT_SUNSET_SATURATION` | multipliers; low saturation shifts toward yellow | raise RAIN_I; low saturation gives gold shafts |
| Color | `ATM_COLOR_MULTS` + `ATM_{MORNING,NOON,NIGHT,RAIN}_{R,G,B,I}` | sky and fog tint | NOON ≈ R0.85 G1.0 B1.05 (grey-teal) |
| Color | `LIGHT_COLOR_MULTS` + `LIGHT_*_{R,G,B,I}` | sun and moon light tint | slightly warm sun (gold highlights against teal shadows) |
| Color | `XLIGHT_R/G/B/I`, `XLIGHT_CURVE` | blocklight tint, intensity and falloff | slightly cooler; higher curve for pools of light |
| Darkness | `CAVE_LIGHTING`, `AMBIENT_MULT` | extra light where there is no skylight; light in shadows | lower both by about 20–30% for the sewers, then check enemy readability |
| Tonemap | `TM_EXPOSURE`, `TM_CONTRAST`, `T_SATURATION`, `T_VIBRANCE`, `TM_DARK_DESATURATION`, `TM_WHITE_PATH` | standard grading | contrast +, saturation about 0.85, dark desaturation + |
| Grading | `COLORGRADING` + `GR_RR … GR_*C` | 3×3 channel mixer plus curves | push greens toward teal; keep skin readable |
| Bloom | `BLOOM_ENABLED`, `BLOOM_STRENGTH` (0.027 = 15%, 0.036 = 20%) | glow on bright pixels and humidity | 20–25%; caves add humidity bloom |
| Water | `WATERCOLOR_MODE` (0 constant / 2 biome / 3 clamped), `WATER_FOG_MULT`, `WATER_ALPHA_MULT`, `BRIGHT_CAVE_WATER` | | 2; fog up; alpha up (murky); bright cave water off |
| Wetness | `RAIN_PUDDLES` (0 off, 1 in rain, 2 full coverage in rain, 3 puddles always, 4 full always); needs `BLOCK_REFLECT_QUALITY` ≥ 1 | puddles; they appear where rain reaches, glass-roof caveat | 2 (Slums in rain). Sewers need baked wetness (§2.4) |
| Colored light | `COLORED_LIGHTING` (ACT), `COLORED_LIGHT_FOG`, `COLORED_LIGHT_FOG_I`, `COLORED_LIGHT_SATURATION`, `COLORED_CANDLE_LIGHT` | Iris-only colored lights and volumetric light fog ("severely impacts performance") | ACT on; light fog only in the boss arena or high profile |
| Lens | `VIGNETTE_R`, `CHROMA_ABERRATION`, `LENSFLARE_MODE`, `MOTION_BLUR_EFFECT` | | subtle vignette; others off for readability |
| Stylized | `DARK_OUTLINE`, `WORLD_OUTLINE`, `PIXELATED_SHADOWS/BLOCKLIGHT/AO` | outline and pixel looks | test `DARK_OUTLINE` for an "anime" read [?] |
| Particles | `GLOWING_COLORED_PARTICLES` | all colored particles glow | off |

**Euphoria additions** seen in a real settings export (EP 1.6.5) [V names]: `NIGHT_DESATURATION`, `RAIN_ATMOSPHERE`, `CAVE_FOG`, `EMISSIVE_SOUL_SAND`, `SOUL_SAND_VALLEY_OVERHAUL`, `BIOME_COLORED_NETHER_PORTALS`, `EYES`, `LAVA_EDGE_EFFECT`, `NO_RAIN_ABOVE_CLOUDS`. Other features listed on the site: darkness desaturation, block emission intensity, seasons, epic thunderstorm, and better modded-block light detection (auto-emissive from light level) [V FAQ/features]. Every EP setting is **off by default** [V].

**Community notes:**
- Complementary's fog is a flat altitude layer with no real *distance* fog, which is weak for silhouetted city vistas.
- Spooklementary, Eclipse and Photon do distance haze better.
- [C] https://www.reddit.com/r/minecraftshaders/comments/1vi68f4/

**Spooklementary** (a Complementary edit by SpacEagle17) adds:
- Cave Lighting Fade
- moon-phase night lighting
- "Cave Sound Effects" (chromatic aberration plus static before cave sounds)
- Blood Moon
- "Eyes in the Dark" (keep off for this project)
- [V https://mcmodwiki.com/shader/spooklementary/26.2]

### 1.3 Photon equivalents [V `en_US.lang`/`shaders.properties`]

- Haze:
  - `AIR_FOG_MIE_DENSITY_{MORNING,NOON,EVENING,MIDNIGHT,RAIN,BLUE_HOUR}`, `AIR_FOG_MIE_FALLOFF_START/HALF_LIFE`
  - per-category Rayleigh fog color and density: `AIR_FOG_RAYLEIGH_{DENSITY,R,G,B}_{RAIN,ARID,SNOWY,TAIGA,JUNGLE,SWAMP}`
  - `OVERWORLD_FOG_INTENSITY`, `CAVE_FOG` ("light, slightly glowing fog underground")
  - `BLOOMY_FOG` ("almost no performance cost")
  - `VL` with `VL_RENDER_SCALE`, `AIR_FOG_CLOUDY_NOISE`
  - `AIR_FOG_COLORED_LIGHT_SHAFTS` (shafts tinted by stained glass)
  - `LPV_VL` (fog lit by blocklight; needs `COLORED_LIGHTS`, a flood-fill)
- Grading:
  - `tonemap` (ACES fit/full, Hejl, Lottes, Uncharted 2, Tech, Ozius, Reinhard…)
  - `TONEMAP_COMPARISON` split screen, useful for look-dev
  - `GRADE_BRIGHTNESS/CONTRAST/SATURATION/WHITE_BALANCE`
  - **`GRADE_TEAL_SAT_BOOST`**, `GRADE_ORANGE_SAT_BOOST`, `GRADE_GREEN_SAT_BOOST/HUE_SHIFT`
- **`PURKINJE_SHIFT`** (night-vision desaturation, good for sewers). **`AUTO_EXPOSURE`** with bias, min, max and rates (eye adaptation when leaving a tunnel). `VIGNETTE`.
- Water and materials: `BIOME_WATER_COLOR`, `RAIN_PUDDLES`, `ENVIRONMENT_REFLECTIONS` (SSR; "big performance impact"), `TEXTURE_FORMAT`, `EMISSION_STRENGTH`, `HARDCODED_SPECULAR/EMISSION`.
- License: modifying and redistributing is allowed except on monetized platforms. Modpack inclusion is allowed [V https://raw.githubusercontent.com/sixthsurge/photon/main/LICENSE].

### 1.4 Bliss/Eclipse equivalents [V https://mcmodwiki.com/shader/bliss-shader/26.2]

- Fog:
  - fog density per time of day, including cloudy variants
  - `Per Biome Environments` plus per-biome toggles (Swamp, Jungle, Dark Forest …) with Uniform or Cloudy density
  - Fog R/G/B and Fog Falloff, Atmospheric Haze Density, Rain Fog Multiplier, Cave Fog
  - "Fog Light Propagation" (flood-fill colored light lights the air)
- Grading and materials: Tone Curve, Color Grading, Bloomy Fog, Porosity, Puddles, Minimum Light Brightness.
- Known issue: Bliss on NeoForge has the invisible-entity issue (`TRANSLUCENT_ENTITIES`) [V, in the existing notes].

### 1.5 Shipping presets

- Iris shader menu has **Import/Export** of a settings `.txt` [V Iris guide https://github.com/IrisShaders/Iris/blob/multiloader-new/docs/guide.md]. The per-pack file lives next to the zip as `shaderpacks/<pack file name>.txt` [C]. Euphoria setting files carry `AAA_THIS_IS_A_EUPHORIA_PATCHES_SETTINGS_FILE=true` [V export dump].
- Ship this:
  - `shaderpacks/<exact pack zip>.txt`
  - `config/iris.properties` (`shaderPack=…`, `enableShaders=true`) [C]
  - the pack zip itself through the CurseForge/Modrinth modpack dependency, unmodified (Complementary License §1.2.c–d) [V]
- Keep **two or three profiles** (`low/med/high`) as separate txt files. One pack-wide preset has to serve both areas, so the per-area difference comes from §1.1 levers.
- [?] Swapping presets at an area change is possible in principle: a mod could rewrite the txt and trigger an Iris reload while a "rift" loading screen is up, which matches AI LIMIT's own load-zone rifts. It is hacky and needs a test.

### 1.6 Supplemental Patches (runtime patches into Euphoria, resource-pack driven)

- [V https://supplemental-patches.pages.dev/documentation/fog] Custom fog: write `void MyFog(inout vec4 color, float lViewPos, …)` under `atmospherics/fog/functions`. Put a call snippet under `atmospherics/fog/fogs`. It is injected into `/shaders/lib/atmospherics/fog/mainFog.glsl` → `DoFog`.
- [V …/colors_and_tints] Custom ACL blocklight colors per block. JSON `{"code": "vec4(r,g,b,extraLight)"}` is injected into `blocklightColors.glsl`. Assign it with `"blocklight": "<color name>"` in the block shader JSON.
- [V …/uniforms] Detects modded biomes with `moddedBiome` and `MOD_BIOME_<ID>` (needs one shader reload after joining). Custom uniforms can be defined through JSON (`uniforms/`). `MOD_<MODID>` detection.
- Versions [V Modrinth/CF]:
  - NeoForge 1.21.1 builds: 1.0.0–1.0.2 (2026-09)
  - 1.0.2 targets Complementary r5.9.3 + EP 1.10.5
  - MIT license; "Can I include this in my modpack? Yes"
  - **Tied to exact Complementary/EP versions**, so pin all three together
- Use it for:
  - `ourmod:sewer_town` → exponential teal-grey fog (density about 0.03/block) mixed toward `vec3(0.16,0.22,0.22)`
  - `ourmod:slums` → long, light, warm-grey distance haze that silhouettes towers (fixes the "no distance fog" complaint)
  - our sapling (묘목) block → gold ACL color

### 1.7 No-shader fallback (low-end players, and anyone who disables shaders)

- Vanilla biome `effects` in 1.21.1: `fog_color`, `sky_color`, `water_color`, `water_fog_color`, `grass_color`, `foliage_color`, `particle {options, probability}`, `ambient_sound`, `mood_sound`, `additions_sound`, `music {sound,min_delay,max_delay,replace_current_music}` (single object, not a list) [V wiki history https://minecraft.wiki/w/Biome_definition_(Java_Edition)].
- **Polytone** (GPL-3.0, NeoForge 1.21.1 `1.21-5.1.2` 2026-10-13) [V wiki https://github-wiki-see.page/m/MehVahdJukaar/polytone/wiki]:
  - per-dimension `fog_colormap`/`sky_colormap`, `no_weather_fog_darken`, `ambient_light`
  - **lightmaps** (`polytone/lightmaps/overworld.png`): teal-tinted darkness without shaders
  - **post chains** (vanilla post-processing color grade)
  - per-biome effect modifiers, **block sound types**, **particle emitters on blocks**, **custom particle types**, **GPU particles**, **variant textures by weather** (wet textures when it rains)
  - built-in colored block light (tints the vanilla lightmap; probably overridden by Iris shaders [?])
- Fog mods (Fog Overrides, Foggy Pale Garden) only affect vanilla fog. Shaders replace it [V #3065 for the 26.x attributes; likewise for 1.21.1 biome fog under Complementary, C].

### 1.8 Performance reminders specific to the mood features

- Expensive: Complementary `LIGHTSHAFT_SMOKE`, `COLORED_LIGHT_FOG`, Extreme shafts; Photon `ENVIRONMENT_REFLECTIONS`, `LPV_VL`; Bliss Fog Light Propagation. Cheap: Photon `BLOOMY_FOG`; Complementary Scene Aware shafts [V lang comments].
- Use the expensive ones only in boss arenas, by building them as a separate dimension with its own preset profile [?], or keep them off.

---

## 2. Resource-pack look

### 2.1 Palette mapped to vanilla 1.21.1 blocks (retexture targets)

- **Grey ruin mass:** stone bricks and cracked variants, **tuff bricks, polished tuff, chiseled tuff (1.21)**, deepslate tiles, andesite, smooth stone, grey concrete.
- **Teal:**
  - **waxed oxidized/weathered copper**, cut copper, **copper grate** (see-through sewer grates), copper door and trapdoor (all 1.21) [V]
  - prismarine and dark prismarine, warped planks, cyan terracotta
- **Gold:** waxed (unoxidized) cut copper, gold block, raw gold, yellow terracotta, chiseled copper.
- **White-gold church:** calcite, smooth quartz, quartz pillar, white concrete, bone block, plus gold trims.
- **Light blocks with fixed shader light colors** (Complementary ACT / Photon / Bliss map light color by block ID) [C/?]:
  - soul lantern, soul torch and soul campfire → cyan-teal
  - sea lantern → pale cyan
  - copper bulbs → warm. **Oxidation sets their brightness: 15 / 12 / 8 / 4**, so oxidized bulbs make dim teal-housed lamps [C]
  - end rod → white
  - shroomlight → orange
  - ochre froglight → yellow
  - `COLORED_CANDLE_LIGHT` → **16 dye-colored candle lights** (small "LED" indicators) [V option]

  **Retexturing a vanilla light block keeps its shader light color.** A soul lantern re-skinned as an emergency strip-light still casts teal [?].

### 2.2 "No plants" rule

- AI LIMIT's core idea is a post-apocalypse **without** plants [V GamingBolt interview https://gamingbolt.com/ai-limit-interview-bosses-level-design-art-style-and-more].
- Replace moss and vines with: black-mud (흑니) seepage, white mineral efflorescence, rust bleed under rebar, cracked plaster, crystalline Mud growth (retextured amethyst clusters can play crystals, and they sparkle with Subtle Effects).
- Petrified or grey dead plants are acceptable. Save living green for the 묘목 sapling checkpoints.

### 2.3 Black mud and sludge, plus drips

- Retexture **`minecraft:mud`**. Its collision is 14/16 tall, so feet sink slightly (good "sludge" feel). Use **soul sand / soul soil** where the sludge should slow the player [C, vanilla behavior].
- Water: biome `water_color` ≈ `#3a4a44`, `water_fog_color` ≈ `#1a2320` [?]. Under shaders it is honored through WATERCOLOR_MODE / BIOME_WATER_COLOR (§0.2).
- **Free drips:** pointed dripstone under a water source drips `dripping_dripstone_water` particles with sound, and fills cauldrons. Retexture pointed dripstone as broken rusty pipe or rebar [C, vanilla mechanic].
- Flowing sewage: Fusion **scrolling textures** for conveyor-like sludge channels [V Fusion README].

### 2.4 LabPBR for wet and metal [V https://shaderlabs.org/wiki/LabPBR_Material_Standard]

- `_s` channels:
  - R = perceptual smoothness
  - G = F0 0–229, or **230–254 predefined metals** (albedo tints the reflection); 255 = albedo used as F0
  - B = **porosity 0–64** (how much rain darkens and wets), 65–255 = SSS
  - A = emission 0–254 (255 = none)
- `_n` is DirectX (Y−), B = AO, A = height. This matches art-bible.yaml.
- Sewer floors and walls are not rain-exposed, so puddle options will not wet them. **Bake wetness in:**
  - high R (smoothness) on the lower 2–4 px of walls and on floors near water
  - darker albedo there
  - porosity at about 40–64 for concrete so the Slums darken in rain
- Rust: G low (non-metal oxide), R low. Exposed steel: G = 230 (iron). Gold trim: G = 231 (gold) [V metal table].

### 2.5 Connected textures on NeoForge 1.21.1

| Mod | 1.21.1 NeoForge | Notes |
|---|---|---|
| **Fusion** (SuperMartijn642) | 1.3.16 (2026-10-05), no deps [V] | connected textures (full or simple layout), **scrolling textures**, connected models, overlays with `"emissive": true`. A Sodium visual bug (#188) was closed after the 1.3.0 rewrite [V]. ARR license, but meant for packs |
| **Athena** | 4.0.6 (2026-05-09) [V] | CTM; an AllTheLeaks mixin conflict was fixed (#94) [C] |
| Continuity | 3.0.0+1.21.neoforge, **requires Connector + Forgified Fabric API** [V Modrinth deps] | avoid. A native port (aspctt, 2026-09, experimental) exists [V] |

### 2.6 Emissive

- With shaders: LabPBR `_s` alpha, `CUSTOM_EMISSION_INTENSITY` (Complementary) or `EMISSION_STRENGTH` (Photon) [V].
- Without shaders:
  - Fusion emissive overlays (blocks)
  - **ETF** `_e` emissive entity textures (7.2.5 NeoForge 1.21.1) [V]
  - GeckoLib glowmask layers
- Known issue: display-entity props (Animated Java) look dimmer under shaders (Iris #3053) [V, existing notes].
- **Do not use model `light_emission`** (that is 1.21.2+) [V].

### 2.7 Custom sky

- Under shaders, the pack draws the sky. Steer it with `ATM_*` multipliers and clouds (`CLOUD_STYLE_DEFINE`, Unbound clouds) [V].
- Without shaders: **Nuit** (formerly FabricSkyboxes) has a NeoForge 1.21.1 build, `1.0.0-beta.6` (2026-09-15) [V]. Polytone dimension sky colormaps also work.
- [?] Untested: whether Nuit skyboxes survive under Complementary. Complementary's `SUN_MOON_STYLE` notes interaction with resource-pack sun/moon textures.

---

## 3. Particles and weather

### 3.1 Vanilla (datapack-only)

- Biome `particle` = random ambient particles around the player. 1.21.1-safe types:
  - `white_ash`, `ash`, `warped_spore` (teal floaters), `crimson_spore`, `spore_blossom_air`, `mycelium`
  - `dust` (any color and size), `dust_color_transition`, `falling_dust`
  - `dripping_water`/`falling_water`, `dripping_dripstone_water`
  - `campfire_cosy_smoke`, `white_smoke` (1.20.3), `soul`, `soul_fire_flame`, `electric_spark`, `scrape`/`wax_off` (teal-white copper glints), `glow`, `end_rod`
  - `trial_spawner_detection`, `vault_connection`, `dust_pillar`, `small_gust`
  - [V list https://minecraft.wiki/w/Particles_(Java_Edition); version gates as in §0.7]
- `/particle … force` in repeating functions works but sends packets every tick. Prefer client-side emitters (§3.2).

### 3.2 Mods (all checked for 1.21.1 NeoForge on 2026-10-13)

| Mod | Version (1.21.1 NeoForge) | What it gives | Agent-authorable? |
|---|---|---|---|
| **Polytone** | 1.21-5.1.2 | **block particle emitters**, custom particle types, **GPU particles** (100k = 1 draw call; not shaded by Iris, drawn with vanilla lighting) [V] | yes (JSON). [?] On "older versions" the wiki says custom particles spawn only through block emitters; confirm on 1.21.1 |
| **Particle Storm** (westernat) | 1.4.3.1 (2026-09-24), LGPL [V] | **runs Bedrock (Snowstorm) particle JSON on Java** | **yes**. This is the Java runtime for files made by `bbmodel_particle_effect`. Small user base (15k downloads) |
| AAA Particles | 2.3.3 (CF, 2026-10) / 2.2.3 (Modrinth), MIT [V] | Effekseer runtime | harder; Effekseer editor files |
| Photon (VFX, KilaBash) | 2.2.7–2.2.8 (maven 2026-10-08) [V] | Unity-like VFX, trails; **2.2.8 adds colored point and spot lights with shadows, volumetric fog volumes and light beams that work with Iris** [V dev video] | GUI editor → `.fx`/`.fxpack` (NBT resources). Hard for agents; **CC BY-NC-SA 4.0** (fine for a non-commercial school map) [V] |
| Veil (Quasar) | 4.5.2, LGPL [V] | JSON particle emitters, editor added in 2026 (PR #163) | yes, but code integration is needed |
| Lodestone | 1.8.2 [V] | VFX library for mod code | code |
| **Subtle Effects** | 1.15.1 (2026-10-12), ARR [V] | **steaming water near light ≥ 12**, boiling, lantern sparks, rain ripples, dust from falling blocks [V config list] | config only |
| **Particle Rain** | v4.0.2 (2026-10-10), MIT [V] | slanted rain, **fog particles in biomes tagged `#c:is_spooky`/`#c:is_wet`**, **water streaks on hard walls**, ripples [V] | tag our biomes |

### 3.3 Weather control

- Weather is global (dimensions derived from the overworld share it). Rain renders only where the biome `has_precipitation` and skylight exist [C].
  - Sewer: `has_precipitation:false`, or use a no-skylight dimension.
  - Slums: rainy biome.
  - Drive it with `/weather` from region triggers and `doWeatherCycle false`.
- [?] Per-player fake weather: the server mod can send `ClientboundGameEventPacket` RAIN_LEVEL_CHANGE / THUNDER_LEVEL_CHANGE to individual players.
- Dimension type `fixed_time` freezes the sun angle per area (an endless overcast dusk for the Slums) [C].

---

## 4. Sound

### 4.1 Vanilla plumbing

- `sounds.json` [V https://minecraft.wiki/w/Sounds.json]:
  - **mono files are positional; stereo files ignore distance**, so use stereo for music and beds and mono for emitters
  - `stream:true` for long files (it limits concurrent instances to 4)
  - `attenuation_distance` (default 16), `preload`, `weight`, `volume`, `pitch`
- Biome: `ambient_sound` (loop), `mood_sound` (cave-style one-shots in dark spots: `tick_delay`, `block_search_extent`, `offset`), `additions_sound` (`tick_chance`), `music` (1.21.1 single object; `replace_current_music:true` for an immediate swap) [V].
- **Boss music:** NeoForge **`SelectMusicEvent`** exists in 1.21.1 and can override or cancel situational music. That suits phase-based boss themes in our mod [V javadoc https://lexxie.dev/neoforge/1.21.1/net/neoforged/neoforge/client/event/SelectMusicEvent.html, PR #862].

### 4.2 Mods

| Mod | 1.21.1 NeoForge | Use | Caveats |
|---|---|---|---|
| **AmbientSounds 6** (CreativeMD, LGPL, needs CreativeCore) | 6.3.10 (2026-10-08) [V] | **engine fully replaceable by resource pack**: dimension → region → sound layers; conditions on biome (scanned with distance falloff), average-height "underground", **air-pocket scan** (tunnel ≈0 vs hall ≈1), **nearby block groups** (water nearby → sewer flow); `/ambient-debug` [V wiki https://github.com/CreativeMD/AmbientSounds/wiki/Engine] | default nature sounds (birds, crickets) contradict "no plants". Ship our own engine |
| **Sound Physics Remastered** (GPL) | neoforge-1.21.1-1.5.1 [V] | ray-traced reverb, occlusion, absorption; per-block reflectivity config | [C] breaks music discs for some users; [C] reverb dropping on looping sounds after the first play; test with looping emitters |
| Sound Physics Perfected (MIT) | 1.17.5 [V] | lighter alternative | [C] some say it sounds worse |
| Presence Footsteps (NeoForge port `pf-neoforge`) | 1.21.1-1.12.0-beta.1 [V] | material footsteps | unofficial port of a Polyform-Shield mod; licensing is murky [?] |
| **Reactive Music** (GPL) | 1.3.5 [V] | songpacks (YAML + mp3); events `BIOME=`, `BIOMETAG=`, `UNDERGROUND`, `DEEP_UNDERGROUND`, `NIGHT`, `RAIN`, **`BOSS` (vanilla boss bar on screen)** [V doc] | only works if bosses use vanilla boss bars |
| Music Triggers | 7.0.4 [V] | trigger-based music | mob trigger bug on NeoForge, fixed in TIL 0.4.6 (#208) [V] |
| Battle Music (CC-BY-4.0) | 1.2.2 [V] | music per entity type | – |
| Dynamic Surroundings Rebirth (port) | 1.4.1, about 3k downloads [V] | | too young; skip |

### 4.3 Making and sourcing audio legally

- **Agent-made (the most in keeping with the assignment):**
  - procedural drones, hum, drips and steam with Python/numpy or `sox synth` → `ffmpeg -c:a libvorbis`
  - mono for emitters, normalize loudness, loop-point crossfades
  - this is license-clean and reproducible in the cloud [?]
- **Libraries:**
  - **Sonniss #GameAudioGDC** bundles: royalty-free, commercial use, no attribution, games allowed. Raw files may not be sold, and the bundles **prohibit any use for AI training or "developing AI"** [V https://sonniss.com/gdc-bundle-license/]. Do not feed them to music-model LoRAs.
  - Pixabay Content License [C]
  - Freesound (pick CC0 or CC-BY; avoid NC unless the project stays non-commercial)
  - Kenney (CC0)
  - **공유마당** (Korea Copyright Commission; filter by CC-BY or 자유이용 and keep the attribution format "작품명 by 저작자, 출처, CCL") [V https://gongu.copyright.or.kr/]
- **AI music, as of Oct 2026:**
  - **Suno:**
    - Free tier: Suno owns the output; non-commercial use only.
    - Since 2026-09-03, free accounts get at most 7 lifetime *trial* downloads, personal use only.
    - Pro 20/month, Premier 60/month; paid downloads carry commercial rights [V https://suno.com/blog/suno-updates-tos, https://help.suno.com/en/articles/2416769].
  - **Udio:** downloads have been disabled for everyone since the Oct 2025 UMG settlement [C https://aimusicdaily.com/udio-commercial-use]. It is unusable for shipping files.
  - **ElevenLabs Music:**
    - Free tier: downloads not permitted.
    - Starter and up: downloads, with commercial use except film/TV/radio/"Studio Games". **Indie games are OK**.
    - Free tier requires attribution [V https://elevenlabs.io/music-terms].
  - **ACE-Step 1.5:** open source (README says MIT; the HF space says Apache-2.0). The base model runs in **< 4 GB VRAM**, so it fits the RTX 4060; XL needs ≥ 12 GB [V https://github.com/ace-step/ACE-Step-1.5].
  - Stable Audio Open: Stability Community License [C]. MusicGen weights: CC-BY-NC [C].
  - Korea Copyright Commission guides (2025-06): purely AI output is not registrable; human contribution is what gets protected. The dispute-prevention guide warns against prompting toward specific existing works and artists [V https://www.copyright.or.kr/information-materials/publication/research-report/view.do?brdctsno=54851]. **Never prompt "in the style of the AI LIMIT OST / Vanguard Sound"**, and keep the prompts and logs as evidence.

---

## 5. References and techniques

- **Sluda Builds, "The Worst City on Earth" (Kowloon Walled City), 4.5M views** [V transcript https://www.youtube.com/watch?v=IWZQB9zDD3Y]. Techniques:
  - 3D-modeled massing imported first, then the terrain slope
  - then interior circulation (doorways punched between touching buildings on every floor) before the facades
  - facades built as a **kit of unique pieces in several widths → combined into columns → placed across the buildings aligned to floor levels**
  - every daylight-facing face has windows
  - laundry, a "rooftop jungle of wires and antennas", "constellations of fluorescent lights"
  - rooftops as an alternative route above the dark alleys
  - bland large buildings around it for contrast

  This kit-based method suits agent-built Slums.
- Sluda Builds, "Futuristic Cyber-City" (XRyHC330fdk). Kōri, "Dystopian Cyberpunk Slums inspired by STRAY" (BsJXkq3JGHo). Elysium Fire, "Cyberpunk Project" (UtLun2-jOQ8, 5.4M views).
- r/Minecraftbuilds "Big Sewer?" (2.4k upvotes). Its **giant animated fan (Create bearing)** drew "Stray / HL2" comments and "neglect, lonesome and dread" [V https://www.reddit.com/r/Minecraftbuilds/comments/1kso4pq/]. Motion plus shafts through fans works. Do it with a GeckoLib block entity rather than Create.
- "Medieval Sewer Starter Base" (Elden Ring-inspired, 970 upvotes): wide vaulted channel, boat travel [V 1upa9rj].
- AverageTuna, "7 Dystopian Build Hacks": machines from levers, buttons, item-frame dragon heads, stained-glass "lasers", shroomlight cores [V CmesRYHnwXk].
- Church references: Anor Londo builds (TSr4iHHZyW8), Irithyll (DTtcYBPixZY). NieR City Ruins (vhk_N1c_fp0). HL2 City 17 (Bxk3_mwDjEQ).
- **VALERIA** (soulslike map, NeoForge 1.21.1, Epic Fight): ships a custom soundtrack and textures resource pack and is distributed as a full `.minecraft` merge [V https://www.planetminecraft.com/project/valeria-6557226/].
- Showcase renders: Mineways → Blender + MCprep (tommstein, pOJkWj1vktg) for trailer stills.

---

## 6. Per-area mood recipes (draft for user review)

### Sewer Town (1st area)

- **Space:**
  - floor at Y ≈ −40…0 so both Complementary and Photon cave modes fire
  - custom biome `ourmod:sewer_town` (or a separate dimension with `has_skylight:false`, `fixed_time`)
  - vaulted brick and tuff channels, copper-grate catwalks
  - one or two **sky shafts** (grates to the surface) for gold light-shaft set pieces
- **Palette:** grey tuff and brick; teal oxidized copper pipes and grates; black-mud floor (mud/soul-soil retex); rust bleed; gold only on the sapling checkpoint and the critical-path lamps.
- **Light:**
  - dim teal from oxidized copper bulbs (light 4) and soul lanterns
  - **warm gold marks the critical path and 묘목**
  - Complementary `CAVE_LIGHTING` and `AMBIENT_MULT` about −25%, ACT on, colored light fog only near the boss reservoir
  - Photon: `PURKINJE_SHIFT`, `AUTO_EXPOSURE`
- **Fog:**
  - shader cave fog
  - optional Supplemental Patches teal exponential fog keyed to `MOD_BIOME_OURMOD_SEWER_TOWN`
  - Photon `CAVE_FOG` + `BLOOMY_FOG`
- **Water:** biome water `#3a4a44`, water fog `#1a2320` [?]; Complementary `WATERCOLOR_MODE=2`, `WATER_FOG_MULT`↑, `BRIGHT_CAVE_WATER` off.
- **Wet:** LabPBR baked wet bands (smoothness↑ near water), puddles from water-logged slabs.
- **Particles:**
  - biome `dripping_dripstone_water` / `white_ash` at low probability
  - pointed-dripstone pipe drips
  - Subtle Effects steam where water sits near lamps
  - Polytone or Particle Storm steam vents
  - faint `warped_spore` motes in the larger halls
- **Sound:**
  - AmbientSounds engine: region "sewer" (biome + underground + water block group) → flowing-water bed and hum
  - air-pocket < 0.3 → tight-tunnel drone; > 0.7 → hall reverb tail
  - additions: distant pipe groans and metal ticks
  - Sound Physics Remastered reverb
  - music: sparse low pad. The Sewer Cleaner boss theme comes through `SelectMusicEvent`, with phase 2 adding layers

### Outer-Wall Ruins – Slums (2nd area)

- **Space:**
  - custom biome `ourmod:slums` (or a re-themed `minecraft:swamp` for Photon/Bliss swamp fog [?]), surface level
  - dimension `fixed_time` at an overcast late afternoon
  - layered shanties stacked against the colossal wall, rooftop routes over dark alleys (Kowloon method)
  - the wall itself as the bland mega-structure for contrast
- **Palette:** grey concrete and tuff, rusted corrugated sheets (retextured iron or copper trapdoors), faded teal tarps, scavenger-camp warm lights; **no greenery**.
- **Weather:** rain most of the time (`/weather rain` on entry), thunder during the Panic Reaper cemetery; Complementary `RAIN_PUDDLES=2`; Particle Rain wall streaks + `#c:is_wet` fog.
- **Fog and grade:**
  - Complementary `ATM_FOG_MULT` 0.95 with altitude at street level
  - grey-teal `ATM_*`, slightly warm `LIGHT_*`, saturation about 0.85
  - Supplemental Patches distance haze for tower silhouettes
  - Photon: swamp/rain Mie density↑, `GRADE_TEAL_SAT_BOOST`↑, `GRADE_ORANGE_SAT_BOOST` slightly↑ (camp fires)
- **Light:** fluorescent "constellations" (end rods or sea lanterns behind glass), colored candles as indicator LEDs, campfire warmth at the Temporary Campsite hub.
- **Particles:** `white_ash` drifting, campfire smoke, `electric_spark` from broken cables, rain ripples.
- **Sound:** rain on metal (Polytone block sound types on the sheet-metal blocks), distant wind through the wall, camp chatter loops near the hub; area music through biome `music` with `replace_current_music`; boss themes through the mod.

### White-gold church (later areas)

Calcite, quartz and gold; clean fog; strong gold sun shafts (`LIGHTSHAFT_BEHAVIOUR=2`) through tall windows; bloom up; reverberant choir pads; a high-contrast break from the teal-grey lower city.

---

## 7. In-game tests to run on the user's PC

1. Complementary cave mode at Y < 5 versus Y > 5 in the sewer test room. Photon at Y < 63.
2. Biome `water_color` under Complementary `WATERCOLOR_MODE=2` and under Photon `BIOME_WATER_COLOR`.
3. A re-themed `minecraft:swamp`: does Photon/Bliss swamp fog apply? Does Iris assign `CAT_SWAMP` to a custom biome tagged like a swamp?
4. Supplemental Patches 1.0.2 + Complementary r5.9.3 + EP 1.10.5 with a custom fog keyed to our biome. Measure the fps cost.
5. Which Iris build is real for our Sodium (see §0.10). Does it include PR #2853 (custom dims with nether effects)?
6. Particle Storm playing a `bbmodel_particle_effect` file. Polytone block emitters and GPU particles under Iris.
7. Sound Physics Remastered with looping positional emitters (reverb drop-out report).
8. Fusion connected and scrolling textures under Sodium 0.8.12 + Iris.
