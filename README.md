# 마크 소울라이크 만들기

마인크래프트의 모드, 리소스팩, 데이터팩 등 쓸 수 있는 수단을 모두 활용해 **소울라이크 장르의 게임형 맵**을 만드는 프로젝트입니다.

- **모티브:** 스팀 게임 *AI LIMIT*의 골자를 따라가고, 모든 메인 NPC를 서브컬처풍 여성 캐릭터로 바꿉니다. 이름과 디자인은 새로 만듭니다. → [기획 초안](docs/design/README.md)
- **AI 활용 과제:** 모델링, 텍스처, 애니메이션, 코딩, 레벨은 AI 에이전트가 만들고, 사용자는 지시·검수·피드백·플레이테스트를 맡습니다.

## 작업 환경

| 항목 | 내용 |
| --- | --- |
| 로컬 기본 작업 폴더 (저장소 폴더) | `C:\Users\gdjam\Downloads\mc-soulslike` |
| 원격 저장소 | GitHub `djdfhhseggyyugtgr/-` |
| 클라우드 작업 브랜치 | `claude/minecraft-soullike-map-wmru3u` |

- 실제 제작과 테스트(클라이언트 실행, 월드 편집)는 로컬 기본 작업 폴더에서 합니다.
- 클라우드 작업(스크립트, 데이터팩 함수, JSON, 문서 등)은 GitHub 저장소를 거쳐 로컬과 주고받습니다.

### 로컬 폴더와 저장소 연결

빈 작업 폴더 안에 저장소를 바로 내려받습니다. 마지막의 `.`은 "현재 폴더에 받기"라는 뜻이고, 폴더가 비어 있어야 동작합니다.

```bat
cd C:\Users\gdjam\Downloads\mc-soulslike
git clone -b claude/minecraft-soullike-map-wmru3u https://github.com/djdfhhseggyyugtgr/-.git .
```

이후 클라우드에서 올라온 변경은 같은 폴더에서 `git pull`로 받습니다.

작업 폴더 경로에는 한글과 공백을 넣지 않습니다. Windows Claude Code에서 한글 경로의 파일 검색이 조용히 실패하는 버그가 있습니다([파이프라인 설계 8.1](docs/pipeline/README.md#81-로컬-폴더는-ascii-경로에-둔다-중요)).

## 기술 스택

목표: 블록 조립과 UV 전개 방식의 모델링과 애니메이션을 최고 퀄리티로 만들고, 플레이어 PC에서 50fps 이상을 유지한다.
근거와 출처는 [기술 스택 조사 결과](docs/research/README.md)에 있다.

- [x] 마인크래프트 버전: **1.21.1** (확정, 2026-10-13. 26.x는 Epic Fight와 셰이더 지원이 나온 뒤 다시 검토)
- [x] 모드 로더: **NeoForge** (확정)
- [x] 핵심 모드: Epic Fight와 애드온(전투, 애니메이션), GeckoLib(커스텀 엔티티), Animated Java(연출), Sodium + Iris(렌더링)
- [x] 모델링 도구: Blockbench 5.2 + Aseprite, Epic Fight 애니메이션은 Blender
- [x] Blockbench MCP와 플러그인 설치: [설치 가이드](docs/setup/blockbench-mcp.md)
- [x] 에이전트 파이프라인 설계: [설계 문서](docs/pipeline/README.md) (Claude Code + Codex + Ollama Cloud)
- [x] 파이프라인 0단계 기반: 공통 규칙 [AGENTS.md](AGENTS.md), 계약·티켓 [.ai/](.ai/README.md), G0 검증기 (진행 상황은 [.ai/PROGRESS.md](.ai/PROGRESS.md))
- [ ] 셰이더 팩과 설정 수준: PC 사양을 받은 뒤 벤치마크로 결정
- [ ] 텍스처 밀도: 기본 16px/블록, 보스·NPC·무기의 32px 적용 여부는 사양을 보고 결정
- [ ] 리소스팩 범위 (모델, 텍스처, LabPBR, 사운드, UI, 폰트)
- [ ] 데이터팩, KubeJS, 커스텀 모드의 역할 분담 (진행도, 체크포인트, 에스투스, 소울 재화, HUD)

## 소울라이크 핵심 요소 (초안)

- [ ] 스태미나 기반 공격, 회피, 방어
- [ ] 구르기와 무적 프레임
- [ ] 패턴형 보스전
- [ ] 화톳불형 체크포인트 (휴식 시 몬스터 재생성, 회복 아이템 충전)
- [ ] 사망 시 재화 드랍과 회수 시스템
- [ ] 레벨업과 스탯 분배
- [ ] 서로 이어지는 맵 구조와 숏컷
- [ ] 환경으로 전하는 스토리 (아이템 설명, 배치)

## 권장 폴더 구조

```
mc-soulslike/
├── README.md          # 이 문서
├── AGENTS.md          # 모든 에이전트 공통 규칙 (Claude Code, Codex)
├── CLAUDE.md          # AGENTS.md + Claude Code 전용 메모
├── .ai/               # 계약(버전·아트·성능·보스), 스키마, 티켓, 증거, 디버그 기록
├── .mcp.json          # Claude Code MCP 서버 설정 (Blockbench)
├── .claude/           # Claude Code 프로젝트 설정(훅)과 스킬 (/blockbench-setup 등)
├── .codex/agents/     # Codex 프로젝트 에이전트 (읽기 전용 리뷰어)
├── docs/              # 기획서, 보스 설계, 맵 구상 등
│   ├── design/        # 기획 초안 (AI LIMIT 모티브)과 원작 조사 노트
│   ├── pipeline/      # 에이전트 파이프라인 설계와 출처
│   ├── research/      # 기술 조사 결과와 출처
│   └── setup/         # 도구 설치 가이드
├── models/            # Blockbench .bbmodel 원본 (헤드리스 MCP 작업 폴더)
├── datapack/          # 데이터팩 소스
├── resourcepack/      # 리소스팩 소스
├── mods/              # 사용 모드 목록 또는 직접 만든 모드 소스
├── world/             # 맵 월드 파일
└── tools/             # 빌드, 패키징, 조사 스크립트 (의존성: npm ci --prefix tools)
    ├── ai/            # G0 계약 검증기와 Claude Code 훅
    ├── blockbench/    # Blockbench 플러그인 설치·확인 스크립트
    ├── mcp/           # MCP 서버 런처
    └── research/      # Ollama 웹 검색, Reddit, 유튜브, X 조사 스크립트
```

## 참고 사항

- 월드 파일과 대용량 텍스처, 사운드 같은 바이너리는 저장소 용량을 크게 늘리므로 Git LFS 사용이나 별도 백업을 고려합니다.
- 외부 모드의 `.jar` 파일은 라이선스 문제를 피하기 위해 저장소에 직접 올리지 않고 이름, 버전, 다운로드 링크만 기록합니다.
- API 키 같은 비밀값은 저장소에 올리지 않습니다. 조사 스크립트는 `OLLAMA_API_KEY` 환경변수나 gitignore된 `.ollama_key` 파일에서 키를 읽습니다.
