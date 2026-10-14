# 二次元 female Minecraft models: Chinese, Japanese, and Korean modeling research

Research date: 2026-10-13. Target: Minecraft Java 1.21.1 + NeoForge; Epic Fight 21.17.3.1; original, non-sexual character designs.

Evidence key: **[V]** verified primary documentation, author page, source file, or release listing; **[C]** community report, discussion, or secondary documentation; **[?]** inference, proposed project convention, incomplete access, or untested compatibility. A verified statement that a developer *advertises* a feature does not mean this research tested that feature in Minecraft.

## 1. Scope and most consequential findings

- [V] The project brief requires original female characters, 32 px/block NPC textures, and age-appropriate treatment of Daisy, the child pilgrim. This report adds modeling-specific findings to the existing research/design/pipeline documents; it does not replace their stack decisions. Local primary brief: [CONTEXT.md](CONTEXT.md).
- [V] **A released YSM–Epic Fight bridge exists for the exact target platform.** `sakuraimikoto33/YSM-EpicFight-Compat` has a `1.0.0-mc1.21.1` release, and CurseForge lists `ysm-epicfight-compat-mc1.21.1-1.0.0-all.jar`, NeoForge, dated 2026-09-11. This is stronger evidence than older claims that compatibility is impossible. [GitHub releases](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat/releases), [specific CurseForge file](https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat/files/8857201).
- [V] Chinese YSM documentation supplies actual eye-tracking, blinking, parallel-animation, controller, and UV rules. The documentation recommends a Bilibili creator, 叶无道_M, whose course covers proportions, joint concealment, texturing, and hair. [Official tutorial referral](https://yesstevemodel.github.io/wiki/video/).
- [V] Japanese creator Gakuto1112 documents a particularly useful face-atlas design in **CatMaid**: separate eye/mouth textures, expression cells, and separate glowing/non-glowing eye parts. This is an editable Minecraft-avatar example, not merely a VRChat model pictured on BOOTH. [Japanese README](https://github.com/Gakuto1112/CatMaid/blob/main/README_jp.md).
- [?] Dedicated Korean YSM anime-character construction tutorials were not verified. Korean sources found here are useful Blockbench/AJ lessons and installation/first-person reports. Claims about a universal Korean anime-modeling convention would overstate the evidence.

## 2. Chinese tutorials: a practical learning route

### YSM and Bilibili

| Evidence | Creator / resource | What was actually verified | Use for this project |
| --- | --- | --- | --- |
| [V] | 叶无道_M, [BB+YSM full workflow collection](https://www.bilibili.com/video/BV1eCuKzSEQ6/) | Public page lists lessons on head/body proportions, anatomy, base-body construction, curves, pivots, joint concealment, UV reuse, color, and hair. | Curriculum map for a reusable adult humanoid base. |
| [V] | Same creator, [expanded collection page](https://www.bilibili.com/video/BV1JZd1BiE7c/) | Lists a head/face/hair lesson and lessons about texture value relationships and adapting base animations. | Locate face and painting instruction without searching only English “anime Blockbench.” |
| [V] | [Paid course page](https://www.bilibili.com/cheese/play/ep1984702) | The page explicitly identifies paid lessons. | Public chapter names are verified; the paid teaching itself was not inspected. |
| [V] | 叶无道_M, [YSM physics usage](https://www.bilibili.com/video/BV1aMsUzBEZA/) | Author page dated 2025-10-27 lists a 4:23 physics lesson and a separate flowing-hair lesson. | Prefer this newer route before copying 2024 formulas. |
| [V] | 叶无道_M, [old physics tutorial](https://www.bilibili.com/video/BV14m42177zq/) and [old anti-gravity-hair tutorial](https://www.bilibili.com/video/BV1DF4m1K75J/) | Pages are explicitly marked old; the latter addresses hair orientation rather than just adding sway. | Historical reference; recheck against current YSM helpers. |
| [V] | 快乐的小盛子, [rigging and auxiliary bones](https://www.bilibili.com/video/BV1hj2CBWENz/) | Four-part series includes grouping, rigging/additional bones, a 57:18 expression/physics episode, and usage. | Another creator’s workflow; the page alone does not establish the formulas used in the video. |
| [V] | ゚烟雨画桥, [YSM effects/plugin series](https://www.bilibili.com/video/BV1aMgdzDEwx/) | Lists ribbon physics, path tracking, image-sequence import, and constraint-like tooling. | Advanced secondary motion and accessories; plugin outputs require runtime verification. |
| [V] | ゚烟雨画桥, [pose-controller example](https://www.bilibili.com/video/BV11GGN6XEj1/) | Author recommends studying the supplied examples; page links a tool collection and bone-constraint example. | A lead for authored constraints, not proof that Blender constraints export automatically. |
| [V] | 酒石酸菌, [Chinese Blockbench fundamentals](https://www.bilibili.com/video/BV1fk4y127qg/) | Ten-part collection includes painting, animation, UV menus, settings, and plugins. | Good terminology foundation; its 2020 UI is historical. |

[?] Suggested study sequence: geometry/proportions → pivots and extreme poses → face and hair groups → per-face UV → palette/textures → blinking and expression states → secondary motion → in-game validation. This ordering is a project synthesis of the curriculum, not an attributed quotation or a claim that the entire course was watched. [Workflow collection](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[V] The current YSM plugin instructions say to select `ysm-utils` for the mod version, keep its filename, and load it through Blockbench’s local-plugin menu. The page says current plugins support Blockbench 4.x and 5.x. [Plugin instructions](https://yesstevemodel.github.io/wiki/plugin/).

### Touhou Little Maid / 车万女仆

- [V] The current TLM model-start page says custom maid/cushion models and voice packs use Bedrock entity-model and animation formats, with a Blockbench helper plugin. [Current TLM documentation](https://tlmwiki.cfpa.team/wiki/model/start/).
- [V] 帕金伊’s 2020 beginner article advises postponing texture painting until the geometry is sufficiently stable, and manually setting pivots for parts not generated by the plugin. It links a short Hatsune Miku modeling demonstration. This is construction advice; the character design is not a reusable original-project asset. [Bilibili article, indexed text](https://www.bilibili.com/opus/393152218130102476).
- [V] The plugin’s primary repository is [TartaricAcid/TLM-Utils-Plugins](https://github.com/TartaricAcid/TLM-Utils-Plugins). [?] Its existence does not establish compatibility of every old plugin build with Blockbench 5.2.2.
- [C] The Chinese custom-pack tutorial describes name-driven presets such as `head`, `armLeft`, `armRight`, `legLeft`, `legRight`, `ahoge`, `blink`, tail/wing motion, and equipment locators. Preserve preset parent names when relying on those built-ins; manually animated extra groups need a deliberate hierarchy. [Chinese tutorial mirror](https://mcmod.robinmc.cn/post/2603.html).
- [C] A preserved 2020 MCBBS collection contains a creator reporting problems with skirt sitting poses, feedback that the character lacked recognisable visual features, and a reply admitting weak pixel-painting skills. This is useful evidence that static shape, texture identity, and seated deformation are separate problems. [MCBBS archive](https://archive.mcbbs.run/thread.html?t=1015497).
- [?] Do not apply older TLM claims that Bedrock animations are unsupported to the current system: an older forked guide says that, while the current maintainer documentation says model **and animation** formats are supported. Pin the TLM version before adopting a preset or export path. [Older fork guide](https://github.com/Demonese/TouhouLittleMaid-fork-for-pr/blob/1.20/docs/custom_model_pack.md), [current start page](https://tlmwiki.cfpa.team/wiki/model/start/).

## 3. Head, face, eyes, highlights, expression, and blinking

### Verified runtime recipes

[V] The YSM recipe page places pupil tracking in a `parallel` animation, using position offsets derived from head yaw/pitch. Its auto-blink recipe uses `pre_parallel`, hides open-eye geometry with scale, and shifts eyebrows. It describes an approximately four-second blink interval. These are model-part transforms, not image recognition or camera-aware AI. [YSM common Molang recipes](https://yesstevemodel.github.io/wiki/molang/common/).

```text
Pupil position X: ysm.head_yaw/180
Pupil position Y: ysm.head_pitch/360
Open-eye scale:  ysm.is_close_eyes ? 0 : 1
```

[V] The reference table also says `ysm.is_close_eyes` becomes true during sleep. It lists previous-frame bone queries and the first/second-order helper signatures. [?] A blink implementation should therefore distinguish a brief blink from a sleeping expression if the latter has different eyebrows/mouth. [Molang reference](https://yesstevemodel.github.io/wiki/molang/ref/).

[V] Gakuto1112’s CatMaid Japanese README describes an eye atlas divided into 6×6-pixel cells. Eye rows distinguish left/right and luminous/non-luminous portions. Columns contain normal, sparkling, surprised, threatened, downhearted, tired, and closed-eye variants. Eye/mouth textures have twice the resolution of other parts; mouth cells are 2×4 pixels. The avatar also advertises blinking, expression changes from health/food, and moving hair. **Its mixed face/body density is an example of a creator choice, not compliance with this project’s uniform 32 px/block rule.** [CatMaid README](https://github.com/Gakuto1112/CatMaid/blob/main/README_jp.md).

### Proposed Blockbench face construction

[?] Use a shallow head volume with a slightly narrower lower-face silhouette, then organise face details as independent children of the actual head bone: eye whites, pupil/iris plates, brows, closed-eye marks, mouth, and a tiny highlight layer. Make the neutral front/three-quarter/side silhouette readable before adding facial microgeometry. This is a suggested translation of the YSM transform recipes into an original model, not a verified YSM-required topology. [YSM recipes](https://yesstevemodel.github.io/wiki/molang/common/).

[?] Keep bangs outside the eye silhouette and reserve a broad, uninterrupted cheek area. A small nose is usually better conveyed by one restrained texture cluster than multiple protruding cubes at this scale. Prefer a few decisive jaw/cheek changes to a staircase of tiny cubes. Review both neutral and side views so the face does not become a flat mask attached to a large rectangular skull. [Head/face/hair curriculum lead](https://www.bilibili.com/video/BV1JZd1BiE7c/).

[?] For an initial approximately 16-pixel-wide face, try a 5–6-pixel-wide eye region: dark upper lash cluster, pale sclera, two iris values, a dark pupil, and one dominant highlight. These dimensions are **prototype targets**, not a community standard. Keep the two main highlights on the same apparent light side rather than mechanically mirroring their positions. Separate brows from pupils so concern, determination, fatigue, and surprise can share the same head geometry. [Relevant creator atlas example](https://github.com/Gakuto1112/CatMaid/blob/main/README_jp.md).

[?] The minimum useful face set is neutral, blink, smile, concern, determination, and fatigue. Build expressions as a small atlas or visible-part switches, not six complete duplicate heads. Closed eyes need a clear eyelid/lash mark; hiding the eyes alone can leave an unsettling blank face. Expression control should own the visible eye set while a blink timer modifies that state only when appropriate. [YSM blink mechanism](https://yesstevemodel.github.io/wiki/molang/common/).

[V] In YSM, a case-sensitive `ysmGlow` prefix enables a glowing group, and the rule acts on that group rather than automatically marking its descendants. [?] If highlights use this mechanism, separate them from lashes/sclera; do not make the entire eye glow merely to keep a one-pixel glint readable. [YSM modeling rules](https://yesstevemodel.github.io/wiki/tph2yetr/).

## 4. Hair layering and physics bones

### What the communities actually expose

[V] YSM lists `ysm.first_order(name, input, response)` and `ysm.second_order(name, input, frequency, coefficient, response)` as helpers introduced in 2.3.0. [Reference](https://yesstevemodel.github.io/wiki/molang/ref/). [V] The changelog explicitly associates first/second-order systems with simplified physical-motion calculations. [2.3.0 changelog](https://ysm.cfpa.team/wiki/log/230/).

[V] White_clams白蛤蜊’s Alice update description mentions changing hair physics, eye tracking, emissive highlights, blink animation, a rear-skirt alignment fix, and adding controllers. These are verified **author-reported changes**, not independent measurements. [Bilibili update](https://www.bilibili.com/video/BV144JJzNEjr/).

[V] Japanese creator 六色’s anime-hair essay distinguishes thin planes from volumetric locks. It proposes grouping bangs, side-bangs, side hair, and back hair, aligning subdivisions across locks sharing a bone, and spending more subdivisions toward moving tips than roots. The article concerns Blender/MMD cel-look hair; its topology advice needs adaptation for cuboids. [Author essay](https://note.com/rikuhayasaka/n/n5ab4a25233d1).

### Proposed construction and tuning

[?] Start with four visual masses: scalp cap, bangs, side locks, and back hair. Use broad overlapping strips/cuboids with progressively smaller tip pieces. Paint smaller strands into the texture. A small silhouette-changing lock deserves geometry; an interior strand that never affects the contour usually does not. This is a cuboid adaptation of the Japanese author’s grouping and root/tip distinction. [Hair essay](https://note.com/rikuhayasaka/n/n5ab4a25233d1).

[?] Parent roots to the head; place a short, two- or three-segment chain only in a genuinely moving lock, ponytail, braid end, or ribbon. Different locks can share motion when their pivot layout and silhouette permit it. Keep the cap stable so the hair does not slide off the scalp while the tips react. Start with front bangs almost rigid, side locks moderately responsive, and long back sections slower. [Newer YSM physics tutorial lead](https://www.bilibili.com/video/BV1aMsUzBEZA/).

[?] Treat “physics bones” here as an authored response system until a collision solver is verified. A spring-like helper is not evidence of cloth self-collision or automatic collision against the face/torso. Limit rotation, supply clearance around shoulders, and make a controlled pose take over during dramatic attacks/rolls if necessary. Use distinct state identifiers for independently simulated channels and verify state resets after teleport, reload, and model switching. [Helper API](https://yesstevemodel.github.io/wiki/molang/ref/), [orientation tutorial](https://www.bilibili.com/video/BV1DF4m1K75J/).

[?] Test start/stop, reverse movement, rapid yaw turns, stairs, jumping, falling, crouching, sitting, lying down, swimming, and all combat extremes. Run those tests at different frame caps. Hair that looks good in one walking preview can flip during a roll or lag excessively after a turn. Do not prescribe numerical frequency/damping settings without observing the installed runtime. [Physics tutorial](https://www.bilibili.com/video/BV1aMsUzBEZA/).

## 5. Slim bodies, waist, and restrained adult torso shaping

[V] The YSM course curriculum contains proportion, body-curve, base-body, and torso/extremity lessons. This verifies that adult body construction is part of the community’s teaching; public metadata does not verify a specific universally accepted body ratio. [Course collection](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[?] **Adult characters only:** design the body as chest/ribcage, waist, pelvis, upper/lower limbs, with proportions chosen from the approved original reference sheet. A modest taper between ribcage and pelvis creates a slimmer silhouette without an extreme pinched waist. Keep enough torso depth for shoulder rotation and a readable clothed silhouette. Do not shrink arm/leg pivots together merely to make the body thin; adapt attachment positions and the animation test poses. [Proportion/pivot curriculum](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[?] For restrained adult chest shaping, use a unified clothed upper-torso volume or shallow symmetric panels with small rotations and clean transitions into the side torso. Let coat seams, a breastplate, or fabric value changes supply most of the form. Avoid separate round protrusions, cleavage lines, exposed anatomy, or secondary-motion emphasis. A fitted jacket/armour can read as an adult design without sexualisation. This is a **project-specific non-sexual design proposal**, not an instruction claimed from the course. [Relevant body-construction curriculum](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[?] Place waist and hip accessories on their own stable attachment groups. A sash or coat front can suggest shape while allowing the underlying body to remain simple. Keep shoulders, elbows, hips, and knees aligned with the motion skeleton; texture and clothing variation should carry much of the character differentiation. [YSM attachment/group documentation](https://yesstevemodel.github.io/wiki/tph2yetr/).

[?] **Daisy gets a separate child design contract:** a natural child silhouette, loose layered pilgrim clothing, a weather cape, practical boots, a small satchel, and an original flower emblem. No adult chest-shaping groups, adult-body rescaling shortcut, revealing wardrobe switches, or suggestive motion. Child expressiveness should come from eyes, brows, head tilt, posture, and hand gestures. This follows the user’s brief, not a claim about all maid-model packs. Local source: [CONTEXT.md](CONTEXT.md).

## 6. Skirts, coats, and avoiding clipping

[C] The historical MCBBS skirt-sitting report and Chinese creator update notes show that clothing problems are often pose-specific. They do **not** establish an automatic no-clipping skirt technique. [MCBBS collection](https://archive.mcbbs.run/thread.html?t=1015497), [Alice alignment update](https://www.bilibili.com/video/BV144JJzNEjr/).

[V] Japanese BOOTH seller エメラル堂’s Amelia4 changelog mentions correcting lower-leg penetration, inverted shins in a sitting pose, ponytail/side-tail orientation, and a waist remaining bent after sneaking. These are author-reported fixes in a different littleMaidMob ecosystem, useful as test-case evidence rather than a TLM/YSM export recipe. [Amelia4 page](https://booth.pm/ja/items/7683276).

[?] **Proposed combat-friendly skirt:** waistband follows the pelvis; a few overlapping front/back/side panels form a shallow flared shell. Optional lower panel children provide controlled bending. Do not rigidly parent the whole skirt to one thigh: that drags the entire garment into the opposite leg. Do not assign the whole skirt to the upper chest: torso twists then produce unrelated hem movement. Test the proposed pelvis hierarchy with the actual combat animation set. [Joint-concealment curriculum](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[?] Keep a neutral-pose clearance envelope around both thighs and widen/tilt panels for stride extremes. Side splits, an open coat front, culottes, or layered trousers under a longer tunic are practical original-design options. Opaque inner layers maintain an age-appropriate silhouette when sitting or rolling. Use geometry overlaps with deliberate depth separation; coplanar faces can flicker, and large translucent layers can produce sorting artifacts. [YSM texture warning](https://yesstevemodel.github.io/wiki/texture/).

[?] Author corrective skirt/coat poses for high-knee running, crouch, sitting, roll, knockdown, overhead strike, and wide stance. Use a lower-cost sway layer for ordinary walking. In combat, corrective clothing motion should follow the final combat pose rather than an independent YSM walking cycle. A cloth-looking oscillation cannot guarantee collision clearance; inspect intermediate frames as well as endpoints. [Bridge pose-composition design](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat/blob/main/docs/implementation.ja.md).

[?] For noncombat NPCs, a longer robe is feasible if their animation set is deliberately restricted. For agile combatants, shorter split coat panels over trousers are a lower-risk prototype. This is a design tradeoff, not a requirement to make female combatants wear short skirts. [Historical seated-garment problem](https://archive.mcbbs.run/thread.html?t=1015497).

## 7. Accessories and runtime bone names

[V] YSM reserves locator/group names: `Head` gets view-following behavior; `AllHead` has first-person/Better Combat hiding behavior; `ViewLocator` positions the camera; `LeftHandLocator`/`RightHandLocator` anchor held items; `ElytraLocator` anchors elytra; `BackpackLocator` serves backpack placement. Missing hand locators can remove held-item rendering. These names are functional contracts, not just organisation labels. [Modeling documentation](https://yesstevemodel.github.io/wiki/tph2yetr/).

[?] Keep bows, goggles, flowers, earrings, cape clasps, scabbards, satchels, and prosthetic-arm ornaments in small local subtrees. Rigid accessories follow their attachment; dangling accessories receive only the bones their visible motion needs. Pair a model-space locator with an actual test item early, before making a detailed hilt or glove. [Locator reference](https://yesstevemodel.github.io/wiki/tph2yetr/).

[V] YSM’s Molang miscellaneous page distinguishes Curios on Forge/NeoForge from Trinkets on Fabric, whose slot types need separate adaptation. [?] Costume buttons or accessories driven by those conditions must be validated on NeoForge, rather than inferred from a Fabric showcase. [Molang miscellaneous documentation](https://yesstevemodel.github.io/wiki/molang/misc/).

## 8. 32 px/block painting, cel-look shading, and thin-detail UVs

### A verified UV rule that changes modeling choices

[V] YSM 2.6.0+ defines a UV unit as configured resolution divided by actual texture resolution. Nonzero-area faces must have UV positions/sizes on integer multiples of that unit, and dimensions must be at least one unit in absolute value. The guide specifically warns about sub-unit box-UV cubes and zero UV dimensions after conversion. It recommends valid per-face UVs or appropriate larger-cube/negative-inflate construction; near-zero geometry still incurs rendering work. The rule’s scope also distinguishes older encrypted packages. [YSM UV standard](https://yesstevemodel.github.io/wiki/ysm-uv-standard/).

[?] Consequently, thin eyelids, hair tips, skirt edges, and jewellery should not rely on “almost zero” cubes with accidental box UVs. Assign each visible face a legitimate texel region; remove unused faces explicitly. Test the exported runtime image, since a correct-looking Blockbench preview can conceal an invalid UV allocation. [UV standard](https://yesstevemodel.github.io/wiki/ysm-uv-standard/).

[V] YSM texture documentation requires PNG and warns that multiple overlapping semitransparent textures can render incorrectly. [?] Prefer opaque painted shading and cutout edges for hair/lashes over many translucent planes. [Texture documentation](https://yesstevemodel.github.io/wiki/texture/).

### Proposed texture convention for the original characters

[?] **32 px/block is density, not a 32×32 whole-character atlas.** With a model convention of 16 authored units per block and unit runtime scale, a face measuring eight units needs about sixteen pixels across to meet 32 px/block. The general calculation is `pixels = 32 × visible world length in blocks`; include any runtime scaling. YSM’s manifest includes height/width scale settings, so an atlas is not density-correct merely because it is 256² or 512². This is a calculation from the project density requirement and runtime scale fields. [Manifest documentation](https://yesstevemodel.github.io/wiki/struct/).

[?] For a cel-like painted texture, begin with base, shadow, and restrained highlight for each material. Use broad shadow clusters under bangs, chin, collar, coat overlap, and skirt folds. Keep skin relatively quiet; allocate contrast to the eyes, hair silhouette, and signature costume motif. Paint a few broad hair shine bands following lock direction rather than noisy single-pixel streaks everywhere. These are proposed art rules, not verified quotations from a 32px YSM manual. [Chinese value/painting curriculum](https://www.bilibili.com/video/BV1JZd1BiE7c/).

[?] Reserve a separate UV island for asymmetric identifiers, such as an original prosthetic-arm emblem or flower clasp. Mirror low-information gloves/boots when appropriate, but avoid mirrored text and keep facial highlight direction consistent. Do UV reuse before painting unique detail. [UV-copy/mirroring lesson listing](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[?] Painted cel-look shading and a runtime toon-lighting shader are different deliverables. Keep a stable painted base first and evaluate it under both plain rendering and the selected Iris shader. PBR shininess/emission is not automatically a two-band anime-lighting system. Do not brighten the whole face to compensate for a dark environment until the shader and material path have been checked. [YSM manifest/PBR fields](https://yesstevemodel.github.io/wiki/struct/).

[?] No verified source in this pass specified a universal YSM “three colors per material,” exact eye size, or fixed 32px anime texture template. Keep those values in the project art contract as adjustable targets, not community requirements.

## 9. Cube, bone, and animation budgets

[?] No authoritative YSM/TLM/BOOTH source located here gave a recommended cube/bone budget guaranteeing 50 fps on the project PC. Keep the existing project performance policy and add a **detail allocation**, not an alleged mod limit.

| Proposed detail allocation | Starting target [all ?] | Reason to spend more |
| --- | --- | --- |
| Face detail | 6–12 auxiliary groups, including expression parts | Close-up dialogue needs separate brows/pupils/mouth. |
| Hair secondary motion | 4–8 moving chains, mostly 2 segments each | A signature braid or long ponytail changes the silhouette. |
| Skirt / coat | 4–8 independently controlled panels; add lower segments selectively | Wide attacks expose repeated clipping in a tested pose. |
| Dangling accessories | 0–4 short chains | Item is visible from normal play distance and communicates character identity. |
| Costume variants | Shared body with selective visibility/atlas changes | A plot-critical alternate costume, not every incidental cosmetic. |

[?] These sub-budgets count within the existing whole-character budget; they are not extra allowances to stack on top. Reduce hidden parts, redundant nested groups, and microcubes before removing eyes or key silhouette masses. Record cube count, visible faces, total groups, animated groups, active expressions, texture dimensions, material passes, and concurrent characters. A bone number alone cannot measure controller complexity or shader cost.

[V] The bridge implementation documents twenty humanoid combat joints plus up to 980 independent model bones within a 1,000-pose layout. **That is an implementation capacity, not a suggested artistic budget or performance promise.** [Implementation](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat/blob/main/docs/implementation.ja.md).

[?] Do not cite claims such as “Minecraft universally refuses models over 1,500 triangles.” Such limits depend on the loader/runtime, and this research did not verify that assertion for YSM, GeckoLib, or Epic Fight.

## 10. Animation controllers: separate cosmetic motion from combat ownership

[V] YSM distinguishes lower-priority `pre_parallel` from higher-priority `parallel`. Its special parallel blend adds rotations but does not add translations/scales. Therefore a decorative rotation can accumulate with locomotion; the same assumption does not hold for visibility scaling. [Parallel-animation documentation](https://yesstevemodel.github.io/wiki/animation/parallel/).

[V] YSM 2.3.0 introduced Bedrock animation controllers. Files are registered through `files.player.animation_controllers`; named controller slots replace earlier hardcoded behavior. Documented slots include `player.main`, `player.pre_main`, `player.post_main`, parallel slots, held-item/use/swing slots, GUI slots, and maid slots. The page exposes `ctrl.*` conditions and animation-finished queries. It also warns that the GeckoLib plugin can interfere with importing controllers into Blockbench. [Controller documentation](https://yesstevemodel.github.io/wiki/controller/).

[?] Suggested ownership for a character adapter:

| Channel | Owner | Bones / state |
| --- | --- | --- |
| Combat pose | Epic Fight | Root/body, limbs, attack timing, weapon anchors. |
| Face state | One cosmetic state machine | Eye variant, blink, brows, mouth. |
| Hair/accessory response | One secondary-motion evaluator | Only designated auxiliary groups. |
| Skirt/coat correction | Pose-aware cosmetic layer | Pelvis-relative panels, with attack/roll corrections. |
| Costume switch | Equipment/story state | Visibility and atlas selection, independent of attack loops. |
| Cutscene performance | Cutscene runtime while explicitly active | Deliberate full-body performance and dialogue face states. |

[?] Each transition should define a priority, reset condition, and blend policy. Blink must not cancel a concerned expression; an emote must not overwrite a live combat attack; hair expressions must not drive the arm bones. This table is a proposed adapter contract, not a guaranteed cross-mod ABI. [YSM layer semantics](https://yesstevemodel.github.io/wiki/animation/parallel/), [bridge design](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat/blob/main/docs/implementation.ja.md).

[V] GeckoLib 4’s controller documentation says simultaneous animations need multiple controllers, warns that two controllers acting on the same bone can conflict, and describes registration order as affecting final priority. [?] For custom NPCs, split face/accessory bones from locomotion/action bones and translate the *concepts* of YSM cosmetics into GeckoLib code. The `ysm.*` helper expressions are not automatically portable just because both exports contain JSON. [GeckoLib 4 controller guide](https://github.com/bernie-g/geckolib/wiki/Defining-Animations-in-Code-(Geckolib4)).

## 11. Epic Fight compatibility: verified alternatives and limits

### A. YSM Epic Fight Compat — actual 1.21.1 release

[V] The tagged 1.0.0 source specifies Minecraft 1.21.1, NeoForge 21.1.235+, Epic Fight 21.17.3.1 with range `[21.17.3.1,21.18)`, YSM 2.6.0+ for the target platform, and YSM Mapping API exactly 0.1.8 in the build properties. The release note says Mapping API 0.1.8 or later; for a reproducible prototype, use the source-pinned baseline rather than assuming every later API build is interchangeable. [Tagged gradle.properties](https://raw.githubusercontent.com/sakuraimikoto33/YSM-EpicFight-Compat/1.0.0-mc1.21.1/gradle.properties), [releases](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat/releases).

[V] Its documented approach compiles Bedrock geometry into an Epic Fight `HumanoidMesh`, maps humanoid roles, retains auxiliary model hierarchies, and composes cosmetic poses with combat skin matrices. Normal rendering remains YSM’s responsibility; the bridge takes over Epic Fight’s overridden rendering path. This explains why installing two renderers without a bridge is insufficient. [Japanese implementation documentation](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat/blob/main/docs/implementation.ja.md).

[V] The README advertises first/third-person support, model controllers and secondary motion, multiplayer cosmetic synchronization, and an Iris PBR bridge on 1.21.1. It also says converted models hide armor/head equipment, need one usable elytra locator, and fall back to Epic Fight’s default mesh when conversion is unavailable. [Primary README](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat).

[?] **Research recommendation:** make this the first player-model integration experiment. Use an original unencrypted folder model with standard humanoid roles, minimal face/hair cosmetics, and clear hand locators. Establish working attacks/guard/roll before adding elaborate clothing. This report verified documentation, source constraints, and distribution; it did **not** install the JAR or test a game client.

[?] Required practical checks: ordinary/battle-mode handoff; both views; skin/model reload; asymmetric arm attachments; all weapon grips; death and knockdown; large coat/long-hair poses; another client seeing the same model; armor/elytra behavior; Iris on/off; shader shadow pass; and frame times in the intended boss encounter. These follow the advertised features and the project’s actual use cases. [README](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat).

[V] A stale search snapshot of the CurseForge landing page showed only Forge 1.20.1/0.6.0; the subsequently opened file list and specific release showed NeoForge 1.21.1/1.0.0. **Use the specific versioned file, not an old search snippet, for compatibility decisions.** [Current file list](https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat/files/all).

### B. Chinese YSMEF listing — different project, different evidence

[C] MC百科’s `YSMEF` entry lists Forge 1.20.1. It describes extracting YSM meshes through OpenYSM/YSMParser, and reports clipping, separated arms/body, complex-geometry errors, and no server verification. Do not merge these caveats into the identity or support table of sakuraimikoto33’s bridge. The MC百科 project is a separate historical/experimental lead. [MC百科 YSMEF](https://www.mcmod.cn/class/29276.html).

### C. YesEpicFightModel — an Epic Fight mesh pipeline

[V] `P1neapplell0/YesEpicFightModel` calls itself Epic Fight Mesh Model Mod. Its Chinese README specifies Minecraft 1.20.1, Forge 47.3.0+, and Epic Fight 20.9.x. Models use Blender/Epic Fight-exported armature/mesh JSON, `config.json`, texture PNG, and optional PBR companions. Despite its repository name, the documented input is **not a promise to directly load any YSM package**. [Primary repository](https://github.com/P1neapplell0/YesEpicFightModel).

[?] This is a useful architectural fallback: preserve the approved cuboid visual design, build a skinning/rig adapter, and export to Epic Fight’s native mesh contract. It needs implementation or porting work for this project; it is not a ready-made 1.21.1 dependency.

### D. Figura + Fightura — another kind of bridge

[V] Fightura’s author describes attaching Figura parts to Epic Fight joints through a render layer, with automatic naming/parent-type mapping or Lua overrides. The installation page targets Minecraft 1.20.1 Forge, Figura 0.1.5, and Epic Fight 20.14.15.1+. It avoids a YSM mesh conversion by synchronising part transforms. [Primary author documentation](https://fightura.isaacdev.org/), [installation](https://fightura.isaacdev.org/install/).

[?] This is evidence that different custom-player-model systems need different compatibility mechanisms. It does not establish a 1.21.1 NeoForge route or prove compatibility of every Japanese Figura avatar with the project stack.

### E. TLM maids and combat NPCs

[V] EpicFight：TouhouLittleMaid currently lists Minecraft 1.20.1 and Forge on Modrinth. The newer player bridge explicitly keeps its 1.21.1 maid adapter inactive without the required mods and states that EFTLM has no 1.21.1 release. [Modrinth versions](https://modrinth.com/mod/epicfight_touhoulittlemaid/versions), [bridge README](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat).

[?] Therefore, use YSM/TLM as modeling references and optional player-rendering infrastructure; do not make all story NPC combat depend on a verified 1.21.1 TLM–Epic Fight integration that this research could not find. The custom NeoForge NPC/boss renderer remains a separate integration task. Reusing a visual style does not reuse a combat entity’s behavior or skinning contract.

## 12. Japanese creators, BOOTH sellers, and transferable practices

| Evidence / primary source | Useful finding | Boundary |
| --- | --- | --- |
| [V] [Gakuto1112 CatMaid](https://github.com/Gakuto1112/CatMaid) | Original avatar with layered face atlas, moving hair, expressions, accessories, and an editable source repository. | Figura assets/scripts need runtime translation for YSM/GeckoLib/Epic Fight. |
| [V] [Gakuto1112 FiguraBlueArchiveCrafters](https://github.com/Gakuto1112/FiguraBlueArchiveCrafters/blob/main/README_jp.md) | Japanese author documents character-specific effects, visible weapon substitutions, expressive actions, and downloadable avatars. | Author explicitly distinguishes visual effects from gameplay. Study non-sexual face/rig organisation; do not copy franchise designs or skill cut-ins. |
| [V] [MyFiguraAvatarPacker](https://github.com/Gakuto1112/MyFiguraAvatarPacker) | Creator’s packaging workflow preserves LICENSE, produces Japanese/English readmes, and removes development-only reference images without changing source. | Useful distribution convention; it does not grant rights to bundled franchise designs. |
| [V] [Vo Workshop: Kaguya](https://booth.pm/ja/items/8008682) | Actual Minecraft Figura female-character download with named animation/physics libraries and credits. | A Touhou fan asset, not an original project character or YSM model. |
| [V] [しまシャツ: Wagi’s Furry Player](https://booth.pm/ja/items/8142480) | Editable `.bbmodel`, Lua, PNG, PSD/Affinity sources; separate skin/clothes textures; palette changes through gradient maps. | Furry template rather than a directly applicable human adult body; inspect redistribution terms. |
| [V] [bulud: Blockbench Witch set](https://booth.pm/en/items/5121437) | Confirms a seller supplying `.bbmodel` with explicit restrictions. | Format match does not mean modification or map redistribution is permitted. |
| [V] [エメラル堂: Amelia4](https://booth.pm/ja/items/7683276) | Multiple maid and armor textures, pose fixes, and explicit tested versions. | littleMaidMob/LMRB ecosystem, not synonymous with Chinese Touhou Little Maid. |
| [V] [歌乃: Blockbench modeling article](https://www.mayonakanouta.com/blog/blockbench-minecraft) | Japanese creator tutorial separates editing, painting, and animation in a Bedrock-addon workflow. | Useful interface vocabulary; its addon deployment instructions are not Java NeoForge instructions. |

[?] The strongest Japanese transfer is **organisation**: separate expression textures, author clear component credits, provide editable sources, and distinguish cosmetic demonstrations from game mechanics. The research does not show a Japanese consensus body ratio or that BOOTH’s general VRM/FBX catalog is Minecraft-ready.

## 13. Korean creator sources and observations

- [V] **도미노 한국인 / Pixel Creator’s Place** publishes Korean Blockbench lessons. The interface/UV lesson distinguishes box UV from per-face UV and recommends per-face UV for flexible face placement. It teaches Java block/item projects, so its rotation/export constraints must not be carried over wholesale to animated entity formats. [Creator’s Tistory lesson](https://pixelcreatorsplace.tistory.com/8), [DC Inside repost](https://gall.dcinside.com/board/view/?id=minecraft&no=102024).
- [V] **Potan** has a Korean Animated Java series. Its basic lesson stresses putting elements into groups, animating groups, node inclusion/exclusion, and checking the bounding box against motion. The variants lesson changes textures/NBT while sharing geometry; the locator/camera lesson discusses timed commands and cutscene cameras. These are useful for a staged NPC/cutscene version, not a player-model compatibility bridge. [Basics](https://potangaming.tistory.com/323), [variants](https://potangaming.tistory.com/324), [locators/camera](https://potangaming.tistory.com/325?category=1270951).
- [C] A Korean server operator reports YSM faces obstructing the first-person Better Combat view and suggests disabling that animation setting as a workaround. This is **Better Combat**, not Epic Fight. It supports testing head/hair/camera clearance but does not prove an Epic Fight bug or solution. [DC Inside server report](https://gall.dcinside.com/mgallery/board/view/?id=steve&no=389605).
- [C] A Korean Blockbench study-group announcement describes recurring equipment/furniture/entity exercises and feedback on concepts/details. It confirms an active local creator-learning route but contains no verified anime-face or cloth recipe. [DC Inside announcement](https://gall.dcinside.com/board/view/?id=minecraft&no=213703).
- [?] Searches of Arca Live/Ruliweb/Naver did not produce a verifiable Korean YSM face/hair-construction guide in this pass. Arca results for “YSM” often referred to unrelated AI-chat modules; those were excluded. Naver Cafe was blocked by robots restrictions. This is a coverage limitation, not evidence that Korean creators do not make such models.

## 14. Model licenses: concrete source-by-source distinctions

| Evidence / asset or code | Verified terms | Consequence for the original map |
| --- | --- | --- |
| [V] [YSM generated default template](https://yesstevemodel.github.io/wiki/tph2yetr/) | The maintainer labels the generated `custom/default` model CC0 and permits modification/distribution. | A promising reusable technical base; this statement does not cover every bundled or third-party YSM character. |
| [C] [甜栗子 original-model Tieba thread](https://tieba.baidu.com/p/10956250902), [accessible forum index](https://tiebac.baidu.com/f/good?cid=0&ie=utf-8&kw=minecraft&pn=0) | Indexed author introduction calls the original template CC-BY 4.0 and invites modifications, resales, and teaching use. | Strong lead for a cleaner teaching base, but the thread/package license was not fetched; verify the actual archive and attribution instructions before reuse. |
| [V] [CatMaid LICENSE](https://raw.githubusercontent.com/Gakuto1112/CatMaid/main/LICENSE) | MIT, copyright Gakuto1112; retain the required notice. | Useful source-data/script base subject to included third-party component terms. |
| [V] [FiguraBlueArchiveCrafters LICENSE](https://github.com/Gakuto1112/FiguraBlueArchiveCrafters/blob/main/LICENSE) | Distinguishes author programs/data from Blue Archive IP; requires official fan guidelines and attribution; prohibits commercial use/sale of the complete fan project. | Do not read “MIT” as permission to adopt the franchise design/branding as an original character. |
| [V] [Vo Workshop Kaguya](https://booth.pm/ja/items/8008682) | Says MIT for its data while prioritising Touhou fan guidelines; credits MIT animation libraries and LGPL-2.1 Swinging Physics. | Separate character rights, model rights, and component code rights. |
| [V] [Wagi template](https://booth.pm/ja/items/8142480) | Permits commercial use, but not distributing/selling unchanged data while falsely claiming authorship. | The visible page is not a blanket formal license; preserve its readme/credits and verify the intended distribution. |
| [V] [bulud Witch set](https://booth.pm/en/items/5121437) | Requires credit in works such as videos; forbids redistribution and modification of models/textures. | A purchased editable-format file is not a suitable modifiable redistributable map asset under those terms. |
| [V] [Amelia4](https://booth.pm/ja/items/7683276) | Forbids unauthorised reposting/commercial use and AI training; allows gameplay screenshots/videos, including monetised video sites. | “Gameplay use” does not establish map-bundling rights. Read the included terms; this research did not download its model. |
| [V] [YSM Epic Fight Compat](https://github.com/sakuraimikoto33/YSM-EpicFight-Compat) | MIT for the compatibility project. | Does not grant a license to user-supplied models. |
| [V] [EpicFight_TouhouLittleMaid repository](https://github.com/xssfww/EpicFight_TouhouLittleMaid/) | Maintainer explicitly marks internal art assets ARR and says they need author permission. | Do not infer art reuse rights from available source code or a community description of code licensing. |

[?] Recommended asset record: original author; source URL; retrieved version/date; geometry license; texture license; animation/script license; underlying character/IP restrictions; required credits; modification permission; redistribution permission; and the exact files reused. Prefer original designs plus explicitly reusable templates. Encryption is a distribution format, not permission to convert or republish a model. [YSM conversion permission warning](https://ysm.cfpa.team/wiki/trans/netease/).

## 15. Evidence quality, missing platforms, and actionable next experiment

- [V] Search and retrieval artifacts from this pass are inside `research/r2/codex_raw/`; fetched page texts and URL metadata are in `codex_raw/modeling/`, with selected built-in web outputs in `web_evidence.txt`. No game installation or runtime benchmark was performed.
- [?] Bilibili public descriptions/chapter lists were readable through search, but direct article opening sometimes returned a CAPTCHA and the public video-info API returned HTTP 412. **No Bilibili comment corpus or video transcript was successfully obtained.** Video statements here are limited to page metadata/author descriptions, not invented spoken instruction.
- [?] Tieba’s forum index was retrieved and its template-thread URL extracted, but the thread itself reset/failed. Its license is accordingly tagged [C]. NGA/Zhihu searches produced no model-construction source strong enough to include as verified evidence.
- [?] Pixiv/Nicovideo/X searches did not yield a directly inspected Minecraft face-construction tutorial. Japanese BOOTH listings, author GitHub sources, a creator blog, and an anime-hair essay supplied the useful evidence. FANBOX links were visible on seller pages but their contents were not inspected; no paywall was bypassed.
- [?] Some broad queries returned promotional AI-modeling articles or machine-localised pages. Those were excluded as evidence of regional creator practice. No universal regional consensus is claimed.
- [?] **Next experiment:** author one original adult clothed humanoid and a separate age-appropriate Daisy blockout. First prove face readability, UV validity, hand attachment, and the target Epic Fight bridge using the adult model. Then add one hair chain and one coat panel at a time. Use identical reference geometry for NPC/cutscene adapters, but implement each runtime’s naming, animation, and attachment contract explicitly. The character silhouettes and all visible source expression remain original. [Target release](https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat/files/8857201), [UV rule](https://yesstevemodel.github.io/wiki/ysm-uv-standard/).

## Summary

[V] Chinese YSM sources provide the clearest directly applicable path: version-matched `ysm-utils`, a standard humanoid hierarchy, explicit face transforms, parallel cosmetic layers, and Bedrock animation controllers. Bilibili’s 叶无道_M course is officially referred by YSM and covers proportions, pivots, joint concealment, UV reuse, painting, and hair. Its public curriculum was verified; paid teaching and video speech were not. [Referral](https://yesstevemodel.github.io/wiki/video/), [course](https://www.bilibili.com/video/BV1eCuKzSEQ6/).

[V] A major integration finding is a **released NeoForge 1.21.1 YSM Epic Fight Compat 1.0.0**, with source targeting Epic Fight 21.17.3.1. [Versioned release](https://www.curseforge.com/minecraft/mc-mods/ysm-epic-fight-compat/files/8857201), [source constraints](https://raw.githubusercontent.com/sakuraimikoto33/YSM-EpicFight-Compat/1.0.0-mc1.21.1/gradle.properties). [?] This makes player-model integration worth prototyping, but documentation/release verification is not a tested performance or visual guarantee. The Chinese YSMEF experiment, older Blender-based YesEpicFightModel, and Figura/Fightura are separate projects with separate limits.

[V] **TLM combat integration remains a different question:** EpicFight：TouhouLittleMaid currently lists Forge 1.20.1. [Versions](https://modrinth.com/mod/epicfight_touhoulittlemaid/versions). [?] Do not assume that a working player bridge supplies combat behavior/rendering for all original story NPCs.

[V] Japanese CatMaid demonstrates separate expression atlases and non-luminous/luminous face components. [Japanese documentation](https://github.com/Gakuto1112/CatMaid/blob/main/README_jp.md). [?] Transfer this organisation into original faces: decisive eye clusters, separate brows/pupils, a closed-eye mark, and restrained highlights. Group hair into a stable cap, bangs, side locks, and back sections, then animate only a few silhouette-important chains. Treat spring-like motion as secondary animation, not verified collision-aware cloth.

[?] Adult slimness should come from moderate clothed torso taper, sensible limb attachment, and costume seams/armour. Keep chest shaping shallow and unified. Daisy receives a separate child silhouette, loose practical pilgrim clothing, boots/satchel, and expressive gestures; no adult shaping or revealing variants.

[?] Skirt safety needs pelvis-relative panels, clearance, and corrective poses for running, sitting, crouching, rolling, and wide attacks. No universal automatic no-clipping method was verified. Korean lessons add per-face UV and Animated Java organisation, while a Korean player report reinforces first-person clearance testing. [Korean UV lesson](https://pixelcreatorsplace.tistory.com/8), [AJ lesson](https://potangaming.tistory.com/323).

[V] YSM’s 2.6+ UV standard is especially relevant to thin lashes/hair: visible faces need valid nonzero UV dimensions on the defined texel grid. [UV rules](https://yesstevemodel.github.io/wiki/ysm-uv-standard/). [?] “32px” means world-space density, not a 32² character atlas. Use broad painted value clusters and check the final shader; budget proposals are unbenchmarked, not mod limits.

[V] Licenses differ sharply: YSM’s generated default is CC0; CatMaid is MIT; some BOOTH assets forbid modification/redistribution; fan models retain underlying franchise restrictions. [Default terms](https://yesstevemodel.github.io/wiki/tph2yetr/), [CatMaid license](https://raw.githubusercontent.com/Gakuto1112/CatMaid/main/LICENSE), [restricted BOOTH example](https://booth.pm/en/items/5121437). [?] Prefer original designs and explicitly reusable technical bases, and record geometry, textures, animation/scripts, and underlying IP separately. Bilibili comments, private Naver cafes, and several poorly indexed regional platforms remain coverage gaps.
