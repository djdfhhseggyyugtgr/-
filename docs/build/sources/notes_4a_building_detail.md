# Round 2 / Branch 4a: Detailed building techniques and decoration tools (2026-10-13/14)

Scope: block palettes, wall detailing, decay, lighting, decoration mods, micro-detail and building tools for
**Minecraft Java 1.21.1 + NeoForge**, for four themes: sewer tunnels, slums, ruined megastructure walls, white-gold
sci-fi gothic church. Written as a handbook a building agent can follow.

Tags: **[V]** verified from a primary source (mod page/API, official docs, wiki, builder-server guide, bug tracker);
**[C]** community / tutorial / single builder's opinion / SEO-style guide; **[?]** uncertain or our own inference.
Raw data: `research/r2/4a/` (S_* search JSON, F_* fetched pages, `mr/` and `mrv/` Modrinth API dumps,
`social/` YouTube transcripts and Reddit threads). Helper scripts: `research/r2/4a_scripts/`.

Note on source quality: several 2026 "guide" sites (minespecs.com, craftdex.net, palettinator, gaialegends, astroworld)
look SEO/AI-written. Where they agree with established builder-server docs (Conquest, WesterosCraft, ArdaCraft) or
with the game's mechanics, I use them as [C]. Claims I could not cross-check are left out or marked [?].

---------------------------------------------------------------------
## 0. Version guardrails for builders (read first)

1.21.1 facts [V] https://minecraft.wiki/w/Java_Edition_1.21.1 : DataVersion **3955**, resource pack format **34**,
data pack format **48**. Use these when writing `.nbt`/`.schem` files and pack metadata.

**Blocks that do NOT exist in 1.21.1** (agents keep suggesting them):
| Added in | Blocks / IDs to avoid | Source |
|---|---|---|
| 1.21.4 | pale oak (all), `pale_moss_block`/`pale_moss_carpet`/`pale_hanging_moss`, `creaking_heart`, `resin_*` (resin bricks, resin clump), `eyeblossom` | [V] https://minecraft.wiki/w/Java_Edition_1.21.4 |
| 1.21.5 | `leaf_litter`, `wildflowers`, `bush`, `firefly_bush`, `cactus_flower`, `short_dry_grass`, `tall_dry_grass`, test blocks | [V] https://minecraft.wiki/w/Java_Edition_1.21.5 |
| 1.21.6 | `dried_ghast` | [C] |
| 1.21.9 | `copper_bars` (+oxidized/waxed), `copper_chain`, `copper_chest`, `copper_golem_statue`, `copper_lantern`, `copper_torch`, `*_shelf`; oxidized lightning rods | [V] https://minecraft.wiki/w/Java_Edition_1.21.9 |
| 26.x | anything newer | — |

**ID renames:** the iron chain is `minecraft:chain` in 1.21.1; it became `minecraft:iron_chain` only in 1.21.9 [V].
`lightning_rod` in 1.21.1 has **one** colour (fresh copper, never oxidizes) [V 1.21.9 changelog].
**Available and useful from 1.21 (Tricky Trials):** `tuff_bricks`, `polished_tuff`, `chiseled_tuff`, `chiseled_tuff_bricks`
(+stairs/slabs/walls), `copper_grate`, `copper_bulb`, `chiseled_copper`, `copper_door`, `copper_trapdoor` (all four
oxidation stages + `waxed_*`), `crafter`, `heavy_core`, `vault`, `trial_spawner` [C, well known].
**Text in NBT:** 1.21.1 still uses JSON-string text components (`text:'{"text":"..."}'`); SNBT text arrived in 1.21.5 [V 1.21.5 page].
**Custom item models:** 1.21.1 `minecraft:custom_model_data` is a single **int** read by item-model `overrides`;
the float/flag/string lists and `item_model` component are 1.21.4+ [V] https://mappings.dev/history/49a880cbde.html .
**Paintings:** data-driven since 1.21 (`data/<ns>/painting_variant/*.json`: `asset_id`, `width` 1–16, `height` 1–16);
`title`/`author` fields are 1.21.2+, so omit them [V] https://minecraft.wiki/w/Painting_variant_definition .
**Gravity / reaction blocks:** sand, gravel, concrete powder, suspicious gravel fall; concrete powder turns into concrete
next to water. Place them only on support or with physics-free tools, and never use concrete powder as "sludge" near water [C].
**No stairs/slabs** for concrete, terracotta, plain deepslate; smooth stone has a slab but no stair [C minespecs].

---------------------------------------------------------------------
## 1. General detailing techniques

### 1.1 How the engine shades (why depth works) [C, matches vanilla behaviour]
- Vanilla face brightness multipliers: top 1.0, north/south 0.8, east/west 0.6, bottom 0.5; smooth lighting (AO) darkens
  inside corners. One block of offset therefore creates up to 4 tonal values from one material.
  https://minespecs.com/blog/why-your-builds-look-flat/
- Shaders add real directional shadows on top, but design must read without them too (the user may lower settings).
- 1 block of projection is the workhorse; 2 often fights the silhouette. Use 2+ only where the form demands it (buttresses,
  chimneys, entrance bays).

### 1.2 Three-layer wall depth (our standard)
Built from the sources above plus interior practice [C]; the layer numbers are our convention [?].
| Layer | Offset from wall plane | What goes here | Typical blocks |
|---|---|---|---|
| L+1 structure ("bones") | +1 (sometimes +2) | columns/pilasters every 5–7 blocks, ribs, buttresses, plinth (bottom 2–3 rows), string course at each floor, cornice/eaves, quoins | darker or contrasting family; caps of stairs/slabs |
| L0 field ("skin") | 0 | gradient-textured wall material | main palette |
| L−1 recess | −1 | panels between columns, window/door reveals, niches, vents, tie holes | same family, 1 step darker in deep recesses |
| micro (sub-block) | +0.5 / +3/16 / −7/16 | slab/stair trims (0.5), trapdoors and pressure plates (3/16 and 1/16 plates), buttons/levers, item frames; panes sit 7/16 back from the face | trapdoors, stairs, slabs, panes, plates |
- Panel rule: recess the panel, not the whole wall; keep the panel touching the column so the AO seam lands on the joint.
  Windows go in recessed panels, never on the column. https://minespecs.com/blog/why-your-builds-look-flat/ [C]
- Interiors: make walls **two blocks thick** (outer skin + independent inner skin) so the interior palette, wainscot bands
  and sills are designed separately from the exterior. Zeeno, https://www.youtube.com/watch?v=32afl6tdMWQ [C]
- Trapdoor trick: an open trapdoor against a face recolours that face without changing geometry; also usable to fake a
  second light direction. Speck, https://www.youtube.com/watch?v=hYEpn_ui5XA [C]

### 1.3 Massing, scale and proportion
- Player = 1.8 tall, eyes 1.62, step 0.6. Interior air heights: 2 = cramped/tunnel, 3 = domestic, 4 = generous,
  5–6 = public, 8+ = monumental. Storey height = air + 1 floor block. https://minespecs.com/blog/scale-and-proportion/ [C]
- The door (1×2) is the ruler: count wall height in doors; >6 door-heights reads as an institution. Give entrances their
  own mass (5–7 wide bay pulled out 1–2), raise them on a plinth, frame them with a 1-deep recess. [C same]
- Oversized builds: pick a whole multiplier (2×, 3×, 4×) and hold it; scale structure, not fittings (doors, ladders,
  lanterns stay 1×, which is what sells the size); at 2×+ swap fine stair/slab fiddling for **material bands 2–3 blocks
  deep**; roof pitch flattens with span. [C same]
- Large builds: base–body–top at about 1:3:1 with a plane or material change at each join; human-scale objects at the
  foot; long approach; taper; check the silhouette from ~150 blocks. [C same]
- Massing: 3–4 distinct cuboids, secondary masses 1/3–1/2 of the primary; odd widths (5/7/9/11) give a centre for
  doors and roof ridges; detail density rises toward the focal point. https://craftdex.net/articles/the-architecture-of-builds [C]
- Rhythm: no flat run longer than ~7 blocks without a change of plane, material or opening. [C minespecs]
- Combat space (soulslike, Epic Fight) [?, our inference, verify in playtest]: main fighting corridors ≥4–5 wide and
  ≥5 high so third-person camera and dodge rolls do not clip; boss arenas enclosed, ≥25–35 blocks across, with
  ceiling ≥8; keep floor clutter (slabs, carpets, fences) off the fighting floor because it breaks footing and hitboxes.

### 1.4 Gradients ("texturing"/colouring)
Established builder-server guidance [V for those servers' practice]:
- Order palettes by **value first, then hue, then texture**. Squint to judge value.
  WesterosCraft https://westeroscraft.com/docs/building/fundamentals/gradients ; ArdaCraft https://www.ardacraft.me/resources/gradient-guide
- **Never skip a palette step** between neighbouring blocks (light touching dark directly) except as a rare,
  deliberate accent. The three faults: *splattering* (skipped steps / random scatter), *smallpox* (shallow palette,
  patchy blobs), *sandwiching* (horizontal sediment-like bands). [V WesterosCraft]
- Two pattern families: **drip** (vertical streaks from sills, cracks, outfalls; weathering from rain) and **cluster**
  (organic blobs of varied size/shape, never in rows or columns). Avoid many diagonal stair-steps, which read as splatter.
  Conquest https://www.conquestreforged.com/guides/gradients [V]
- Palette depth must match surface size: too many blocks over-details, too few looks bland; a highly detailed
  (deep) surface wants a simpler gradient and vice versa; balance neighbouring buildings (cohesion over individual
  prettiness). [V ArdaCraft]
- Use gradients to **reveal form**: lighter edge around arches, selective drip that separates two wall depths;
  darken under windows (drip stains), corners, bases, openings and joints between wall angles. [V Conquest/ArdaCraft]
- Connected/varied textures can fight a gradient at specific coordinates; move the pattern or add an in-between block. [V ArdaCraft]
- Workflow: build in a placeholder/canvas block, finish shape and cracks, then paint the gradient. [V ArdaCraft/WesterosCraft]
- Four colouring layers (Speck, architecture student; https://www.youtube.com/watch?v=hYEpn_ui5XA) [C]:
  1) *shading* from a chosen key-light direction (base block + 2 darker + 1 lighter used sparingly);
  2) *texturing* = adding/removing noise (calm a noisy block like planks with a smoother one);
  3) *patina* = story weathering (leaks under pipes, salt/water damage, repairs with the wrong material);
  4) *realism* = all three combined. **Rustication**: coarse, chunky textures low, finer and smoother higher.

### 1.5 Avoiding noise [C, synthesis]
- Hierarchy: one hero element per view; detail density increases toward it; leave rest areas (plain fields) between
  busy zones. https://craftdex.net/articles/the-architecture-of-builds
- "Make a base pattern of shapes, then interrupt it with one variation" (e.g., a row of open windows with one blocked).
  elodie dot txt, https://www.youtube.com/watch?v=xScy8kmjLag
- Every detail should have a reason (structure, function, story). Random noise painting is "tier 1"; story-driven
  patina is the goal. [C Speck]
- At large scale use material bands and depth, not stair/slab clutter, which turns into visual noise from afar. [C minespecs]
- Graffiti/murals in **low-noise blocks** (terracotta, concrete) so they sit in the wall. [C elodie]
- Backdrops: build against a context (neighbouring masses, skyline), never in a void. [C elodie]

### 1.6 Organic decay and ruin [C, synthesis]
Rabniff https://www.youtube.com/watch?v=_6QCEcLntvo ; WesterosCraft; concrete video https://www.youtube.com/watch?v=pkjqQ0HIXGI
1. Pick the failure point with structural logic (corner, unsupported span, impact); damage spreads from it.
2. Glass and light fittings go first; doors removed or broken; windows boarded (trapdoors/signs) or shards (panes of
   mixed light-grey/plain glass).
3. Break edges are stepped with **lower-tier versions of the same material** (stone bricks → cobblestone stairs/slabs;
   concrete → andesite/tuff stairs) so the edge looks worn, not cut.
4. Floors thin out toward the break; beams/joists (logs, fences, chains) hang or lie across the gap.
5. **Conservation of mass**: rubble of the same materials below the break (some may be "looted" away); mix in whole
   blocks of the original so it reads as part of the building.
6. Cracks where stress and water concentrate (corners, openings, joints); cracks are also the darkest gradient points.
7. Vegetation follows water and light: vines/moss on ledges, cracks and under drips; not on dry sheer faces;
   dry ruins use cracked/dusty blocks rather than moss.
8. Small secondary holes (roof, walls) around the main collapse.

### 1.7 Lighting placement
- `minecraft:light` block: invisible, levels 0–15 (`/setblock ~ ~ ~ minecraft:light[level=7]`), waterloggable, intended for
  map makers [V] https://minecraft.wiki/w/Light_(block). Use for fill light and to hide sources.
- Hide sources: under carpets, behind trapdoors, wall blocks, iron bars, panes; sea lanterns and end rods suit sci-fi
  [C LeonSBU https://www.youtube.com/watch?v=Z_AqgJH39no].
- Soulslike rule of thumb [?]: light in **pools** with dark gaps; warm light = safety (checkpoint saplings, NPCs), cold light
  = danger zones; key light on boss arenas and on enemy spawn points so telegraphs stay readable; avoid evenly spaced torches.
- Shaders: colour per block comes from the shader pack's `block.properties` IDs. Modded blocks only get special treatment
  if the pack maps them; Iris 1.7+ allows tag-based entries (`%namespace:tag`) [V]
  https://shaders.properties/current/reference/miscellaneous/block_properties/ . For our custom lamps rely on LabPBR
  emissive (`_s` alpha) plus a vanilla-tagged light level, and test under the chosen pack [?]. Datapack fog/light colours
  are ignored by Iris+Complementary (see research README §6.3).
- Smoke for life: lit campfires (smoke particles), with a hay bale underneath for tall signal smoke [C].

### 1.8 Interior detailing [C]
- Zone by function first (workshop / living / shrine), then floors per zone, then wall bands (base trim, mid stripe,
  sill trims), then windows, then furniture, then small props. Zeeno https://www.youtube.com/watch?v=32afl6tdMWQ
- Rooms need footprints that fit furniture plus walking space (bed room ≥4×5; table with chairs ≥5×5). [C minespecs]
- Use contrast between floor and wall; one bold accent family per room; tie interior accent to window glass colour.

### 1.9 Signage and murals (1.21.1-safe)
| Method | Good for | Cost / caveat | Tag |
|---|---|---|---|
| `text_display` + custom font glyphs (resource pack) | crisp shop signs, church script, holo text; `billboard`, `background`, `brightness`, `line_width`, `see_through` | entity; set `view_range` and culling `width`/`height` (0 = never culled); 1.21.1 uses JSON text strings | [V] https://www.elkonia.com/wiki/codex/display-entities.html |
| Custom **painting variants** | posters, murals, billboards up to 16×16 blocks | entity, cheap; datapack + `textures/painting/` sprite | [V] wiki painting variant |
| Signs / hanging signs (glow ink) | small labels | block entity with special renderer; many signs = FPS cost | [V] MC-271606 |
| Banners | cloth, flags, faction marks | block entity renderer; keep counts low | [V] MC-271606 |
| Maps in item frames | photo-like images | **expensive**: 144 maps dropped a user from ~80 fps (MC-160583); avoid | [V] https://mojira.dev/MC-160583 |
| Low-noise block murals (terracotta/concrete) | graffiti, faded logos | free (terrain mesh) | [C] |

### 1.10 Procedural recipes for an agent (code-based building) [?, our design from the rules above]
Agents build by script (`.nbt`/`.schem` generators, WorldEdit commands), not by hand, so the rules must become algorithms.
1. **Massing pass**: boxes/arches in a placeholder block (e.g., `white_wool`); check odd widths, bay grid (5–7), storey heights.
2. **Depth pass**: extrude L+1 elements on the bay grid, carve L−1 panels and reveals, add plinth/string course/cornice.
3. **Material pass**: assign per element role (structure, field, recess, trim, metal, accent) from the theme table; 60/30/10.
4. **Gradient pass** (per surface): `t = a·height_term + b·noise(u,v) + c·damage_proximity + d·concavity(AO)`;
   noise = low-frequency simplex/metaball (cluster scale 6–12 blocks) or vertically stretched noise (drip, 3–4× taller
   than wide) seeded under sills/outfalls; never white noise. Map `t` to palette index, then run a **no-skip
   relaxation**: while any 4-neighbour pair differs by >1 step, pull the outlier toward the neighbour mean; allow ≤2% of
   cells as deliberate accents. Perturb any height term by ≥±1.5 steps of noise to avoid sandwiching.
5. **Decay pass**: exposure score (air neighbours, edges, corners, openings); crack/mossy/rubble substitutions by
   probability; mossy only where wet (≤3 blocks above water, under drips); rubble cone volume ≈30–60% of removed volume,
   same material family, surface smoothed with stairs/slabs oriented down-slope.
6. **Greeble pass**: place prop "stamps" (pipes, vents, cables, crates) from a library on allowed anchor points, with
   minimum spacing and density weighted toward focal points.
7. **Light pass**: place light pools at nodes of the path graph (junctions, arenas, checkpoints), hidden sources first.
8. **Review pass** (pipeline G5/5.0): screenshots at ~3, ~30 and ~150 blocks; squint/blur test; silhouette test.

---------------------------------------------------------------------
## 2. Per-theme recipes

Value orders below are approximate; verify each palette with an in-game swatch screenshot under the chosen shader [?].
All IDs are `minecraft:` unless prefixed.

### 2.1 Sewer tunnels (Sewer Town–Southwest)
Mood: grey-teal, damp, Victorian brick and poured concrete, rust/verdigris metal; sparse cold light with rare warm pools.
Original reference: AI LIMIT's grey/teal ruins and sewers with robots and Void beasts (`docs/design/sources/notes_ailimit.md` §7) [V there].

| Role | Blocks (1.21.1 IDs) |
|---|---|
| Ribs / arches / pier bases (L+1, dark) | `deepslate_bricks`, `deepslate_tiles`, `polished_deepslate` (+stairs/slabs/walls), `cracked_deepslate_bricks/tiles` |
| Wall field gradient (light → dark) | `polished_andesite` → `andesite` → `stone_bricks` → `tuff_bricks` / `polished_tuff` → `tuff` → `cobbled_deepslate` |
| Alternative warm brick sewer | `bricks` → `mud_bricks` → `packed_mud` (+ `mud_brick_*`) |
| Waterline band (0–3 above water) | `mossy_stone_bricks`, `mossy_cobblestone`, `moss_block`, `moss_carpet`, `mud`, `packed_mud`, `glow_lichen` |
| Channel bed / sludge | `mud`, `gravel`, `coarse_dirt`, `soul_soil` (dark "black mud"); dark `water` via a custom biome water colour [?] |
| Walkways | `smooth_stone_slab`, `stone_brick_slab`, `polished_andesite`, edge `stone_brick_stairs`, `iron_trapdoor` grates |
| Metal / pipes | `iron_bars` (grates), `iron_trapdoor`, `chain`, `hopper` (spouts), `cauldron`, `lightning_rod` (thin copper conduit), `end_rod` (white conduit, emits light), `waxed_oxidized_copper_grate`, `waxed_weathered_cut_copper` (+stairs/slabs) for large pipes and verdigris stains, `chiseled_copper` rings, `lever`/`tripwire_hook`/`grindstone` as valves |
| Decay | `cracked_stone_bricks`, `cobweb`, `hanging_roots`, `vine`, `pointed_dripstone` + `dripstone_block` (drips under a water source) |
| Light | `soul_lantern` (cold), `waxed_copper_bulb` (wall lamps), `sea_lantern` behind `iron_bars`, `lantern` (warm, checkpoints only), `light` fill |
| Mods (optional) | Create Deco catwalks / mesh fences / sheet metal / supports / cage lamps / hazard decals; Create fluid pipes & valves as static props; Supplementaries faucet, iron gate, rope, sconces; Macaw's metal bridges, doors, trapdoors, wall lamps; FramedBlocks slopes for egg-shaped profiles |

Geometry and recipe [?, from real sewer typology + the rules above; fWhip suggests mixing straight runs with large
reservoir/holding chambers instead of a single straight line, https://www.youtube.com/watch?v=4OzJt0wBazw [C]]:
- Main collector 11–13 wide × 8–10 high: channel 5 wide, water surface 1 below walkways, walkways 3 wide each side,
  segmental or pointed vault. Dark rib every 6 blocks (+1 deep, 1 thick); recessed brick panel (−1) between ribs.
- Secondary tunnels 5–7 wide × 5–6 high, egg-shaped (narrow invert, wider crown). Reservoirs/cisterns: pillared halls
  (good boss arenas; pillars are cover and camera anchors).
- Water features: outfalls from wall pipes (hopper or copper grate mouth + flowing water) into the channel; weirs
  (1-block steps of flowing water); side drains under `iron_trapdoor`; ceiling drips via pointed dripstone.
- Gradient: darkest and mossy at the waterline/splash zone, lighter toward the crown; drip streaks below outfalls and
  cracks; irregular waterline (no sandwich band).
- Greebles: pipe runs on brackets along the upper wall (offset +1), cable runs (`chain` horizontal), valve wheels,
  manhole shafts with `ladder`, maintenance doors, numbered markers (text_display or painted terracotta).
- Grate trick: an armour stand under a stair/slab reads as a dark grate (DetailCraft, 407 upvotes)
  https://www.reddit.com/r/DetailCraft/comments/v7irk8/ [C]; entity cost, use sparingly.

### 2.2 Slums (Outer-Wall Ruins–Slums)
Mood: dense, vertical, shanties of salvage on ruined concrete; rust, tarps, laundry, cables, warm interior light.

| Role | Blocks |
|---|---|
| Old base / ground | `cobblestone`, `andesite`, `stone`, `bricks`, `cracked_stone_bricks`, `light_gray_concrete`, `gray_concrete`, `packed_mud`, `mud_bricks`, `gravel`, `coarse_dirt` |
| Shanty boards | panels of `spruce_planks`, `dark_oak_planks`, `mangrove_planks`, `stripped_spruce_log`, `stripped_dark_oak_log`, `bamboo_planks`/`bamboo_mosaic`; vertical boards via `*_trapdoor` and `*_fence` |
| Scrap metal | `iron_trapdoor`, `waxed_exposed_cut_copper` / `waxed_weathered_cut_copper` / `waxed_oxidized_cut_copper` (+slabs/stairs), `waxed_*_copper_trapdoor`, `waxed_*_copper_door`; mod: Create Deco sheet metal |
| Roofs / tarps | `*_trapdoor`, `*_slab`, copper slabs; tarps from `*_wool`/`*_carpet` in muted brown, grey, cyan, blue, green; `*_banner`; Supplementaries awnings; Macaw's Roofs |
| Supports / access | `scaffolding`, `ladder`, `*_fence`, stripped logs, `chain`, `iron_bars` rails; Macaw's rope bridges and balconies |
| Clutter | `barrel`, `composter` (crates), `cauldron`, `smoker`, `blast_furnace`, `crafting_table`, `loom`, `grindstone`, `chipped_anvil`, `hay_block`, `dried_kelp_block`, `flower_pot`, `candle`; few `decorated_pot`/`chest` (block entities) |
| Cables / lines | `chain` and `lever` wiring rotated with the debug stick (elodie, https://www.youtube.com/watch?v=xScy8kmjLag [C]); `tripwire` string; Supplementaries rope + bunting/flags for laundry (bunting-on-rope placement not verified [?]); long sagging spans: Immersive Engineering wire connectors or display-entity segments (§4) |
| Light | `lantern`, `candle`, `redstone_lamp` (lit state), `shroomlight` behind trapdoors, `waxed_copper_bulb`; tinted light through `*_stained_glass` under shaders |
| Mods (optional) | Supplementaries (awnings, buntings, rope, sacks, notice board, sign posts, item shelf, flags), Macaw's (bridges, doors, windows/shutters, roofs, lights), Another Furniture / Handcrafted (stools, shelves), Create Deco (sheet metal, catwalks, ladders, postboxes) |

Recipe:
- Modules 3–5 wide, 3–4 high per storey, stacked with 1–2 block overhangs and offsets; never align floor lines across
  neighbours (vary ±1); bridges and ladders between modules; alleys 2–3 wide, main fight streets 5–7 wide [?].
- Segment façades with awnings, ledges, balconies; each module its own material, but cap the district palette
  (~10 families) and move a few colour "key points" across the scene so it reads as one composition [C elodie].
- Patina story: rust streaks under metal sheets, soot above stove chimneys, repairs in mismatched boards, water stains
  under roof edges; smoke stacks a bit taller than buildings but lower than the smoke column [C elodie].
- Market stalls: fence/log frame, slab or barrel counter, awning (Supplementaries awning or banners/carpet on slabs),
  goods in item frames/pots; lanterns hung under the awning.
- Story props: laundry lines, ladders to roofs, rooftop gardens in pots, dumpsters (`barrel`/`composter` groups),
  graffiti in terracotta.

### 2.3 Ruined megastructure walls (outer wall)
Mood: brutalist precast concrete at 4× scale, exposed rebar, collapsed floors, overgrowth where water collects.

| Role | Blocks |
|---|---|
| Concrete field (light → dark) | `smooth_stone` → `light_gray_concrete` → `polished_andesite` → `andesite`/`stone` → `polished_tuff` → `tuff` → `gray_concrete` / `cyan_terracotta` |
| Imprinted/board-formed concrete | `tuff`, `cobblestone`, `dead_brain_coral_block` (reads recessed), `lodestone` top face [C concrete video] |
| Structural steel / dark bands | `polished_basalt`, `smooth_basalt`, `polished_blackstone`, `deepslate_tiles` |
| Rebar | `iron_bars` (vertical runs), `chain` (horizontal), `lightning_rod` (thin orange rod, any facing) — the video used waxed copper bars, which are 1.21.9+, so substitute these [V version, C technique] |
| Formwork ties / tie holes | `chain` stubs; stair pockets in a grid (every ~4 blocks at large scale) [C concrete video] |
| Joints | recessed stair or wall rows between pour lifts / precast panels; light-to-dark mini-gradient per lift, repeated [C concrete video https://www.youtube.com/watch?v=pkjqQ0HIXGI] |
| Collapse / rubble | slabs stepped to fake tilt, `*_stairs`/`*_walls` for rough edges, `cobblestone`, `cobbled_deepslate`, `andesite`, `tuff`, `gravel`, `coarse_dirt`; FramedBlocks slopes or tilted block displays for hero pieces |
| Overgrowth | `moss_block`, `moss_carpet`, `vine`, `cave_vines` (glow berries emit light), `hanging_roots`, `glow_lichen`, `azalea_leaves`, `short_grass`, `fern`, `dead_bush` |
| Accents | faded hazard stripes (`yellow_terracotta` + `black_terracotta`), rust stains (`waxed_weathered_cut_copper`), broken window grids (`gray_stained_glass_pane` + gaps) |
| Large greebles | vent arrays (`iron_trapdoor` or copper grates), 3×3/5×5 pipe cylinders, catwalks/gantries (Create Deco), floodlights (`redstone_lamp`/`sea_lantern` under trapdoor hoods), normal-size service doors for scale |

Recipe:
- Work in a 4× module: precast panels 8×8 or 12×12 with 1-block recessed joints; floor slabs visible as horizontal bands;
  tie-hole grid; vertical drip stains under joints.
- Breaks follow panel joints; rebar sticks out 1–3 blocks from break faces in the slab plane; pancaked floors (stacked
  slabs with stepped tilt); rubble cones below; dust (gravel) on ledges; vegetation on ledges and in cracks.
- Keep human-scale fittings (doors, ladders, railings, lamps) at the base and on catwalks so the wall reads as huge;
  break the top silhouette so it reads as ruined from 150+ blocks.

### 2.4 White-gold sci-fi gothic church (Garden Church / cathedral)
Mood: pristine, sacred, high-tech: white panels, gold trims, cyan/white light; grime only in neglected lower levels.
Original reference: the gold-and-white Church sci-fi cathedral and its "half-data surreal" upper level (notes_ailimit §4, §7) [V there]; copy structure and mood only, never the original's designs.

| Role | Blocks |
|---|---|
| White field (60%), light → shade | `smooth_quartz` → `quartz_block` → `quartz_bricks` → `white_concrete` → `calcite` → `polished_diorite` |
| Columns | base `chiseled_quartz_block`, shaft `quartz_pillar` or `bone_block` (fluted look), capital `chiseled_quartz_block` + gold |
| Secondary warm stone (30%) | `smooth_sandstone`, `cut_sandstone`, `chiseled_sandstone`, or `end_stone_bricks` (pale gold-cream) |
| Gold (≤10%) | `gold_block` (trim, metallic under LabPBR), `raw_gold_block` (shadow-side gold), `honeycomb_block` (amber), `light_weighted_pressure_plate` (1/16-thick gold inlay on floors and sills), `ochre_froglight` (glowing gold); Supplementaries gold bars / gold door / gold trapdoor / gold gate |
| Dark contrast (floors, inlays) | `polished_blackstone`, `gilded_blackstone`, `black_concrete` |
| Glass | `white_`, `light_blue_`, `cyan_`, `yellow_`, `orange_stained_glass(_pane)`; tracery from trapdoors, fences, walls (cathedral tutorial https://www.youtube.com/watch?v=9MOxFWIvrk0 [C]); Macaw's Windows mosaic glass (arched variants [?]) |
| Light | `sea_lantern` (cool), `end_rod` (light strips, candle points, pinnacle tips), `pearlescent_froglight`, `glowstone` behind `white_stained_glass` (diffuse panels), `light` fill |
| Mods (optional) | Macaw's Windows, Rechiseled (CTM quartz/calcite/sandstone variants), FramedBlocks (slopes for vault webs and buttress tops), Supplementaries (gold blocks, candle holders, pedestals), Create Deco (calcite pillars, layered/cut calcite) |

Gothic rules [C] Build Like the Greats https://www.youtube.com/watch?v=sMXO8UVTfw0 :
- Ratios 1:2 (narrow windows, details), **2:3 (most common: windows, nave divisions)**, 3:5 (late/large cathedrals).
- Pointed arches: steep 45° segments at the top, more vertical segments toward the springing; larger arches allow
  smoother curves. Tracery suggests circles/trefoils; lead cames can be copper grates or bars.
- Flying buttresses carry vault thrust to piers; pinnacles on buttresses and corners. Towers: lower part ≈ nave height,
  upper part ≈ half that; spires can double the tower height.
- Plan: cruciform (nave, transept, choir/apse) or long hall without transept.
Workflow [C] https://www.youtube.com/watch?v=9MOxFWIvrk0 : build one complete **nave bay** (pier, arcade arch, triforium,
clerestory, buttress, vault with ribs in a contrasting block and plaster-like infill), then clone it along the axis; build
the apse by shearing the bay 45° and mirroring. For agents: make the bay a parameterised generator and stamp it.
Sci-fi layer [?]: glowing joints (end rods or sea lanterns recessed one block behind panel seams), gold 1/16 inlays,
floating pinnacles, hexagonal/branch motifs in custom blocks, holo text (text_display with our church glyph font),
"half-data" glitches: cyan glass shards and offset block displays. Keep large white fields slightly off-white
(calcite/quartz bricks) so shader bloom does not blow them out; use smooth quartz for trims [?].

---------------------------------------------------------------------
## 3. Decoration and block mods for 1.21.1 NeoForge

Versions from the Modrinth API (`/v2/project/<slug>/version?loaders=["neoforge"]&game_versions=["1.21.1"]`, dumps in
`research/r2/4a/mrv/`), licences from `/v2/projects` (`research/r2/4a/mr/`) [V], unless marked.

| Mod | Latest 1.21.1 NeoForge | Licence | Downloads | What it gives us | Verdict [?] |
|---|---|---|---|---|---|
| Supplementaries (+Moonlight lib) | 1.21.1-4.0.1 (2026-10-11) | Supplementaries Team licence; "free to include in your modpack" | 28.7M | awnings, buntings, rope, sacks, iron/gold gates, gold bars/doors/trapdoors, sconces, candle holders, notice boards, sign posts, faucets, item shelves, pedestals, stone lamps, timber frames | **Yes** (core) |
| Amendments | 1.21-2.1.11 (2026-10-10) | same | 19.7M | wall lanterns, hanging-sign tweaks, vanilla block improvements | Yes |
| Macaw's Doors / Windows / Trapdoors / Bridges / Roofs / Lights & Lamps / Stairs / Fences / Paths | 1.1.5 / 2.4.2 / 1.1.5 / 3.1.2 / 2.3.2 / 1.1.5 / 1.0.2 / 1.2.1 / 1.1.1 (2025–26) | Doors, Trapdoors, Fences, Paths: MIT; others ARR (modpack permission not checked [?]) | 4–11M each | windows, mosaic glass, blinds, shutters, curtains [V]; arched/gothic variants [?]; metal doors, bridges, roofs, street/wall lamps, stair handrails and balconies | **Yes**, pick the sub-mods we use |
| Macaw's Furniture | 3.4.1 | ARR | 7.3M | furniture | maybe |
| Chipped | 4.0.2 (**2024-10-15**, needs Athena + Resourceful Lib) | ARR | 23.6M | huge variant sets of vanilla blocks | Either Chipped **or** Rechiseled, not both |
| Rechiseled (+Fusion, SuperMartijn642 libs) | 1.2.6 (2026-09-13) | ARR | 15.7M | connected-texture variants (quartz, stone, sandstone…) | **Yes** for church/sewer panels |
| Handcrafted | 4.0.3 (2025-03-22) | Terrarium licence | 27.2M | furniture | optional interiors |
| Another Furniture | 4.0.3 (2026-09-23) | custom | 16.3M | benches, shelves, curtains | optional |
| FramedBlocks | 10.6.3 (2026-10-11) | LGPL-3.0 | 2.2M | 100+ shapes (slopes, corner slopes, slope slabs, pillars, panels) wearing any block texture | **Yes** for slopes; block entities (camo data) |
| Create | 6.0.10+mc1.21.1 (2026-04-21) | Create licence | 27.6M | animated machinery, pipes, valves | only if we want moving set pieces (heavy) |
| Create Deco (needs Create) | 2.1.3 (2026-04-18) | MIT on Modrinth, ARR on CurseForge (conflict) | 7.8M | catwalks, sheet metal, bars, mesh fences, supports, cage lamps, hulls, decals, layered stones | good for sewers/walls if Create is in |
| Create: Copycats+ | 3.0.9 (2026-09-06) | ARR | 10.8M | copycat slopes/panels | alternative to FramedBlocks (needs Create) |
| Stoneworks | v21.1.0 (2024-09-17) | MPL-2.0 | 10.3M | cobbled/brick/tile/pillar/shingle variants of every vanilla stone | good, vanilla-faithful |
| Dusty Decorations | 2.3.0 (2026-10-13) | MIT | 3.5M | port/market props | maybe (slum market) |
| Yuushya Townscape | 2.3.0 **beta** | CC-BY-NC-SA-4.0 | 4.8M | 2600+ townscape blocks; needs Architectury, a CTM mod, and Indium with Sodium | risky (Sodium compatibility) |
| Immersive Engineering | 12.4.2-194 (2025-07-05, CurseForge) | custom | 197M | steel/treated-wood/sheet-metal/concrete deco, **catenary wires between connectors**, cage lamps with variable light | only for cables; heavy tech mod |
| Engineer's Decor & Controls Reforged | 1.1.58 (2026-10-13, CurseForge) | MIT | 4k, 4 months old | industrial decor port | immature, skip |
| Domum Ornamentum | 1.0.231 release / 1.0.236 snapshot (GitHub, 2026) | GPL-3.0 | 56.7M | architect's cutter: any block skin on frames, shingles, panels | maybe; block entities |
| LittleTiles | 1.6.0-**pre234** (beta) | LGPL-3.0 | 0.23M | 1/16+ micro-blocks | **No** (beta, heavy, hard to script) |
| Conquest Reforged | 1.20.1 only (v1.7.0, 2026-08-21) | ARR | 1.6M | 12,000 blocks | **Not available for 1.21.1** [V CurseForge files] |
| Fusion (CTM) | 1.3.16 (2026-10-05) | ARR | 15.6M | connected textures for resource packs/our blocks | Yes if we want CTM |
| Athena (CTM) | 4.0.6 | MIT | 24.2M | CTM library (Chipped dependency) | with Chipped |
| Continuity: NeoForged | 3.0.7+1.21.1 (2026-09-24) | LGPL-3.0 | 7k (new third-party port) | OptiFine-format CTM/emissive packs | watch, not yet |
| Polytone | 1.21-5.1.2 | GPL-3.0 | 18.6M | resource-pack lightmaps, colormaps, biome/sky colours, block sounds | useful for mood (test with Iris) |

Sources: Modrinth API dumps; Conquest https://www.curseforge.com/minecraft/mc-mods/conquest-reforged/files/all ;
IE https://www.curseforge.com/minecraft/mc-mods/immersive-engineering/files/6701835 ; Domum
https://github.com/ldtteam/Domum-Ornamentum (GPL-3.0) ; Engineer's Decor Reforged
https://www.curseforge.com/minecraft/mc-mods/immersive-engineers-decor-controls-tools-reforged ;
Supplementaries block list https://wiki.9minecraft.net/supplementaries-mod/blocks/ (+/2/) [C mirror];
Create Deco block list https://wiki.9minecraft.net/create-deco-mod/blocks/ [C mirror].

**Mods vs our own blocks** [?, recommendation]:
- Use mods for generic architecture (windows, doors, slopes, rope, awnings, furniture): huge coverage, maintained, free
  to include in a modpack manifest (never commit the jars; see AGENTS.md).
- Make **our own Blockbench `java_block` props** for anything that carries identity or story: branch-sapling checkpoints,
  church glyph panels and gold filigree, black-mud (흑니) growths, sewer valve wheels/outfalls, signature lamps. Reasons:
  style cohesion, LabPBR maps (modded blocks have none unless we write them), shader block-ID control, our licence.
  Keep 1.21.1 JSON limits (one rotation axis, ±22.5/45°, coords −16..32) and the prop budget (≤40 cubes).
- Every extra deco mod adds blocks without LabPBR, so under Complementary/Photon they look flatter than vanilla
  (vanilla gets the packs' integrated PBR) [?]. Keep the set small: Supplementaries+Amendments, chosen Macaw's,
  Rechiseled+Fusion, FramedBlocks; add Create+Create Deco only if moving machinery is wanted.

---------------------------------------------------------------------
## 4. Micro-detail and performance

| Technique | How | Cost | Use for |
|---|---|---|---|
| Custom block models (resource pack or our mod) | baked into the chunk mesh | paid at chunk rebuild only; cheapest per frame | default for all static props |
| FramedBlocks / Domum skins | block entity holding camo, baked model | modest; rebuild on change | slopes, curved roofs, vaults |
| Block entities with special renderers (chests, signs, hanging signs, banners, beds, bells, decorated pots, heads, shulkers, conduit, enchanting table) | drawn every frame per instance | grows with count in view | sparingly; never as wall texture [V] https://mojira.dev/MC-271606 |
| Item frames (+custom_model_data items) | entity | per-frame entity render; maps are worst (MC-160583) | small props, shelves |
| Paintings (custom variants) | entity | cheap | posters, murals |
| Display entities (block/item/text) | entity with free transform (any rotation/scale) | per-frame entity render, also in shader shadow pass; set `width`/`height` (0 = never culled), small `view_range`, `shadow_radius` 0 | tilted debris, sagging cables, floating church parts, holo text [V elkonia; Axiom docs https://axiomdocs.moulberry.com/contextmenu/displayentities.html] |
- High entity counts are handled poorly; Sodium was measured slower than vanilla with ~1000 entities on 1.21.5, and
  servers with many display entities showed it (closed as external) [V] https://github.com/CaffeineMC/sodium/issues/3141 .
- Budget (estimate, benchmark in G6) [?]: ≤~150 display entities visible at once in combat areas, ≤~400 in quiet vistas;
  ≤~20 item frames and ≤~10 signs/banners per view; no maps-in-frames walls; prefer baking anything static into blocks.
- **BDEngine** (free web editor for display-entity models and animations, exports commands/datapacks; version "2027.1",
  2026-10-07, with Blockbench import guide) [V] https://bdengine.app/ , https://www.block-display.com/ . Fine for one-off
  set pieces (cables, tilted beams, a broken bell); convert recurring props into real block models instead.
- Player heads with custom textures are block entities with a renderer (MC-271606 list): avoid as "micro texture".
- Optimisers worth checking for 1.21.1 NeoForge in the render branch: Entity Culling (already in stack), block-entity
  render-distance limiters [?].

---------------------------------------------------------------------
## 5. Building tools and workflow

### 5.1 Axiom (Fabric only) [V]
- Axiom 6.1.3 has a Fabric 1.21.1 build (2026-09-25) — the 1.21.1 line is still updated [V Modrinth API]. ARR + EULA;
  commercial use needs a commercial licence (already noted in gameplay notes).
- Detail-relevant tools (third-party manual for 5.4.1, https://kokecacao.me/html/axiom-manual/ [C]): Painter (gradient
  mode), **Gradient Painter**, **Noise Painter** (simplex, splatter, Voronoi edges for cracks, Worley, metaball), Script
  brush (Lua), Sculpt draw / Weld / **Melt** / Roughen / Blend / **Shatter** (fractured shards), **Path tool with
  Catenary curves** (cables, sagging lines), **Stamp** (scatter saved blueprints = rubble/props), Text tool, colour picker +
  gradient helper, display-entity editor with culling fields.
- Builders use Axiom replace mode + colour picker/gradient helper for texturing (Speck) and 45° shear + mirror for
  cathedral apses (cathedral video) [C].
- Workflow for us: separate Fabric 1.21.1 + Axiom instance on a copy of the map region with vanilla blocks only; export
  `.bp`/`.schem`; import in NeoForge with WorldEdit; place modded blocks in NeoForge. Agents cannot drive Axiom's GUI, so
  Axiom is for the user's optional manual touch-ups [?].
- Arceon (Arcaniax): **paid, Patreon-gated FAWE plugin** (Bukkit/Paper) with erode-blend, boulder, vine, spike brushes;
  an "Arceon x Axiom" addon brings the boulder brush into Axiom (server needs Arceon ≥0.5.3) [V]
  https://arceon.gitbook.io/arceon-wiki . goBrush/goPaint (Arcaniax) also need FAWE [V Spigot]. None runs on NeoForge
  single player; only usable on a separate Paper server for vanilla-block terrain.
- "Goliath" brushes: no building tool by that name found [?]; maybe confused with goBrush/goPaint.

### 5.2 WorldEdit 7.3.8 (NeoForge 1.21.1, 2024-10-21) [V]
- Brushes: sphere, cylinder, set, clipboard, smooth, gravity, forest, extinguish, butcher, deform (expressions),
  raise, lower, biome; per-brush `/mask`, `/material`, `/size`, `/range`, `/tracemask` [V]
  https://worldedit.enginehub.org/en/latest/usage/tools/brushes/
- Masks: block/state masks, negation `!`, `#existing`, `#solid`, `>`/`<` offset (above/below), `~` adjacency,
  `#region`, `#clipboard`, `##tag`, **`%N` random noise**, `^[state]` [V]
  https://worldedit.enginehub.org/en/latest/usage/general/masks/
- Weighted random patterns (`//replace stone_bricks 60%stone_bricks,25%cracked_stone_bricks,15%mossy_stone_bricks`):
  weights, not exact shares [V masks page notes the difference]. Note: this is splatter, so use it only for low-value
  surfaces; real gradients come from scripts (§1.10) or hand passes.
- Useful decay combos [?]: `//replace "~air stone_bricks" 30%cracked_stone_bricks` (exposed faces only),
  `//overlay moss_carpet` with `%40` mask, gravity brush on rubble, `//deform` noise for organic edges.
- FAWE is Paper/Bukkit only (gameplay notes).

### 5.3 Litematica on NeoForge
- **Forgematica** 0.4.3+mc1.21.1 (2026-10-13), unofficial Litematica port, LGPL-3.0, needs MaLiLib-Forge [V Modrinth API,
  https://github.com/ThinkingStudios/Litematica-Forge]. Client-side: overlay a schematic as a guide, verify placement,
  material lists. Optional for the user.

### 5.4 Structure files (`.nbt`) for our pipeline
- Structure block UI saves at most 48³; mods raise it: Huge Structure Blocks (LGPL-3.0, up to 512, 1.21.1-1.1.6 NeoForge)
  [V Modrinth], Structure Expansion (Forge/NeoForge incl. 1.21.1) [V modpacks.ch]. Code-written templates are not limited
  by the UI, but keep pieces modest (e.g., ≤64³) for load and diff size [?].
- Converters: `.schem → .nbt` web tools (schematicraft.com, createmod.com/tools/convert/schem-to-nbt) and npm
  `@taku128/java-schematic` (MIT) [V existence]. Python: `nbtlib` (MIT), `nbt-structure-utils` (MIT), `mcschematic`
  (Apache-2.0, `.schem`), `litemapy` (GPL-3.0, `.litematic`), `mcblueprint` (MIT, new) [V PyPI]. Write DataVersion 3955.
- Generators should emit `.nbt` pieces + a placement function, matching docs/pipeline 5.5.

### 5.5 Other in-game tools (1.21.1 NeoForge) [V Modrinth API]
Effortless Building 4.2 (LGPL-3.0; mirror/array/radial placement), Building Wands (Apache-2.0), Jake's Build Tools
(trowel/chisel), Mech Trowel (random palette placement, ARR), Building Gadgets 2 (MIT, CurseForge; exact 1.21.1 build
not checked [?]). Debug stick (vanilla) for block-state tweaks like rotated levers/chains.

### 5.6 Schematic libraries and licences
- Planet Minecraft, minecraft-schematics.com, CreateMod.com, mc-mod.net host many sewer/slum/cathedral schematics
  (e.g., modular sewer, Fallout-style sewer block, white-quartz gothic cathedrals), but licences are per author and some
  are paid ("non-free") [V listing pages]. Planet Minecraft content is governed by its terms of use and each author.
- Recommendation [?]: do **not** import third-party schematics into the map (AGENTS.md: agents make the assets; licence
  risk). Use them only as visual references, like any reference image, and record the URL in the ticket.

---------------------------------------------------------------------
## 6. Gaps and open questions
- No hard numbers for display-entity counts vs FPS on 1.21.1 + Sodium 0.8 + Iris: measure in the benchmark arena (G6).
- Whether Complementary/Photon colour our modded lamp blocks without patching `block.properties` [?] (render branch).
- Yuushya Townscape with Sodium on NeoForge (needs Indium, a Fabric mod) [?].
- Create Deco licence conflict (MIT on Modrinth vs ARR on CurseForge): ask/confirm before relying on it.
- Building Gadgets 2 1.21.1 NeoForge build/version not verified.
- Reddit coverage limited this round: Arctic Shift returned timeouts/422 under load; only DetailCraft sewer threads and
  two slum threads were read (`social/rd_*.txt`).
