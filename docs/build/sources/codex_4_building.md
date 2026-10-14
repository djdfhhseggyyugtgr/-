# East Asian Minecraft building research and AI construction pipeline

Research date: 2026-10-13. Target: Minecraft Java **1.21.1 + NeoForge**, original soulslike adventure map; school milestone covers Sewer Town–Southwest and Outer-Wall Ruins–Slums. The later white/gold church is a kit-development target, not an expansion of the milestone.

## Evidence conventions and scope

- **[V]** Verified in a primary source: author documentation, actual release metadata/artifact, paper, official institution, or directly readable creator post. This verifies the stated feature or report, not that it has been independently reproduced here.
- **[C]** Community technique, aesthetic judgment, wiki interpretation, or creator showcase without independently inspected build data.
- **[?]** Unverified lead, inference, or an explicitly proposed design/engineering parameter. All dimensions, palette percentages, performance budgets and project-specific layouts below are proposals unless expressly attributed to a source.
- [V] Read `research/r2/CONTEXT.md` and the four existing documents named there. This report adds building research and concrete implementation choices; it does not re-investigate the approved combat/model/animation stack.
- [V] Used built-in web search, direct page opens, public Modrinth metadata and in-memory inspection of three official mod JARs. Raw release metadata, extracted asset-ID inventories and a source-discovery audit are in [codex_raw/building](codex_raw/building/). No game instance was launched; no compatibility or FPS result is claimed.
- [?] Bilibili direct opens returned HTTP 412 or inaccessible-page errors; its public metadata API also returned 412. **No Bilibili comments or full video transcript were retrieved.** Indexed descriptions are explicitly marked below. Search also returned substantial unrelated material; rejected matches are not evidence.
- [?] Coverage is strongest for Chinese creator descriptions/MC百科/Yuushya, Japanese creator blogs/academic papers/GDMC, and Korean DC Inside/MINECAP. Searches of NGA, Zhihu, Pixiv, Naver cafes, Arca Live and Ruliweb did not produce a directly inspectable, sufficiently specific building tutorial. Fanbox/X technical claims and MCBBS archived post contents are not asserted. A lack of retrievable results does not establish a lack of projects.

## 1. Conclusions for this map

[?] Build through **LLM-authored structured plans plus deterministic geometry**, with a small original component library. Require visual inspection and traversability checks separately. Adopt the best ideas from T2BM, Japanese preset/code generation, Luban and GDMC; do not expect a general survival bot to design a polished soulslike level. Supporting primary research is examined in §5.

[?] Keep ordinary blocks responsible for collision, large surfaces and occlusion. Use decorative mods for pipes, air conditioners, ventilation, selective stone patterns and church trim. Prototype **Yuushya Townscape + one of Chipped/Rechiseled** first; add FramedBlocks only for shapes that cannot be achieved cleanly with ordinary stairs/slabs. Prototype special props with Yuushya Modelling or LittleTiles separately. These are selection proposals; release availability is verified in §4.

[V] A particularly relevant existing implementation is **harrynull/mcbuild**: offline voxel generation, multi-view critique, schematic export, and a live **NeoForge 1.21.1** bridge. Its checked Gradle properties declare Minecraft 1.21.1 and NeoForge 21.1.235. This is a concrete prototype candidate, not proof of compatibility with our combat/shader stack. Sources: [repository](https://github.com/harrynull/mcbuild), [version properties](https://github.com/harrynull/mcbuild/blob/main/mod/gradle.properties).

## 2. East Asian source atlas: what can actually be learned

### 2.1 Chinese-language builders and libraries

**CN1 — 赵相机咔咔一顿拍: miniature Kowloon Walled City.**

[C] The indexed creator description calls this their most chaotic build and a miniature reconstruction of Kowloon. The profile describes the creator as a former urban planner and GNwork member. This is a useful reference for tightly packed, individually articulated buildings, rather than a reproducible material/dimension specification. The video is 5:32, dated 2024-08-03; these are indexed page metadata, not a watched-video claim. Source: [这就是玩MC的意义：用方块再现九龙城寨！](https://www.bilibili.com/video/BV1QJvQeyEef/).

[?] A related 4:33 tutorial, **教你建南美贫民窟——单个楼房最小的一集**, appears in indexed Bilibili listings under the same creator, dated 2024-09-29. The direct BV identifier was not resolved. Treat it as a follow-up lead, not verified instructions or a usable schematic license. Discovery URL: [indexed building-tutorial list](https://search.bilibili.com/all?keyword=MINECRAFT%E5%BB%BA%E7%AD%91%E6%95%99%E7%A8%8B).

**CN2 — Shylock_Crovoz / The World of Akra: megastructure reference.**

[C] The indexed description offers a public map, identifies an ArtStation floating-building inspiration, links Eclipse shader, and requests author/video attribution when using the map or presets. The upload is dated 2026-08-20. It is especially relevant to immense repeated structural masses, voids and industrial atmosphere; an exact block palette was not accessible. Sources: [creator video](https://www.bilibili.com/video/BV1yfbd63E9B/), [linked inspiration](https://www.artstation.com/artwork/ZaVDQX), [creator-linked map document](https://docs.qq.com/doc/DTGd1RmxFWHNLT1Zk).

[?] Use Akra as a reference for silhouette and scale relationships. A public download and attribution request do not establish permission to redistribute its geometry inside our adventure map.

**CN3 — AAD / 龙铭新学: Gothic facade interpretation.**

[C] The indexed description of **Minecraft团队讲解哥特建筑:巴黎圣母院（1）正脸的艺术** credits a collaboration between the AAD classical architecture society and 龙铭新学, with named writing/review/image contributors. This is a targeted Chinese Gothic-analysis lead; no full transcript or exact building recipe was retrieved. Source: [Bilibili video](https://www.bilibili.com/video/BV15i4y1u7Lo/).

**CN4 — 白小久: mundane infrastructure creates believable streets.**

[C] The creator's indexed 2018 description reports a hand-built Japanese residential town, modified cocricot textures, electrical poles/high-voltage wires and a sewer. It describes many camera takes and about 65 hours of building. These are creator-reported production observations, not benchmark data. Source: [仿佛置身于动漫场景（一）](https://www.bilibili.com/video/BV19p411d7RG/).

[?] Transfer the underlying principle: inhabited districts need utility networks and everyday objects, including behind buildings. Do not transfer old cocricot/1.12-era dependencies into the 1.21.1 runtime without version evidence.

**CN5 — Yuushya official ecosystem, found through MC百科.**

[V] The official Chinese site describes a mod/resource-pack building ecosystem, architectural decorations, and a modelling system for translating/rotating/combining block models, including models from other mods. MC百科 independently indexes Townscape and Modelling, with original MCBBS links. Sources: [official Townscape](https://yuushya.com/townscape/), [MC百科 Modelling](https://www.mcmod.cn/class/11555.html), [MC百科 Townscape history](https://www.mcmod.cn/class/diff/0-125750.html).

[V] The official workshop distributes **share codes containing layers and layer properties**, with distinct item-block and entity-block loading modes. Its submission guidance suggests combinations spanning about 2–3 blocks, preferably split vertically. This is a useful small-prop library pattern. Its reuse rules preserve creator rights and distinguish personal modifications, reposts and nonprofit code sharing. Source: [Chinese workshop and terms](https://yuushya.com/townscape/workshop.html).

[?] For our own library, create original multi-layer “utility cabinet,” “broken condenser,” “drain assembly” and “shrine terminal” presets. Preserve their share-code/NBT data as well as screenshots; a block ID alone cannot encode the assembled prop.

**CN6 — Chinese-speaking builder connecting infrastructure and science fiction.**

[C] An indexed Bahamut creator post, **各種風格/題材試蓋**, explicitly describes a sci-fi scene inspired by a Japanese giant underground flood-control chamber and another scene partly inspired by Control. This connects the sewer/megahall theme to East Asian builders' own references. Direct fetch returned 403, so specific blocks and dimensions remain unverified. Source: [creator post](https://forum.gamer.com.tw/Co.php?bsn=18673&sn=984618).

**CN7 — XeKr and 24K_SaltedFish: distinguish surface depth from scene depth.**

[C] XeKr's indexed author description identifies the third Minecraft/modern-architecture lecture as a practical explanation of layers. A Chinese community guide by 24K_SaltedFish separately organizes color/composition, irregular placement for paths/rocks/weathering, facade/roof layering, and spatial layering through small exterior/building components. It recommends starting with components within roughly a 10×10×10 volume rather than an enormous first build. Sources: [XeKr lecture](https://www.bilibili.com/video/BV13W411r7gW/), [community guide](https://www.bilibili.com/opus/466441436989264755).

[?] Transfer the separation of scales: facade depth belongs to the room module, while scene depth comes from foreground utilities, a readable midground route and a distant landmark. The guide's informal randomized-landscaping example is not our damage algorithm or an appropriate combat-path specification.

**CN8 — 启StCheese: original-vanilla Gothic construction tutorial.**

[C] The indexed 2021 creator description identifies a three-part Gothic church tutorial using vanilla textures and BSL, with parts approximately 24:36, 24:51 and 45:14. It is a better follow-up construction reference than a generic Gothic image search, but exact block quantities and the full procedure were not inspected. Source: [哥特式教堂建筑教程（重制）](https://www.bilibili.com/video/BV1hK4y1U7B5/).

### 2.2 Japanese builders: concrete techniques and level readability

**JP1 — WIEN: one-block facade depth.**

[V] WIEN's illustrated author article explicitly moves the wall **one block behind the columns**. The explanation is that column sides become available for decoration and previously excessive projections become balanced. The article also presents twin front towers for cathedral massing, L-shaped additions, and cruciform symmetry for an imposing effect. Source: [建築のすべてを教えます](https://note.com/wien_mcbuild/n/n84d4826d918e).

[C] Transfer this as a reliable starting technique, not a universal law that all walls need identical depth. Main columns, the wall plane, window glass and ornamental frames should remain visibly separate.

**JP2 — SOU: exact ruin palette and a version trap.**

[V] SOU's **16×16 small ruin** tutorial provides a material table: stone bricks, cracked/mossy stone bricks, stone-brick/mossy slabs and stairs, bricks; oak leaves, short grass, bush, lantern, campfire and barrel; dirt/cobblestone/mossy cobblestone on the floor. The creator asks reference users to credit the blog or linked social/video accounts. Source: [SOU tutorial and material list](https://minecraft-log.com/2902).

[?] **Do not blindly import its 2026 material list.** The generic “bush” is a later-version block if it means the newer bush item. Replace that slot in our 1.21.1 palette with `minecraft:dead_bush` or `minecraft:fern`, as visually appropriate. This replacement is ours, not SOU's original instruction.

**JP3 — curasunaya: a ruined temple city designed to suggest a playable level.**

[V] The creator explicitly cites Mario/Dark Souls-style stages, imagines strong enemies and a locked door opened from behind as a shortcut, and uses a great temple as a visible future destination. They also state that this is **not a finished adventure map**, interiors remain hollow, and a sewer is still an ambition. Source: [でっかい寺院のある街](https://note.com/nayakura/n/nc27a8c9dcb7e).

[?] Keep the landmark/shortcut technique, but do not cite this post as evidence that its sewer has been built. For our map, show the outer wall and a later church through selected vistas; blocked sightlines between vistas can limit rendering cost.

**JP4 — VIP de Minecraft 九龍城: additive connected settlement.**

[C] This Japanese community wiki describes an enormous connected slum built through individual additions and alterations. Builders extend corridors and attach rooms to the shared structure; separate disconnected buildings are discouraged, and hidden rooms/passages are welcomed. It expressly does not prioritize convenient transport. Source: [project wiki](https://w.atwiki.jp/vip_minecraft/pages/1.html).

[?] Use additive growth to avoid a tiled suburb appearance. Preserve a deliberately legible critical route for our soulslike: the project's unconstrained maze rule is an aesthetic reference, not suitable gameplay acceptance criteria.

**JP5 — Minecraft街発展にっき: industrial dressing with spatial logic.**

[V] The water-treatment build documents staged basins, a stepped divider, mixers assembled from walls/fences/trapdoors, gravel filtration supported by iron bars, a covered tank, a pump building, underground pipe work and a roofed reservoir with columns. The author identifies some buried layouts as imagined. This is a **waterworks** build, not a sewer engineering manual. Source: [浄水場を作る](https://www.machihatten.me/entry/c7wpplant).

[?] Reuse the staging logic: inlet → settling space → grate → pump → discharge. It creates meaningful reasons for chambers and side passages; not every pipe needs functional fluid simulation.

**JP6 — MLIT's actual Minecraft flood-control model.**

[V] Japan's Ministry of Land, Infrastructure, Transport and Tourism publishes import instructions for the Metropolitan Area Outer Underground Discharge Channel Minecraft world. The checked PDF names a **Bedrock `.mcworld`** package and provides its official download URL. This is credible large-scale infrastructure reference, but not a NeoForge schematic. Sources: [official instructions](https://www.ktr.mlit.go.jp/ktr_content/content/000912281.pdf), [official world archive](https://www.ktr.mlit.go.jp/ktr_content/content/000912119.zip).

[?] Study the underground chamber's structural rhythm and shaft-to-hall transitions; rebuild an original arrangement. Do not rename the Bedrock package to `.schem` or assume lossless Java conversion.

**JP7 — older ruin-video archive.**

[C] Nicozon indexes **Ruinscraft – 廃墟と暮らすマインクラフト**, including a 2012 first episode and later world-distribution links. It is a Japanese ruin-building lineage worth following, not verified modern-mod guidance. Sources: [indexed episode](https://www.nicozon.net/watch/sm17683648), [original Nicovideo URL](https://www.nicovideo.jp/watch/sm17683648).

### 2.3 Korean builders and architectural advice

**KR1 — DC Inside: cathedral/modern hybrid with interiors and night review.**

[V] A directly readable August 2026 builder post describes an original city hall combining medieval cathedral and modern design. It discusses the back facade, successive interior floors, an elevator-like central volume, a large hall with symbolic stained glass, and lighting added for night views. Some rooms are explicitly unfinished. Source: [새 도시청사가 완공되었음!](https://gall.dcinside.com/board/view/?id=minecraft&no=215454&page=1).

[C] This is a relevant Korean example of combining religious massing with modern infrastructure. Its red/white/yellow symbolism and Fire Force references are creator-specific; our flower/AI motifs should remain original. Neither exact block IDs nor measured facade depths are supplied.

**KR2 — MINECAP / jio0412: depth and inhabited surroundings.**

[C] The first Korean tutorial recommends planning style, size, blocks, interiors and surroundings, projecting a wall by one block, using stairs/slabs/trapdoors, breaking up broad glazing, and completing even small interiors. The second favors modest irregularity, mixed stone materials, columns, aged walls and environmental dressing. Sources: [건축 강좌 1편](https://minecap.co.kr/posts/3083), [건축 강좌 2편](https://minecap.co.kr/posts/3084).

[?] Apply these to the camp and slum housing: each small building needs a purpose and a furnished visible room. “Ruined” should not mean every structure is an empty shell.

**KR3 — Namu building-block behavior: aesthetics can change navigation.**

[C] The Korean building-block article discusses slab placement and cases where carpets/trapdoors on barriers change what players and mobs can traverse. These are community descriptions requiring a 1.21.1 collision/pathfinding test for our use. Source: [나무위키: 건축 블록](https://www.namu.moe/w/%EB%A7%88%EC%9D%B8%ED%81%AC%EB%9E%98%ED%94%84%ED%8A%B8/%EC%95%84%EC%9D%B4%ED%85%9C/%EA%B1%B4%EC%B6%95%20%EB%B8%94%EB%A1%9D).

[?] Include decorative trapdoors, fences, slabs and narrow stairs in route tests. A beautiful passage that the enemy AI cannot use is a failed encounter space.

## 3. Detailed original construction specifications

[?] **Everything in §3 is a proposed implementation**, synthesized for this map from the references above. It is not a claim that a named builder uses these exact IDs, dimensions or percentages. Vanilla IDs name intended 1.21.1 blocks; verify state/collision behavior against the actual server registry. Suggested proportions refer to eligible surface blocks, not entire map volumes.

[C] As a version sanity check, every explicitly namespaced vanilla ID in this report was matched against Misode's community-extracted **1.21.1** block table; none was absent. The checked table is saved in the raw evidence folder. This checks identifiers against a version-pinned dataset, not loaded modded collision or allowed-state combinations. Source: [1.21.1 block data](https://raw.githubusercontent.com/misode/mcmeta/1.21.1-summary/blocks/data.json).

### 3.1 Shared geometry and material rules

[?] Separate five systems: load-bearing frame; wall infill; openings; service network; damage/dressing. Generate them in that order so weathering does not randomly erase structure or navigation.

[?] Treat wall depth as a section, not extra random protrusions:

| Zone | Frame relative to nominal wall | Infill | Glass / recess | Detail |
|---|---:|---:|---:|---|
| Sewer | +1 block | 0, backed by another structural block | −1 where space permits | pipes above/beside paths |
| Slum | +1 on supports | 0 | −1 | thin shutters, awnings, external stairs |
| Megastructure | +2 to +4 on major ribs | 0 | −1 to −2 service channels | subordinate braces, ladders, panels |
| Church | +1 to +3 buttresses | 0 | −1 to −2 | contrasting thin gold trim |

[?] Avoid palette noise: reserve a dominant material for large quiet surfaces; cluster secondary materials around joints, exposure and repair seams. Start with no shader, then inspect with the intended shader. A scene that is legible only under cinematic exposure is not ready for combat.

[?] Establish three scales of detail: silhouette at 30–100 blocks; bays/rooms at 5–16 blocks; trims/junctions at 0.25–2 blocks where available. Decorate according to viewing distance. Detail hidden in unreachable rear walls should serve silhouette or shadow rather than consume a dense prop budget.

### 3.2 Sewer Town: 下水道 / 下水 / 하수도

**Proposed vanilla palette.**

| Function | Full block IDs | Starting share / use |
|---|---|---|
| Structural masonry | `minecraft:stone_bricks`, `minecraft:stone`, `minecraft:andesite` | 55%, 20%, 10% of masonry |
| Damage | `minecraft:cracked_stone_bricks` | 10%, clustered at leaks and failed joints |
| Damp growth | `minecraft:mossy_stone_bricks`, `minecraft:mossy_cobblestone` | combined 5%, near wet/shaded surfaces |
| Vaults / ledges | `minecraft:stone_brick_stairs`, `minecraft:stone_brick_slab`, `minecraft:stone_brick_wall` | shaped components, outside share calculation |
| Drain sediment | `minecraft:mud`, `minecraft:packed_mud`, `minecraft:brown_terracotta`, `minecraft:gray_terracotta` | bounded deposits and waterline bands |
| Metalwork | `minecraft:iron_bars`, `minecraft:iron_trapdoor`, `minecraft:chain`, `minecraft:polished_basalt` | grates, access covers, cables and thick pipes |
| Copper accents | `minecraft:cut_copper`, `minecraft:exposed_cut_copper`, `minecraft:weathered_cut_copper`, `minecraft:oxidized_cut_copper` | coherent corrosion progression |
| Light / clutter | `minecraft:lantern`, `minecraft:soul_lantern`, `minecraft:barrel`, `minecraft:cobweb` | control lantern density; webs outside fights |

[?] Where copper color must remain fixed, choose the corresponding `minecraft:waxed_*` block. Waxed variants of the cut-copper IDs above are `waxed_cut_copper`, `waxed_exposed_cut_copper`, `waxed_weathered_cut_copper` and `waxed_oxidized_cut_copper`, all in the `minecraft` namespace.

**A reproducible tunnel module.**

[?] Begin with an **8-block-long bay**, 15 blocks across including the backing walls. Local X=0–14. Walls occupy X=0–1 and X=13–14. Left walkway X=2–4, central channel X=5–9, right walkway X=10–12. Channel bottom Y=0; water occupies Y=1; solid walkway tops sit at Y=3 if their blocks occupy Y=2. Specify walking elevations consistently in generator metadata.

[?] Shape the inner vault with a symmetric ceiling profile: about 6 blocks above the walkway near the edges and 9–10 in the center. Build one stepped arch slice from full blocks/stairs/slabs, then repeat it. Make the rib bay boundary distinguishable with one deeper ring, while preserving the declared walkway clearance. Put pipes in wall recesses or overhead, not at ankle/head level on the route.

[?] Use this module for traversal; widen into **25×25 or larger provisional pump halls** for combat. Actual arena size must come from Epic Fight weapon reach, enemy count and camera tests. Connect dry ledges to stairs or ramps; label water as scenic, traversable or hazardous in the level contract.

**Greebling with a plausible service network.**

[?] Generate a pipe graph with explicit source, junction, valve, outlet and maintenance access nodes. Give one main pipe a thick silhouette; subordinate narrow pipes follow the same wall or ceiling. Every turn gets a consistent elbow. Breaks should reveal a recognizable severed connection instead of randomly stopping a pipe in empty space.

[?] Vanilla approximation: full basalt/metal-like blocks for a main trunk; stairs at corners; iron trapdoors as flange plates; walls/iron bars/chain for thinner runs; stone buttons or levers as fasteners/controls. Thin diagonal hoses need a custom prop or modelling system. Do not invent vanilla copper-pipe IDs.

[?] Use visible but nonfunctional pump shells, settling tanks and dry service balconies following JP5's staged-waterworks logic. Let the progression route cross the same main channel more than once at different heights, then unlock a maintenance gate back to the checkpoint.

**Decay and storytelling.**

[?] Use water-height and leak masks: a continuous waterline band, concentrated moss below drips, cracks around pipe fixings, debris at corners where flow would collect it. Keep intact masonry between damaged areas. Give a collapsed vault a matching rubble mound beneath it, and preserve an alternate route.

[?] Reserve warm lights and maintained equipment for the camp/maintenance refuge; colder sparse lights for abandoned branches. A blanket of blue lights makes every passage equally important. Place a distinctive pump silhouette or tall shaft where it can reappear after a loop.

### 3.3 Outer-Wall Ruins–Slums: 贫民窟 / スラム / 빈민가

**Proposed vanilla palette.**

| Function | Full block IDs | Placement rule |
|---|---|---|
| Aged concrete | `minecraft:light_gray_concrete`, `minecraft:gray_concrete`, `minecraft:andesite`, `minecraft:tuff` | contiguous walls, patch strips, foundations |
| Warm infill | `minecraft:bricks`, `minecraft:terracotta`, `minecraft:brown_terracotta`, `minecraft:orange_terracotta` | one warm family per dwelling |
| Improvised boards | `minecraft:spruce_planks`, `minecraft:dark_oak_planks`, `minecraft:stripped_spruce_log` | floors, doorframes, repairs |
| Sheet-metal stand-ins | `minecraft:cut_copper`, `minecraft:exposed_cut_copper`, `minecraft:iron_trapdoor` | small roof sections, not every surface |
| Window / shutter | `minecraft:gray_stained_glass_pane`, `minecraft:spruce_trapdoor`, `minecraft:dark_oak_trapdoor` | glass recessed behind supports |
| Occupancy | `minecraft:barrel`, `minecraft:composter`, `minecraft:flower_pot`, `minecraft:lantern`, `minecraft:white_carpet`, `minecraft:brown_carpet` | deliberate domestic clusters |
| Ground | `minecraft:coarse_dirt`, `minecraft:gravel`, `minecraft:packed_mud`, `minecraft:cobblestone` | footsteps and drainage explain mixing |

[?] Give a building approximately 65–75% one neutral wall material, 15–25% warm/repair material, and the remainder dark utility accents. Across the district, vary the warm material by household, while maintaining a common neutral frame. “Poverty” should read through repair and constrained space, not uniformly ugly or dehumanizing dressing.

**Room and street kit.**

[?] Start with 7×9 external footprints and 5-block storey increments, allowing a small useful interior after wall thickness. Create mirror/rotation variants, offset upper floors by one block on selected buildings, and attach rooftop sheds or external stairs. Do not repeat every upper-floor offset in the same direction.

[?] Prototype main alleys at **5 blocks clear**, wider at encounters and corners; side exploration passages may be narrower after testing. Awnings/balconies must leave enough headroom and camera space. A clear block count is only an initial screening measure: final acceptance uses actual collision shapes and the combat camera.

[?] Follow the Kowloon/VIP additive principle visually: connect roof bridges, corridors and small annexes to a shared mass. Underneath, maintain a route graph with a checkpoint, two or more recognizable loops, an optional branch and a shortcut opened from the far side. Protect that graph while decorative buildings grow around it.

**External utilities and occupancy.**

[?] Make electrical boxes, condensers, ventilators and drains belong to buildings: a pipe reaches a drain, an air conditioner faces an open court, and external stairs reach a usable landing. Use Yuushya props identified in §4 for close views. For skyline-only housing, model these details with simple block clusters.

[?] Furnish at least the visible rooms: cooking/eating, sleeping, repair and storage. Cluster supplies near the inhabitants' work. A safe camp needs recognizable maintained paths, shared water and modest planting; abandoned rooms can show partial removal or salvage.

[?] Break a roof at a few coherent locations; reinforce surviving edges with planks or braces; place fallen material below. Keep damage out of the main fighting floor. Use vertical soot stains beneath chimneys and runoff beneath failed gutters. Scatter trash according to access and corners, not equal probability everywhere.

### 3.4 Ruined megastructures: 废墟 巨构 / 巨大廃墟 / 거대 폐허

**Proposed vanilla palette.**

| System | Full block IDs | Visual role |
|---|---|---|
| Primary frame | `minecraft:deepslate_tiles`, `minecraft:polished_deepslate`, `minecraft:gray_concrete` | heavy ribs and buttresses |
| Light cladding | `minecraft:light_gray_concrete`, `minecraft:smooth_stone`, `minecraft:polished_andesite` | quiet large planes |
| Damage | `minecraft:cracked_deepslate_tiles`, `minecraft:cracked_deepslate_bricks`, `minecraft:tuff` | failed panels and rubble |
| Industrial dark | `minecraft:black_concrete`, `minecraft:polished_blackstone`, `minecraft:polished_basalt` | shafts, machinery and cavities |
| Frame details | `minecraft:deepslate_tile_stairs`, `minecraft:deepslate_tile_slab`, `minecraft:deepslate_brick_wall`, `minecraft:iron_bars` | coherent trusses and railings |
| Warning marks | `minecraft:yellow_concrete`, `minecraft:black_concrete` | sparse meaningful hazard bands |

[?] Use a hierarchy: an 8- or 16-block structural bay, several bays per chamber, and one dominant shaft/bridge/frame visible across the zone. Make catwalks, pipes and doors smaller subordinate elements. “Mega” is conveyed by repetition and human-scale markers, not exclusively by extreme dimensions.

[?] Keep major ribs 3–5 blocks thick provisionally; recess infill panels 1–2 blocks behind them. Embed service galleries rather than attaching detail to every panel. Use different spacing for primary supports and secondary braces so the result does not look like one uniform lattice.

[?] Generate an intact construction graph first. Select a few destruction events: blast breach, shear failure, roof fall, flooded lower floor. Each event affects connected geometry, creates matching debris, and exposes interior framing. Preserve enough intact neighboring bays for the original structure to remain intelligible.

[?] Use a spatially correlated damage field and an exposure mask, not independent random block removal. Remove larger pieces along a failure plane, then erode its edges with slabs/stairs/cracked variants. Debris must have contact/support; floating debris needs an explicit fictional levitation device or field.

[?] Place large opaque geometry between playable spaces. Skyline shells need no furnished rooms, but near-player sections require enough interior thickness to avoid seeing through the backdrop. The target RTX 4060 and CPU need an actual shader benchmark; neither Akra's showcase nor a screenshot predicts our FPS.

### 3.5 White/gold science-fiction Gothic churches: 科幻 哥特 教堂

**Proposed vanilla palette.**

| Role | Full block IDs | Starting distribution |
|---|---|---|
| White ceramic shell | `minecraft:smooth_quartz`, `minecraft:white_concrete`, `minecraft:quartz_bricks` | 70–80% of visible architectural surfaces |
| Sculpted white ribs | `minecraft:quartz_pillar`, `minecraft:quartz_stairs`, `minecraft:quartz_slab`, `minecraft:smooth_quartz_stairs`, `minecraft:smooth_quartz_slab` | structural articulation |
| Weathered white | `minecraft:calcite`, `minecraft:polished_diorite`, `minecraft:diorite` | selective repair and base damage |
| Gold / aged warm accents | `minecraft:gold_block`, `minecraft:raw_gold_block`, `minecraft:yellow_terracotta`, `minecraft:yellow_concrete` | 5–10%, concentrated at ribs and focal nodes |
| Dark seams | `minecraft:black_concrete`, `minecraft:polished_blackstone`, `minecraft:gray_stained_glass` | 10–15% cavities and technological joints |
| Colored light | `minecraft:sea_lantern`, `minecraft:white_stained_glass`, `minecraft:light_blue_stained_glass_pane` | small, deliberate luminous areas |

[?] Do not create a fictitious vanilla `gold_stairs` or `white_concrete_stairs` entry. Use verified Rechiseled variants for narrow gold stairs/slabs (§4), FramedBlocks with stored camouflage data, or original custom-model trim.

**Massing and depth.**

[?] Prototype a nave around 17 blocks wide and 35 long, with roughly 20–24 blocks of interior height. Use two distinct facade towers, repeated pointed side bays, a crossing/transept, and a rear apse. These are provisional kit dimensions, not copied church plans. Grow a smaller sample before committing to the full later-game church.

[?] Build an odd-width pointed-arch profile once, verify its apex and symmetry, and instantiate it at 5- or 7-block bay intervals. White outer ribs stay forward; window panels sit one or two blocks behind; gold traces follow rib edges. Buttresses must meet a visible load path and project beyond the wall plane. WIEN's one-block recess is the starting reference, not the whole facade.

[?] Use the rose-window position for an original flower/circuit symbol. Split stained-glass/terminal glazing into a disciplined repeating pattern. Keep the entrance, altar/data core and upper gallery distinguishable from subordinate windows.

**Science fiction through construction logic.**

[?] Give each Gothic feature a technological equivalent: buttress → articulated external support; rib vault → energy-routing spine; rose window → data lens; altar → original AI interface; clerestory → tall emissive light channel. Add restrained panel seams and access hatches to the white surfaces. Large exposed cables should connect these systems visibly.

[?] Weather this district differently from the sewer: hairline cracks, fractured ceramic panels, soot near machinery, tarnished warm trim and sparse dead planting. Preserve large white planes and a clean sanctuary silhouette. Applying the sewer's moss/noise distribution everywhere would erase faction identity.

[?] Review day/night and shader-off views, following the Korean hybrid's attention to back facades/interiors/night lighting. Check gold for blown highlights and white for washed-out enemy silhouettes. Bloom is an accent, not the main way of distinguishing the critical path.

### 3.6 A reusable decay operator

[?] Recommended pseudocode semantics, not a tested implementation:

```text
intact = generate(frame, infill, openings, service_graph)
protected = navigation_volume + spawn_volume + shortcut_mechanisms
events = sample_failure_events(seed, authored_event_regions)
damage = correlated_field(events) * exposure_mask(intact)
damage[protected] = 0

apply_coherent_removal(damage, whitelist_of_damageable_components)
add_rubble_below_matching_failed_components()
replace_edge_blocks_with_valid_stairs_slabs_cracked_variants()
add_waterline_stains_and_leak_growth()
add_salvage_and_habitation_clusters()
validate_supports_routes_states_and_bounds()
```

[?] Record separate seeds for geometry, damage and decoration. A correction to damage should not rebuild the room layout. Pair geometry removal and rubble creation by event ID, allowing the reviewer to identify inconsistent collapsed features.

## 4. Decoration/building mods: exact 1.21.1 NeoForge evidence

### 4.1 Verified release shortlist

[V] The following releases were verified by **jointly filtering** the public Modrinth version API for `game_versions=["1.21.1"]` and `loaders=["neoforge"]`; Zcraft was checked on its exact CurseForge file page. A project's generic loader/version badges alone were not used. Metadata is saved under `codex_raw/building/*_neoforge_1211.json`.

| Mod | Verified compatible release candidate | Dependencies / evidence | Proposed role [?] |
|---|---|---|---|
| Chipped | 4.0.2; `chipped-neoforge-1.21.1-4.0.2.jar` | Athena + Resourceful Lib; [release](https://modrinth.com/mod/chipped/version/eqVowbGc) | cracked masonry, concrete panels, rails, selective church carving |
| Rechiseled | 1.2.6-neoforge-mc1.21; metadata also includes 1.21.1 | SuperMartijn642 Core Lib + Config Lib + Fusion; [release](https://modrinth.com/mod/rechiseled/version/6muGRqvu) | coherent metal/quartz variants, gold stairs/slabs |
| FramedBlocks | 10.6.3; `FramedBlocks-10.6.3.jar` | no required dependencies listed in this version's API record; [release](https://modrinth.com/mod/framedblocks/version/5g0Yxvfb) | select sloped/partial facade shapes |
| Yuushya Townscape | 2.3.0; `yuushya-1.21.0-neoforge-2.3.0.jar` | Architectury API; [release](https://modrinth.com/mod/yuushya-townscape/version/L2HpYsbq) | sewer/slum close-up utility props |
| Yuushya Modelling | 2.4.1; `yuushya_modelling-1.21.1-2.4.1.jar` | project description says Architectury required although version record lists none; [release](https://modrinth.com/mod/yuushya-modelling/version/BEzfp616) | original transformed/assembled hero props |
| LittleTiles | 1.6.0-pre234 beta, 1.21.1 | CreativeCore; [release](https://modrinth.com/mod/littletiles/version/GO0Nhohq) | experimental fine-detail kit, limited use |
| Zcraft Decoration | 1.0.0; `Zcraft_Decorations-1.21.1-1.0.0.jar` | exact file declares NeoForge + 1.21.1; [file](https://www.curseforge.com/minecraft/mc-mods/zcraft-decoration/files/8085772) | abandoned/post-apocalyptic props |

[V] Zcraft's author describes abandoned/post-apocalyptic props and simple block-based models with detailed textures. This is a closer thematic fit than a generic furniture pack. Source: [author project page](https://www.curseforge.com/minecraft/mc-mods/zcraft-decoration).

[?] Resolve the Yuushya Modelling dependency discrepancy during instance assembly; do not treat the empty version dependency array as proof that Architectury is unnecessary. Its current description and old MC百科 notes also discuss Indium; those are not instructions to install a Fabric Indium jar in NeoForge.

[V] Chipped's author description emphasizes decorative and connected-texture variants. Rechiseled provides variant exchange and shaped stairs/slabs; FramedBlocks provides shapes with camouflage materials. Sources: [Chipped](https://modrinth.com/mod/chipped), [Rechiseled](https://modrinth.com/mod/rechiseled), [FramedBlocks](https://modrinth.com/mod/framedblocks).

[?] Do not adopt all three huge material systems initially. Pick a short district palette and freeze it. More block choices do not automatically improve coherence, and performance costs differ by model, connected-texture system and use.

### 4.2 Exact modded IDs checked in release artifacts

[V] Downloaded the author-hosted artifacts referenced by the release API into memory and enumerated `assets/<namespace>/blockstates/*.json`. The following **asset identifiers exist in those exact JARs**. Full lists and artifact URLs/hashes are stored in `chipped_block_ids.json`, `rechiseled_block_ids.json` and `yuushya-townscape_block_ids.json`. This is asset-level verification; runtime registry/state/collision validation remains [?].

| Kit | Checked IDs | Intended use [?] |
|---|---|---|
| Sewer/slum services | `yuushya:pipe_horizontal`, `yuushya:pipe_vertical`, `yuushya:pipe_hub`, `yuushya:mounted_pipe_horizontal`, `yuushya:mounted_pipe_vertical` | exposed pipe routes |
| Sewer elbows | `yuushya:pipe_corner_bottom_left`, `yuushya:pipe_corner_bottom_right`, `yuushya:pipe_corner_top_left`, `yuushya:pipe_corner_top_right` | consistent bends after orientation tests |
| Drainage | `yuushya:drain`, `yuushya:drainage_channel` | grates/curb drains |
| Slum utilities | `yuushya:air_conditioning_condenser`, `yuushya:rusty_air_conditioning_condenser`, `yuushya:rusty_ventilator`, `yuushya:ventilator` | old/maintained service contrast |
| Industrial skin | `chipped:bolted_gray_concrete`, `chipped:gray_concrete_panel`, `chipped:grill_gray_concrete`, `chipped:barbed_iron_bars` | selective machinery/panel detail |
| White technical shell | `chipped:bolted_white_concrete`, `chipped:reinforced_white_concrete`, `chipped:rusted_white_concrete` | white panels and controlled aging |
| Damaged church stone | `chipped:cracked_quartz_block_bricks`, `chipped:cracked_flat_quartz_block_tiles` | localized structural wear |
| Gold trim | `rechiseled:gold_block_beams`, `rechiseled:gold_block_beams_stairs`, `rechiseled:gold_block_beams_slab` | narrow gold banding |
| White trim | `rechiseled:quartz_block_bordered`, `rechiseled:quartz_block_bordered_stairs`, `rechiseled:quartz_block_bordered_slab` | consistent framed openings |
| Metal panel | `rechiseled:iron_block_bordered`, `rechiseled:iron_block_bordered_slab` | machine casings and maintenance platforms |

[V] Artifact versions are [Chipped 4.0.2](https://modrinth.com/mod/chipped/version/eqVowbGc), [Rechiseled 1.2.6](https://modrinth.com/mod/rechiseled/version/6muGRqvu), [Townscape 2.3.0](https://modrinth.com/mod/yuushya-townscape/version/L2HpYsbq).

[?] Export the installed registry and allowed properties before generating coordinates. Asset filenames provide an excellent allowlist seed but are not a substitute for an authoritative loaded registry. Do not infer elbow facing, shape or light behavior solely from English ID names.

### 4.3 Shape/NBT and performance concerns that affect the pipeline

[V] Yuushya Modelling creates transformed/combined models; the workshop share-code format includes layer properties. LittleTiles provides small tiles and assembled furniture/doors rather than merely new full cubes. Sources: [Yuushya Modelling](https://modrinth.com/mod/yuushya-modelling), [LittleTiles](https://modrinth.com/mod/littletiles), [Yuushya workshop](https://yuushya.com/townscape/workshop.html).

[?] For transformed or camouflaged props, store the **complete block-entity payload** and verify round-trip placement. A schematic containing only the carrier block may lose the intended appearance. Use solid collision proxies for combat architecture, and compare the rendered object against the proxy.

[?] Prefer ordinary opaque block models for repeated sewer ribs and skyline modules. Restrict tile/model composites, glass layers and animated props to where they materially improve the camera view. Profile a representative decorated room before distributing the technique across the map.

[?] Build a compatibility coupon containing each shortlisted block, representative states, transformed props, lights and cutout/translucent surfaces. Test Sodium/Iris and all intended shaders, reload the save, and export/import it. Release metadata establishes availability, not compatibility.

## 5. AI-driven building research and community projects

### 5.1 Chinese research: T2BM, SUSTech, IEEE CoG 2024

[V] Hu, Huang, Hu and Liu's **3D Building Generation in Minecraft via Large Language Models** is from Southern University of Science and Technology, Shenzhen. T2BM refines a brief, emits a structured intermediary with geometry/material/state fields, repairs naming/property errors, then places through GDPC. Its prompt context is Minecraft **1.19.2 Forge**, not our target. It evaluates connected structural completeness and requested-material presence. With 50 runs per setting, GPT-4's fraction satisfying both checks rises from **0.12 to 0.38** with refined prompts; completeness alone rises from 0.80 to 0.82. These checks do not measure art direction or combat quality. Source: [paper, especially II–III and Table I](https://arxiv.org/html/2406.08751v1).

[V] The linked public repository currently presents README and supplementary material, not a complete runnable generator implementation. Do not schedule its installation as though the full code were available. Source: [authors' supplement repository](https://github.com/SUSTechGameAI/Text-to-Building-in-Minecraft).

[?] Transfer its compact component representation and measured insistence on validation. Replace “invalid material → oak planks” repair with a hard error or explicit reviewed substitution for our palette; silent wood substitution would damage a concrete/gold district.

### 5.2 Chinese research: Luban, 2024

[V] Luban is a USTC/Chinese Academy of Sciences-led creative-building agent. It first generates decomposed CAD-style structural programs and visually checks them, then constructs in the environment and generates functional verification actions. Its Minecraft benchmark contains five creative tasks. Evaluation uses human studies and Elo-style comparison of appearance and pragmatism. Examples include climbable stairs, a bridge, a two-storey house and a tower with a ladder. The project's landing page still labels code as **“Coming Soon”**; paper/procedure availability should not be confused with a supported production package. Sources: [project](https://luban-paper.github.io/), [paper](https://arxiv.org/html/2405.15414v1).

[?] The important transfer is **appearance + actual use**. A “bridge” must support crossing and a shortcut must work under the relevant game state. Five benchmark tasks are not evidence of complete automatic soulslike-map production.

### 5.3 Chinese research: redstone city generation, SUSTech/NYU, 2023

[V] Huang et al. submitted a procedural redstone-style city generator to GDMC 2023. It separates terrain preparation, layout, A* route planning, light placement and perimeter work. It compares heuristic/evolving/random layouts, with stronger heuristic speed on flat areas and better evolutionary behavior on rugged areas. Its user study has **six participants**, each viewing the generated cities in first person and judging GDMC's four dimensions. The paper reports weak narrative despite functional redstone systems, partly because the systems were hidden from visitors. Source: [paper](https://arxiv.org/html/2307.09777v1).

[?] Transfer collision-aware placement and explicit road graphs. For a damaged city, preserve vertical terrain and route intentions; do not flatten the whole build area. Visible cause-and-effect storytelling matters more than hidden technical complexity.

### 5.4 Japanese-language academic research: presets → source code → GDPC

[V] At IEICE's 2025 General Conference, poster **TPO-1-107**, ZHAO SHUANG and THAWONMAS Ruck describe a multimodal building-generation system inspired by T2BM. The accessible Japanese abstract specifies three in-context preset types: material-name mapping, expansion rules and output/code format. Inputs can be short text or diagrams. The workflow expands the description, translates it into source code using an actual-code preset, then generates through GDPC. Source: [official abstract, published 2025-03-17, presentation 2025-03-25](https://www.ieice.org/publications/conferences/summary.php?ConfCd=2025G&conf_type=G&expandable=0&id=CONF0000150607&lecture_number=TPO-1-107&session_num=TPO-1&year=2025).

[?] Only the abstract was readable; the full PDF is pay-per-view. No quantitative aesthetic success rate, model-specific robustness, public code release or 1.21.1 support was verified. This is a particularly good rationale for supplying our agents with a real palette dictionary and worked component-code examples.

### 5.5 Japan-based GDMC teams: procedural agents are not necessarily LLMs

[V] Tsukuba's official Japanese announcement confirms a university team won GDMC in 2021 under Claus Aranha's supervision. The named students were visiting students; “Japan-based team” is more accurate than assuming their nationality. Source: [Tsukuba university announcement](https://www.coins.tsukuba.ac.jp/2021/210816.php).

[V] The 2025 Tsukuba team's public repository instead implements needs-based multi-agent settlement simulation: agents explore, build houses and form relationships; a central firecamp supplies the settlement focus. README requirements use Python 3.10+ and Minecraft **1.21.4**. Sources: [2025 repository](https://github.com/Xabi08YT/GDMC2025-MX), [official competition results](https://gendesignmc.wikidot.com/wiki:2025-settlement-generation-competition).

[V] GDMC's 2025 table lists Tsukuba at **3.69 final score**, versus **5.95** for first-place Gaussianly Filtered. Tsukuba's 2021 win should not be conflated with a 2025 win. GDMC judges adaptation, embodied functionality, narrative and aesthetics through human inspection. Source: [official results/evaluation context](https://gendesignmc.wikidot.com/wiki:2025-settlement-generation-competition).

[?] A needs-driven settlement is useful for organic habitation: a household needs access, shelter, work and storage. Constrain its decorative growth around our fixed encounter/shortcut graph. It is not evidence that autonomous agents should decide boss progression.

### 5.6 Japanese education research: an especially relevant school-project precedent

[V] A DiGRA Japan paper reports Minecraft/AI workshops for students aged 13+ in 2023 and 2024, with **18 total participants**. Participants use Copilot for concept images and Python building code, then compare intentions and results and present benefits/limitations. The implementation uses **Minecraft Java 1.12.1 + Forge + RaspberryJamMod**. Its evaluation concerns students' experience of AI assistance, not expert architectural quality. Source: [DiGRA Japan proceedings paper, p.115 onward](https://www.jstage.jst.go.jp/article/digrajproc/15/0/15_115/_pdf/-char/ja).

[?] Preserve generated plans, failed outputs, revisions and playtest evidence as the school deliverable. Do not adopt its old runtime. Our milestone should demonstrate an inspectable iterative process as well as a playable result.

### 5.7 Chinese community project: MoLing-Minecraft

[C] A Bilibili demonstration dated 2025-04-13 links **gojue/moling-minecraft** and describes LLM/MCP-driven building. This is indexed creator-description evidence; the video/comments were not inspected. Source: [让AI大模型来玩《我的世界》，造建筑](https://www.bilibili.com/video/BV1KzdkYkEJx/).

[V] The repository documents an MCP server, construction/control functions, a coordinate-based tower brief and an Apache-2.0 license. The demonstrated installation starts a Java server and configures an MCP client. The checked README does not establish NeoForge 1.21.1 support or measured output quality. Source: [project repository](https://github.com/gojue/moling-minecraft).

[?] Useful as a transport/prompt example. A two-minute building demonstration is not evidence that its output meets our navigation, visual and shader gates.

### 5.8 Japanese community explanations: MinePal and AI-assisted server experiments

[V] Sonoisa's Japanese Qiita article explains **MinePal** through planning/action/perception and fast reactions versus deliberation. It describes interactions, memory and changing goals; its example is largely survival/social behavior. This is an author-written architecture explanation, not a high-quality cathedral generator benchmark. Source: [Japanese article](https://qiita.com/sonoisa/items/675e349a7feb762a0d99).

[?] Keep this distinction in searches: “AI plays Minecraft” often means gathering/fighting, not structure generation. Only promote a project to our build pipeline after it can export geometry/state data and accept visual/functional feedback.

### 5.9 An implementable community prototype: mcbuild

[V] The author README documents a sandboxed Python blueprint DSL, sparse voxels, rendered multiview contact sheets, iterative vision-model critique, region edits, block queries and WorldEdit-ready `.schem` output. It also provides a NeoForge 1.21.1 WebSocket bridge. Limitations include simplified rendering for unsupported block types, no cross-run memory, and a local/trusted single-build live mode. Code is MIT except separately identified bundled Minecraft assets. The README says acceptance-checklist gating is still future work. Source: [mcbuild](https://github.com/harrynull/mcbuild).

[?] Best immediate experiment: offline generation of **one original sewer bay**, followed by export into a copied 1.21.1 NeoForge test world. Do not run its unconstrained live iterations over the final map. Add our palette allowlist, component library, collision tests, frozen-region policy and independent reviewer.

[?] The repository owner's name alone is not proof of national affiliation; this English technical source is included for its exceptionally close target-version match, not presented as Chinese-language research.

### 5.10 Additional lead: Build-For-Me

[V] NightEpiphany/Build-For-Me provides a Minecraft LLM building-assistant README and `/auto-build <from> <to> <building-request>` followed by confirmation. This demonstrates bounded-blueprint requests. No working NeoForge 1.21.1 release or quality evaluation was verified. Source: [repository](https://github.com/NightEpiphany/Build-For-Me).

[?] Prefer mcbuild's documented artifact/review loop for the prototype. Keep Build-For-Me as a secondary design reference until version and implementation checks are complete.

## 6. Placement, projections, schematic libraries and Python NBT

### 6.1 Tool/version matrix

| Tool | Verified feature [V] | Boundary / selection [?] |
|---|---|---|
| WorldEdit | 7.3.8 release metadata supports 1.21 and 1.21.1 with NeoForge; clipboard documentation covers schematic save/load and paste | use the matching release; validate origin, rotation, entities and air policy |
| Litematica | author describes a client-side schematic tool with creative paste/clone/fill functions; current official 1.21.1 NeoForge filter returned no release | use in separate Fabric tooling only when appropriate; do not call it a NeoForge jar |
| Forgematica | unofficial (Neo)Forge Litematica port; 0.4.2+mc1.21.1 and 0.4.3+mc1.21.1 metadata match NeoForge; requires MaFgLib | suitable projection/review tool; 0.4.3 was published on research day, so prefer testing a pinned version before upgrade |
| GDPC | Python client for GDMC HTTP with buffered placement and geometry helpers | library is not the server mod and does not establish server-version compatibility |
| GDMC HTTP | documented release table covers 1.19.2, 1.20.2, 1.21.4 and 1.21.11; current 1.21.1 NeoForge API filter returned **zero releases** | use an isolated supported generation environment and export, or port a bridge; do not advertise drop-in 1.21.1 support |
| nbtlib | Python NBT reading/writing, compressed data, typed tags and schemas | NBT serializer, not a complete world editor or automatic format converter |
| Litemapy | reads/writes `.litematic`, regions and basic metadata; entities/tile entities/pending updates only partly supported | useful vanilla kit/projection exchange; validate complex modded payloads |

[V] Sources: [WorldEdit 7.3.8](https://modrinth.com/mod/worldedit/version/WTAFvuRx), [clipboard guide](https://worldedit.enginehub.org/en/latest/usage/clipboard/), [Litematica](https://github.com/maruohon/litematica), [Forgematica](https://modrinth.com/mod/forgematica), [0.4.2](https://modrinth.com/mod/forgematica/version/71jxaAwz), [GDPC](https://github.com/avdstaaij/gdpc), [GDMC HTTP](https://github.com/Niels-NTG/gdmc_http_interface), [nbtlib](https://github.com/vberlier/nbtlib), [Litemapy](https://github.com/SmylerMC/litemapy).

[V] Forgematica's description warns that schematic rendering with shaders depends on Minecraft version and shader pack; its explicit 1.21.3+ warning is not a claim of guaranteed trouble on 1.21.1. Source: [author compatibility notes](https://modrinth.com/mod/forgematica).

[?] Use shader-off projection review for exact block comparison, then separate shader-on art review. The user should review screenshots/playtests rather than hand-place the projection; agents remain responsible for all construction.

### 6.2 Distinguish the file formats

[V] Sponge schematic v3 defines dimensions, Minecraft DataVersion, palette/block-state identifiers and associated data. It is a specified format, not simply a vanilla structure file with a different extension. Source: [Sponge v3 specification](https://github.com/SpongePowered/Schematic-Specification/blob/master/versions/schematic-3.md).

[?] Use three exports from the same canonical voxel/component representation:

1. **Vanilla structure NBT** for engine-owned runtime placement. Store size, palette, relative block positions/states and needed block-entity payloads. Split large builds into bounded modules appropriate to the placement path.
2. **Sponge `.schem`** for WorldEdit staging/import. Use a format library or verified spec implementation; preserve origin and state metadata.
3. **`.litematic`** for projection review and material count. It is a review artifact, not the canonical generator source.

[?] Check origin offset, negative/rotated region extents, palette indices, compression, DataVersion and all carrier block entities. Round-trip a tiny asymmetric sample with north/east markers, a staircase, door, waterlogged block and custom prop before exporting a district.

[?] Define distinct paste policies: **replace volume** explicitly includes air to remove old geometry; **overlay decoration** skips air. An accidental air-skipping replace leaves old blocks inside the new build; an accidental air-including overlay destroys existing interiors. Preserve a world copy or before-state diff for every application.

[?] Do not downgrade complete 1.21.4+ generated worlds into 1.21.1. Export only the intended structures, enforce the 1.21.1 ID/state allowlist, and replace unsupported features deliberately. Newer version labels are not evidence of backwards-compatible block data.

### 6.3 Libraries and original module inventory

[V] Chinese Yuushya's workshop is a real transformed-prop share-code library. Chinese MCBlock advertises building libraries, layered 3D teaching and projection editing/export; its assets require item-by-item provenance and version inspection. Sources: [Yuushya workshop](https://yuushya.com/townscape/workshop.html), [MCBlock](https://mcblock.top/).

[C] Japanese BOOTH includes Minecraft-specific map/build listings among many Unity/Blender/VRChat models. One Richters church listing specifies Minecraft 1.17.1 and a 26×55×58 footprint. This is a creator listing, not permission to redistribute or an original Japanese builder attribution; the text is Chinese. Source: [Minecraft Building – 歐風禮拜堂](https://booth.pm/ja/items/4113598).

[?] Distinguish Minecraft-ready structures from generic “church” 3D assets. Do not buy or import a Blender church and assume it is block-based. For this original map, reference libraries teach composition; **our agents should create and own the actual module geometry**.

[?] First original inventory:

| Priority | Modules to create | Evidence to keep |
|---|---|---|
| P0 sewer | straight bay, turn, T-junction, stepped vault, drain, pipe/valve set, service door, stair/ledge | topology ports, palette/state list, four views, walk test |
| P0 slums | 3 dwelling masses × 2 facades, rooftop annex, external stair, bridge, awning, utility wall, camp room | clear interior/access, day/night views, camera test |
| P1 ruins | intact/breached rib bay, fallen slab/rubble pair, shaft, catwalk, broken machinery shell | paired damage event, silhouette view, support/path test |
| P2 church | pointed arch, buttress, rose/data window, gold rib, nave bay, terminal/altar | front/section/interior views, glare/readability test |

[?] Record each module's source inspirations and license separately from its exported format. “投影分享,” a download button or an available paid file does not alone establish redistribution rights.

## 7. Recommended high-quality AI-agent pipeline

[?] This extends the existing project's ticket/evidence workflow specifically for map building; it does not replace the approved orchestration plan. User role remains direction, visual review and playtesting. Agent roles below can run sequentially or under the project's approved task system; no extra research agents were spawned for this report.

### Stage 0 — runtime registry and architectural coupons

[?] Freeze the exact mod manifest and create an installed registry/state dump. Map semantic roles such as “aged concrete” or “gold rib” to a **small allowed set** of actual IDs. Inspect each ID under the chosen resource pack and shader, because the same ID can look very different in another texture pack.

[?] Build four compact original samples: sewer bay, slum facade/interior, damaged structural bay, and church arch. Supply screenshots plus dimensioned sections. Start by reviewing these before applying the palette to hundreds of rooms.

### Stage 1 — level graph before facades

[?] Encode checkpoints, mandatory boss paths, optional branches, vertical transfers and shortcuts. Each shortcut has states: locked on arrival, reachable unlock action, open afterwards, persistent after save/reload and death. This prevents the architecture generator from producing a picturesque but disconnected district.

[?] Author provisional route widths, camera volumes, enemy movement space, no-detail encounter floors and landmark sightlines. Generate a graybox and run navigation/combat checks before dressing it. Terrain only changes where the route contract permits it.

### Stage 2 — compact scene specification and worked examples

[?] Supply the LLM with component names, real source-code examples, material mapping, cardinal directions, terrain occupancy, protected volumes and explicit output schema. This is the practical synthesis of the Japanese preset work and T2BM. The output should be parseable geometry instructions, not a free-form list of tens of thousands of block coordinates.

[?] Example design contract; values are illustrative, not approved final measurements:

```yaml
id: sewer_pump_approach_01
target: {minecraft: "1.21.1", loader: neoforge}
seed: {geometry: 1401, damage: 2102, dressing: 3103}
bounds: {origin: [0, 0, 0], size: [48, 24, 48]}
palette: sewer_v1
components:
  - {kind: tunnel_bay, count: 3, ports: [west, east]}
  - {kind: pump_hall, access: [west, upper_north]}
protected:
  - critical_route
  - encounter_floor
  - shortcut_gate_and_trigger
style:
  wall_backing_blocks: 2
  pipe_networks: 1
  coherent_damage_events: 2
required_evidence:
  - registry_validation
  - route_and_gate_state_report
  - daylight_and_shader_contact_sheet
  - first_person_route_capture
```

### Stage 3 — deterministic generation and controlled changes

[?] A geometry library supplies cuboids, hollow volumes, arch profiles, transforms, repeated bays, facade grammar and pipe graph placement. The LLM chooses layout/parameters, then the library enforces boundaries and emits blocks/states/NBT.

[?] Keep component IDs stable. A reviewer requesting “deeper windows” should regenerate only the facade component. Preserve navigation, approved neighboring modules and independent decoration seeds. Store a before/after block diff and rollback artifact for every staged patch.

[?] Run support checks as design heuristics, not real Minecraft structural physics. Sand/gravel/fluids and multi-block states need actual engine behavior tests. An architectural plausibility score should not be advertised as a game mechanic.

### Stage 4 — art passes in descending scale

[?] Review silhouette → room/bay rhythm → facade depth → materials → service network → coherent destruction → inhabitants/props → lighting. Large proportion failures should be corrected before polishing valves and chairs.

[?] Generate several candidates for one **small module** and compare them at identical camera angles. Save the selected module as a library entry. Do not spend vision-model iterations randomly rebuilding an entire district.

### Stage 5 — independent visual and functional review

[?] Use two separate review outputs:

| Review | Evidence | Automatic checks | Human/VLM judgment |
|---|---|---|---|
| Functional | coordinates, collision/state data, route captures | critical path connectivity, headroom, shortcut state, reachable interactions, no unwanted leaks, bounds | player camera/lock-on and encounter feel |
| Visual | four exterior views, interior sections, key first-person vistas, day/night, shader off/on | palette membership, repeated patterns, excessive prop counts, missing faces/models | silhouette, hierarchy, depth, coherent age, original identity |

[?] A VLM can identify likely problems and propose local edits. Require a reviewer to reference exact images/coordinates and compare against the contract. Randomize candidate ordering for comparisons where practical. A self-critique score is not sufficient to approve `finish()`.

[?] Render sections and back faces: an isometric front view cannot show a blocked staircase, empty interior, fake pipe route or a detail obscuring an enemy. Use actual in-client shader captures for final appearance; mcbuild's software renderer is useful early feedback but cannot validate mod rendering/Iris.

### Stage 6 — placement and actual engine checks

[?] Place modules into a copied staging world through matching WorldEdit, our custom NeoForge placement bridge, or runtime structure NBT. Verify every imported block-entity payload. Read back selected coordinates/material histograms and compare them to generated data.

[?] Recheck critical paths after engine updates: door halves/hinges, stair shape, wall/bar connections, waterlogging, fluid spread, unsupported plants, gravity blocks and opaque/cutout/translucent surfaces. Save/reload and test a rotated placement; successful raw file serialization is insufficient.

[?] Prefer a custom bridge with bounded transactions, build-area limits, staging preview, full-state export and rollback. If adopting mcbuild's bridge, keep its local/trusted-world boundary and add an independent gate before writing to final content.

### Stage 7 — gameplay and performance gate

[?] Test **the actual approved stack**, not a vanilla screenshot instance: representative boss, mobs, camera, props, particles and target shader at 1080p on the RTX 4060 / Ryzen 5 5600 machine.

[?] Record both average FPS and low-percentile/frame-time behavior. A reasonable provisional acceptance target is sustained ≥50 FPS with percentile limits specified explicitly in the project's performance contract; average alone can conceal combat stutters. Start from representative rooms and vistas before scaling the district.

[?] Inspect dense corners, long shafts, stacked slum interiors, stained-glass halls and prop-heavy refuges. If cost is excessive, reduce repeated transformed props, hidden model complexity, transparent layers and unnecessary exposed views before removing the district's major silhouettes.

### Stage 8 — concrete review package for the user

[?] Produce: route diagram, selected reference/kit board, exact mod/palette manifest, six to ten critical first-person screenshots, a short route/boss video, before/after changes, automated-check report and performance capture. Ask for review of this concrete package; agents carry out the revisions.

[?] The school milestone's first vertical slice should join **one sewer approach + one pump encounter + one shortcut + one slum arrival/camp**. Demonstrate the loop end-to-end, then expand the two areas. The later church should initially exist as a palette/arch coupon only.

## 8. Quality rubric and immediate experiment

[?] Adapt GDMC's four dimensions into a project rubric, but keep hard failures separate from beauty:

| Dimension | Questions for this map | Evidence |
|---|---|---|
| Adaptation | Does the build fit terrain, neighboring architecture and intended vertical layering? | terrain/section overlay; transition views |
| Functionality | Can the player and enemies traverse, fight, use interactions and shortcuts? | engine route/encounter/state tests |
| Narrative | Do habitation, services and damage have visible causes and original faction identity? | three environmental story clusters per area |
| Aesthetics | Are silhouette, depth, palette and detail hierarchy coherent from the player camera? | identical-view comparisons; actual shader captures |

[?] Suggested scores: 1–5 per dimension, with local repair notes. Hard failures include disconnected required route, invalid block/state, broken shortcut persistence, unintended fluid flooding, model loss after reload, or failure of the agreed combat performance gate. An attractive build cannot average its way past these failures.

[?] First prototype comparison: generate the same 8-block sewer bay with (A) a structured geometry template and an agent selecting parameters, and (B) mcbuild's free blueprint/self-critique loop. Compare time/cost, valid-state rate, route clearance, pipe continuity, all-view visual quality and the amount of revision needed. Preserve both successes and failures.

[?] Use the result to choose how much freedom agents receive. If unconstrained generation repeatedly misses proportions or collision, constrain the DSL and example kit rather than repeatedly enlarging the prompt.

## 9. Remaining uncertainties and negative findings

- [?] No verified CN/JP/KR tutorial for the exact combined style “white-gold sci-fi Gothic” was retrieved. The report's church kit is an original synthesis of Gothic depth/massing, a Korean modern hybrid and verified material options.
- [?] No Bilibili comment consensus is claimed. HTTP 412 blocked the comment-discovery path before comments could be requested successfully.
- [?] MCBBS links survive in official/MC百科 sources, but their historic article contents were not recovered. Do not cite an inaccessible archive as an inspected tutorial.
- [?] The favela tutorial was found only in listings; it needs a direct video and visual/material inspection before extracting its detailed recipe.
- [?] Japanese IEICE evidence is an abstract; code release and quantitative evaluation remain unverified.
- [?] GDPC-compatible current server versions differ from our runtime. A 1.21.1 port, custom bridge or schematic-export path is required; release availability must not be inferred from GDPC's Python API.
- [?] Yuushya's project-description compatibility advice includes historical Fabric/Indium references. Confirm the exact NeoForge renderer behavior and dependency manifest in our instance.
- [?] Modded IDs were verified against packaged blockstate assets, not a loaded server registry. Rendering, CTM, collision and complex NBT need the coupon tests.
- [?] No full-world generation project found here establishes expert-level original map quality with Epic Fight, all custom assets and ≥50 FPS on the target machine.
- [?] Public, free, paid and open-source have different meanings. Preserve provenance and respect the actual item's redistribution terms. This research did not purchase assets, contact creators or redistribute maps.

## Summary

[?] The most practical approach is an agent-driven **structured plan → deterministic modules → visual and gameplay review** pipeline. Let agents choose composition and revise code, while a geometry library enforces approved palettes, bounds, states and routes.

[V] Japanese builder WIEN explicitly demonstrates one-block wall recesses behind columns and cathedral massing with twin front towers. SOU provides a concrete stone/cracked/mossy ruin palette. [WIEN](https://note.com/wien_mcbuild/n/n84d4826d918e), [SOU](https://minecraft-log.com/2902).

[C] Chinese Kowloon and Akra showcases are useful for dense additive housing and immense structural silhouettes. Korean DC Inside supplies a cathedral/modern hybrid with interior and night-lighting discussion. Bilibili evidence is indexed creator descriptions; comments and full videos were inaccessible. [Kowloon](https://www.bilibili.com/video/BV1QJvQeyEef/), [Akra](https://www.bilibili.com/video/BV1yfbd63E9B/), [Korean hybrid](https://gall.dcinside.com/board/view/?id=minecraft&no=215454&page=1).

[?] For the sewer, prototype an 8-block bay with thick backing, a stepped vault, dry walkways and one coherent pipe network. Age it with leak/waterline masks. For slums, use small furnished dwellings, irregular extensions, connected roofs and visible utilities around a protected route graph. Megastructures need repeated structural hierarchy and coherent collapse events. The later church should preserve broad white planes, pointed ribs, recessed glazing, thin gold traces and original flower/circuit motifs.

[V] Verified 1.21.1 NeoForge releases exist for Yuushya Townscape/Modelling, Chipped, Rechiseled, FramedBlocks, LittleTiles and Zcraft. Artifact inspection confirmed useful pipe/drain/condenser IDs and gold/quartz shaped variants. This proves available assets, not compatibility or FPS. [Townscape](https://modrinth.com/mod/yuushya-townscape/version/L2HpYsbq), [Rechiseled](https://modrinth.com/mod/rechiseled/version/6muGRqvu), [Zcraft](https://www.curseforge.com/minecraft/mc-mods/zcraft-decoration/files/8085772).

[V] Chinese T2BM demonstrates compact structured generation and validation, but its refined GPT-4 outputs pass both measured constraints only 38% of the time. Luban separates visual and functional checks. A Japanese IEICE abstract adds material mappings, preset rules and actual-code examples. These are design lessons, not evidence of automatic production-ready map quality. [T2BM](https://arxiv.org/html/2406.08751v1), [Luban](https://luban-paper.github.io/), [Japanese abstract](https://www.ieice.org/publications/conferences/summary.php?ConfCd=2025G&conf_type=G&expandable=0&id=CONF0000150607&lecture_number=TPO-1-107&session_num=TPO-1&year=2025).

[V] **mcbuild** is the strongest immediate prototype candidate: blueprint DSL, multiview critique, schematic export and a NeoForge 1.21.1 bridge. **Forgematica** supplies a matching projection alternative. Current GDMC HTTP metadata has no matching 1.21.1 NeoForge release. [mcbuild](https://github.com/harrynull/mcbuild), [Forgematica](https://modrinth.com/mod/forgematica), [GDMC HTTP](https://github.com/Niels-NTG/gdmc_http_interface).

[?] Start with an original sewer/encounter/shortcut/slum-camp vertical slice. Keep geometry, damage and decoration seeds separate. Require loaded-registry validation, collision/navigation tests, save/reload and schematic round trips, actual shader screenshots, and combat performance captures. Export NBT/schematic/projection files from canonical source data; preserve complex prop NBT. The user reviews concrete visuals and playtests while agents perform all construction and revision.

