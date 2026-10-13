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

## 사람이 정해야 할 것
- PC 사양(GPU, CPU, RAM, 해상도·주사율) → 셰이더 팩, `perf-budget.yaml`의 목표, 보스·무기 텍셀 밀도(16 또는 32)
- `art-bible.yaml` 승인 (지금은 draft)
- 첫 보스와 그 무브 시트
