# 디버그 프로토콜

실제로 확인한 문제와 해결책만 적는다. 작업 전에 읽고, 새로 확인한 해결책은 같은 형식으로 아래에 추가한다. 추측은 적지 않는다.

형식: `## 날짜 · 영역 · 제목` 아래에 증상, 원인, 해결, 확인 방법을 쓴다.

---

## 2026-10-13 · Windows · 한글 경로에서 Claude Code 파일 검색이 빈 결과를 냄
- **증상**: 파일이 있는데 Glob이 "No files found"를 반환한다. 오류가 나지 않아서 파일이 없다고 판단하게 된다.
- **원인**: Claude Code 버그(anthropics/claude-code#84966, 미해결). 경로 인자에 한글이 있고 패턴에 디렉터리가 들어가면 생긴다.
- **해결**: 작업 폴더를 `C:\Users\gdjam\Downloads\mc-soulslike`로 옮겼다. 경로와 파일 이름에 한글과 공백을 쓰지 않는다.

## 2026-10-13 · Windows · Claude Code가 ECONNREFUSED로 재시도만 반복
- **증상**: "Connection refused ... Retrying in 3s · attempt N/10".
- **원인**: 로컬 AI 앱 Jan이 남긴 사용자 환경변수 `ANTHROPIC_BASE_URL=http://127.0.0.1:1337`과 `ANTHROPIC_AUTH_TOKEN=jan`. Jan이 꺼져 있으면 연결이 거부된다.
- **해결**: PowerShell에서 `[Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL', $null, 'User')`, 같은 방법으로 `ANTHROPIC_AUTH_TOKEN`도 지운다. 열려 있던 cmd 창은 모두 닫는다.
- **주의**: `reg delete`는 변경을 알리지 않아서 새 창에도 옛 값이 남을 수 있다.
- **확인**: 새 cmd에서 `set ANTHROPIC` → "정의되지 않았습니다".

## 2026-10-13 · MCP · npx로 띄운 헤드리스 서버가 Windows에서 경고와 EPERM을 냄
- **증상**: `DEP0190 DeprecationWarning`, `npm warn cleanup ... EPERM`.
- **원인**:
  - DEP0190: 인자 배열과 `shell: true`를 함께 쓰면 최신 Node가 경고한다.
  - EPERM: npx 캐시 파일이 잠겨 있어 npm이 정리하지 못했다.
- **해결**: `tools/mcp/bbmodel-headless.mjs`가 처음 한 번 `tools/mcp/.cache/`에 설치하고, 이후에는 Node로 bin을 직접 실행한다.
- **확인**: `node tools\mcp\bbmodel-headless.mjs --help`에서 `blockbench-mcp-headless 1.10.0`이 나온다.

## 2026-10-13 · Blockbench MCP · `risky_eval`이 코드를 거부함
- **원인**: 입력 검사가 `console.`, `//`, `/* */`가 들어간 코드를 막는다. URL 문자열의 `//`도 걸린다.
- **해결**: eval 코드에는 주석, URL, console을 넣지 않는다. 설명은 별도 문서에 쓴다.

## 2026-10-13 · Blockbench · 한 세션에서 플러그인을 12개째 설치하면 확인 창이 뜸
- **증상**: `risky_eval`로 설치하던 도중 멈춘 것처럼 보인다.
- **원인**: Blockbench가 12번째 설치부터 확인 창을 띄우고 사용자가 누를 때까지 기다린다. 지원 종료된 플러그인을 설치할 때도 같다.
- **해결**: 한 번에 11개 이하로 설치한다. 창이 뜨면 사용자에게 눌러 달라고 한다.

## 2026-10-13 · Blockbench MCP · 헤드리스로 만든 GeckoLib 모델이 박스 UV로 생성됨
- **원인**: `bbmodel_create`에서 `geckolib_model` 형식의 기본값이 `box_uv: true`다.
- **해결**: 만들 때 `box_uv: false`를 넘긴다. 이 프로젝트는 면별 UV를 쓴다.

## 2026-10-13 · Blockbench MCP · 클라우드에서 헤드리스 렌더가 안 됨
- **원인**: `bbmodel_render`와 `bbmodel_contact_sheet`는 Node 23.6 이상이 필요한데, 클라우드 컨테이너는 Node 22다.
- **해결**: 렌더는 사용자 PC(Node 24 LTS)에서 한다.

## 2026-10-13 · 렌더링 · Iris 1.8.14-beta.1에서 블록 엔티티 그림자가 빠짐
- **원인**: Iris #3283 (NeoForge 1.21.1).
- **해결**: 아직 없음. 1.21.1용 Iris 정식판은 1.8.12뿐이고, 이 판은 Sodium 0.6.13과 짝이다. Sodium 0.8을 쓰려면 1.8.14-beta.1을 써야 한다. 두 조합은 `versions.yaml` 주석 참고.

## 2026-10-14 · 버전 · 존재하지 않는 버전을 고정했던 실수
- **증상**: `versions.yaml`에 Iris 1.8.13을 고정했는데, 1.21.1용으로 출시된 적이 없다.
- **원인**: 1차 조사 때 깃허브 이슈 본문의 버전 표기 한 줄을 근거로 삼았다.
- **해결**: 버전은 Modrinth API(`/v2/project/<id>/version?game_versions=["1.21.1"]&loaders=["neoforge"]`)나 CurseForge 파일 목록으로 확인하고, 의존성(`dependencies`)까지 본 뒤 고정한다.

## 2026-10-13 · Codex · `codex exec`가 스크립트에서 멈춤
- **증상**: "Reading additional input from stdin..."에서 멈춘다.
- **해결**: 표준 입력을 닫는다. bash는 `< /dev/null`, Windows cmd는 `< NUL`.

## 2026-10-13 · Codex · `codex mcp-server`가 없음
- **원인**: 0.149.1에서 폐기 예정이 됐고, 2026-09-05에 제거됐다.
- **해결**: Claude Code에서는 공식 플러그인 `openai/codex-plugin-cc`를 쓰고, 스크립트에서는 `codex exec`를 쓴다.

## 2026-10-13 · Ollama Cloud · JSON 스키마(`format`)를 무시하고 산문으로 답함
- **원인**: Ollama Cloud는 구조화 출력을 지원하지 않는다.
- **해결**: `/v1/messages`에 목표 스키마를 `input_schema`로 가진 도구를 정의해서 호출한다. 결과는 반드시 검증한다. 엄격한 JSON이 필요하면 `gpt-6-luna`나 `codex exec --output-schema`를 쓴다.
