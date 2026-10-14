# 기술 스택 조사 결과 (2026-10-13)

> **목표:** 블록을 조립하고 UV를 펼치는 마인크래프트 방식의 모델링과 애니메이션을 최고 퀄리티로 만들되, 플레이어 PC에서 50fps 이상을 유지한다.

## 조사 방법

- **일반 웹:** Ollama `web_search` / `web_fetch` API로 공식 문서, 깃허브, CurseForge/Modrinth, 개발 블로그, 논문을 조사했다.
- **Reddit:** reddit.com이 직접 접근을 막아서 Arctic Shift API로 글과 댓글을 검색했다. 주로 본 곳은 r/feedthebeast, r/Blockbench, r/MinecraftCommands, r/minecraftshaders.
- **유튜브:** 검색 결과를 직접 파싱하고, 관련도가 높은 영상은 자막 전문을 읽었다.
- **X:** 검색 경로가 모두 막혀 있다. 다른 페이지에 걸린 게시물 링크만 fxtwitter API로 읽었고, 실제 인용은 1건뿐이라 커버리지가 낮다.
- **진행 방식:** 모델링, 애니메이션, 렌더링, 게임플레이 4개 분야를 나눠 조사했다. 결론을 좌우하는 주장은 원문으로 다시 확인했다.

**표기:** **[확인]** 공식 문서나 원문으로 확인 · **[커뮤니티]** 사용자 의견 · **[추정]** 자료를 바탕으로 한 추론

---

## 1. 결론: Minecraft 1.21.1 + NeoForge (2026-10-13 확정)

| 후보 | 판정 | 이유 |
| --- | --- | --- |
| **1.21.1 NeoForge** | **권장** | Epic Fight 최신판(21.17.3.1, 2026-05-31)과 그 애드온, 보스 모드 대부분이 이 버전에 있다. Sodium 0.8 백포트(0.8.12, 2026-07-06) 덕분에 렌더링 성능도 좋다(Iris와의 짝은 아래 2장 참고). 최근 소울라이크 모드팩(Ashen Vow 등)과 소울라이크 어드벤처 맵(VALERIA)도 이 버전을 쓴다. [확인] |
| 26.3 (최신 정식판) | 보류 | 이유는 아래 세 가지. |
| 1.20.1 Forge | 비권장 | 모드 생태계는 가장 크다. 하지만 렌더링 모드인 Embeddium과 Oculus는 업데이트가 멈췄고, 최신 Sodium의 성능 개선도 들어오지 않는다. [확인] |

**26.3을 보류하는 이유**
- Epic Fight의 26.x 포팅은 아직 출시 전 알파이고, 애드온과 보스 모드는 26.x 판이 하나도 없다. [확인]
- 게임이 Vulkan으로 전환하는 중인데, 셰이더 로더 Iris는 OpenGL에서만 동작한다. [확인]
- 엔티티 움직임이 끊기는 버그(MC-311974)가 아직 열려 있어서 근접 전투 체감이 나쁘다. [확인]

**26.x로 옮길 시점**
- Epic Fight 26.x가 정식 출시되고 주요 애드온이 포팅된 뒤.
- Iris(또는 후속작 Aperture)가 Vulkan을 지원한 뒤.

**라이선스 변화:** Epic Fight는 26.x부터 GPLv3에서 All Rights Reserved로 바뀐다. 무료 모드팩에 넣는 것은 원본 파일 그대로, 출처를 표기하는 조건으로 허용된다. [확인]

### 지금 버전 상황 (2026-10-13 기준)

- Minecraft Java 최신 정식판은 **26.3**(2026-09-15)이다. 26.1부터 연도 기반 버전 번호를 쓰고, 코드 난독화가 사라졌다.
- Vulkan은 26.2에서 실험 옵션으로 들어왔고, **26.4 스냅샷부터 기본값**이다. OpenGL을 언제 제거할지는 발표되지 않았다.
- Bedrock의 Vibrant Visuals는 Java 개발판에 아직 들어오지 않았다. 셰이더 팩을 대신할 수 없다.

---

## 2. 권장 기술 스택 (1.21.1 NeoForge)

| 분야 | 선택 | 조사 시점 버전 | 메모 |
| --- | --- | --- | --- |
| 모델링·UV | Blockbench | 5.2.2 (10-08) | 아마추어, IK 폴, 화면 기준 브러시, UV 크기 편집기 |
| 텍스처 | Aseprite + Blockbench 페인트 | Aseprite 1.3.18.6 | Blockbench의 "외부에서 편집"으로 실시간 반영 |
| 셰이더용 재질 | LabPBR 1.3 (`_n`, `_s` 맵) | — | 노멀, 거칠기, 금속성, 발광 |
| 전투·플레이어 애니메이션 | Epic Fight + Blender 공식 익스포터 | 21.17.3.1 | 스태미나, 회피 무적, 가드, 경직, 락온, 게임 안 데이터팩 편집기 |
| 무기 모션 | WOM, Dawn Day, EpicFight-Extra | WOM 2.0.178 | Dawn Day는 소울라이크풍 무기와 사망 모션 포함 |
| 타격감 | Impactful 포크 (1.21.1용) | — | 히트스톱, 화면 흔들림. 원본은 1.20.1 전용 |
| 적 AI | Indestructible 포크 (1.21.1용) | — | Epic Fight 몹 AI 강화 |
| 커스텀 엔티티 | GeckoLib | 4.9.3 (1.21.1용) | Java 코드가 필요하다 |
| 연출용 리그, 컷신 | Animated Java | 1.11.0 (10-09) | 바닐라 디스플레이 엔티티 기반 |
| 카메라 연출 | Director's Camera | — | JSON 또는 KubeJS로 제어, 스킵, 화면 흔들림 |
| 렌더링 최적화 | Sodium | 0.8.13 또는 0.6.13 | Iris와 짝이 맞아야 한다. 정정(2026-10-14): `.ai/contracts/versions.yaml` 참고 |
| 셰이더 로더 | Iris | 1.8.14-beta.1 또는 1.8.12 | 1.8.14-beta.1(Sodium 0.8용 베타, #3283 버그) 또는 1.8.12(Sodium 0.6용 정식). 1.8.13은 1.21.1용으로 없다 |
| 셰이더 팩 후보 | Complementary Unbound + Euphoria Patches / Bliss(Eclipse) / Photon | — | PC 사양을 받은 뒤 벤치마크로 결정 |
| 성능 모드 | ModernFix, FerriteCore, Entity Culling, ImmediatelyFast, MoreCulling, Epic Fight FPS Optimizer | — | |
| 게임 로직 | 데이터팩 + KubeJS + 소형 커스텀 모드 | — | 에스투스, 소울 재화, HUD는 직접 구현 |
| NPC, 퀘스트 | Easy NPC, FTB Quests | — | 1.21.1에는 바닐라 `/dialog` 명령어가 없다 |
| 체크포인트, 사망 | Waystones(화톳불로 재구성), Corpse | — | |
| 맵 보호 | YAWP + 어드벤처 모드 | — | `mobGriefing false`, 보스 블록 파괴 설정 끄기 |
| 건축 | WorldEdit / Axiom(별도 Fabric 1.21.1 인스턴스) | — | Axiom은 Fabric 전용이고 상업적 이용은 유료 |

**섞지 말 것:** Better Combat, Combat Roll은 Epic Fight와 같이 쓰지 않는다. 전투 시스템 두 개가 화면에서 충돌한다. [커뮤니티]

---

## 3. 모델링과 UV

### 형식별 제약
- **엔티티(보스, 몹, NPC):** GeckoLib이나 Epic Fight 형식으로 만든다. 면별 UV를 쓸 수 있고 큐브를 세 축으로 자유롭게 회전할 수 있다. [확인]
- **블록, 아이템 모델(소품):** 1.21.1 바닐라 JSON 규칙을 따른다. [확인]
  - 회전은 한 축만, 각도는 ±22.5°, ±45°만 가능하다.
  - 좌표는 -16~32 범위 안이어야 한다.
  - 이 제한은 1.21.6과 1.21.11에서 풀렸지만 1.21.1에는 적용되지 않는다.
  - Free Rotation 플러그인도 1.21.4 이상이 필요해서 쓸 수 없다.

### UV
- **면별 UV(per-face UV)를 기본으로 쓴다.** 면 단위로 재사용, 회전, 미러링, 촘촘한 배치가 된다. [확인]
- 박스 UV는 Modded Entity 형식에서만 필수다. 크기가 소수인 큐브를 반올림해서 믹셀(크기가 다른 픽셀이 섞이는 현상)을 만든다.

### 텍셀 밀도
- 기본은 **1픽셀 = 1/16블록**. 보스, NPC, 손에 드는 무기만 32px/블록을 고려한다. [추정]
- 한 모델 안에서 밀도를 섞지 않는다. 믹셀은 커뮤니티에서 강하게 기피한다. [커뮤니티]
- 블록, 아이템 텍스처는 16의 배수로 만든다. 크기가 하나라도 맞지 않으면 아틀라스 전체의 밉맵 품질이 떨어진다. [확인]
- 텍스처 아틀라스가 16384²를 넘으면 게임이 리소스팩 전체를 꺼버린 사례가 있다(MC-135848). [확인]

### 텍스처링 스타일
- 색상 램프는 색조를 조금씩 옮겨 가며(휴 시프트) 만든다. 계단 같은 명암(밴딩), 가장자리만 어두운 필로우 셰이딩, 노이즈, 불필요한 디더링은 쓰지 않는다. [확인/커뮤니티]
- 엔티티는 윗면과 앞면을 밝게 칠한다.
- 품질 기준으로 참고할 만한 것은 Hytale 공식 모델링 가이드다. [확인]
  - 캐릭터와 무기는 64px/유닛, 소품은 32px/유닛.
  - 텍스처는 0.7~1.3배까지만 늘린다.
  - 명암과 AO를 텍스처에 직접 칠하고, 순수한 검정과 흰색은 쓰지 않는다.
  - 우리 스타일에 맞게 조정해서 적용한다.

### Blockbench 플러그인
- **핵심:** GeckoLib Models & Animations 4.2.5, Animated Java 1.11.0
- **텍스처 보조:**
  - Texture Stitcher: 텍스처 합치기
  - Plaster: UV 경계에 생기는 얇은 번짐 선 제거
  - Colour Gradient Generator: 휴 시프트 색상 램프
  - Palette Swap, Grayscale Preview
- **확인 필요:** Optimize(숨은 면 제거)가 Blockbench 5.2에서 동작하는지.
- **사용 불가:** PBR Tools. Blockbench 4.11.9까지만 지원한다. [확인]

### Blender
- 실제로 게임에 들어갈 에셋은 모두 Blockbench에서 만든다. [추정]
- Blender는 세 가지 용도로만 쓴다.
  - Epic Fight 애니메이션 제작(공식 익스포터가 Blender용이다)
  - 트레일러 렌더
  - AO를 구워서 덧칠할 참고용으로 쓰기

### 복잡도 예산 [추정. 공식 기준은 없다]

| 종류 | 큐브 수 | 본 수 | 텍스처(16px / 32px 밀도) |
| --- | --- | --- | --- |
| 소품(블록 모델) | 1~40 | — | — |
| 일반 몹 | 30~150 | 10~30 | 64~128² / 128~256² |
| 정예 몹 | 150~300 | — | — |
| 보스 | 300~800 (상한 약 1,500) | 40~80 | 256² / 512² |
| Animated Java 리그 | — | 큐브가 든 그룹 25~40개 이하 | — |

- 엔티티 정점은 매 프레임 CPU 렌더 스레드에서 변환된다. 셰이더 팩은 그림자 패스로 같은 비용을 한 번 더 쓴다.
- 그래서 본과 큐브 수가 곧 프레임 비용이다. 실제 맵에서 F3 화면과 Spark로 측정해서 조정한다.

---

## 4. 애니메이션

### 대상별 도구와 런타임

| 대상 | 제작 도구 → 게임 안 런타임 | 이유 |
| --- | --- | --- |
| 플레이어 전투 모션, 무기 무브셋 | Blender + Epic Fight 익스포터 → Epic Fight 데이터팩 편집기 | 공격 단계(예비 동작 → 선딜 → 판정 → 후딜), 관절에 붙는 판정, 1인칭 전용 애니메이션 [확인] |
| **보스 (권장)** | Blender 메시와 아마추어 → Epic Fight 몹 설정 | 전투 시스템과 가장 잘 맞는다. 무브셋을 가중치와 조건으로 구성한다 [확인] |
| 커스텀 몹, 움직이는 소품 | Blockbench → GeckoLib | 이징 30종 이상, 사운드·파티클 키프레임, Molang 지원. 게임 안에서 IK는 안 된다 [확인] |
| 컷신, 연출용 리그 | Blockbench → Animated Java | 바닐라 디스플레이 엔티티로 동작. 카메라 키프레임은 롤 회전이 없다 [확인] |
| 카메라 연출 | Director's Camera | 보스 등장 연출, 스킵, 화면 흔들림 [확인] |

### Blockbench 5.2
- IK 폴, 아마추어 IK, 미러 애니메이팅, 그래프 편집기(베지어 곡선)가 있다. [확인]
- 단, 내보낼 때 IK는 키프레임으로 구워진다. 아마추어로 메시를 변형하는 기능은 GeckoLib과 Animated Java 형식으로 내보내지지 않는 것으로 보인다. [추정]

### 작업 원칙
- 예비 동작, 접촉, 회복이 확실히 읽히게 한다.
- 프레임을 늘리기보다 핵심 포즈를 잠깐 멈춰 보여준다(홀드).
- 다리 → 몸통 → 팔 순서로 움직임이 전달되게 한다. [커뮤니티]

### 모션 캡처
- Rokoko Video 같은 영상 기반 도구 → Blender에서 리타깃 → 과장과 홀드로 다듬는다.
- 마인크래프트 전용 모션 캡처 도구는 찾지 못했다. [확인/커뮤니티]

### 통합 원칙
- 모든 적을 Epic Fight 몹으로 설정해서 통합한다. 설정하지 않은 GeckoLib 몹은 자기 애니메이션만 쓰기 때문에 전투 체감이 떨어진다. [커뮤니티]
- Epic Fight가 담당하는 몹에서는 Epic Fight 애니메이션이 Fresh Animations보다 우선한다. [확인]

---

## 5. 렌더링과 50fps

### GPU 등급별 권장 설정 [추정. 여러 측정 사례를 종합한 값이라 실제 PC에서 확인이 필요하다]

| GPU 등급 | 해상도 | 셰이더 팩과 설정 | 시야 거리, 원거리 지형(LOD) | PBR | 예상 FPS |
| --- | --- | --- | --- | --- | --- |
| GTX 1060 / RX 580 | 1080p | Complementary 낮음~중간(대안: BSL 낮음), 그림자 해상도 1024 | 8청크, LOD 없음 | 16~32x, 시차 효과 끔 | 약 50~70 |
| GTX 1660S / RX 6600 / RTX 2060 | 1080p | Complementary 중간 + Euphoria, 또는 Photon/Bliss 중간 | 10청크 | 32x, 시차 효과 끔 | 약 60~90 |
| RTX 3060 / 4060 / RX 6700 XT | 1080p 높음 / 1440p 중간 | Complementary 높음, Photon 높음, Bliss/Eclipse | 12청크, 전망 지점에만 Distant Horizons | 32x, 시차 효과 낮음 | 약 60~100 |
| RTX 4070 / RX 7800 XT | 1440p 높음~최고 | Photon 최고 또는 Complementary 최고 + Euphoria | 12~16청크, 전망 지점에만 LOD | 32~64x | 약 70~120 |
| RTX 4090 / RX 7900 XTX | 1440p~4K 최고 | 어떤 팩이든 가능. 1440p에서 Rethinking Voxels | 16청크 이상 | 64~128x, 시차 효과 켬 | 4K Complementary 150 이상 |

### FPS가 부족할 때 줄이는 순서
1. 셰이더 설정 한 단계 낮추기
2. 그림자 해상도와 거리
3. 볼류메트릭 단계 수(안개 자체는 유지)
4. 반사와 AO
5. 컬러 복셀 조명

피사계 심도와 모션 블러는 끄고, 적이 많은 전투에서는 엔티티와 블록 엔티티 그림자를 끈다.

### 프레임 생성은 50fps 목표에 넣지 않는다
프레임 생성은 입력 지연을 늘려서 패리 타이밍을 망친다. 50fps는 실제로 렌더링된 프레임 기준으로 맞춘다.

### 맵 설계로 성능 확보하기
- 닫힌 아레나와 안개 벽을 쓰고, 시야 거리는 8~12청크로 둔다.
- 컬러 조명 셰이더를 쓴다면 청크당 광원 수를 제한한다.
- 반투명 보스 모델은 피한다.
- 보스 에셋을 아레나 진입 전에 보이지 않는 곳에서 미리 불러온다. 처음 등장할 때 1초가량 끊기는 현상(Iris #3149)을 피하기 위해서다. [추정]

### 셰이더 팩 배포
셰이더 팩은 라이선스상 대부분 모드팩에 같이 넣을 수 없다. 설정 프리셋 파일과 설치 안내를 따로 배포한다. [추정]

---

## 6. 알려진 위험과 직접 테스트할 항목

1. **Epic Fight + Iris + 셰이더 팩**
   - `epicfight:custom` 텍스처가 Complementary와 Bliss에서 깨진다(#1921).
   - 1.21.1에서 텍스처가 변형되는 문제가 있다(#2580).
   - 컴퓨트 셰이더 애니메이션 경로에서 화면 깨짐이 생길 수 있다.
2. **Animated Java 디스플레이 엔티티**는 셰이더 아래에서 발광이 약해진다(Iris #3053).
3. **데이터팩으로 바꾼 안개, 조명 색**이 Iris + Complementary 조합에서 무시된다(#3065). 분위기는 셰이더 팩 설정으로 잡아야 한다.
4. **Bliss/Eclipse**를 NeoForge에서 쓰면 플레이어가 투명해질 수 있다. 팩의 디버그 설정에서 `TRANSLUCENT_ENTITIES`를 끈다(#514).
5. **Iris 1.8.14-beta.1**에서는 블록 엔티티가 그림자 패스에서 빠진다(#3283). 이 베타가 Sodium 0.8과 짝인 유일한 판이라, 성능(Sodium 0.8)과 안정성(Iris 1.8.12 + Sodium 0.6.13) 중 PC 벤치마크로 고른다. (정정 2026-10-14: 예전 문서의 "정식판 1.8.13"은 존재하지 않는다.)
6. **GeckoLib 5.5.2+**가 Windows가 아닌 OS에서 커스텀 발광을 끈다는 보고가 있다. 다만 1.21.1에서 쓰는 4.9.3과는 관계가 없을 수 있어 확인이 필요하다.
7. **CurseForge 서드파티 다운로드를 막아 둔 모드**가 있다. 이런 모드는 런처가 자동으로 받지 못한다. 배포 전에 모든 모드의 설정을 확인한다.
8. **Marium's Soulslike Weaponry**는 1.21.1에서 Fabric 전용이다. NeoForge에서는 Sinytra Connector가 필요하고 설정이 적용되지 않는다는 보고가 있다.

---

## 7. 다음 단계

1. PC 사양(GPU, CPU, RAM, 해상도와 주사율)을 받아서 셰이더 팩, 설정 수준, 텍스처 밀도를 확정한다.
2. 1.21.1 NeoForge 테스트 인스턴스를 구성한다(2장 스택).
3. 벤치마크 아레나를 만든다. Epic Fight + Iris + 후보 셰이더 팩 + 보스 1체 + 일반 몹 여러 마리를 넣고 F3와 Spark로 프레임 타임을 잰다.
4. 파이프라인을 시험 제작한다. 보스 1체를 Blockbench로 모델링하고, Blender로 리깅하고, Epic Fight 몹으로 설정하고, LabPBR 맵까지 만들어 본다.

---

## 상세 자료

- [`sources/notes_modeling.md`](sources/notes_modeling.md): 모델링, UV, 텍스처링
- [`sources/notes_animation.md`](sources/notes_animation.md): 애니메이션 런타임, 제작 흐름, 컷신
- [`sources/notes_render.md`](sources/notes_render.md): 렌더링, 셰이더, 성능
- [`sources/notes_gameplay.md`](sources/notes_gameplay.md): 소울라이크 모드, 맵 제작 도구, 버전 호환표, 배포

상세 노트는 영어 원문이고, 모든 주장에 출처 URL이 달려 있다. 노트 안의 `research/...` 경로는 조사 당시 원본 데이터가 있던 위치로, 저장소에는 넣지 않았다.

## 다시 조사하는 방법

`tools/research/`의 스크립트로 같은 방식의 조사를 다시 할 수 있다. API 키는 `OLLAMA_API_KEY` 환경변수나 저장소 루트의 `.ollama_key` 파일에서 읽는다. `.ollama_key`는 `.gitignore`에 들어 있다.

```bash
python3 tools/research/osearch.py search research_raw/topic "검색어1" "검색어2"
python3 tools/research/osearch.py fetch research_raw/topic "https://..."
python3 tools/research/social.py reddit-posts feedthebeast "epic fight" 2026-01-01
python3 tools/research/social.py yt-search "blockbench animation"
python3 tools/research/social.py yt-transcript VIDEO_ID
python3 tools/research/social.py x-post https://x.com/USER/status/ID
```
