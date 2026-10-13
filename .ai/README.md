# .ai/

에이전트와 사람이 함께 쓰는 작업 기준, 티켓, 증거를 두는 곳이다. 규칙은 루트의 `AGENTS.md`, 설계 근거는 `docs/pipeline/README.md` 4장에 있다.

| 경로 | 내용 | 누가 고치나 |
| --- | --- | --- |
| `contracts/versions.yaml` | 버전 고정 목록 | 사람 승인 |
| `contracts/art-bible.yaml` | 텍셀 밀도, UV, 텍스처, LabPBR, AI 사용 범위 | 사람 승인 |
| `contracts/perf-budget.yaml` | 큐브·본·텍스처 상한, FPS 목표 | 사람 승인 |
| `contracts/bosses/<boss>.yaml` | 보스 무브 시트 (`_template.yaml` 복사) | 사람 승인 |
| `schemas/` | 위 파일과 티켓, 리뷰 결과의 JSON Schema | 오케스트레이터 |
| `tickets/<id>.yaml` | 작업 티켓 (`_template.yaml` 복사) | 오케스트레이터, 작성자는 status만 |
| `evidence/<id>/` | 게이트 결과 로그, 스크린샷, 프로파일 | 작성자, 검증자 |
| `debug_protocol.md` | 검증된 문제와 해결책 | 모두 (검증된 것만) |
| `PROGRESS.md` | 단계별 진행 상황 | 오케스트레이터 |

## 검증 (G0)

```bash
npm ci --prefix tools        # 처음 한 번
node tools/ai/validate.mjs   # .ai/ 전체 검사
```

검사하는 것:
- 각 파일이 스키마를 지키는지 (예: Minecraft 버전은 반드시 1.21.1)
- 보스 기술의 판정 시작이 예비 동작이 끝난 뒤인지, 판정 구간의 순서가 맞는지
- 티켓 id가 파일 이름과 같은지, 참조한 계약 파일이 있는지
- `status: PASS`인 티켓에 증거 파일이 있는지 (기본값 실패 규칙)

Claude Code에서는 `.ai/` 파일을 고칠 때마다 훅이 같은 검사를 자동으로 돌린다.
