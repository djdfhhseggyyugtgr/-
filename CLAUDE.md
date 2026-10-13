@AGENTS.md

## Claude Code 전용
- **MCP 서버** (`.mcp.json`)
  - `blockbench`: 사용자 PC에서 실행 중인 Blockbench. 편집기 하나를 조작하므로 한 번에 한 에이전트만 쓴다. 클라우드 세션에서는 연결되지 않는 것이 정상이다.
  - `bbmodel`: 헤드리스 `.bbmodel` 서버. 여러 에이전트가 동시에 써도 된다. 클라우드에서는 Node 버전 때문에 PNG 렌더가 되지 않는다.
- **스킬**: `/blockbench-setup` (Blockbench 플러그인 설치·확인)
- **훅**: `.ai/` 아래 YAML·JSON을 고치면 G0 검증이 자동으로 돌고, 실패하면 이유가 도구 결과 옆에 표시된다. 표시되면 바로 고친다.
- **교차 리뷰**: Codex 플러그인의 `/codex:review --base <브랜치>` 또는 `/codex:adversarial-review`. 리뷰 결과는 다수결로 고르지 말고 근거를 보고 반영하거나 기각한다.
- **실행 위치 구분**: 환경변수 `CLAUDE_CODE_REMOTE`가 있으면 클라우드 세션이다.
