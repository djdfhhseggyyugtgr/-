# Blockbench MCP 설치 가이드

Claude Code(또는 Codex)가 Blockbench를 직접 조작하고, 프로젝트용 플러그인을 대신 설치할 수 있게 만드는 설정이다.

## 구성

| 서버 | 방식 | 하는 일 | 어디서 동작하나 |
| --- | --- | --- | --- |
| `blockbench` | HTTP `http://localhost:3000/bb-mcp` | 실행 중인 Blockbench를 조작한다. 도구 140개 이상: 큐브, 메시, UV, 페인트, 애니메이션, GeckoLib 내보내기, 화면 캡처, `risky_eval`(JavaScript 실행) | 사용자 PC만 |
| `bbmodel` | stdio (헤드리스) | Blockbench 없이 `.bbmodel` 파일을 만들고, 고치고, 검증하고, 변환하고, PNG로 렌더한다. 여러 에이전트가 동시에 써도 된다 | PC와 클라우드 세션 모두 |

- 둘 다 [jasonjgardner/blockbench-mcp-plugin](https://github.com/jasonjgardner/blockbench-mcp-plugin) v1.10.0(2026-10-01)이다.
- 설정 파일은 저장소 루트의 `.mcp.json`이다. 헤드리스 서버는 `tools/mcp/bbmodel-headless.mjs`가 v1.10.0으로 고정해서 실행하고, 작업 폴더는 저장소의 `models/`로 제한한다.
- 클라우드 세션에서는 `blockbench` 서버가 "연결 실패"로 보인다. PC의 Blockbench에 닿을 수 없어서 생기는 정상 동작이다.
- 클라우드에서 헤드리스 서버로 모델 생성, 큐브 추가, 검증까지 실제로 동작하는 것을 확인했다(2026-10-13).

## PC에서 한 번만 할 일

### 1. 필요한 프로그램
- Blockbench 5.2.2 이상
- Node.js 24 LTS. 헤드리스 서버의 PNG 렌더는 Node 23.6 이상이 필요하다.

### 2. Blockbench에 MCP 플러그인 설치
이 플러그인은 공식 스토어에 없다. 스토어가 AI 기능을 허용하지 않아서다. 그래서 이 단계만 손으로 한다.

1. Blockbench를 열고 **File > Plugins > Load Plugin from URL**을 누른다.
2. 다음 주소를 붙여 넣는다: `https://jasonjgardner.github.io/blockbench-mcp-plugin/mcp.js`
3. **Settings > General**에서 기본값을 확인한다.
   - MCP Server Port: `3000`
   - MCP Server Endpoint: `bb-mcp`
   - risky eval: 켜짐

### 3. 저장소 받기
저장소 폴더는 `C:\Users\gdjam\Downloads\mc-soulslike`이다. 처음이면 루트 README의 방법으로 내려받고, 이미 받았다면 그 폴더에서 `git pull`을 실행한다. 아래 명령은 모두 이 폴더에서 실행한다.

### 4. 헤드리스 서버 미리 받기
첫 실행은 다운로드 때문에 오래 걸려서 MCP 연결 시간 제한에 걸릴 수 있다. 저장소 폴더에서 한 번 실행해 둔다.

```bat
node tools\mcp\bbmodel-headless.mjs --help
```

### 5. Claude Code 연결
1. 저장소 폴더에서 `claude`를 실행한다. Claude 앱에서 조작하고 싶다면 `claude remote-control`을 실행한다.
2. `.mcp.json`의 서버 2개를 승인한다.
3. `/mcp`로 `blockbench`와 `bbmodel`이 연결됐는지 확인한다.

### 6. 플러그인 설치
Claude Code에서 `/blockbench-setup`을 실행한다.

- 아래 필수 플러그인 11개가 Blockbench 공식 스토어에서 설치된다.
- `risky_eval` 실행 전에 승인을 묻는다.
- Blockbench에 확인 창이 뜨면 직접 눌러 준다.

### Codex에서 쓰기
```bat
codex mcp add blockbench --url http://localhost:3000/bb-mcp
codex mcp add bbmodel -- node C:\Users\gdjam\Downloads\mc-soulslike\tools\mcp\bbmodel-headless.mjs
```

## 플러그인 목록 (Blockbench 공식 레지스트리 기준, 2026-10-13)

### 필수 (`/blockbench-setup`이 설치)

| ID | 이름 | 버전 | 용도 |
| --- | --- | --- | --- |
| `geckolib` | GeckoLib Models & Animations | 4.2.5 | GeckoLib 엔티티 모델과 애니메이션 내보내기 |
| `animated_java` | Animated Java | 1.11.0 | 컷신, 연출용 리그(Blockbench 5.1.4 이상) |
| `colour_gradient_generator` | Colour Gradient Generator | 3.0.0 | 색조를 옮겨 가는 색상 램프 생성 |
| `plaster` | Plaster | 1.1.0 | UV 경계에 생기는 얇은 번짐 선 제거 |
| `texture_stitcher` | Texture Stitcher | 1.0.7 | 여러 텍스처를 하나로 합치기 |
| `grayscale_preview` | Grayscale Preview | 1.0.0 | 명암 대비 확인 |
| `bone_view` | Bone View | 1.0.0 | 피벗과 본 연결을 Blender처럼 표시 |
| `expand_bone_timeline` | Expand Bone Timeline | 2.2.0 | 본과 하위 본의 타임라인을 한 번에 펼치기 |
| `true_mirror` | True Mirror | 1.0.0 | 바꾼 부분만 대칭 복사 |
| `duplicate_renamer` | Duplicate Bone Renamer | 1.0.0 | GeckoLib에서 문제가 되는 중복 본 이름 정리 |
| `optimize` | Optimize | 1.2.8 | 가려진 면 숨기기. Blockbench 5.2에서 동작하는지 확인 필요 |

### 선택 (요청할 때만 설치)
- `palette_swap`: 텍스처의 색 계열 바꾸기
- `baked_ambient_occlusion`: 메시 전용 AO 굽기
- `mesh_tools`, `uv_locker`: 메시 모델링 도구
- `cem_template_loader`, `emf_animation_addon`: EMF/ETF용 바닐라 몹 리모델
- `structure_importer`, `structure_to_model`: 맵 구조물을 Blockbench로 가져와 크기 기준으로 쓰기
- `resourcepack_packager`: Java 모델과 텍스처를 리소스팩으로 묶기

### 설치하지 않음

| ID | 이유 |
| --- | --- |
| `free_rotation` | 1.21.4 이상 아이템 모델 전용. 이 프로젝트는 1.21.1이다 |
| `pbr_preview` (PBR Tools) | Blockbench 4.11.9까지만 지원 |
| `animation_utils` | 지원 종료. `geckolib`으로 대체됨 |
| `ambient_occlusion` | 지원 종료 |

## 보안과 주의

- `risky_eval`은 Blockbench 안에서 임의의 JavaScript를 실행한다. 호출할 때마다 승인 여부를 확인하고, 쓰지 않을 때는 Settings에서 끌 수 있다.
- v1.10.0부터 MCP 서버는 로컬 루프백에서만 연결을 받고, 다른 사이트에서 오는 요청은 거부한다.
- MCP로 수정한 프로젝트에는 `ai_used` 표시가 남는다. Project settings에서 지울 수 있다.
- GeckoLib 형식은 새 모델의 기본값이 박스 UV다. 이 프로젝트는 면별 UV를 쓰므로 새 모델을 만들 때 박스 UV를 끈다. 헤드리스 서버에서는 `box_uv: false`를 넘긴다.
