# 진행 상황

오케스트레이터가 갱신한다. 단계 정의는 `docs/pipeline/README.md` 10장에 있다.

## 단계

| 단계 | 상태 | 비고 |
| --- | --- | --- |
| 0. 기반 | 진행 중 | 아래 체크리스트 참고 |
| 1. 단일 에이전트 + 게이트 | 대기 | NeoForge 1.21.1 모드 골격, Gradle, GameTest, CI |
| 2. 교차 리뷰 | 대기 | |
| 3. 병렬화 | 대기 | |
| 4. QA 자동화 | 대기 | |

## 0단계 체크리스트
- [x] 버전 확정: Minecraft 1.21.1 + NeoForge (`.ai/contracts/versions.yaml`)
- [x] 작업 폴더를 ASCII 경로로 이동 (`C:\Users\gdjam\Downloads\mc-soulslike`)
- [x] Blockbench MCP 연결과 플러그인 설치 (사용자 PC)
- [x] Codex 플러그인 설치 (사용자 PC, `codex@openai-codex`)
- [x] 공통 규칙 `AGENTS.md`와 `CLAUDE.md`
- [x] 계약·스키마 골격 `.ai/`와 G0 검증기, PostToolUse 훅
- [x] Codex 읽기 전용 리뷰어 `.codex/agents/reviewer.toml`
- [ ] PC에서 `npm ci --prefix tools` 실행과 G0 통과 확인
- [ ] 클라우드 환경 비밀값 등록: `OLLAMA_API_KEY` (Codex를 클라우드에서 쓰려면 `OPENAI_API_KEY`도)
- [ ] 클라우드 환경 허용 도메인: `ollama.com` (필요하면 `api.openai.com`)
- [ ] Codex 프로젝트 신뢰 설정 후 `reviewer` 에이전트가 보이는지 확인

## PC 사양 (2026-10-13 측정)
- RTX 4060 8GB, Ryzen 5 5600 (6코어 12스레드), DDR4-3200 16GB 1개(싱글 채널), NVMe SSD, 1920x1080 60Hz, Windows 11, 데스크톱
- 조사 문서의 GPU 등급 "RTX 3060/4060"에 해당: 1080p 높음 설정, 12청크, Distant Horizons는 경치 구간에만
- 60Hz 모니터라 평상시 60fps 고정, 보스전 최저 평균 50fps
- 병목은 GPU보다 CPU와 싱글 채널 메모리 쪽일 가능성이 높다. 같은 사양 16GB를 하나 더 꽂으면(듀얼 채널) 개선 여지가 크다
- 마인크래프트 메모리 할당은 6GB로 시작하고 spark로 확인한다

## 결정된 것
- 역할: 모델링, 텍스처, 애니메이션, 코드, 레벨은 에이전트가 만들고, 사용자는 지시·검수·피드백·플레이테스트·승인을 맡는다 (AI 활용 과제, 2026-10-13)
- 보스·NPC·무기 텍셀 밀도 32px/블록, 일반 몹·소품 16px/블록 (2026-10-13)

- 모티브: AI LIMIT의 골자를 따르고 모든 메인 NPC를 서브컬처풍 여성 캐릭터로 바꾼다. 기획 초안 `docs/design/README.md` (2026-10-13)

## 사용자가 정해야 할 것
- 과제 마감일과 범위 (기획 초안 5장: A 수직 단면 / B 1막 / C 축약 전체판)
- 용어와 NPC 이름 가칭 승인 (기획 초안 2장, 4장)
- 셰이더 팩: 보스 아레나 벤치마크(G6) 후 결정
- `art-bible.yaml` 승인 (지금은 draft)
- 첫 보스와 그 무브 시트

## 기술 위험
- 공명율(원작의 싱크율): Epic Fight는 스태미나 중심이라 커스텀 모드로 대체해야 한다. 1단계에서 Epic Fight 21.17.3.1 소스를 읽고 시험 구현으로 연동 가능성을 먼저 확인한다
