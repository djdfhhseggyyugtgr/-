# Round 2, extra branch 5: Total-conversion UI on Minecraft 1.21.1 + NeoForge

Date: 2026-10-14. Scope: replace every piece of vanilla UI and "vanilla feel" so the game plays like a standalone anime soulslike (AI LIMIT-like HUD: LP bar with a segmented Sync gauge above it, heal-item counter, left-arm ability icon, spell slots, currency, boss bar).

**Tags:** [V] verified in a primary source (NeoForge/Epic Fight/mod source code at the 1.21.1 branch, the vanilla 1.21.1 client jar, official docs, Modrinth API) · [C] community report or single secondary source · [?] uncertain, inferred, or needs an in-game test.

**Method.**
- Web search and fetch through the user's Ollama API (`tools/osearch.py`), Reddit through Arctic Shift, YouTube transcripts (`tools/social.py`).
- Mod versions and licences from the Modrinth API (fetched through Ollama `web_fetch`), filtered to `game_versions=["1.21.1"]` and `loaders=["neoforge"]` on 2026-10-14.
- Primary code read from shallow clones:
  - NeoForge, branch `1.21.1` (`neoforged/NeoForge`)
  - Epic Fight, branch `1.21.1` (HEAD = 21.17.3, 2026-05-26; we pin 21.17.3.1)
  - Kingdom Keys 2, branch `1.21.1`
  - the vanilla 1.21.1 client jar and asset index from Mojang's piston-meta
- Raw data: `research/r2/5/` (fetch JSON), `research/r2/5_src/` (clones and the NeoForge changelog), `research/r2/5_jar/` (client jar and asset index).

Related prior notes, not repeated here:
- `research/notes_gameplay.md` covers FancyMenu/Drippy, Enhanced Boss Bars, Glyphsmith/HUDEngine and FlexHUD.
- `research/notes_render.md` covers the Iris core-shader limitation.
- `r2/notes_3b_level_design.md` covers Shoulder Surfing defaults.

---

## 0. Key facts that change the plan

1. **[V] NeoForge 21.1.x already has everything needed for a full HUD replacement in code.**
   - There are 25 named vanilla HUD layers.
   - Any layer can be cancelled, replaced or wrapped.
   - Data attachments now **auto-sync** to the client.
     - Syncable attachments were backported in **21.1.197**; `wrapLayer`/`replaceLayer` in **21.1.190**.
     - The NeoForge 1.21.1 docs page still says attachments must be synced by hand. That page is out of date.
   - Source: changelog <https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.259/neoforge-21.1.259-changelog.txt> (lines "21.1.197 Backport to 1.21.1: Syncable Data Attachments (#2544)" and "21.1.190 … Add method to wrap gui layers (#2444)").
   - Our pinned loader is 21.1.259, so both are available.
2. **[V] Epic Fight 1.21.1 draws its HUD as four named GUI layers:** `epicfight:stamina_bar`, `epicfight:skills`, `epicfight:weapon_innate`, `epicfight:charging_bar` (`ClientModBusEvent.java` lines 102–108). We can cancel each one by name. No mixin is needed.
3. **[V] Vanilla 1.21.1 has no tooltip sprites.**
   - The `tooltip/` sprite group is empty in the 1.21.1 jar.
   - `tooltip_style` is a 1.21.2+ component; `tooltip_display` is 1.21.5+.
   - Custom tooltip frames therefore need code (NeoForge `RenderTooltipEvent`) or a tooltip mod.
4. **[V] A resource pack can't do the whole job reliably here.** The server-style "core shader HUD" tricks (MCC Island, Origin Realms) are ignored by Iris whenever a shader pack is active. We plan to ship Iris with a shader pack (docs/research §2), so the HUD must be drawn by Java code.
5. **[V] FancyMenu (DSMSLv3.1) can restyle and override every vanilla or modded screen with no code.**
   - It sets the window title and icon and handles the title-screen music.
   - With Drippy plus its early-loading module, it also covers the loading screens, including NeoForge's early window, on 1.21.1.
   - Licence constraint: list it as a dependency. Never bundle the jar.

---

## 1. HUD replacement in code

### 1.1 GUI layer API (NeoForge 21.1.x)

**[V] The vanilla layer IDs come from `VanillaGuiLayers` (1.21.1 branch), listed in render order:**
1. `camera_overlays`
2. `crosshair`
3. `hotbar`
4. `jump_meter`
5. `experience_bar`
6. `player_health`
7. `armor_level`
8. `food_level`
9. `vehicle_health`
10. `air_level`
11. `selected_item_name`
12. `spectator_tooltip`
13. `experience_level`
14. `effects`
15. `boss_overlay`
16. `sleep_overlay`
17. `demo_overlay`
18. `debug_overlay`
19. `scoreboard_sidebar`
20. `overlay_message` (action bar)
21. `title`
22. `chat`
23. `tab_list`
24. `subtitle_overlay`
25. `saving_indicator`

Source: <https://github.com/neoforged/NeoForge/blob/1.21.1/src/main/java/net/neoforged/neoforge/client/gui/VanillaGuiLayers.java>

**[V] How the NeoForge `Gui.java` patch groups the layers:**
- Health, armour and food form a sub-manager. It renders only when `gameMode.canHurtPlayer()`.
- Everything except `sleep_overlay` is skipped while `options.hideGui` (F1) is on.
- `leftHeight` and `rightHeight` are reset to 39 each frame so modded bars can stack.
- Source: `patches/net/minecraft/client/gui/Gui.java.patch`.

**[V] `RegisterGuiLayersEvent` (mod bus, client only):**
- `registerBelowAll`, `registerBelow(other, id, layer)`, `registerAbove(other, id, layer)`, `registerAboveAll`
- `replaceLayer(id, replacement)` and `wrapLayer(id, UnaryOperator)`, added in 21.1.190.
- `wrapLayer` is the intended way to move or resize an existing layer (pose transform).
- `replaceLayer` throws if the ID is not registered yet. To replace another mod's layer, run at a lower priority.
- Source: <https://github.com/neoforged/NeoForge/blob/1.21.1/src/main/java/net/neoforged/neoforge/client/event/RegisterGuiLayersEvent.java>

**[V] Events on the game bus:**
- `RenderGuiLayerEvent.Pre` is cancellable per layer (`getName()`). `.Post` follows it.
- `RenderGuiEvent.Pre` is cancellable for the whole HUD.
- `GuiLayerManager.renderInner` posts Pre/Post around every layer, vanilla and modded alike.
- Source: `client/gui/GuiLayerManager.java` lines 54–70.

**Recommended pattern [V API / ? design]:**
- On the mod bus, call `registerAbove(VanillaGuiLayers.CAMERA_OVERLAYS, id, layer)` for each of our layers: LP/Sync, quick slots, currency, status icons, lock-on, boss bars, banners and the death overlay.
- On the game bus, cancel these in `RenderGuiLayerEvent.Pre`:
  - `HOTBAR`, `EXPERIENCE_BAR`, `EXPERIENCE_LEVEL`, `PLAYER_HEALTH`, `ARMOR_LEVEL`, `FOOD_LEVEL`, `AIR_LEVEL` (or restyle it), `SELECTED_ITEM_NAME`, `EFFECTS`, `BOSS_OVERLAY` (or use §1.7), `JUMP_METER`, `VEHICLE_HEALTH`
  - the four `epicfight:*` layers
  - `DEBUG_OVERLAY` and `CHAT` in release builds
- Keep `TITLE`, `SUBTITLE_OVERLAY` and `CAMERA_OVERLAYS`. Restyle them through fonts and sprites.

**Reference implementations on 1.21.1 NeoForge:**
- **Kingdom Keys 2** 2.9.4d-1.21.1 (2026-10-11), LGPL-3.0, <https://modrinth.com/mod/kingdom-keys-2>, source <https://github.com/Wehavecookies56/Kingdom-Keys/tree/1.21.1>. It is the closest thing to a total-conversion HUD for an action RPG.
  - [V] `client/ClientSetup.java` lines 130–150 register 20 layers: HP bar, MP bar, drive gauge, command menu, player portrait, lock-on, party HUD, shotlock, item-get pop-ups, minimap and others.
  - [V] Lines 214–242 cancel layers conditionally, including vanilla `PLAYER_HEALTH`.
  - [V] It also ships a HUD editor screen (`HUDEditorScreen`), a custom KO/death screen (`client/gui/KOGui.java`) and a `RegisterDimensionTransitionScreenEvent` loading screen.
- **RPG-HUD** 3.13 (2026-06-20), GPL-3.0, <https://modrinth.com/mod/rpg-hud>, src <https://github.com/Raelzaryn/RPG-Hud>. [V] It replaces the vanilla health/food/XP bars with an RPG frame.
- **Stardew HUD (星露谷HUD)** 1.2.5, CC0-1.0, <https://modrinth.com/mod/stardew-hud>, src <https://github.com/Weatheraintbad/StardewHUD>. [V] Chinese-made full HUD reskin under CC0, so its code may be copied freely.
- **Souls Message Banners** 1.2.2 (1.21.1 NeoForge), MIT, <https://modrinth.com/mod/souls-message-banners>, src <https://github.com/tablesouls/souls_message_banners>. [V] Elden Ring-style event banners. Useful as a reference for the death and area-name banners. Write our own text.
- **Souls Combat HUD**, MIT, <https://www.modpackindex.com/mod/166327/souls-combat-hud>. [V] Soulslike quick slots, crest, status bars, boss bar and an "alternative skill overlay UI for Epic Fight". **1.20.1 Forge only**, so use it as reference code, not as a dependency.

### 1.2 Hiding or replacing Epic Fight's HUD (21.17.x)

**[V] Layers.** Epic Fight registers `stamina_bar`, `skills`, `weapon_innate` and `charging_bar` with `registerAboveAll`.
- Cancel them in `RenderGuiLayerEvent.Pre` by `ResourceLocation.fromNamespaceAndPath("epicfight", …)`.
- If we hide `skills`, we must draw our own cooldown and charge state for the left-arm ability.
- Source: <https://github.com/Antikythera-Studios/epicfight/blob/1.21.1/src/main/java/yesman/epicfight/client/platform/neoforge/event/ClientModBusEvent.java>

**[V] Client config keys** (`config/ClientConfig.java`):
- `ingame.show_target_indicator`
- `ingame.health_bar_show_option` = `NONE | HURT | TARGET | TARGET_AND_HURT` (in-world mob health bars)
- `ingame.show_epicfight_attributes` (tooltip lines)
- `ingame.first_person_model`
- `ingame.camera.camera_mode` = `DISABLED | ON_AIMING | ALWAYS` (Epic Fight's own third-person camera; default `ON_AIMING`)
- `ingame.camera.lock_on_range`, `ingame.camera.lock_on_quick_shift`
- `ingame.ui.*` position keys for the stamina bar, innate skill, passives and charging bar

There is no "hide stamina bar" toggle, so cancelling the layer is the clean method.

**[V] Textures we can reskin through a resource pack:**
- `epicfight:textures/gui/battle_icons.png`
- `healthbars1.png`, `healthbars2.png` (in-world bars)
- `screen/skill_edit.png`, `screen/skillbook.png`

**[V] Boss bar hook.** Epic Fight hooks `CustomizeGuiOverlayEvent.BossEventProgress` only to add a stun-shield bar to the Ender Dragon (`RenderEngine.java` lines 606–624). It does not conflict with a custom boss bar.

**[V] Default Epic Fight keys** (`client/input/EpicFightKeyMappings.java`):
- L-Shift, K (skill edit), Y, L-Alt, Space, R (mode switch), G
- arrow keys left/right
- middle mouse (lock-on)

Rebind or hide these through Default Options (§4).

### 1.3 Drawing bars and icons with `GuiGraphics`

**[V] Sprites in the GUI atlas.**
- `GuiGraphics.blitSprite(...)` draws from the GUI atlas.
- `atlases/gui.json` in the 1.21.1 jar is a `directory` source on `gui/sprites` with an empty prefix. Any `assets/<ourmod>/textures/gui/sprites/**.png` is therefore stitched in automatically and addressed as `ourmod:path`.
- A `.png.mcmeta` with `gui.scaling` selects `stretch`, `tile` or `nine_slice`. Example: vanilla `widget/button.png.mcmeta` = `{"type":"nine_slice","width":200,"height":20,"border":3}`.
- Sources: <https://docs.neoforged.net/docs/1.21.1/gui/screens> (blitSprite and scaling), and the 1.21.1 jar.

**[V] Animated GUI sprites work in 1.21.1.**
- Vanilla `icon/trial_available.png.mcmeta` and `realm_status/expires_soon.png.mcmeta` use `"animation"`.
- Sync-gauge shimmer, low-HP pulse and spell-ready glints can therefore be texture animations with no code.

**[V] Linear filtering.**
- `"texture": {"blur": true}` in a `.png.mcmeta` turns on linear filtering. Vanilla uses it on `title/minecraft.png`.
- Use it for high-resolution, non-pixel-art UI art such as an anime-style HUD frame or the logo.

**[V] What can be reskinned with no code.** The 1.21.1 jar has 400 GUI sprites:
- 75 `hud/*`: hearts, food, armour, air, XP bar, hotbar, crosshair, jump bar
- 22 `boss_bar/*`: 7 colours plus notched 6/10/12/20, background and progress
- 11 `toast/*`
- 32 `widget/*`: button, slider, text field, tab, scroller, checkbox
- 100 `container/*`
- plus `advancements`, `recipe_book`, `world_list` and others
- Non-sprite GUI textures: `menu_background.png`, `inworld_menu_background.png`, `header_separator.png`/`footer_separator.png`, `title/minecraft.png`, `title/edition.png`, `title/background/panorama_0..5.png`, `title/mojangstudios.png`, and `texts/splashes.txt`.

**1080p scaling:**
- [C/derived] "Auto" GUI scale picks the largest integer that keeps the scaled screen at least 320×240 (vanilla `Window` has `BASE_WIDTH`/`BASE_HEIGHT` constants; [V] the names appear in the Forge 1.21 javadoc <https://mcstreetguy.github.io/ForgeJavaDocs/1.21-latest/com/mojang/blaze3d/platform/Window.html>). At 1920×1080 this gives scale 4, which is a 480×270 GUI space.
- [?] Recommended: draw our HUD on a **virtual 1920×1080 canvas**.
  - Inside the layer, `pose().scale(s, s, 1)` with `s = window.getHeight() / 1080f / window.getGuiScale()`.
  - Then author HUD textures at native 1080p pixel size.
  - The HUD then looks the same at any GUI scale the player picks, and vanilla screens still follow the GUI scale.
- [V] Noxcrew's client mod Noxesium exists partly to "restrict GUI rescaling" and to "receive … the client's GUI scale and window size to better align custom UIs" (<https://github.com/Noxcrew/noxesium>). GUI scale is the main alignment problem for resource-pack UIs, and a mod avoids it.
- For pixel-art style, author at 1/4 resolution and keep nearest filtering. For anime and non-pixel style, author at 1:1 1080p and use `blur:true`. Pick one per element and don't mix.

**Smooth animation [V API / ? design]:**
- Every layer receives a `DeltaTracker`. Interpolate tick-synced values with `getGameTimeDeltaPartialTick(false)` (prev/cur lerp).
- Drive purely visual easing with real time (`Util.getMillis()`): damage "ghost" trail on LP, Sync-segment fill and flash, number count-up.
- Values arrive at 20 Hz from the server, so never show the raw value directly.

**Shaders and blur in the UI:**
- [V] Vanilla 1.21.1 ships the menu blur as the post chain `shaders/post/blur.json` (`box_blur`). Its strength is the option `menuBackgroundBlurriness` (0–10, default 5).
- [V] Custom screens get blur by calling `Screen.renderBlurredBackground(partialTick)`. NeoForge fixed a z-order bug in that blur in 21.1.84.
- [C] Pitfall: FancyMenu issue #1665 ("[NF 1.21.1] Invisible screens when menu blur is enabled", closed 2026-07-12) appears in larger packs when mods (Iris's shader-pack screen, Tensura) drive the blur post chain themselves. Use the vanilla call in our screens, or set blur to 0. <https://github.com/Keksuccino/FancyMenu/issues/1665>
- [V] Custom GLSL in the GUI is possible: `RegisterShadersEvent` gives a `ShaderInstance`, drawn with `RenderSystem.setShader`.
- [V] Iris's guidance is that "custom shaders added by mods … are ignored by Iris when an Iris shader pack is loaded" and that mods should keep "fallback rendering pathways that do not use custom shaders". <https://github.com/IrisShaders/Iris/blob/1.21.11/docs/development/compatibility/core-shaders.md>
- [?] Whether a mod `ShaderInstance` used only in the GUI pass is affected by an active Iris pack is not documented. Test before relying on it.
- Default to sprite animation plus additive blending for glows.

### 1.4 Syncing values to the HUD

**[V] Synced data attachments (21.1.197+):**
- `AttachmentType.builder(...).serialize(codec).sync(streamCodec)` syncs to every client that tracks the holder.
- `.sync((holder, player) -> predicate, streamCodec)` limits it, for example to the owning player only, or to trackers for enemy Sync gauges.
- `setData` and `removeData` trigger the sync (`AttachmentHolder.java` lines 80/101/113).
- After mutating an object in place, call `holder.syncData(TYPE)`.
- Sources: `src/main/java/net/neoforged/neoforge/attachment/AttachmentType.java` lines 247–290 and `IAttachmentHolder.syncData`; <https://github.com/neoforged/NeoForge/tree/1.21.1/src/main/java/net/neoforged/neoforge/attachment>
- Note: <https://docs.neoforged.net/docs/1.21.1/datastorage/attachments> still says "you need to send a packet to the client yourself". That is out of date for 21.1.197+.

**[V] Custom payloads for one-off events** (hit flash, boss phase change, "parried!", death banner):
- `RegisterPayloadHandlersEvent` → `PayloadRegistrar.playToClient(type, streamCodec, handler)`
- `PacketDistributor.sendToPlayer(...)`
- <https://docs.neoforged.net/docs/1.21.1/networking/payload>

**Suggested data split [?]:**
- **Player attachment `resonance`**: Sync value, level layout from the equipped seal, emergency-recovery flag. Owner-only sync.
- **Player attachment `inventory_state`**: dew charges, dew max, currency, equipped left-arm ability with cooldown end tick, three spell slots with costs. Owner-only sync.
- **Boss entity attachment `boss_gauge`**: Sync or posture and phase. Synced to trackers.
- The HUD reads these with `player.getData(...)` and needs no polling packets.

### 1.5 Boss bars

**[V] Hooking the vanilla boss event.**
- `CustomizeGuiOverlayEvent.BossEventProgress` is cancellable and fires per bar.
- It provides the `LerpingBossEvent` (name, progress, colour, overlay), x, y and the increment.
- Cancel it and draw our own bar while keeping vanilla `ServerBossEvent` for server→client sync.
- Source: `client/event/CustomizeGuiOverlayEvent.java` lines 50–60.

**Richer bars.** For a second gauge (rival Blader Sync, posture) or multi-phase LP, use a boss attachment (§1.4) and our own layer. Alternatively, cancel `BOSS_OVERLAY` entirely.

**[V] No-code fallback.** `boss_bar/*` sprites are re-texturable.
- Enhanced Boss Bars has a 1.21.1 NeoForge mod (1.21.1-1.0.0, 2026-01-29, ARR) <https://modrinth.com/mod/enhanced-boss-bars-mod>.
- We don't need it if we draw our own.

---

## 2. Screens

### 2.1 Replacing any vanilla screen

**[V] `ScreenEvent.Opening`.**
- Fired from `Minecraft.setScreen` for every screen, with `getNewScreen()` and `setNewScreen(screen)`.
- 21.1.247 fixed its nullability annotations.
- One event handler can swap `InventoryScreen`, `PauseScreen`, `DeathScreen`, `TitleScreen`, `AdvancementsScreen`, `ChatScreen`, `LevelLoadingScreen`, `ReceivingLevelScreen` and Epic Fight's `SkillEditScreen` for our own.
- Source: `client/event/ScreenEvent.java` lines 985–1012.

**[V] What NeoForge adds to vanilla screens.**
- The `PauseScreen` patch adds a "Mods" button.
- The `TitleScreen` patch adds a Mods button plus branding lines ("NeoForge x.y", "N mods loaded").
- Both disappear when the screen is replaced or customised in FancyMenu.
- `showLoadWarnings` (NeoForge client config) hides the mod-loading warning screen.
- Source: `patches/net/minecraft/client/gui/screens/*.patch`, `common/NeoForgeConfig.java` line 113.

**[V] Dimension transitions.** `RegisterDimensionTransitionScreenEvent` (21.1.33+) registers a custom `ReceivingLevelScreen` per incoming, outgoing or specific pair of dimensions. Use it if our areas are separate dimensions (AI LIMIT uses rifts and train rides between zones). Kingdom Keys uses it (`ClientSetup.java` line 125).

### 2.2 Inventory → equipment, seal and stats screens; removing crafting

**[V] Menu framework.**
- `MenuType` via `IMenuTypeExtension.create(factory)` (extra data through `RegistryFriendlyByteBuf`).
- `AbstractContainerMenu`, `AbstractContainerScreen`.
- `RegisterMenuScreensEvent`.
- Open on the server with `IPlayerExtension#openMenu(provider, buf -> ...)`.
- <https://docs.neoforged.net/docs/1.21.1/gui/menus>

**Pattern [?]:**
1. Cancel `InventoryScreen` in `ScreenEvent.Opening`.
2. Send a C2S payload.
3. The server opens `EquipmentMenu`, with slots for weapon 1 and 2, consumable quick slots, seal slots and the player inventory.
4. Our screen draws stats from the synced attachments.

- Vanilla `InventoryMenu` slot positions are final and include the 2×2 crafting grid, so a separate menu is cleaner than reusing it.
- Removing `InventoryScreen` also removes the recipe-book button and the 2×2 crafting grid from the player's view.

**[V] Removing crafting data.**
- 1.21.1 ships `data/minecraft/recipe/` (1,290 files) and `data/minecraft/advancement/` (1,399 files, of which 1,277 are `advancement/recipes/*` recipe-unlock advancements). The 1.21 folder names are singular.
- A datapack whose `pack.mcmeta` has `"filter": {"block": [{"namespace":"minecraft","path":"recipe/.*"}, {"namespace":"minecraft","path":"advancement/.*"}]}` hides them from all lower packs.
- The filter section is documented at <https://minecraft.wiki/w/Pack.mcmeta>.
- Data pack format for 1.21.1 is **48**; resource pack format is **34** (`version.json` in the jar).
- [?] Test for log spam from mods that reference vanilla recipes or advancements.

**Mod alternatives:**
- [V] NERB "Not Enough Recipe Book" 0.4.3 (ARR, needs ShatterLib) <https://modrinth.com/mod/notenoughrecipebook>
- gamerule `doLimitedCrafting`

### 2.3 Controller-friendly navigation

- **[V] Controlify** 3.0.1+lts for 1.21.1 NeoForge (2026-07-10), LGPL-3.0-or-later, needs YACL. <https://modrinth.com/mod/controlify>
  - It offers a `ScreenProcessor` API for explicit controller handling of custom screens: <https://controlify.isxander.dev/developers/screen-operation-api>
  - Vanilla focus navigation (arrow/Tab through `GuiEventListener`s) is the fallback.
- **[V] Epic Fight 1.21.1 has a Controlify compat module**, compiled against `controlify 2.5.0+1.21.1-neoforge` (`gradle/libs.versions.toml`, `compat/controlify/*`).
  - [?] Whether it works with 3.0.x LTS needs a test.
- **Design rule [?]:** build every custom screen from focusable widgets (subclasses of `AbstractWidget` with narration). Never rely on mouse-only hit tests. This also helps keyboard play.

### 2.4 Pause and options

**Pause [?].**
- Replace `PauseScreen` with our screen (Resume, Equipment, Settings, Return to Title).
- Copy the save-and-quit logic from vanilla `PauseScreen.onDisconnect()`: disconnect, show the "Saving world" `GenericMessageScreen`, then open the title screen. Kingdom Keys `KOGui.action("exit")` shows a minimal version.

**Options [?].**
- Keep the vanilla `OptionsScreen` tree. Reskin it through `widget/*` sprites, `menu_background.png` and the font, or through FancyMenu button and slider templates.
- Writing our own full settings screen is large and low value.
- The Sodium 0.8 video-settings screen and the Iris shader-pack screen use their own UI and will still look "modded".

### 2.5 Death screen ("you died" style)

- Swap `DeathScreen` in `ScreenEvent.Opening` for our screen.
  - It should not close on ESC and should not pause.
  - Show a banner and fade, then call `minecraft.player.respawn()` after N seconds or on a button press.
- Server side: currency loss (seal retention rate) and respawn at the last sapling via `ServerPlayer.setRespawnPosition`.
- Alternative: gamerule `doImmediateRespawn true` plus our own overlay layer. That skips the death screen entirely, but it also cuts off an Epic Fight death animation.
- Reference: Kingdom Keys `KOGui` (custom death UI with give-up and quit) and Souls Message Banners (banner styling).

### 2.6 Tooltips

**[V] What 1.21.1 offers.**
- No tooltip sprites. The background and border are colours.
- NeoForge hooks:
  - `RenderTooltipEvent.GatherComponents` (cancellable; edit lines, max width)
  - `RenderTooltipEvent.Pre` (cancellable; `setFont`, `setX`, `setY`, so you can cancel and draw your own nine-slice frame)
  - `RenderTooltipEvent.Color` (background start/end, border start/end)
- Custom rich rows through `RegisterClientTooltipComponentFactoriesEvent`.
- Source: `client/event/RenderTooltipEvent.java`.

**[V] Hiding vanilla lines.**
- In 1.21.1 the item components `minecraft:hide_additional_tooltip`, `minecraft:hide_tooltip` and `show_in_tooltip:false` (on `attribute_modifiers`, `enchantments`, `unbreakable`) still exist. They were replaced by `tooltip_display` in 1.21.5: <https://github.com/ViaVersion/ViaVersion/issues/4470>, <https://minecraft.wiki/w/Data_component_format/tooltip_display>.
- NeoForge `AddAttributeTooltipsEvent` and `GatherSkippedAttributeTooltipsEvent` (21.1.60+) control attribute lines.
- Epic Fight config `ingame.show_epicfight_attributes=false`.

**[V] Mods, if we don't write our own:**
- Legendary Tooltips 1.5.5 (2025-04-08), CC-BY-NC-ND-4.0, needs Iceberg and Prism (both CC-BY-NC-ND). Frames are resource-pack configurable. <https://modrinth.com/mod/legendary-tooltips>
- Obscure Tooltips 4.2.5 (2026-09-19), custom "Obscuria Ecosystem" licence, needs Fragmentum. <https://modrinth.com/mod/obscure-tooltips>
- A custom renderer is about 1–2 days of work and avoids the licence questions.

### 2.7 Chat

- **[V] Events:**
  - `ClientChatReceivedEvent` (and `.System`, `.Player`) is cancellable and lets you rewrite the message.
  - `CustomizeGuiOverlayEvent.Chat` moves the chat box.
  - Cancel the `CHAT` layer to hide it. Swap `ChatScreen` to block the T key in release builds.
- **[?] Design:** route system messages (item pickups, "sapling restored") into our own notification feed layer. Keep chat for debugging only.
- Option `chatVisibility` (0–2) is a blunt fallback.

### 2.8 Toasts

- [V] `ToastAddEvent` is cancellable and fires before any toast is queued (advancement, recipe, tutorial, system). Cancelling everything except our own toast classes is a few lines. Source: `client/event/ToastAddEvent.java`.
- [V] Mod alternative: Toast Control 1.21.1-9.0.1 (MIT, needs Placebo) <https://modrinth.com/mod/toast-control>.

---

## 3. Title, loading screens and other menus without code

### 3.1 FancyMenu

**[V] Version and dependencies.**
- FancyMenu **3.9.14-1.21.1-neoforge** (2026-09-28).
- Requires Konkrete 1.9.9 (Apache-2.0) and Melody 1.0.10 (MIT).
- Licence **DSMSLv3.1**: "You can use this mod in modpacks, but you must not include its files directly … list it as a dependency (mod reference) that points to an official download source."
- <https://modrinth.com/mod/fancymenu>, <https://github.com/Keksuccino/FancyMenu/blob/master/LICENSE.md>

**[V] Global Customizations:**
- game intro animation or video before the title screen
- custom window icon and title (needs 16×16, 32×32 and a macOS `.icns`; icons need at least one transparent pixel)
- default GUI scale, force fullscreen
- global button and slider textures (nine-slice), menu background and panorama
- custom menu music tracks, button click sound
- "Seamless World Loading" (screenshot as the loading background)
- <https://docs.fancymenu.net/docs/en-US/global-customizations>, <https://docs.fancymenu.net/docs/en-US/window-customization>

**[V] Custom GUIs.**
- Brand-new screens built from elements (buttons, sliders, images, text, tickers, audio) and action scripts.
- **"Override Current with Custom GUI"** replaces any vanilla or mod screen whenever it opens.
- Actions include `loadworld <folder>`, `join_last_world`, `opengui`, `quitgame` and leave world.
- <https://docs.fancymenu.net/docs/en-US/custom-guis>, <https://docs.fancymenu.net/docs/en-US/action-scripts>

**[V] Shipping a setup.**
- Copy `config/fancymenu/`.
- Set `modpack_mode=true` in `config/fancymenu/options.txt` to hide the editor bar and hotkeys.
- <https://docs.fancymenu.net/en/modpacks>

**[C] Agent-friendly.** Layouts are plain-text `fancymenu_layout` files, for example <https://git.sfkao.net/SFKao/All-Of-Create/src/commit/8069d8ebfe4d77e1fe1af13489f0426d53ffa8ec/config/fancymenu/customization/drippy_loading_overlay_layout.txt>. Agents can create and diff them. The user reviews screenshots.

**[C] Video.** Video backgrounds need an extra media mod and are fiddly. APNG or sprite-sheet animations are the safer path (Gingie tutorial transcript, <https://www.youtube.com/watch?v=5N0sxfw7Pdo>).

**Recommendation [?].** Use FancyMenu for:
- the title screen (New Game / Continue via `loadworld` / `join_last_world`, Settings, Quit)
- styling the options screens
- the world-load and saving screens
- the window title, icon and menu music

Use Java for the gameplay screens (inventory, equipment, sapling menu, death, HUD), which need live game data.

### 3.2 Loading screens

**Startup has three stages:**

1. **NeoForge early window (FML)**, before the Minecraft renderer exists.
   - [V] Drippy Early Loading Module **3.1.5-1.21.1-neoforge** (DSMSLv3) extends Drippy to this stage. <https://modrinth.com/mod/drippy-early-loading-module>
   - [V] Simple Custom Early Loading **2.2-neoforge** (1.21–1.21.4, LGPL-2.1, 2026-03-19): images and APNG, toggles for the fox, progress and log. Set `earlyWindowProvider = "SimpleCustomEarlyLoading"` in `config/fml.toml`. Its author says "I won't allow removing the Mojang logo". <https://github.com/lukaskabc/SimpleCustomEarlyLoading>
   - [V] FML's own early-screen theming (NeoForge PR #2346) is 1.21.6+ only. <https://github.com/neoforged/NeoForge/pull/2346>
2. **Mojang `LoadingOverlay`** (resource reload).
   - [V] Drippy Loading Screen **3.1.5-1.21.1-neoforge** (DSMSLv3, needs FancyMenu): a full layout editor, custom progress bars, "Disable Vanilla Progress Bar". <https://modrinth.com/mod/drippy-loading-screen>
   - [V] Without mods, options `darkMojangStudiosBackground:true` (black instead of red) and `title/mojangstudios.png` are the only levers.
3. **World loading and saving** (`LevelLoadingScreen`, `ReceivingLevelScreen`, `GenericMessageScreen`). These are ordinary screens, so use FancyMenu layouts or `ScreenEvent.Opening`, plus `RegisterDimensionTransitionScreenEvent` (§2.1).

### 3.3 Window title and icon

- **[V] Icons can't come from a resource pack.**
  - The window icons are in the asset index root `icons/icon_16x16.png … icon_256x256.png`, `icons/minecraft.icns`, outside any `assets/minecraft` namespace.
  - Vanilla loads them from the vanilla pack at startup, so a resource pack can't replace them. (Inspected `assetindex.json` for 1.21.1.)
- Use FancyMenu Global Customizations, or code: a mixin on `Minecraft.createTitle()` and `Window.setIcon`.
- [V] Custom Window Title (chylex, Unlicense) lists NeoForge builds. <https://modrinth.com/mod/custom-window-title>
  - [?] Its newest builds are tagged 1.21.2+. Confirm a 1.21.1 jar before use.

### 3.4 Cursor

- [V] Custom Cursor 3.0.3 (1.21–1.21.1 NeoForge, **beta**, LGPL-3.0) <https://modrinth.com/mod/custom-cursor>.
- Code alternative [?]: `GLFW.glfwCreateCursor(GLFWImage, hotX, hotY)` plus `glfwSetCursor(window, cursor)` when our screens open. The cursor is hidden in-world while the mouse is grabbed anyway.

### 3.5 Fonts, including Korean

**[V] Provider types** (<https://minecraft.wiki/w/Font>):
- `bitmap` (PNG grid; `height` = render scale, `ascent`)
- `space` (advances; negative widths allowed)
- `ttf` (`file`, `size`, `oversample`, `shift`, `skip`; kerning and ligatures are stripped)
- `unihex` (GNU Unifont `.hex` in a zip, 16 px tall, widths 8/16/24/32, `size_overrides`)
- `reference`
- optional `filter` `{uniform, jp}`

**[V] Vanilla font files.**
- 1.21.1 `font/default.json` is just references: `include/space`, then `include/default` (filtered `uniform:false`), then `include/unifont`.
- The Unifont data is `minecraft/font/unifont.zip` and `unifont_jp.zip` in the asset index.
- Hangul in vanilla therefore comes from 16-px Unifont drawn at half size, which is why it looks thinner than Mojangles.

**HD-font trick [V wiki semantics / ? tuning].**
- A bitmap provider whose PNG glyphs are 16 px tall with `"height": 8` lays out like the vanilla font but renders at 2× detail. At GUI scale ≥2 that gives crisp small text.
- For HUD numbers, use a separate font ID (`ourmod:hud_digits`) applied with `Style.withFont(...)`, so the vanilla default isn't touched.

**[V] Korean pixel fonts, all OFL 1.1:**
- **Galmuri** (11/9/7 px; all 11,172 Hangul syllables; TTF and BDF) <https://github.com/quiple/galmuri>
- **Neo둥근모 / NeoDGM** (16 px) <https://neodgm.dalgona.dev/>
- **Mulmaru** (2025) <https://github.com/mushsooni/mulmaru>

**[V] Examples:**
- "Immersive Korean Font (Galmuri9)" packs `Galmuri9.ttf` under OFL and requires Force Unicode off. <https://modrinth.com/resourcepack/immersive-kr-font>
- BetterHangulFont (MIT, hand-made, its own combining source) <https://github.com/oruur/bhf4mc>
- KoreanRefreshed uses Neo둥근모.

**Choice [?]:**
- **TTF** is fastest to integrate. Tune `size` to the font's pixel em and `oversample` to an integer (for example 4 at GUI scale 4) so pixel fonts stay sharp.
- **unihex** (convert Galmuri BDF → `.hex`) gives exact pixel-grid glyphs that match the vanilla Unifont pipeline.
- **bitmap** pages for 11,172 syllables are impractical.

**Global or scoped [?].**
- Overriding `minecraft:font/default.json` re-fonts the whole game, including other mods' screens. That is right for a total conversion, but test legibility.
- Keep the OFL text in the pack and credits. OFL forbids selling the font by itself and requires keeping the licence.

### 3.6 Sounds and music

- **[V] UI sounds.** UI sounds are sound events (`ui.button.click`, `ui.toast.in`, `ui.toast.out`, `ui.toast.challenge_complete`). Replace them in `assets/minecraft/sounds.json` with `"replace": true`. The 1.21.1 asset index has `minecraft/sounds/ui/toast/*.ogg`.
- **[V] Music control in code.**
  - NeoForge `SelectMusicEvent` (21.0.69+) fires whenever `MusicManager` picks situational music.
  - Set our `Music(holder, minDelay, maxDelay, replaceCurrentMusic)` for area, boss or menu themes, or `null` to silence vanilla music.
  - Source: `client/event/SelectMusicEvent.java`.
- **[V] Menu music without code.** FancyMenu custom menu music tracks, or replacing `music.menu` in `sounds.json`.
- **[C] Per-area ambience.** Custom biomes carry `music`, `ambient_sound`, `mood_sound` and `additions_sound`. Paint them over the finished map with `/fillbiome` (1.19.3+).
  - [V, prior notes] Biome fog colours are ignored under Iris and Complementary.

### 3.7 Shipping the assets

- **[V] Built-in packs.** `AddPackFindersEvent.addPackFinders(location, PackType, name, PackSource, alwaysActive, Pack.Position)` registers a built-in resource pack or datapack inside our jar. Use `alwaysActive=true` and `Pack.Position.TOP` so our UI pack always wins. Source: `event/AddPackFindersEvent.java` line 71.
- [C] Without this, packs need Paxi or "Global Packs"-style mods. A Reddit thread about Cisco's RPG shows users confused by a HUD baked in through Paxi: <https://www.reddit.com/r/feedthebeast/comments/1os18xb/>.
- **[V] Shipping options.** Default Options 21.1.8 (needs Balm, ARR) ships default `options.txt`, keybinds and server lists without overwriting user files on update. <https://modrinth.com/mod/default-options>

---

## 4. Removing the vanilla feel

**Gamerule names.** 1.21.1 uses the **camelCase** names. The snake_case names on today's wiki arrived in 1.21.11 (25w44a). Several rules (`spawnerBlocksEnabled`, `spawnMonsters`, `pvp`, `tntExplodes`, `locatorBar`) don't exist in 1.21.1. Source: history table at <https://minecraft.wiki/w/Game_rule>.

| Vanilla thing | How to remove it on 1.21.1 | Tag |
|---|---|---|
| Hunger | No gamerule. Each tick (server, `PlayerTickEvent.Post`): `getFoodData().setFoodLevel(20)`, saturation 5, exhaustion 0. Cancel the `FOOD_LEVEL` layer. Sprint still needs food >6, so keep 20. Mod alternatives: Hunger Strike 1.21-9.0.0 (beta, MIT, 2024), Melancholic Hunger | [V events and layer] [? exact FoodData setters] |
| Natural regen | `naturalRegeneration false`. Healing only from our dew item | [V] |
| XP orbs, XP bar | `doMobLoot false` stops mob items **and** XP orbs. Or keep loot and zero XP with `LivingExperienceDropEvent`, `BlockDropsEvent`, `PlayerXpEvent.PickupXp`. Cancel the `EXPERIENCE_BAR` and `EXPERIENCE_LEVEL` layers | [V] |
| Vanilla mob spawning | `doMobSpawning false` (natural and global spawns only; spawner blocks, commands and spawn eggs still work), plus `doPatrolSpawning`, `doTraderSpawning`, `doWardenSpawning`, `doInsomnia false`, `disableRaids true`. Spawn our enemies from our own spawner logic, reset at saplings | [V] |
| Day/night, weather | `doDaylightCycle false`, `doWeatherCycle false`, `/time set`, `/weather clear`. Atmosphere comes from the shader pack | [V] |
| Block breaking and placing | Adventure mode, YAWP regions (prior notes), `mobGriefing false`, `doFireTick false`, `randomTickSpeed 0` (no leaf decay or growth on the built map) | [V] |
| F3 debug | `reducedDebugInfo true` (also blocks F3+B hitboxes and F3+G chunk borders). Cancel the `DEBUG_OVERLAY` layer in release builds. `CustomizeGuiOverlayEvent.DebugText` to strip lines | [V] |
| Vanilla keybinds | Default Options for defaults. `InputEvent.InteractionKeyMappingTriggered` (cancellable) to neutralise attack/use/pick-block where Epic Fight doesn't. Swap `AdvancementsScreen` (L) and `SocialInteractionsScreen` (P) in `ScreenEvent.Opening`. Can't unregister vanilla `KeyMapping`s; hide them from a custom controls screen | [V events] [? hiding] |
| Advancements, recipe toasts | Datapack `filter` blocking `minecraft:advancement/.*` and `recipe/.*` (§2.2). `announceAdvancements false`. `ToastAddEvent` cancel | [V] |
| Tutorial hints | options `tutorialStep:none`, `joinedFirstServer:true`, `onboardAccessibility:false` (narrator welcome), `skipMultiplayerWarning:true`, `hideSplashTexts:true`. Shipped through Default Options | [V] option keys from <https://minecraft.wiki/w/Options.txt> |
| Death messages, command spam | `showDeathMessages false`, `sendCommandFeedback false`, `commandBlockOutput false`, `logAdminCommands false` | [V] |
| First-person hand | `RenderHandEvent` (cancellable) and `RenderArmEvent`. Epic Fight already cancels the vanilla hand to draw its animated first-person model (`RenderEngine.java` lines 627–650, config `ingame.first_person_model`). In a forced third-person game this rarely shows | [V] |
| Camera | **Epic Fight's own TPS camera** `ingame.camera.camera_mode=ALWAYS` plus lock-on (middle mouse) needs no extra mod | [V] config |
| Camera, alternative | **Shoulder Surfing Reloaded 1.21.1-5.2.0+neoforge** (2026-09-29, MIT). Epic Fight 1.21.1 ships `compat/shouldersurfing/ShoulderSurfingCompat.java`, compiled against SSR 4.18.1: turns the player toward the target on attack and charge, explicit lock-on support, disables EF's TPS camera. SSR marks Better Third Person, Nimble and YDM's Custom Camera View incompatible | [V] Modrinth deps and EF source; [?] SSR 5.x vs EF 21.17.3.1 API (EF issue tracker: Exopandora/ShoulderSurfing#359 closed 2025-12-05) |
| Inventory hotbar scroll | Cancel `InputEvent.MouseScrollingEvent` in-game. Hide the `HOTBAR` layer. Our weapon and consumable quick slots read from the synced attachment | [V event] [? design] |

---

## 5. Case studies: what total-conversion experiences actually do

| Project | Technique | What it teaches us | Tag |
|---|---|---|---|
| **MCC Island** (Noxcrew) | Server resource pack that **overrides vanilla core shaders**: Noxcrew dev Aeltumn on Sodium's 1.20.2 warning, "certain shaders are being overriden". Custom fonts for UI. Optional client mod **Noxesium** (LGPL-3.0, Fabric) adds server-controlled features: restrict GUI rescaling, report GUI scale and window size, lock the camera, restrict debug features and F1, prevent moving GUI items, hover sounds, custom sounds with offsets, text at arbitrary x/y | Even the best resource-pack UI needs a client mod to beat GUI-scale alignment, F1/F3 and input control. We ship a mod anyway, so we get all of this for free | [V] <https://mcchampionship.com/threads/error-message-saying-that-the-server-resource-pack-is-not-compatible-with-sodium.11060/>, <https://github.com/Noxcrew/noxesium> |
| **Wynncraft** | Server resource pack (custom font HUD). Optional client mod **Wynntils** draws overlays: v4.1.0-beta.4 added overlays that "replace the vanilla boss bar" | Server "UI" is fonts, boss bars and action bar. Rich UI moves into a client mod | [V] <https://github.com/Wynntils/Wynntils/releases/tag/v4.1.0-beta.4> |
| **Origin Realms** | Custom core shaders (armour, UI). Named by Iris as unsupported | Shows the Iris limitation | [V] <https://github.com/IrisShaders/Iris/blob/1.21.1/docs/usage/limitations.md> |
| **ItemsAdder / Oraxen / BetterHud** (server plugins) | Font glyphs mapped to PNGs, shifted with negative-space characters, put into container titles (custom inventory art) and the action bar or boss bar (HUD). BetterHud generates a pack with images, fonts and shaders | Read-only art. Can't move slots ("a pack … cannot move a slot, add one, resize the window"). Breaks with GUI scale. Not needed with a mod | [V] <https://docs.oraxen.com/configuration/glyphs/huds>, <https://wiki.itemsadder.com/adding-content/font-images/guis>, <https://github.com/AmberWat/NegativeSpaceFont> |
| **Kingdom Keys 2** (mod, 1.21.1 NeoForge, LGPL-3.0) | About 20 GUI layers, HUD editor, own death (KO) screen, own menus, dimension transition screen | Closest open-source proof that a full action-RPG HUD and menu replacement works on our exact loader and version | [V] §1.1 |
| **Souls of Lunareth** (1.20.1 Forge soulslike pack) | "Every menu in the pack was built by hand, from the title screen and its music to the settings, the audio mixer and the player profile." Uses Simple Custom Early Loading | A modpack-level total UI conversion is normal practice. Menus in FancyMenu-style tools, music levelled by hand | [V] <https://www.modpackindex.com/modpack/163659/souls-of-lunareth> |
| **Cisco's Fantasy Medieval RPG** | HUD and menu restyle through the "Stoneborn" resource pack, forced through Paxi | Players can't remove a pack-forced HUD easily. Shipping it in the mod jar is cleaner | [C] <https://www.reddit.com/r/feedthebeast/comments/1oc628t/>, <https://www.reddit.com/r/feedthebeast/comments/1os18xb/> |
| **Stardew HUD** (Chinese, CC0), **ModernUI** (Chinese UI framework, LGPL-3.0, 3.13.0.1 for 1.21.1) | Full HUD reskin. ModernUI replaces text rendering and screen backgrounds globally | Stardew HUD is copyable reference code. **Avoid ModernUI**: it changes global rendering and is a known FancyMenu conflict (FancyMenu #971, cited in #1665) | [V] Modrinth; [C] conflict |

The Chinese, Japanese and Korean side of this topic (整合包 UI 美化, 史诗战斗 HUD 隐藏 and so on) is covered by the parallel Codex run: `research/r2/codex_5_total_conversion.md`.

**Resource pack only vs mod (our situation).**
- **Resource pack only can do:**
  - restyle every vanilla sprite (hearts, bars, hotbar, buttons, boss bars, toasts) and the menu backgrounds, logo, panorama and splashes
  - fonts and sounds
  - HUD text through title, action bar and boss-bar glyph tricks
- **Resource pack only can't do:**
  - move or resize vanilla widgets (only hide them by transparency)
  - add live data (Sync, dew count) except through server-sent text
  - tooltip frames (1.21.1)
  - window icon
  - early loading screen
  - core-shader effects while Iris is on
- **A mod adds:**
  - arbitrary layers bound to synced data, new screens and menus
  - screen replacement, input control, toast, chat and music control
  - GUI-scale-independent layout

---

## 6. Recommended architecture for our mod

### 6.1 What goes where

| Layer | Contents | Tool |
|---|---|---|
| **Java (our NeoForge mod, client package)** | HUD layers: LP plus segmented Sync gauge (0–IV colours from the seal layout), damage trail, dew counter, left-arm ability icon and cooldown, 3 spell slots with Sync-cost borders, currency, status icons, lock-on reticle, boss bar(s) with an optional second gauge, area-name and death banners, interaction prompt. Layer cancels for vanilla and Epic Fight. Screen swaps (inventory → equipment/seal/stats, pause, death, sapling rest menu, Epic Fight skill edit, advancements, chat in release builds). Tooltip renderer. Toast and chat filters. `SelectMusicEvent` music director. Optional GLFW cursor | NeoForge 21.1.259 APIs (§1–2) |
| **Java (common/server)** | Attachments with `.sync(...)` (resonance, inventory state, boss gauge). Payloads for events. Menus. Hunger, XP and drops handlers. Respawn and currency loss | §1.4, §4 |
| **Built-in resource pack in the jar** (`AddPackFindersEvent`, TOP, always active) | All UI art (`textures/gui/sprites/**` with nine-slice and animation `.mcmeta`), vanilla sprite overrides (widgets, boss bars, toasts, menu backgrounds, logo, panorama, `mojangstudios.png`), fonts (Galmuri or NeoDGM through ttf or unihex, plus an HD bitmap digits font), `sounds.json` overrides, `texts/splashes.txt` emptied | §1.3, §3.5–3.7 |
| **Built-in datapack / world datapack** | `pack.mcmeta` filter removing vanilla recipes and advancements. Gamerules applied by a load function. Custom biomes for music and ambience | §2.2, §4 |
| **FancyMenu 3.9.14 + Drippy 3.1.5 + Drippy Early Loading Module 3.1.5** (dependencies, not bundled) | Title screen (New Game / Continue / Settings / Quit), restyled options screens, world-loading and saving screens, window title and icon, menu music, startup intro, early and Mojang loading screens. `modpack_mode=true` | §3.1–3.3 |
| **Config defaults** (Default Options, or modpack `config/` files) | `options.txt` defaults (GUI scale, blur, tutorial and onboarding off, dark Mojang background, keybinds). Epic Fight client config (camera ALWAYS, lock-on, health bars, attribute lines). NeoForge `showLoadWarnings=false` | §4 |

### 6.2 Effort estimates

All estimates are [?]: agent-written code with user review rounds. Art is counted separately.

| Item | Estimate |
|---|---|
| HUD framework (virtual 1080p canvas, sprite helpers, easing, layer cancels) | 2–3 days |
| LP/Sync/dew/arm/spells/currency HUD | 4–7 days (+ art) |
| Boss bar (+ rival Sync gauge) | 2–3 days |
| Banners and death overlay | 2 days |
| Synced attachments and payloads | 2–3 days |
| Equipment/seal/stats menu and screen (with server validation) | 1.5–3 weeks |
| Sapling rest menu (level-up, travel, upgrade) | 1.5–3 weeks |
| Pause and death screens | 2–3 days |
| Tooltip renderer | 1–2 days |
| Toast, chat and music control | 1–2 days |
| Fonts (Korean TTF or unihex plus digits) | 1–3 days |
| FancyMenu title, loading and options restyle | 3–5 days (+ art) |
| Vanilla-feel removal (gamerules, filter datapack, handlers, option defaults) | 2–4 days |
| Controller support (optional) | +1–2 weeks |

**For milestone M1 [?].** Build the HUD set, boss bar, death screen, pause swap, FancyMenu title and loading screens, fonts, and vanilla-feel removal first (about 4–6 weeks). The full equipment and sapling menus can start as minimal screens.

### 6.3 Pitfalls

1. **Iris.** Never depend on resource-pack core shaders. Treat mod GUI shaders as [?] and keep a non-shader fallback. [V]
2. **ImmediatelyFast `hud_batching`.** Our perf list includes ImmediatelyFast (1.6.15+1.21.1-neoforge, 2026-10-13). Its HUD batching has a history of breaking custom HUD and tooltip rendering:
   - ImmediatelyFast #233, #227, #296, #485 ([1.21.1 NeoForge] Cosmetica HUD overflow)
   - Simulated-Project #158
   - Test our HUD with `hud_batching` on and off. Ship it off if anything misdraws. <https://github.com/RaphiMC/ImmediatelyFast/issues/485> [C/V issue reports]
3. **Menu blur and FancyMenu.** Invisible screens appear with heavy UI mod sets plus Iris (#1665). Use vanilla `renderBlurredBackground`, or set `menuBackgroundBlurriness:0`. [C]
4. **GUI scale.** Design the HUD on a virtual 1080p canvas. Lock the default GUI scale (FancyMenu "Default GUI Scale" or Default Options) for the vanilla screens and FancyMenu layouts. Test at scales 2, 3 and 4. [?]
5. **Layer order with Epic Fight.** Epic Fight registers with `registerAboveAll`. Cancel its layers by ID rather than relying on order. Re-check the four IDs after each Epic Fight update (they are a public-facing contract only in practice). [V]
6. **Paused screens.** Our inventory, equipment and rest screens should return `isPauseScreen() = false` if we want soulslike "the world keeps going" behaviour. That is a design decision for the user. The pause menu itself pauses in singleplayer. [?]
7. **Licences.**
   - FancyMenu and Drippy (DSMSL): reference only.
   - Legendary Tooltips, Iceberg and Prism (CC-BY-NC-ND): no modification.
   - Balm and Default Options (ARR): fine as dependencies.
   - OFL fonts: keep the licence file.
   - Epic Fight textures are ARR. Reskin through our pack. Never redistribute their PNGs modified.
   [V licences from Modrinth]
8. **Sodium and Iris option screens stay off-style**, and so do other mods' config screens. Hide them from players or accept them. [?]
9. **Shoulder Surfing vs Epic Fight camera.** Use one camera system. Start with Epic Fight's `ALWAYS` TPS and lock-on. Add SSR 5.2.0 only if the user wants decoupled orbit, and test the compat first. [V/?]
10. **The 1.21.1 attachments docs page is stale.** Agents must follow the 21.1.259 source and changelog, not the docs page (§1.4). [V]
