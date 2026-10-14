# 토탈 컨버전 UI (2차 조사, 2026-10-14)

> **용도:** 인벤토리, 체력·경험치 바, 메뉴, 로딩 화면, 글꼴, 소리까지 바닐라 UI를 모두 새로 만드는 방법. 1.21.1 + NeoForge 21.1.259 + Epic Fight 21.17.3.1 기준.
>
> **출처:** [`sources/`](sources/) — `notes_5_total_conversion_ui.md`(NeoForge·Epic Fight 1.21.1 소스, 1.21.1 클라이언트 JAR 직접 확인), `codex_5_total_conversion.md`(중국어·일본어·한국어 자료, Modrinth 버전 조회, Epic Fight 소스 JAR)
>
> **표기:** [확인] 1차 출처(소스, JAR, 공식 문서, Modrinth API) · [커뮤니티] · [추정] 우리 설계나 미시험

---

## 0. 계획을 바꾸는 사실 다섯 가지

1. **NeoForge 21.1.x만으로 HUD 전체를 코드로 바꿀 수 있다** [확인]. 바닐라 HUD 층 25개에 이름이 있고, 층마다 취소·교체·감싸기가 된다. `wrapLayer`/`replaceLayer`는 21.1.190, 동기화되는 데이터 어태치먼트는 21.1.197에 1.21.1로 백포트됐다. 우리는 21.1.259라 둘 다 쓴다.
2. **Epic Fight HUD는 이름 붙은 층 네 개**다 [확인: 21.17.3.1 소스]: `epicfight:stamina_bar`, `epicfight:skills`, `epicfight:weapon_innate`, `epicfight:charging_bar`. 이름으로 취소하면 되고 믹스인이 필요 없다.
3. **리소스팩만으로는 안 된다** [확인]. 서버들이 쓰는 "코어 셰이더 HUD" 기법(MCC Island, Origin Realms)은 Iris 셰이더 팩이 켜지면 무시된다. 우리는 Iris를 쓰므로 HUD는 Java 코드로 그린다. 리소스팩은 그림·글꼴·소리를 담는 **에셋 층**이다.
4. **1.21.1에는 툴팁 스프라이트가 없다** [확인: JAR]. `tooltip_style`은 1.21.2, `tooltip_display`는 1.21.5부터다. 툴팁 틀은 코드(`RenderTooltipEvent`)로 그린다.
5. **FancyMenu + Drippy(+ 초기 로딩 모듈)로 코드 없이 모든 메뉴와 로딩 화면 세 단계를 바꿀 수 있다** [확인]. 단 라이선스상 **JAR를 동봉하지 못하고 의존성으로만** 적는다.

---

## 1. 구조: 무엇을 어디서 만드나

**원칙: 게임 상태는 하나(서버), 화면 요소마다 주인은 하나.** HUD를 Java와 SpiffyHUD 양쪽에서 그리는 식의 "임시 이중 소유"를 만들지 않는다 [Codex].

| 층 | 내용 | 도구 |
| --- | --- | --- |
| **우리 모드, 클라이언트** | HUD 층(체력 + 구간형 공명율, 피해 잔상, 수액 병 개수, 왼팔 기능 아이콘과 쿨다운, 주문 3칸, 정수, 상태 아이콘, 락온 표시, 보스 바, 지역 이름·사망 배너, 상호작용 안내), 바닐라·Epic Fight 층 취소, 화면 교체(인벤토리 → 장비·인장·능력치, 일시정지, 사망, 묘목 휴식 메뉴, Epic Fight 스킬 편집, 발전 과제, 출시판 채팅), 툴팁, 토스트·채팅 필터, 음악 감독, 커서(선택) | NeoForge API (§2, §3) |
| **우리 모드, 공통·서버** | 동기화 어태치먼트(공명, 소지 상태, 보스 게이지), 이벤트 페이로드, 메뉴, 배고픔·경험치·드롭 처리, 부활과 정수 손실 | §2.4, §5 |
| **모드 JAR 안의 내장 리소스팩** (`AddPackFindersEvent`, TOP, 항상 켜짐) | UI 그림 전부(`textures/gui/sprites/**` + 9분할·애니메이션 `.mcmeta`), 바닐라 스프라이트 덮어쓰기(위젯, 보스 바, 토스트, 메뉴 배경, 로고, 파노라마, `mojangstudios.png`), 글꼴, `sounds.json`, 빈 `texts/splashes.txt`, 번역 | §2.3, §4 |
| **내장·월드 데이터팩** | 바닐라 레시피·발전 과제를 지우는 `pack.mcmeta` 필터, 로드 함수로 게임 규칙 적용, 음악·환경음용 커스텀 바이옴 | §3.2, §5 |
| **FancyMenu 3.9.14 + Drippy 3.1.5 + Drippy 초기 로딩 모듈 3.1.5** (의존성, 동봉 안 함) | 타이틀(새 게임 / 이어하기 / 설정 / 종료), 설정 화면 꾸미기, 월드 불러오기·저장 화면, 창 제목과 아이콘, 메뉴 음악, 시작 인트로, 초기·모장 로딩 화면. `modpack_mode=true` | §4.1 |
| **기본 설정 파일** (Default Options 또는 모드팩 `config/`) | `options.txt` 기본값(GUI 배율, 흐림, 튜토리얼 끔, 어두운 모장 배경, 키), Epic Fight 클라이언트 설정, NeoForge `showLoadWarnings=false` | §5 |

리소스팩을 Paxi로 강제하는 방식은 플레이어가 끄기 어렵고 혼란을 준다(Cisco's RPG 사례) [커뮤니티]. **모드 JAR 안 내장 팩**이 깔끔하다.

```
서버 상태(진행, 공명, 장비, 정수)
  ⇄ 버전 붙은 페이로드·어태치먼트(스냅숏, 검증된 행동)
  ⇄ 클라이언트 UI 뷰 모델
      → HUD·보스 렌더러, 게임 화면·메뉴, FancyMenu(타이틀·설정)
리소스팩(글꼴, 스프라이트, 소리, 번역) → 위 전부와 Drippy
```

---

## 2. HUD를 코드로

### 2.1 층 API (NeoForge 21.1.x) [확인: 1.21.1 브랜치 소스]
바닐라 층(그리는 순서): `camera_overlays`, `crosshair`, `hotbar`, `jump_meter`, `experience_bar`, `player_health`, `armor_level`, `food_level`, `vehicle_health`, `air_level`, `selected_item_name`, `spectator_tooltip`, `experience_level`, `effects`, `boss_overlay`, `sleep_overlay`, `demo_overlay`, `debug_overlay`, `scoreboard_sidebar`, `overlay_message`(액션 바), `title`, `chat`, `tab_list`, `subtitle_overlay`, `saving_indicator`.

- **등록**: `RegisterGuiLayersEvent`(모드 버스, 클라이언트). `registerAbove/Below/AboveAll/BelowAll`, `replaceLayer`, `wrapLayer`. 콜백은 `LayeredDraw.Layer`(`GuiGraphics, DeltaTracker`)다. 1.20.4 튜토리얼의 `IGuiOverlay`, `RegisterGuiOverlaysEvent`는 옛 API라 쓰지 않는다 [Codex: 중국어 튜토리얼 함정].
- **숨기기**: `RenderGuiLayerEvent.Pre`(게임 버스)를 `getName()`으로 골라 취소. `RenderGuiEvent.Pre`를 통째로 취소하면 **우리 HUD도 사라진다** [확인: GuiLayerManager].
- **F1 주의**: 우리가 등록한 층은 바닐라 하위 그룹의 표시 조건을 물려받지 않는다. `options.hideGui`, 컷신, 관전·사망 상태를 직접 확인한다 [확인].
- 체력·방어·배고픔 묶음은 `gameMode.canHurtPlayer()`일 때만 그린다.

**숨길 것**: `HOTBAR`, `EXPERIENCE_BAR`, `EXPERIENCE_LEVEL`, `PLAYER_HEALTH`, `ARMOR_LEVEL`, `FOOD_LEVEL`, `SELECTED_ITEM_NAME`, `EFFECTS`, `BOSS_OVERLAY`(또는 §2.5), `JUMP_METER`, `VEHICLE_HEALTH`, `AIR_LEVEL`(또는 다시 그림), Epic Fight 네 층, 출시판의 `DEBUG_OVERLAY`·`CHAT`.
**남길 것**: `TITLE`, `SUBTITLE_OVERLAY`, `CAMERA_OVERLAYS`. 글꼴과 스프라이트로 꾸민다. 대체물이 있는 것만 숨긴다. 물속 공기·독처럼 플레이어에게 영향을 주는 것은 우리 방식으로라도 보여 준다 [Codex].

예시 (API 이름은 확인, 컴파일은 안 함):
```java
// 클라이언트 모드 버스
static void registerHud(RegisterGuiLayersEvent e) {
    e.registerAboveAll(ResourceLocation.fromNamespaceAndPath(MODID, "combat_hud"), (g, delta) -> {
        var mc = Minecraft.getInstance();
        if (mc.player == null || mc.options.hideGui || mc.player.isSpectator() || Cutscene.active()) return;
        GameHud.draw(g, delta.getGameTimeDeltaPartialTick(false));
    });
}
// 게임 버스
static final Set<ResourceLocation> HIDDEN = Set.of(
    VanillaGuiLayers.HOTBAR, VanillaGuiLayers.PLAYER_HEALTH, VanillaGuiLayers.ARMOR_LEVEL,
    VanillaGuiLayers.FOOD_LEVEL, VanillaGuiLayers.EXPERIENCE_BAR, VanillaGuiLayers.EXPERIENCE_LEVEL,
    VanillaGuiLayers.SELECTED_ITEM_NAME,
    ResourceLocation.parse("epicfight:stamina_bar"), ResourceLocation.parse("epicfight:skills"),
    ResourceLocation.parse("epicfight:weapon_innate"), ResourceLocation.parse("epicfight:charging_bar"));
static void suppress(RenderGuiLayerEvent.Pre e) { if (HIDDEN.contains(e.getName())) e.setCanceled(true); }
```

**참고 구현 (1.21.1 NeoForge)** [확인]
- **Kingdom Keys 2** 2.9.4d(LGPL-3.0): 액션 RPG용으로 가장 가까운 토탈 HUD. 층 20개(HP, MP, 드라이브 게이지, 커맨드 메뉴, 초상화, 락온, 파티, 미니맵 등), HUD 편집기, 자체 KO 화면, 차원 전환 화면.
- **Stardew HUD**(중국, CC0): HUD 전체 재스킨. CC0라 코드를 그대로 가져다 써도 된다.
- **Souls Message Banners** 1.2.2(MIT): 엘든 링식 배너. 사망·지역 이름 배너 참고. 글은 우리가 쓴다.
- RPG-HUD 3.13(GPL-3.0), Souls Combat HUD(MIT, 1.20.1 Forge만 → 참고 코드로만).

### 2.2 Epic Fight HUD 처리 [확인: 21.17.3.1 소스]
- 네 층은 `registerAboveAll`로 등록된다. 순서에 기대지 말고 **ID로 취소**한다. Epic Fight를 올릴 때마다 네 ID를 다시 확인한다.
- `skills`를 숨기면 왼팔 기능의 쿨다운·충전 표시는 우리가 그린다. `BattleModeGui`는 `EpicFightCapabilities.getCachedLocalPlayerPatch()`로 스태미나와 스킬 컨테이너를 읽는다. 고정한 소스에 맞춘 어댑터를 쓴다.
- **스태미나 표시를 숨기는 것과 스태미나 소모를 끄는 것은 별개다.** 공명율은 이름만 바꾼 스태미나가 아니라 새 메커니즘이다(기술 위험, `.ai/PROGRESS.md`).
- **월드 속 엔티티 UI는 다른 경로**다. 화면 층을 꺼도 몹 머리 위 체력 바·대상 표시는 남는다. 클라이언트 설정 `ingame.health_bar_show_option=NONE`, `ingame.show_target_indicator`, `ingame.enable_target_entity_guide`, 또는 게임 규칙 `disableEntityUI true`(전부 끔). 락온 로직은 따로 유지한다.
- 그 밖 설정: `ingame.show_epicfight_attributes=false`(툴팁 줄), `ingame.camera.camera_mode=ALWAYS`(자체 3인칭), `lock_on_range`, `lock_on_quick_shift`, `ingame.ui.*` 위치. "스태미나 바 숨기기" 토글은 없다.
- 다시 칠할 수 있는 텍스처: `epicfight:textures/gui/battle_icons.png`, `healthbars1/2.png`, `screen/skill_edit.png`, `screen/skillbook.png`. Epic Fight 그림은 ARR이라 **수정본 PNG를 재배포하지 않고** 우리 그림으로 덮는다.
- Epic Fight의 보스 바 훅은 엔더 드래곤 기절 막대만 더한다. 우리 보스 바와 부딪치지 않는다.
- 기본 키: L-Shift, K(스킬 편집), Y, L-Alt, Space, R(모드 전환), G, 좌우 화살표, 가운데 클릭(락온). Default Options로 다시 정한다.

### 2.3 그리기 [확인: 1.21.1 JAR]
- `GuiGraphics.blitSprite`는 GUI 아틀라스에서 그린다. `assets/<modid>/textures/gui/sprites/**.png`는 자동으로 아틀라스에 들어가고 `<modid>:경로`로 부른다.
- `.png.mcmeta`의 `gui.scaling`: `stretch`, `tile`, `nine_slice`(예: 바닐라 버튼 `{"type":"nine_slice","width":200,"height":20,"border":3}`). 인벤토리를 고정 스크린숏 한 장으로 만들지 말고 9분할 패널과 막대로 짠다.
- **GUI 스프라이트 애니메이션이 1.21.1에서 된다**(바닐라 `icon/trial_available`). 공명율 반짝임, 저체력 맥동, 주문 준비 빛은 코드 없이 텍스처 애니메이션으로.
- `"texture": {"blur": true}`로 선형 필터. 애니풍 고해상도 HUD 틀과 로고에 쓴다.
- 코드 없이 다시 칠할 수 있는 것: GUI 스프라이트 400개(`hud/*` 75, `boss_bar/*` 22, `toast/*` 11, `widget/*` 32, `container/*` 100 등), `menu_background.png`, `inworld_menu_background.png`, 구분선, `title/minecraft.png`, `title/edition.png`, 파노라마 6장, `title/mojangstudios.png`, `texts/splashes.txt`. 옛 `gui/icons.png`, `widgets.png` 안내는 1.21.1과 맞지 않는다 [Codex].

**1080p 배율** [추정]: 자동 GUI 배율은 1920×1080에서 4(480×270 공간)다. HUD는 **가상 1920×1080 캔버스**에 그린다. 층 안에서 `pose().scale(s, s, 1)`, `s = 창 높이 / 1080 / GUI 배율`. 그러면 플레이어가 GUI 배율을 바꿔도 HUD는 같고 바닐라 화면은 배율을 따른다. MCC Island도 GUI 배율 정렬 문제 때문에 클라이언트 모드(Noxesium)를 만들었다 [확인]. 픽셀아트 요소는 1/4 해상도 + 최근접 필터, 애니풍 요소는 1:1 + `blur:true`. **요소마다 하나를 고르고 섞지 않는다.** MC Story Mode 팩은 1080p·GUI 배율 2에 고정해서 다른 배율에서 깨졌다 [확인: 작가 경고].

**부드러운 움직임**: 서버 값은 20Hz로 온다. 날것을 바로 보여 주지 않는다. 틱 값은 `getGameTimeDeltaPartialTick(false)`로 보간하고, 순수 시각 효과(체력 피해 잔상, 공명 구간 채움과 번쩍임, 숫자 올라가기)는 실제 시간(`Util.getMillis()`)으로. 사망 연출 길이도 **경과 시간 기준**으로 한다. 저프레임에서 사망 연출이 길어진 중국 팩 사례가 있다 [커뮤니티].

**셰이더와 흐림**: 바닐라 메뉴 흐림은 `shaders/post/blur.json`, 강도 옵션 `menuBackgroundBlurriness`(0~10). 우리 화면은 `Screen.renderBlurredBackground(partialTick)`를 부른다. GUI에 커스텀 GLSL(`RegisterShadersEvent`)도 되지만 Iris 팩이 켜졌을 때 GUI 패스에서 어떻게 되는지는 문서가 없다 [미확인]. **기본은 스프라이트 애니메이션 + 가산 혼합**으로 빛을 낸다.

### 2.4 HUD에 값 보내기
- **동기화 어태치먼트** [확인: 21.1.259 소스와 changelog]: `AttachmentType.builder(...).serialize(codec).sync(streamCodec)`이면 추적하는 모든 클라이언트에, `.sync((holder, player) -> 조건, streamCodec)`이면 주인에게만. `setData`/`removeData`가 동기화를 일으키고, 객체 안을 고친 뒤에는 `holder.syncData(TYPE)`.
  - ⚠ **두 조사가 엇갈린다.** Codex는 1.21.1 문서 페이지("클라이언트로 직접 패킷을 보내야 한다")를 근거로 자동 동기화가 없다고 봤다. Claude 조사는 1.21.1 브랜치 소스(`AttachmentType.java` 247~290행)와 changelog("21.1.197 Backport to 1.21.1: Syncable Data Attachments")를 읽었다. 소스와 changelog가 더 구체적이라 그쪽을 따르되, **1단계 모드 골격에서 21.1.259로 컴파일해 확인**한다. 안 되면 페이로드로 보낸다.
- 일회성 사건(타격 번쩍임, 보스 페이즈 전환, "패리!", 사망 배너)은 `RegisterPayloadHandlersEvent` → `playToClient` → `PacketDistributor.sendToPlayer`.
- 정수(화폐)처럼 큰 값과 복합 데이터는 `DataSlot` 대신 페이로드로. 클라이언트가 보낸 화폐 값을 믿지 않는다.
- 어태치먼트는 기본적으로 사망 때 복사되지 않는다. `copyOnDeath`나 `PlayerEvent.Clone`으로 정한다. 정수 손실은 서버에서 **한 번만** 적용하고 부활 때 새 스냅숏을 보낸다.

데이터 나누기 [추정]:
| 어태치먼트 | 내용 | 동기화 |
| --- | --- | --- |
| 플레이어 `resonance` | 공명 값, 장착 인장에서 온 구간 배치, 긴급 회복 표시 | 주인만 |
| 플레이어 `inventory_state` | 수액 병 충전·최대, 정수, 왼팔 기능과 쿨다운 끝 틱, 주문 3칸과 비용 | 주인만 |
| 보스 엔티티 `boss_gauge` | 공명이나 자세, 페이즈 | 추적자 |

HUD는 `player.getData(...)`로 읽는다. 폴링 패킷이 필요 없다. **매 프레임 디스크 접근, 글꼴 파싱, JSON 읽기, 서버 질의 금지.** 전투 HUD 추가 CPU 렌더 시간 목표는 1ms 이하 [Codex 제안].

### 2.5 보스 바
- `CustomizeGuiOverlayEvent.BossEventProgress`(취소 가능, 바마다)를 취소하고 우리 바를 그린다. 동기화는 바닐라 `ServerBossEvent`를 그대로 쓴다.
- 두 번째 게이지(라이벌 블레이더의 공명, 자세)나 여러 페이즈 체력은 보스 어태치먼트 + 우리 층. 아니면 `BOSS_OVERLAY`를 통째로 끈다. **주인은 하나만.**
- 원작 배치: 맨 위 가운데 아주 얇은 선, 가시 달린 양 끝, 위에 세리프 이름, 빨간 피해 잔상([`docs/design/original.md`](../design/original.md) 3.3절).

---

## 3. 화면

### 3.1 아무 화면이나 바꾸기 [확인]
- `ScreenEvent.Opening`(게임 버스, 취소 가능)이 `Minecraft.setScreen`마다 온다. `setNewScreen`으로 `InventoryScreen`, `PauseScreen`, `DeathScreen`, `TitleScreen`, `AdvancementsScreen`, `ChatScreen`, `LevelLoadingScreen`, `ReceivingLevelScreen`, Epic Fight `SkillEditScreen`을 우리 것으로 바꾼다. 리스너 안에서 다시 `setScreen`을 부르지 않는다.
- 진행 콜백이나 서버 컨테이너를 가진 화면도 있으니 **무조건 바꾸는 라우터를 만들지 않는다** [Codex].
- NeoForge가 바닐라 화면에 넣는 "Mods" 버튼과 "NeoForge x.y / N mods loaded" 문구는 화면을 바꾸거나 FancyMenu로 꾸미면 사라진다. 모드 로딩 경고 화면은 `showLoadWarnings`로 숨긴다.
- 구역이 다른 차원이면 `RegisterDimensionTransitionScreenEvent`(21.1.33+)로 차원 쌍마다 전환 화면을 등록한다. 원작은 지역 사이 검은 로딩 화면이 "세계가 끊긴 느낌"이라는 비판을 받았다 [커뮤니티]. 전환 화면에 그림과 팁을 넣는다.

### 3.2 인벤토리 → 장비·인장·능력치, 제작 제거
- 메뉴 틀 [확인]: `MenuType`(`IMenuTypeExtension.create`), `AbstractContainerMenu`(슬롯과 상태), `AbstractContainerScreen`(그리기와 입력), `RegisterMenuScreensEvent`, 서버에서 `openMenu(provider, buf -> ...)`.
- 흐름 [추정]: `InventoryScreen`을 `ScreenEvent.Opening`에서 막고 → C2S 페이로드 → 서버가 `EquipmentMenu`(무기 1·2, 소모품 퀵슬롯, 인장 칸, 소지품) 열기 → 화면은 동기화 어태치먼트로 능력치를 그린다. 바닐라 `InventoryMenu`는 슬롯 위치가 고정이고 2×2 제작 칸이 있어서 **별도 메뉴가 깔끔하다**. 배경 PNG만 바꾸면 슬롯 판정 위치는 그대로다.
- 장비는 클라이언트 아이콘 배열이 아니다. 서버가 장착·강화 비용·조건을 검증하고 결과를 돌려준다. 중복 클릭, 강화 중 접속 끊김, 사망 후 재접속에서 정수·아이템이 복제되거나 손실이 반복되지 않아야 한다.
- **제작 데이터 제거** [확인]: 1.21.1에는 `data/minecraft/recipe/` 1,290개, `data/minecraft/advancement/` 1,399개(그중 1,277개가 레시피 해금용)가 있다. 데이터팩 `pack.mcmeta`에 `"filter": {"block": [{"namespace":"minecraft","path":"recipe/.*"}, {"namespace":"minecraft","path":"advancement/.*"}]}`. 데이터팩 형식 48, 리소스팩 34. 바닐라 레시피를 참조하는 모드의 로그 경고는 시험한다.
- 원작 메뉴 구조: 3단(능력치 / 목록 / 상세), 능력치는 신체·기량·방어·저항으로 묶음.

### 3.3 일시정지와 설정
- `PauseScreen`을 우리 화면(계속, 장비, 설정, 타이틀로)으로 바꾼다. 저장 후 종료는 바닐라 `PauseScreen.onDisconnect()`(연결 끊기 → "월드 저장 중" → 타이틀)를 따라 한다.
- 설정은 바닐라 `OptionsScreen`을 남기고 `widget/*` 스프라이트, 메뉴 배경, 글꼴, FancyMenu 버튼·슬라이더 템플릿으로 꾸민다. 설정 화면 전체를 새로 쓰는 건 크고 얻는 게 적다. 그래픽, 소리, 키, 언어, 접근성 설정은 남긴다.
- **Sodium 영상 설정과 Iris 셰이더 화면, 다른 모드 설정 화면은 여전히 "모드 티"가 난다.** 플레이어에게 숨기거나 받아들인다.

**메뉴를 열면 게임이 멈추나?** 원작 AI LIMIT은 **메뉴를 열면 멈추고**, 플레이어들이 이 점을 좋게 평가했다(Rushdown: "멈출 때는 멈춰야 한다") [커뮤니티, `design/sources/notes_1c_story_ui_art.md`]. 소울라이크 관례(다크 소울은 안 멈춤)와 다르지만 원작을 따르는 쪽을 권한다.
- 권장: 일시정지 메뉴, 장비·인벤토리 화면, 대화·컷신 건너뛰기 확인은 `isPauseScreen() = true`(싱글에서 멈춤). 묘목 휴식 메뉴는 안전 지대라 어느 쪽이든 상관없고 멈춤으로 통일한다. **사망 화면만 멈추지 않는다**(연출이 흘러야 한다).
- 사용자 결정이 필요하다(§8).

### 3.4 사망 화면
- `DeathScreen`을 우리 화면으로. ESC로 닫히지 않고 멈추지 않는다. 배너와 페이드 후 N초 뒤 또는 버튼으로 `respawn()`.
- 서버: 들고 있던 정수의 일부 손실(인장 유지율), `ServerPlayer.setRespawnPosition`으로 마지막 묘목에서 부활. 재접속으로 손실이 두 번 일어나지 않게.
- 대안 `doImmediateRespawn true` + 우리 오버레이는 사망 화면을 건너뛰지만 Epic Fight 사망 애니메이션도 끊는다.
- 원작: 진흙 끓는 소리와 함께 부활. 참고 구현 Kingdom Keys `KOGui`, Souls Message Banners.

### 3.5 툴팁
- [확인] `RenderTooltipEvent.GatherComponents`(줄 편집, 최대 폭), `.Pre`(취소, 글꼴·위치 → 취소하고 우리 9분할 틀을 그림), `.Color`(배경·테두리 색). 아이콘 줄 같은 풍부한 행은 `RegisterClientTooltipComponentFactoriesEvent`.
- 바닐라 줄 숨기기: 1.21.1에는 아직 `minecraft:hide_additional_tooltip`, `hide_tooltip`, `show_in_tooltip:false`가 있다(1.21.5에서 `tooltip_display`로 바뀜). 속성 줄은 `AddAttributeTooltipsEvent`, `GatherSkippedAttributeTooltipsEvent`(21.1.60+).
- 모드 대안: Legendary Tooltips 1.5.5(+Iceberg, Prism, 모두 CC-BY-NC-ND), Obscure Tooltips 4.2.5(자체 라이선스). **우리 렌더러는 1~2일이면 되고 라이선스 문제가 없다** → 직접 만든다.
- 내용: 공격 속성, 공명 상호작용, 요구 능력치, 장착 비교. 아이템마다 기능 줄 + 설정 줄([`docs/design/original.md`](../design/original.md) 3.6).

### 3.6 채팅, 토스트, 대화
- 채팅: `ClientChatReceivedEvent`(취소·수정), `CustomizeGuiOverlayEvent.Chat`(위치), `CHAT` 층 취소, 출시판에서 `ChatScreen` 막기. 시스템 메시지(아이템 획득, "묘목 회복")는 **우리 알림 층**으로 보내고 채팅은 디버그용으로.
- 토스트: `ToastAddEvent`를 취소해서 우리 토스트만 남긴다. 원작처럼 일반 획득은 작은 토스트, 열쇠 아이템·인장은 큰 배너.
- 대화: 원작은 대화창 없이 아래 가운데 세리프 자막, 오른쪽 아래 확인·건너뛰기. 초상화·이름·선택지·넘기기·줄바꿈을 Java로. 중국 MistInteract(대화 플러그인)의 키보드·스크롤 선택 패턴은 참고만 한다 [Codex].
- 자막(접근성)을 끄지 말고 Epic Fight UI와 겹치지 않게 자리를 비운다. 일본 DawnCraft 가이드가 자막 겹침을 보고했다 [커뮤니티].

### 3.7 컨트롤러 (선택)
Controlify 3.0.1+lts(1.21.1 NeoForge, LGPL-3.0, YACL 필요)의 `ScreenProcessor` API. Epic Fight 1.21.1에 Controlify 호환 모듈이 있지만 2.5.0 기준이라 3.0 LTS와는 시험 필요. **모든 우리 화면은 포커스 가능한 위젯(`AbstractWidget` + 내레이션)으로 만든다.** 마우스 전용 판정에 기대지 않는다. 키보드 플레이에도 좋다.

---

## 4. 코드 없이 바꾸는 것

### 4.1 FancyMenu와 Drippy [확인: Modrinth API, 1.21.1 NeoForge]
| 모드 | 버전 | 라이선스 | 비고 |
| --- | --- | --- | --- |
| FancyMenu | 3.9.14-1.21.1-neoforge (2026-09-28) | DSMSLv3.1 | Konkrete 1.9.9(Apache-2.0), Melody 1.0.10(MIT) 필요 |
| Drippy Loading Screen | 3.1.5 | DSMSLv3 | 모장 로딩 화면 편집 |
| Drippy Early Loading Module | 3.1.5 | DSMSLv3 | NeoForge 초기 창 |
| SpiffyHUD | 3.1.2 | DSMSLv3 | HUD 편집기. **Java HUD와 겹치므로 안 씀**(빠른 시안용으로만) |

- **라이선스**: 모드팩에서 쓰는 건 되지만 파일을 직접 넣으면 안 되고, 공식 다운로드를 가리키는 의존성으로 적어야 한다. 우리 레이아웃과 에셋만 `config/fancymenu/`에 둔다.
- **할 수 있는 것**: 타이틀 화면 전 인트로 애니메이션·영상, 창 아이콘과 제목(16×16, 32×32, macOS `.icns`, 아이콘에 투명 픽셀 하나 이상), 기본 GUI 배율, 전체 화면 강제, 9분할 버튼·슬라이더 텍스처, 메뉴 배경과 파노라마, 메뉴 음악, 클릭 소리, 월드 로딩 배경, 커서 요소(32×32나 64×64 PNG + 핫스팟).
- **커스텀 GUI**: 버튼·이미지·글자·오디오로 새 화면을 만들고 "Override Current with Custom GUI"로 아무 화면이나 대체. 액션 `loadworld <폴더>`, `join_last_world`, `opengui`, `quitgame`.
- **에이전트 친화적**: 레이아웃이 평문 `fancymenu_layout` 파일이다 [커뮤니티]. 다만 손으로 문법을 지어내지 말고, 고정한 편집기 버전으로 저장한 파일을 diff로 관리한다 [Codex]. 사용자는 스크린숏으로 검수한다.
- 배포: `config/fancymenu/` 복사, `config/fancymenu/options.txt`에 `modpack_mode=true`(편집 막대와 단축키 숨김). 개발 프로필에서는 복구 수단을 남긴다(`Ctrl+Alt+C`).
- 확장: FancyMenu v3 개발 문서의 `Placeholder`/`PlaceholderRegistry`, `Action`/`ActionRegistry`로 우리 상태(공명, 정수, 저장 존재 여부)를 레이아웃에 노출하고 "이어하기" 액션을 만든다. 문서가 2024년 것이라 3.9.14 API로 서명을 확인한다.
- 영상 배경은 추가 미디어 모드가 필요하고 까다롭다. **APNG나 스프라이트 시트 애니메이션**이 안전하다 [커뮤니티].
- 중국어 Bilibili 튜토리얼 일부는 FancyMenu 2.x 기준이라 의존성 목록이 다르다(영상 페이지가 직접 경고) [Codex].

**역할 분담**: FancyMenu는 타이틀, 설정 꾸미기, 월드 불러오기·저장 화면, 창 제목·아이콘, 메뉴 음악. **실시간 게임 데이터가 필요한 화면(인벤토리, 장비, 묘목 메뉴, 사망, HUD)은 Java.**

### 4.2 로딩 화면 세 단계 [확인]
| 단계 | 도구 | 주의 |
| --- | --- | --- |
| 1. NeoForge 초기 창(렌더러가 생기기 전) | **Drippy Early Loading Module 3.1.5** | 월드, 플레이어, 글꼴 시스템에 기대지 않는 단순 그림 + 진행. `earlyWindowControl=false`는 초기 창을 끄는 우회책이지 꾸미는 방법이 아니다. 대안 Simple Custom Early Loading 2.2(LGPL-2.1, 모장 로고 제거 불가), Custom Loading Screen 0.2.0(베타, ARR). **초기 창 제공자는 하나만** |
| 2. 모장 `LoadingOverlay`(리소스 다시 불러오기) | **Drippy Loading Screen 3.1.5** | 처음 실행과 F3+T 둘 다 시험. 모드 없이는 `darkMojangStudiosBackground:true`와 `title/mojangstudios.png`뿐 |
| 3. 월드 불러오기·저장 | FancyMenu 레이아웃(`world_load_progress` 플레이스홀더) 또는 `ScreenEvent.Opening` | 장식 애니메이션이 아니라 실제 진행을 묶는다 |

연결 중, 연결 끊김, 저장 중, 월드 생성, 오류 화면도 따로 확인한다. 실패 이유와 취소·뒤로·종료 동작은 남긴다. FML 자체 초기 창 테마(NeoForge PR #2346)는 1.21.6부터라 못 쓴다.

### 4.3 창 제목, 아이콘, 커서
- 창 아이콘은 에셋 인덱스 루트 `icons/`에 있어서 **리소스팩으로 못 바꾼다** [확인]. FancyMenu 전역 설정이나 믹스인(`Minecraft.createTitle()`, `Window.setIcon`).
- 커서: FancyMenu 커서 요소, Cursors Extended 3.11.3(MIT), Custom Cursor 3.0.3(베타), 또는 `GLFW.glfwCreateCursor`. **주인은 하나만.** 모든 GUI 배율에서 핫스팟을 시험하고 화면을 나갈 때 원래 포인터로 돌린다.

### 4.4 글꼴 (한국어 포함)
- 제공자 종류 [확인]: `bitmap`, `space`(음수 폭 가능), `ttf`(`size`, `oversample`, `shift`, `skip`; 커닝·합자 제거), `unihex`(16px Unifont `.hex`), `reference`, `filter`.
- 1.21.1 `font/default.json`은 `include/space` → `include/default` → `include/unifont` 참조뿐이다. JAR 안 `include/unifont.json`은 빈 껍데기이고 실제 `unihex` 정의는 에셋 인덱스에서 받는다 [확인]. **바닐라 한글은 16px Unifont를 반 크기로 그려서 Mojangles보다 가늘다.** CJK 글리프가 빠지면 JAR만 보지 말고 에셋 인덱스까지 본다.
- `default.json`과 `uniform.json`(유니코드 강제) **둘 다** 덮어야 완전히 바뀐다.

후보 [확인: 라이선스]:
| 글꼴 | 라이선스 | 쓰임 [추정] |
| --- | --- | --- |
| **Pretendard** | OFL-1.1 | 한국어 본문·제목 1순위 시험. 정적 데스크톱 TTF 사용(웹폰트 아님) |
| **Galmuri** (11/9/7px, 한글 11,172자) | OFL-1.1 | 픽셀 느낌 보조 테마, 작은 글자 |
| Neo둥근모 (16px) | OFL-1.1 | 픽셀 대안 |
| Source Han Sans | OFL-1.1 | 넓은 CJK 대체 글꼴. 파일이 커서 메모리 측정 |
| BIZ UDGothic | OFL-1.1 | 일본어 |
| LXGW WenKai | OFL-1.1 | 중국어 서사 느낌 |
| BetterHangulFont(bhf4mc) | MIT | 한글 비트맵 생성 예시 |

글꼴 세 층 [Codex 제안]: `<modid>:body`(읽는 글), `<modid>:display`(제목), `<modid>:icons`(사용자 정의 영역 그림 문자). 체력 같은 핵심 숫자는 글리프가 없어도 보이게 일반 그리기로 한다. HUD 숫자는 별도 비트맵 글꼴(`<modid>:hud_digits`)을 `Style.withFont`로. 16px 글리프에 `"height": 8`을 주면 바닐라처럼 배치되고 2배 선명하다.

TTF 시작값(실제 글꼴로 조정):
```json
{ "providers": [
  { "type": "ttf", "file": "<modid>:body.ttf", "size": 11, "oversample": 2, "shift": [0, 0] },
  { "type": "reference", "id": "minecraft:include/unifont" } ] }
```
- 픽셀 글꼴은 `size`를 글꼴의 픽셀 em에, `oversample`은 정수(GUI 배율 4면 4)로.
- 정밀한 픽셀 격자가 필요하면 Galmuri BDF → `.hex` 변환해 `unihex`로. 11,172자를 `bitmap` 페이지로 만드는 건 비현실적.
- 음수 공백 글꼴(Negative Space Font, CC-BY-4.0)은 채팅·튜토리얼·타이틀 그림 문자에. 계속 움직이는 전투 게이지와 인벤토리 패널은 `GuiGraphics`로 직접.
- **Modern UI 3.13.0.1**(LGPL-3.0)은 부드러운 글자와 좋은 대체 글꼴을 주지만 전역 렌더링을 바꾸고, FancyMenu와 충돌 보고(#971)가 있고, 바닐라 TTF의 `oversample`·`shift`·`skip`을 다르게 다룬다 [확인: 작가 설명]. **기본은 바닐라 TTF**, Modern UI는 같은 장면에서 비교 시험만.
- OFL 라이선스 파일을 팩과 크레딧에 남긴다. 글꼴만 따로 팔 수 없다. "내 PC에 있는 맑은 고딕"은 배포할 수 없다.
- 시험 문장 [Codex]: `공명율 · 정수 1234567890`, `裝備 / 装备`, `生命值`, `装備・共鳴率`, 화살표, %, 빼기, 문장부호, 여러 줄 대화, 한글·영문 혼합. GUI 배율 1~4, 유니코드 강제 켜고 끄기, F3+T, 대체 글리프, IME 입력.
- 원작은 한국어·일본어 현지화와 글자 배치로 비판받았다 [확인: 나무위키]. 한국어 글자 배치를 처음부터 실제 폭(`Font.width`)으로 계산한다.

### 4.5 소리와 음악
- UI 소리는 사운드 이벤트(`ui.button.click`, `ui.toast.in/out`, `ui.toast.challenge_complete`)다. `assets/minecraft/sounds.json`에서 `"replace": true`로 우리 OGG로 바꾼다.
- 우리 UI 이벤트 [Codex 제안]: `<modid>:ui.confirm`, `cancel`, `focus`, `tab`, `error`, `equip`, `checkpoint`, `death`. 포커스 소리는 포커스가 바뀔 때만.
- 음악: NeoForge `SelectMusicEvent`(21.0.69+)에서 지역·보스·메뉴 곡을 정하거나 `null`로 바닐라 음악을 끈다. `PlaySoundEvent.setSound(null)`로 상황별 차단(취소는 안 됨).
- 지역 환경음은 커스텀 바이옴의 `music`, `ambient_sound`, `mood_sound`, `additions_sound`를 `/fillbiome`으로 칠한다. 음악 출처와 라이선스는 [`docs/world/README.md`](../world/README.md) 3.3.

### 4.6 에셋 배치 (제안)
```
assets/<modid>/
  font/body.json, body.ttf, display.json, icons.json, hud_digits.json
  textures/gui/sprites/hud/..., panels/...
  textures/gui/portraits/...
  textures/font/ui_icons.png
  lang/ko_kr.json, en_us.json
  sounds/ui/..., sounds.json
  ui/theme.json            # 우리 형식: 위치, 여백, 색, 스프라이트·글꼴 ID, 애니메이션 시간만
config/fancymenu/
  assets/...               # 인스턴스 상대 경로
  customization/...        # 고정 편집기로 저장한 레이아웃
```
테마 파일에는 **보이는 것만** 넣는다. 전투 계산, 경제 규칙, 부활 판정은 넣지 않는다. 리소스 다시 불러오기(`RegisterClientReloadListenersEvent`) 때 파싱하고 캐시한다. 스프라이트·글꼴 ID가 없으면 읽을 수 있는 대체를 보인다.

---

## 5. 바닐라 느낌 없애기

1.21.1 게임 규칙은 **camelCase**다. 지금 위키의 snake_case 이름은 1.21.11부터다. `spawnerBlocksEnabled`, `spawnMonsters`, `pvp`, `tntExplodes`, `locatorBar`는 1.21.1에 없다 [확인].

| 바닐라 요소 | 1.21.1에서 없애는 법 |
| --- | --- |
| 배고픔 | 게임 규칙이 없다. 서버 `PlayerTickEvent.Post`에서 음식 20, 포화 5, 소모 0으로 고정. 달리기에 음식 6 초과가 필요하므로 20 유지. `FOOD_LEVEL` 층 취소 |
| 자연 회복 | `naturalRegeneration false`. 회복은 수액 병으로만 |
| 경험치 구슬·바 | `doMobLoot false`(아이템과 경험치 둘 다 막음) 또는 `LivingExperienceDropEvent`, `BlockDropsEvent`, `PlayerXpEvent.PickupXp`로 경험치만 0. 경험치 층 취소 |
| 바닐라 몹 생성 | `doMobSpawning false`, `doPatrolSpawning`, `doTraderSpawning`, `doWardenSpawning`, `doInsomnia false`, `disableRaids true`. 적은 우리 생성 로직으로, 묘목에서 초기화 |
| 낮밤, 날씨 | `doDaylightCycle false`, `doWeatherCycle false`. 분위기는 셰이더 |
| 블록 부수기·놓기 | 모험 모드, YAWP 구역, `mobGriefing false`, `doFireTick false`, `randomTickSpeed 0` |
| F3 디버그 | `reducedDebugInfo true`, 출시판에서 `DEBUG_OVERLAY` 취소, `CustomizeGuiOverlayEvent.DebugText` |
| 바닐라 키 | Default Options로 기본값. `InputEvent.InteractionKeyMappingTriggered`로 공격·사용·블록 집기 무력화. L(발전 과제), P(소셜) 화면은 교체. 바닐라 `KeyMapping`은 등록 해제가 안 되니 우리 조작 화면에서 숨긴다 |
| 발전 과제·레시피 토스트 | 데이터팩 필터(§3.2), `announceAdvancements false`, `ToastAddEvent` |
| 튜토리얼 안내 | 옵션 `tutorialStep:none`, `joinedFirstServer:true`, `onboardAccessibility:false`, `skipMultiplayerWarning:true`, `hideSplashTexts:true` |
| 사망 메시지, 명령 출력 | `showDeathMessages false`, `sendCommandFeedback false`, `commandBlockOutput false`, `logAdminCommands false` |
| 1인칭 손 | `RenderHandEvent`, `RenderArmEvent`. Epic Fight가 이미 바닐라 손을 취소하고 1인칭 모델을 그린다. 3인칭 고정이면 거의 안 보인다 |
| 카메라 | **Epic Fight 자체 3인칭 `camera_mode=ALWAYS` + 락온**(추가 모드 불필요). 대안 Shoulder Surfing Reloaded 5.2.0(MIT): Epic Fight에 호환 코드가 있지만 SSR 4.18.1 기준이라 5.x는 시험 필요. **카메라 시스템은 하나만** |
| 핫바 스크롤·숫자 키 | `HOTBAR` 층을 숨겨도 숫자 키·스크롤 슬롯 전환은 남는다. `InputEvent.MouseScrollingEvent` 취소, 숫자 키는 우리 퀵슬롯에 매핑 |

숨기기만 하고 시스템이 남아 있으면 안 된다. 예: 배고픔 바를 숨겼는데 실제로 굶어 죽거나, 자연 회복이 남아 있는 경우 [Codex].

---

## 6. 사례에서 배운 것

| 사례 | 방법 | 교훈 |
| --- | --- | --- |
| MCC Island (Noxcrew) | 서버 리소스팩이 코어 셰이더를 덮음 + 선택 클라이언트 모드 Noxesium(GUI 배율 제한, 배율·창 크기 보고, 카메라 잠금, F1·디버그 제한) | 최고 수준 리소스팩 UI도 결국 클라이언트 모드가 필요했다. 우리는 모드를 어차피 배포하므로 이 이점을 그냥 얻는다 |
| Wynncraft | 서버 팩(글꼴 HUD) + 클라이언트 모드 Wynntils가 보스 바 대체 | 풍부한 UI는 클라이언트 모드로 간다 |
| ItemsAdder·Oraxen·BetterHud | 글꼴 글리프 + 음수 공백으로 컨테이너 제목·액션 바에 그림 | 읽기 전용 그림. 슬롯을 옮기거나 더할 수 없고 GUI 배율에 깨진다 |
| **Kingdom Keys 2** | 층 20개, HUD 편집기, 자체 사망·메뉴·전환 화면 | **우리 로더와 버전에서 액션 RPG 전체 UI 교체가 된다는 오픈소스 증거** |
| Souls of Lunareth (1.20.1) | "타이틀부터 설정, 오디오 믹서, 프로필까지 모든 메뉴를 손으로" | 모드팩 수준 토탈 UI는 흔한 관행 |
| Ashen Vow 1.0.0 (1.21.1 NeoForge, Epic Fight) | 커스텀 타이틀·로딩, 초기 로딩 모듈 별도 설치 언급 | 같은 플랫폼 소울라이크 참고. 시체 회수식 사망 규칙은 가져오지 않는다 |
| MC Story Mode: Perfect Pack (1.20.1) | 인게임 GUI·핫바, 타이틀 두 개, 부팅 UI, 일시정지 페이드, 소리 교체 | 1080p·GUI 배율 2 고정이라는 실패 사례 |
| HoYoI (MIT) | 원신식 로딩·ESC 화면, 언어별 팁 | 화면 구성 참고. 1.21.1 NeoForge 파일은 없다 |
| 한국 DC 스티브 갤러리 개발 글 | KubeJS UI를 모드 코드로 바꾸고 FPS 약 10배 개선 주장 | 벤치마크 없음. 그래도 **Java로 그리는 방향**을 지지한다 |
| 중국 PaiUI | HTML/CSS/JS로 인벤토리·ESC·사망·HUD 교체, 유료·비공개 | 브라우저 UI 경로. 메모리 비용 미측정이라 쓰지 않는다 |

리소스팩만으로 **되는 것**: 모든 바닐라 스프라이트, 메뉴 배경·로고·파노라마·스플래시, 글꼴, 소리, 타이틀·액션 바·보스 바 글리프 트릭.
**안 되는 것**: 바닐라 위젯 이동·크기 변경(투명으로 숨기기만), 실시간 데이터, 툴팁 틀, 창 아이콘, 초기 로딩 화면, Iris가 켜진 상태의 코어 셰이더.

**쓰지 않기로 한 것** [확인]: KubeJS Painter(1.21 이후 제거. 별도 PainterJS 1.2.0이 있지만 매 프레임 전투 UI는 Java로), CustomHUD(Fabric만), HoYoI·Auudio·YOSBR(1.21.1 NeoForge 파일 없음), Connector로 Fabric UI 모드 끌어오기, ModernUI 기본 채택, Blur+ 추가 흐림 시스템.

---

## 7. 함정과 시험 목록

1. **Iris**: 리소스팩 코어 셰이더에 기대지 않는다. 모드 GUI 셰이더는 미확인이니 셰이더 없는 대체 경로를 둔다.
2. **ImmediatelyFast `hud_batching`**: 우리 성능 목록의 ImmediatelyFast 1.6.15는 HUD 일괄 처리로 커스텀 HUD·툴팁을 깬 이력이 있다(#233, #227, #296, #485는 1.21.1 NeoForge). 켜고 끄고 시험해서 문제가 있으면 끄고 배포한다.
3. **메뉴 흐림 + FancyMenu**: 큰 UI 모드 조합 + Iris에서 화면이 안 보이는 문제(#1665). 우리 화면은 바닐라 `renderBlurredBackground`를 쓰거나 `menuBackgroundBlurriness:0`.
4. **GUI 배율**: HUD는 가상 1080p 캔버스. 바닐라 화면과 FancyMenu 레이아웃은 기본 GUI 배율 고정. 배율 1~4, 1280×720, 창 크기 변경 시험.
5. **Epic Fight 층 순서**: 순서가 아니라 ID로 취소. 업데이트마다 네 ID 재확인.
6. **1.21.1 어태치먼트 문서는 낡았다**: 21.1.259 소스와 changelog를 따른다(§2.4의 엇갈림은 1단계에서 확인).
7. **라이선스**: FancyMenu·Drippy(DSMSL)는 참조만, Legendary Tooltips 계열(CC-BY-NC-ND)은 수정 금지, Balm·Default Options(ARR)는 의존성으로 괜찮음, OFL 글꼴은 라이선스 파일 유지, Epic Fight 텍스처(ARR)는 우리 그림으로 덮기.
8. **보고된 문제를 시험으로**: Drippy Early + FancyMenu macOS 크래시(#126, 우리 대상은 Windows), 1.21.1 편집기 클릭 문제·Sodium 테두리 없는 창 충돌·Iris 전환 깜빡임(Drippy 이슈), 초기 창 전환 때 파노라마 알파(NeoForge #3258).

**통과 기준** [Codex 제안을 우리 환경에 맞춤]
| 시험 | 통과 |
| --- | --- |
| 해상도 | 1920×1080, 1280×720, 창 크기 변경, GUI 배율 1~4에서 핵심 정보가 잘리지 않고 슬롯 판정이 맞음 |
| 한국어 | 한국어·영어 기본, 유니코드 강제 켜고 끄기, 긴 이름·대화, 대체 글리프, IME |
| HUD 주인 | 체력 바 하나, 공명 게이지 하나, 의도한 보스 UI만. Epic Fight 스태미나·스킬이 어느 전투 모드에서도 겹치지 않음. F1과 컷신 정책을 따름 |
| 입력 | 마우스, 키보드 포커스, 다시 정한 인벤토리·일시정지·회복 키, 숫자·스크롤. 메뉴 클릭이 전투 행동을 일으키지 않음 |
| 수명 주기 | F3+T, 창 크기·전체 화면, 사망·부활, 저장·종료 후 커서·가위 영역·소리 반복·낡은 보스 상태가 남지 않음 |
| 규칙 | 숨긴 배고픔·제작·경험치가 실제로 꺼짐 |
| 경제 | 중복 클릭, 강화 중 끊김, 사망 + 재접속에서 정수·아이템 복제나 이중 손실 없음 |
| 성능 | RTX 4060 / Ryzen 5 5600 / 16GB, 1080p 보스전에서 HUD 켜고 끄고 프레임 시간 비교. 50fps = 평균 20ms 이하, 끊김은 따로 보고 |

---

## 8. M1 구현 순서와 사용자 결정

**공수 추정** [추정, 에이전트가 쓰고 사용자가 검수, 그림은 별도]
| 항목 | 기간 |
| --- | --- |
| HUD 틀(가상 1080p, 스프라이트 도우미, 보간, 층 취소) | 2~3일 |
| 체력·공명·수액 병·왼팔·주문·정수 HUD | 4~7일 |
| 보스 바(+ 라이벌 공명 게이지) | 2~3일 |
| 배너와 사망 오버레이 | 2일 |
| 동기화 어태치먼트와 페이로드 | 2~3일 |
| 장비·인장·능력치 메뉴(서버 검증 포함) | 1.5~3주 |
| 묘목 휴식 메뉴(레벨업, 이동, 강화) | 1.5~3주 |
| 일시정지·사망 화면 | 2~3일 |
| 툴팁 렌더러 | 1~2일 |
| 토스트·채팅·음악 제어 | 1~2일 |
| 글꼴(한국어 TTF나 unihex + 숫자) | 1~3일 |
| FancyMenu 타이틀·로딩·설정 꾸미기 | 3~5일 |
| 바닐라 느낌 제거(게임 규칙, 필터 데이터팩, 처리기, 옵션 기본값) | 2~4일 |
| 컨트롤러(선택) | +1~2주 |

**M1 먼저**(약 4~6주): HUD 세트, 보스 바, 사망 화면, 일시정지 교체, FancyMenu 타이틀·로딩, 글꼴, 바닐라 느낌 제거. 장비·묘목 메뉴는 최소 화면으로 시작.

**단계** [Codex 제안, 채택 권장]
1. **데이터와 HUD 경계 증명**: 플레이어 하나와 시험 보스. 바닐라·Epic Fight 층 숨기기, 체력·공명·수액 병·정수 표시, 피해, 사망, 부활, 재접속. 화면 20개를 예쁘게 만들기 전에 게임 상태가 맞는지 먼저 확인. **1단계의 공명율 시제품과 같이 한다.**
2. **체크포인트 거래 하나 완성**: 장비·능력치 화면, 수액 병 충전, 무기 강화, 복귀. 서버 검증, 정수 부족 안내, HUD 반영.
3. **세션 고리**: 처음 실행 → 초기 창 → 스플래시 → 타이틀 → 이어하기 → 월드 로딩 → 플레이 → 일시정지·설정 → 사망 → 부활 → 저장·종료. 같은 그림과 소리로 고리를 완성한 뒤 다음 구역으로.
4. **드문 화면과 현지화 점검**: 연결 끊김, 로딩 취소, 리소스 다시 불러오기, 빠진 글리프, 독·공기·효과, 채팅·명령 입력, 크레딧, 포커스 이동, 커서 복귀. 개발용 글꼴이 없는 새 인스턴스에서.

**사용자가 정할 것**
1. **메뉴를 열면 게임이 멈추나**: 권장은 원작처럼 **멈춤**(사망 화면만 예외). §3.3
2. **한국어 기본 글꼴 느낌**: 매끈한 윤곽 글꼴(Pretendard) 대 픽셀 글꼴(Galmuri). 둘 다 시안을 렌더해서 보여 드린 뒤 고르시면 된다.
3. **컨트롤러 지원**: M1에 넣을지(1~2주 추가)
