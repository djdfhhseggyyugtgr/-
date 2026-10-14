# 2A. Anime-style (서브컬처) female character models in Minecraft: ecosystem and quality bar (2026-10-13)

Tags: [V] verified from a primary source (official page, repo, file I measured myself); [C] community / single-source opinion; [?] inference or unconfirmed.
Raw data: `research/r2/2a/` (S_*/F_* search and fetch JSON), `research/r2/2a/raw/ysm_builtin_stats.txt`, `research/r2/2a/raw/tlm_builtin_stats.txt`, measurement scripts in `research/r2/2a/scripts/`.
Measured repos (shallow, blob-filtered, sparse): `YesSteveModel/YesSteveModel` @74c53b5 (2026-09-21), `TartaricAcid/TouhouLittleMaid` @8a3ac5e (2026-05-09). Only read for measurement; nothing from them is copied into the project.

Content rule reminder (from CONTEXT.md): school project. Daisy (child) gets age-appropriate design only. Body-shape techniques are for adults only and stay non-sexual. Several ecosystem sources below contain R-18 material; I did not open those and do not link them.

---------------------------------------------------------------------
## 0. One-paragraph summary

"Anime girls everywhere" in Minecraft is mostly one ecosystem: **Yes Steve Model (YSM)**, a Chinese player-model mod (16.3M Modrinth downloads) built on GeckoLib/Bedrock geometry, with thousands of fan models (mostly unlicensed fan art of Genshin, Blue Archive, Hololive, etc.), a paid commission/retail market, and a 2026 crack-and-open-source drama. Its sibling **Touhou Little Maid (TLM)** has 189 built-in chibi maid models. The West has **Figura** avatars, Sketchfab/Blockbench-Workshop showcases and Model Engine server characters. The measured "standard" YSM anime girl (official Wine Fox, 22 outfits) is: 7×7×7 skull cube, ~41.6 model units tall rendered at 0.7 scale (≈1.82 blocks), **≈5.5 heads by skull / ≈4.2 heads counting hair volume**, median ≈590 cubes (276–1554, one 4533 outlier), ≈195 bones, 256² texture at nominally 1 texel per unit but with many stretched faces (median ≈55% exactly 1:1), 74–100% of cubes with fractional sizes, faces built from separate tiny eyelid/pupil/mouth cubes. Almost none of the attractive models are reusable by us: licences are ARR, CC BY-NC-SA, "personal use only", Sketchfab "NoAI", or they are unlicensed fan art. Only CC0/CC-BY items (YSM default template, a few Blockbench-Workshop models) are legally reusable, and even those are better used as structural reference.

---------------------------------------------------------------------
## 1. Yes Steve Model (YSM)

### 1.1 What it is, versions, loaders
- Replaces the vanilla player model with Bedrock-format models and animations; "uses geckolib at its core"; supports Bedrock geometry ≥1.12.0 and Bedrock animation 1.8.0; animation controllers and sounds since 2.3.0. [V] https://yesstevemodel.github.io/en/wiki/type/ , https://modrinth.com/mod/yes-steve-model
- Latest 2.6.5 supports 1.20.1 Forge, 1.20.1/1.21.1 Fabric, **1.21.1 NeoForge** and 26.1.2 NeoForge. 1.21.1 NeoForge jar `ysm-2.6.5-neoforge+mc1.21.1-release.jar` published 2026-04-22, 61 MB. [V] https://yesstevemodel.github.io/en/wiki/intro/ , https://modpacks.ch/mods/minecraft/86xjpqqS/yes-steve-model/versions/HZWaR0LY
- Since 1.2.0 the encryption and rendering core is C++ (VMProtect); Windows/Linux x64 + Android client only, **no macOS**. Must be on client and server for full function. [V] intro page; https://ysm.cfpa.team/wiki/install/
- Licence on Modrinth: **ARR**. Modrinth 16.3M downloads, 2.3K followers. [V] https://modrinth.com/mod/yes-steve-model
- Official open-source rewrite started 2026-08: `YesSteveModel/YesSteveModel`, code Apache-2.0, "Asset Container Spec / Model Schema" CC0, built-in assets licensed per their own `ysm.json`; marked unfinished, formats not frozen. [V] https://github.com/YesSteveModel/YesSteveModel
- Mod compat list: TACZ guns, Carry On, SlashBlade, Parcool, SWEM, TLM, Sophisticated Backpacks, Better Combat (attack anims), Iron's Spells, Iris/Oculus PBR. [V] intro page. Community reports Better Combat attack anims break YSM models / head clips the camera. [C] https://www.reddit.com/r/feedthebeast/comments/1f6xc32/ , https://www.reddit.com/r/feedthebeast/comments/1n2k6eq/
- First-person problem: big anime heads/hair cover the screen in first person (warden model + TACZ). [C] https://www.reddit.com/r/feedthebeast/comments/1isdl0i/

### 1.2 Model format and authoring conventions (official wiki)
- Folder format (`ysm.json` + `models/main.json`, `arm.json` + `animations/*.animation.json` + `textures/*.png` + optional `controller/`, `sounds/`, `functions/*.molang`, `lang/`), zip, or encrypted `.ysm` (cannot be converted back; export with `/ysm export`). [V] https://ysm.cfpa.team/wiki/struct/ , https://yesstevemodel.github.io/en/wiki/type/
- `ysm.json` has `metadata.license.type` (required), authors with roles/contacts, `properties.height_scale` / `width_scale` (**default 0.7**), texture list with optional LabPBR-style `normal`/`specular` maps (Iris/Oculus), `all_cutout` flag "to support negative-size outline models", extra (emote wheel) animations with Molang-driven config sliders. [V] https://ysm.cfpa.team/wiki/struct/
- Authoring tool: Blockbench + `ysm-utils` plugin (supports BB 4.x and 5.x). [V] https://ysm.cfpa.team/wiki/plugin/
- Standard group (bone) names give behaviour: `Head`, `AllHead` (hidden in first person / Better Combat), `ViewLocator`, `LeftHandLocator`/`RightHandLocator` (2–8 extra), `ElytraLocator`, shoulder/waist/blade/sheath/pistol/rifle/backpack locators, any group starting `ysmGlow` = emissive under most shaders. The `config/yes_steve_model/custom/default` model is **released CC0** "to encourage model packs". [V] https://ysm.cfpa.team/wiki/tph2yetr/
- YSM UV standard (2026-01-04, YSM ≥2.6.0): UV coords and sizes must be integer multiples of the UV unit; no zero-size UV on faces with area; box-UV cubes with a side <1 are invalid (use bigger cube + negative inflate, or per-face UV). Tool `UV0Fixer`. [V] https://ysm.cfpa.team/wiki/ysm-uv-standard/
- Performance note in 2.6.5 changelog: "once a model uses translucent material, rendering efficiency drops greatly; minimise translucency". [V] https://www.mcmod.cn/class/version/8616.html
- Memory: server with ~1000 YSM models makes every client preload all of them (8 GB pack → 24 GB). [C] https://github.com/YesSteveModel/YSM-Wiki-Issues/issues/358
- Main video course recommended by the official wiki: **叶无道_M "BB+YSM建模全流程教程"** (Bilibili, 32 parts, 162k views on the head-ratio episode). Chapter list is itself the community's quality checklist: 头身比 (head ratio), 人体比例技法, 胸臀手脚, 雕刻技法 (sculpting), **混素技法 (mixed-pixel technique)**, 锐角三角形/圆形/环形/**负尺寸技法 (negative-size cubes)**, 身体曲线, 头脸蛋头发, 骨骼轴点调整, **关节防穿帮 (joint anti-gap, 13 min)**, 色卡制作 (colour cards), 重复物件先上纹理/复制UV/镜像UV, 头发专题, 纹理明暗关系. [V] https://www.bilibili.com/video/BV1SRuKzGENC/ ; https://ysm.cfpa.team/wiki/video/ (the linked Feishu doc returned 404)

### 1.3 Measured: official built-in YSM models (my own measurement) [V]
Script: `scripts/ysm_stats.py`, `ysm_ratio.py`, `ysm_uv.py`. "heads(skull)" = (skull top − feet) / skull-cube height; "heads(hair)" = (hair top − feet) / (hair top − chin). Models with hidden props under `Head` give nonsense hair numbers and are omitted from the hair column.

| Model | Licence | Cubes | Bones | Rotated cubes | Texture | Skull | heads(skull) | heads(hair) | In-world height @scale |
|---|---|---|---|---|---|---|---|---|---|
| default (girl template) | **CC0** | 172 | 64 | 84 | 128² | 7×7 | 5.72 | 4.22 | 1.89 blk |
| misc/3_default_boy | CC0 | 156 | 58 | 81 | 128² | 7×8 | 5.02 | 4.25 | 1.84 |
| misc/1_alex, 2_steve | CC0 | 46–47 | 61 | 4 | 64² | 8×8 | 3.99 | 3.99 | (scale 1.0) 2.0 |
| wine_fox/07_jk | CC BY-NC-SA 4.0 | 335 | 113 | 255 | 256² | 7×7 | 5.51 | 4.18 | 1.82 |
| wine_fox/02_new_year | CC BY-NC-SA | 342 | 138 | 239 | 256² | 7×7 | 5.53 | 4.19 | 1.82 |
| wine_fox/06_hanfu | CC BY-NC-SA | 471 | 117 | 367 | 512² | 7×7 | 5.77 | 4.36 | 1.90 |
| wine_fox/18_wedding | CC BY-NC-SA | 1554 | 317 | 1385 | 256² | 7×7 | 5.56 | 4.08 | 1.85 |
| wine_fox/21_saint | CC BY-NC-SA | 750 | 185 | 642 | 256² | 6.7×6.6 | 5.79 | 4.37 | 1.81 |
| wine_fox/13_matured (adult version) | CC BY-NC-SA | 634 | 260 | 485 | 2048² | 6.0×6.2 | **6.44** | – | scale 0.8 |
| wine_fox/12_little (child) | CC BY-NC-SA | 407 | 153 | 312 | 256² | 7×7 | **4.14** | 3.20 | 1.40 |
| wine_fox/17_mini (chibi) | ARR | 513 | 194 | 369 | 1024² over 128 UV (8 texels/unit) | 10.7×8.4 | **3.30** | 1.98 | 1.70 |
| wine_fox/08_sta (mecha transform) | CC BY-NC-SA | **4533** | 526 | 3410 | 1024² | 7×7 | 4.99 | 4.10 | 1.62 |

Across the 22 Wine Fox outfits: cubes 276–4533, **median ≈593**; bones 101–526, median ≈195; 20 of 22 at render scale 0.7 (09_hailuo 0.6, 13_matured 0.8). The skeleton is shared: Root → AllBody → UpBody/UpperBody (AllHead → Head → Eyes{EyeBrow, Eyelid→EyelidBase→Pupil/Dot}, Ear, Hair{Bangs, SideHair, LongHair chains, BaseHair}, Mouth{4 expression groups}) + Arm{Left/RightArm → ForeArm → Hand → locators} + cloth{Front/Back/Left/RightClothe} + Tail chain; DownBody → Left/RightLeg → LowerLeg → Foot. The CC0 default girl uses the same pattern with `Skirt → Front/Back/Left/RightSkirt`.

Other measured conventions [V, from the same files]:
- **Texel density**: nominal 1 texel per model unit (declared texture size = image size, except 17_mini at 8×); with the 0.7 render scale that is ≈22.9 texels per world block. Measured per-face UV/size (edges ≥1 unit): the CC0 default/Steve/Alex templates are 86–90% exactly 1:1, but Wine Fox outfits are only 6–76% 1:1 (median ≈55%), 17–74% stretched within 0.7–1.3×, and up to 77% outside that range. 74–100% of Wine Fox cubes have **non-integer sizes**, and thin (<1 unit) cubes reach 61–66% in detailed outfits (wedding, survivor, zhiban). Official YSM practice openly uses mixels ("混素"); the plain templates do not.
- **Face built from geometry**: in 07_jk the head is one 7×7×7 cube; each eye is a 2×2×1 eyelid + 1.4×2×1 eyelid base + 1.15×1.5×2 pupil (inflate −0.3) + 1.2×1×1 highlight (inflate −0.35); eyebrows are 1-unit cubes; the mouth has 4 alternative expression groups (smile, slight smile, surprise, fear) made of 0.125–0.7-unit cubes, toggled by animation. This enables blinking and expressions without texture swaps.
- **Skirts split into 4 panels** (front/back/left/right) so legs do not clip through them (default and JK). This is the standard answer to "dress clipping" questions (e.g. https://www.reddit.com/r/Blockbench/comments/1q8xrwd/ ).
- **Two-segment limbs** (upper arm/forearm, thigh/shin/foot) with filler cubes; vanilla has single-segment limbs.
- **Palette**: the Wine Fox base textures use only 61–135 unique colours (07_jk 135, 01_taisho 84, 04_kongfu ~72); the painterly outliers go to 600–3800 colours. Atlases are only 20–35% filled. One pure-black/white colour per texture (outline/eye) is common.
- **Outlines**: negative-size cubes are rare (0–16 per model), so inverted-hull outlines are not the norm in official models.

### 1.4 Epic Fight compatibility (relevant to our stack)
- YSM itself showed a start-up warning about Epic Fight; crash reports exist. [V] https://github.com/YesSteveModel/YSM-Wiki-Issues/issues/178 . Epic Fight closed a "please support YSM" request as not planned (2026-06-21). [V] https://github.com/Antikythera-Studios/epicfight/issues/2577
- **EpicYSM** (Argorice, MIT, client-only): 1.21.1 NeoForge + Epic Fight 21.15+ + YSM 2.6+. Readable (folder/zip) models are converted to Epic Fight's own mesh format on the fly; encrypted `.ysm` are posed by writing EF's pose into YSM's skeleton; optional hair/cloth physics; leaves models with unreadable body-bone names to YSM. 6.0K downloads, updated 2026-09-20. [V] https://www.curseforge.com/minecraft/mc-mods/epicysm
- **YSM Epic Fight Compat** (sakuraimikoto33, MIT): 1.21.1 NeoForge 21.1.235+, YSM 2.6.0+, **Epic Fight 21.17.3.1 ≤ v < 21.18** (exactly our pinned EF), needs "YSM Mapping API" 0.1.8+; Iris integration; TLM maid integration 1.20.1 only. [V] https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat
- Implication [?]: a YSM-format protagonist could fight with EF animations, but it adds YSM (ARR, native DLL, no macOS) + 1–2 bridge mods + a mapping API, and EF animations are authored for EF's biped proportions; longer anime limbs may misalign weapons/feet. Not recommended as our main path; a fallback worth one test at most.

### 1.5 Community, market and controversy (why we only reference)
- YSM is the de-facto standard for custom player models in the Chinese community; a commission and retail market exists where encrypted versions and editable source files are priced separately (source costs several times more). [C] https://catme0w.org/zh-tw/observations/ysm/
- Encryption history: AES v1/v2 cracked → C++/VMProtect v3 (2024) → fully cracked 2026-05-03 (YSMParser, OpenYSM) → official open-source announcement 2026-05-16 → Apache-2.0 rewrite repo 2026-08. DMCA takedowns, doxxing allegations, and removal of an official contributor over R-18 models. [V/C] https://www.mcbbs.co/thread-5253-1-1.html , https://nmfwiki.miraheze.org/wiki/YSM%E5%BC%80%E6%BA%90%E4%BA%8B%E4%BB%B6 , https://github.com/OpenYSM/OpenYSM
- Official stance: YSM opposes R-18 creations; future official showcase requires "detailed modelling, reasonable textures, good compatibility, healthy content, no R-18/gore/copyright infringement". [V/C] mcbbs Q&A above.
- Selling unlicensed fan models of other IPs is described even by YSM-friendly writers as infringing ("grey area" only in enforcement). [C] mcbbs Q&A.
- Collections: `Elaina69/Yes-Steve-Model-Repo` (3.5k stars, "free to use", folders named after commercial IPs: Genshin, Blue Archive, Arknights, Nikke, Elden Ring, NieR…). The fan-collection `nekohalawrence/YSM-Model-Author` says most of its models are corrupted and points to third-party sites. 750-model "addon" packs circulate on YouTube. [V] https://github.com/Elaina69/Yes-Steve-Model-Repo , https://github.com/nekohalawrence/YSM-Model-Author , https://www.youtube.com/watch?v=ZM4opivPaKs
- Players note the default Wine Fox reads young ("an adult version for those not into the loli vibe"). [C] same video. → our adult characters need clearly adult proportions (≥6 heads), not the 5.5-head default.

---------------------------------------------------------------------
## 2. Other ecosystems

### 2.1 Touhou Little Maid (TLM)
- 1.21.1 NeoForge 1.5.3 (2026-05-09), 6.5M CurseForge downloads. **Code MIT, assets CC BY-NC-SA 4.0** (LICENSE-CC: "Copyright (c) 2019-2025 tartaric_acid, for the assets part"). Artists: Succinum, Pajinyi, ZeniCrow, Tian_mi, Paulzzh, YurisCat (+Hoishi, CrystalizedSun, FumoLover in the pack file). [V] https://www.curseforge.com/minecraft/mc-mods/touhou-little-maid , repo LICENSE-CC
- Model packs: Bedrock entity geometry in `tlm_custom_pack`, Blockbench `tlm-utils` plugin, animation auto-assigned by group names; can also render YSM models on maids (YSM 2.4+). Pack index site: http://page.cfpa.team/MaidCustomPack/zh/ ; tutorial https://www.mcmod.cn/post/3476.html [V]
- Measured built-in classic maid pack (189 models, Touhou characters): **cubes median 68 (p10 26, p90 168, max 355)**, almost no rotated cubes, mostly 128² textures, total height 26 units, 8-unit head → **≈3.25 heads** (chibi), some 1.7–2.6. Built-in GeckoLib pack (27 Wine Fox/Zhiban models): median 546 cubes (p10 329, p90 1272), 5.5 heads, `render_entity_scale` 0.65. [V] `raw/tlm_builtin_stats.txt`

### 2.2 Figura
- Client-only avatar mod, Blockbench models + Lua scripting, cloud sync; MC 1.16.5–1.21.4 incl. **NeoForge 1.21.1**; licence **PolyForm Noncommercial 1.0.0**. [V] https://modrinth.com/mod/figura
- Blockbench 5 `.bbmodel` broke Figura (issue #445); parser rework merged 2026-01-30 (PR #448); a "Figura v5 support" add-on covers older builds. [V] https://github.com/FiguraMC/Figura/issues/445 , https://github.com/FiguraMC/Figura/pull/448
- Examples: Gilgames32/vixen (288 stars; tail physics, action wheel, 5 skins, sleep eyes) https://github.com/Gilgames32/vixen ; aclassyfren "Monoko & Monoe" (code MIT, low-poly, smooth vs flat normals) https://aclassyfren.itch.io/monoko-and-monoe ; Japanese hobbyist mascot built with Blockbench+Figura https://minecraft-hourouki.hatenablog.com/entry/2024/09/07/062108 . Figura allows meshes, so many "anime" avatars are low-poly meshes rather than cubes. [V]
- Critics of YSM point to Figura as the open alternative; a YSM→Figura converter ("Yosemite Compiler") was announced. [C] https://catme0w.org/zh-tw/observations/ysm/

### 2.3 NPC mods
- **Easy NPC** (1.21.1 NeoForge bundle 7.1.1): skins from built-in/player/URL/local; render types incl. `EASY_MODEL_ENTITY`; with **Easy Model Entities** (MIT, 1.21.1 NeoForge 2.0.0, 2026-09) a Blockbench model becomes an NPC without Java; pose editor needs bone names `head, body, left_arm, right_arm, left_leg, right_leg…`. [V] https://github-wiki-see.page/m/MarkusBordihn/BOs-Easy-NPC/wiki/ModIntegration , https://modrinth.com/project/ngLoLP1P
- CustomNPCs: anime content is skin packs (e.g. JoJo skins port); GeckoLib models via CNPC-Gecko-Integration (MIT) / CNPC+ Gecko Addon (1.7.10, ARR). Not on our 1.21.1 path. [V] https://www.curseforge.com/minecraft/mc-mods/cnpc-gecko-addon
- MCA Reborn: 1.21.1 NeoForge builds, GPLv3; villagers keep vanilla-like bodies with layered skins, not anime geometry. [V for version/licence; ? for style]

### 2.4 Bedrock Marketplace / character creator
- Anime packs are texture-driven on the vanilla 4-head body: "Anime HD" (PixelOneUp, HD skins), "Anime Idols 4K" (GoE-Craft), character-creator items like "Anime Lava Kimono"; third-party "4D custom geometry" packs. The anime read comes from big painted eyes and hair silhouettes, not proportions. [C] https://bedrockexplorer.com/@pixeloneup/anime-hd-v2 , https://auth.bedrockexplorer.com/@goe-craft/anime-lava-kimono

### 2.5 Showcase sites (Sketchfab API, likeCount order, 2026-10-13) [V numbers; triangles ÷12 ≈ cubes]
| Creator / model | Triangles (≈cubes) | Licence / tags | Note |
|---|---|---|---|
| W'Projects – 32x Cute Anime Elf Girl https://sketchfab.com/3d-models/32x-ute-anime-elf-girl-minecraft-blockbench-639f4b797b834313a73ce7a34b32ab6a | 290 (≈24) | none | most-liked; proves a very low cube count can read as "anime" |
| Zonovv – Lucy / Shiroko / Raiden (fan) https://sketchfab.com/zonovv | 5.6k–15k (≈470–1270) | none; some NoAI | high-density YSM-style |
| NekuroMC – YSM VTuber/anime models https://sketchfab.com/NekuroMC | 0.6k–15k (≈50–1270) | many **NoAI** | prolific YSM modeller listed on the YSM Modrinth page |
| iJUNE (Pixelar) – "[MC] Java: C_01" original cyberpunk samurai https://sketchfab.com/3d-models/mc-java-c01-46722d7712af4a0392baa322957ec466 | 5.0k | – | **419 cubes, 128² texture, 3 blocks tall, 9 combat anims (idle, walk, run, slide, attack 1–3, block, death)** |
| iJUNE – Reaper / Dark Knight / Desert Golem (Model Engine) | 2.5–5.6k | Standard | 207–462 cubes, 128², 3 blocks |
| Scalbylossus – Anime Wuxia Girl https://sketchfab.com/3d-models/anime-wuxia-girl-blockbench-aca6550b20134308815e116f9139da4a | 4.4k (≈370) | none | |
| CanberraLamb – Momonaku (YSM) https://sketchfab.com/3d-models/momonaku-040bd851e9ff46fe9e336c57f192835c | 3.7k | CC-BY | |
| Bogard_ – Anime girl minecraft style https://sketchfab.com/3d-models/anime-girl-minecraft-style-8eb0821c4e3943eba7b2a2b0d9b30c04 | 3.9k | **NoAI** | |
- Sketchfab "NoAI" tag text: "This model may not be used in datasets for, in the development of, or **as inputs to generative AI programs**." → do not feed these images into our agents even as references. [V]
- Blockbench Workshop (new marketplace with per-model licence + element/bone/texture counts): anime category 15 models/7 creators https://blockbenchworkshop.com/models/anime . Marcille (ARR showcase) 14 elements, 6 bones, 128²; Verity (CC-BY) 26 elements, 22 bones, 128²; Mahoraga (Standard licence) 110 elements, 28 bones, 256² — but "Creator states this is original work" is an uploader claim even for obvious IP fan models. [V]
- Planet Minecraft YSM originals by Fllz ("Liora", "Alice"): "not for sale… **Personal use only**, Vgen shop for monetization licence". [V] https://www.planetminecraft.com/texture-pack/ysm-mod-original-liora/ , https://www.planetminecraft.com/texture-pack/ysm-mod-alice/
- 80.lv features: Mull's "Loansword" (original Sekiro-O'Rin-inspired rōnin woman, Blockbench, 24 h) https://80.lv/articles/mysterious-r-nin-lady-inspired-by-sekiro-s-o-rin-in-blockbench ; Sven_Roku low-poly Miku https://80.lv/articles/hatsune-miku-in-low-poly-3d-with-pixel-art-textures (mesh low-poly, not cube style). [V]
- Leak sites (BlackSpigot) re-host Sketchfab/Workshop models byte-for-byte. Avoid entirely. [V]

---------------------------------------------------------------------
## 3. Proportions and conventions (synthesis)

| Reference | Head unit | Height | Heads (skull) | Heads incl. hair | Cubes | Texture / density |
|---|---|---|---|---|---|---|
| Vanilla player | 8 px | 32 px (model), hitbox 1.8 blk | 4.0 | 4.0 | 6 (+6 overlay) | 64² skin, 16 px/blk |
| TLM classic maid | 8 u | 26 u | ≈3.25 | – | median 68 | 128², 1 texel/u |
| YSM CC0 default girl | 7 u ×0.7 | 43 u ×0.7 ≈1.89 blk | 5.7 | 4.2 | 172 | 128², ≈23 texel/blk |
| YSM Wine Fox standard | 7 u ×0.7 (4.9 world px) | 41.6 u ×0.7 ≈1.82 blk | 5.5 | 4.2 | median ≈593 | 256², ≈23 texel/blk |
| YSM adult variant | 6 u ×0.8 | – | 6.4 | – | 634 | 2048² |
| YSM child variant | 7 u ×0.7 | 1.40 blk | 4.1 | 3.2 | 407 | 256² |
| YSM chibi | 10.7×8.4 u | 1.70 blk | 3.3 | 2.0 | 513 | 8 texel/u |
| Model Engine characters (iJUNE) | – | 3–4 blk | – | – | 207–462 | 64²–128² |
| Hytale official (already in docs) | – | – | – | – | – | 64 px/unit characters, stretch 0.7–1.3× |

Readability at Minecraft camera distance [? computed]: 1080p, FOV 70, third-person 4 blocks → ≈193 screen px per block; a 1.8-block character ≈347 px, a 0.31-block head ≈60 px, one texel at 32 px/blk ≈6 px. At 16 blocks: ≈48 px per block, head ≈15 px, texel ≈1.5 px → faces dissolve; identity must come from silhouette (hair mass, weapon, coat shape) and 2–3 dominant colours plus an emissive accent.

---------------------------------------------------------------------
## 4. Praise and criticism

Praise [C]:
- Expressive faces (blink, mouth shapes) and polished emote/gun/parkour animations; "the best skin mod" in showcase videos. https://www.youtube.com/watch?v=ZM4opivPaKs
- Eye highlights matter: "add some shines to those eyes so he looks less soulless". https://www.reddit.com/r/Blockbench/ (comment search "mixels", post 1q3sgt4)

Criticism [C]:
- **Mixels**: strong aversion in r/Blockbench ("Mixels = bleghh", "always look bad in Minecraft", "make the eye 3×3 instead"), with a minority defending smaller facial pixels for expression. https://www.reddit.com/r/Blockbench/comments/1vjx5qn/ , https://www.reddit.com/r/Blockbench/comments/1mdu0nw/ . This is the main split between Western vanilla-style taste and the YSM style.
- **Over-sexualised bodies** are mocked or rejected (top comments on a large-chest statue model are ridicule; "Why are there so many gooners on the blockbench sub? I want my cool looking mixel-less models back"). https://www.reddit.com/r/Blockbench/comments/1tlf9gt/ (I read only the comment text.)
- **Clipping**: skirts vs legs; first-person head/hair blocking view; Better Combat camera inside the head.
- **Performance**: translucency is expensive (official note); preloading hundreds of models eats RAM; GeckoLib processes every animated bone each frame (optimiser mods exist: GeckoLib Animation Optimizer for 1.21.1, ARR). https://www.curseforge.com/minecraft/mc-mods/geckolib-animation-optimizer
- **Closed format / paywalls / fan-IP reselling** dominate Chinese debate in 2026.
- Low-quality AI-written "guides" circulate (e.g. tsight.io articles quoting 5,000–20,000 vertices and 1024–2048² textures for NPCs); their numbers do not match measured models. [V that they mismatch]

---------------------------------------------------------------------
## 5. Licensing verdict

| Source | Licence | Can we reuse? |
|---|---|---|
| YSM mod binary | ARR (Modrinth); new rewrite Apache-2.0 | Not needed; don't ship |
| YSM default template model | **CC0** (wiki + ysm.json) | Legally yes. Use only as **structure reference** (bone layout, split skirt). One credited author was later removed over R-18 work, and our assignment requires agent-made assets. |
| YSM schema/spec (new repo) | CC0 | Yes, as a format reference |
| Wine Fox built-ins | CC BY-NC-SA 4.0 (3 outfits ARR) | No (share-alike + NC + recognisable mascot) |
| TLM assets | CC BY-NC-SA 4.0; Touhou characters are ZUN's IP | No |
| Figura | PolyForm Noncommercial (mod); avatars individually | Reference only |
| Elaina/other YSM collections, 750-model packs | mostly none / fan art of commercial IPs | **No** |
| Paid/encrypted YSM models; YSMParser output | seller terms / decrypted third-party work | **No, never decrypt** |
| Sketchfab "NoAI" models | NoAI clause | **Do not even use as AI input** |
| PMC Fllz etc. | Personal use only | No |
| Blockbench Workshop CC0 / CC-BY items | as stated, provenance unverified | Possible for props; not for our original heroines |
| EpicYSM, YSM-EF Compat, Easy Model Entities | MIT | Usable code if ever needed |

Bottom line: assume reference-only. Study measured conventions (numbers, rig layout, face construction, skirt split), never copy geometry or textures, and do not feed NoAI-tagged or fan-IP images into the agents.

---------------------------------------------------------------------
## 6. Proposed spec for our heroines (for user approval; contract changes are proposals)

1. Units and scale: model in GeckoLib units (1 u = 1/16 block), **render scale 1.0** (no hidden 0.7), texture **32 px/block = 2 texels/unit**, per-face UV, cube sizes and offsets snapped to **0.5 u (= 1 texel)** so there are no sub-texel mixels. This gives YSM-equivalent world size with finer texture and no mixels.
2. Proportions (skull cube = head unit):
   - Adult heroines (Linea, Acacia, Laurel, Melissa, Nightshade, Amaranth, gardeners): skull 5×5×5 u; skull top at 28–30 u → **5.6–6.0 heads**; hair top ≈30–31 u (≈1.85–1.95 blocks). Compare YSM default 5.5–5.7 (reads young) and YSM adult 6.4.
   - Tall warrior (Heather): 6.0–6.5 heads, ≈2.0–2.1 blocks.
   - **Daisy (child)**: 4.0–4.2 heads, ≈1.3–1.4 blocks, rounder face, simple clothes; no body-shape techniques.
   - Adult figures read as adult through height, longer legs, shoulder line and costume, never through exaggerated anatomy.
3. Budgets: hero NPC/player **200–450 cubes (hard cap 600)**, **≤60 bones (≤40 animated)**, texture 256×256–512×512 at 32 px/blk; no translucency; at most one inflate layer; no inverted-hull outline by default.
4. Rig conventions (from YSM, adapted to Epic Fight): two-segment limbs with joint filler cubes; skirt/coat split into front/back/left/right panels following the thighs; hair as 2–4 short bone chains; locator bones for hands, back weapon and the left-arm Spell Frame; emissive group naming per our LabPBR rules.
5. Face: 10×10-texel front face; eyes 2–3 texels wide × 3–4 tall with 1 highlight texel; separate thin eyelid/pupil planes (≥1 texel) for blink and 4–6 expressions; 1-texel mouth.
6. Readability: identity must survive 16 blocks: unique hair silhouette, 2–3 dominant colours, one emissive accent. Check renders at 4 m and 16 m distances in the review sheet.
7. Never: R-18 or suggestive geometry; copying fan-IP designs; sub-texel cubes; translucency; NoAI or fan-IP images as agent input.
