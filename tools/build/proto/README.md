# 건축 파이프라인 가능성 시험 (2차 조사 4b, 2026-10-13)

클라우드에서 GPU 없이 1.21.1 구조 파일을 만들고 렌더할 수 있는지 확인한 스크립트다. 정식 생성기가 아니라 시험용이다. 결과와 근거는 [`docs/build/README.md`](../../../docs/build/README.md) 6.2절과 6.4절.

| 파일 | 하는 일 |
| --- | --- |
| `nbt_test.py` | nbtlib로 DataVersion 3955 구조 `.nbt`를 쓰고 다시 읽은 뒤 SNBT 왕복이 같은지 확인. mcschematic과 litemapy의 버전 지원도 출력 |
| `big_test.py` | 64×24×64 시험 구조(약 8,000블록)를 만든다 |
| `render_test.mjs` | deepslate 0.27.2 + headless-gl로 구조를 PNG로 렌더 |

결과 이미지: [`docs/build/proto/deepslate_render_test.png`](../../../docs/build/proto/deepslate_render_test.png) (1024×768, 약 5.9초)

## 시험한 환경
- Python: `nbtlib 2.0.4`, `mcschematic 11.4.4`, `litemapy 0.11.0b0` (따로 만든 venv)
- Node 22 + `deepslate@0.27.2`, `gl`(미리 빌드된 바이너리), `pngjs`, `gl-matrix`, `Xvfb :97` 아래 Mesa llvmpipe
- 에셋: `https://raw.githubusercontent.com/misode/mcmeta/1.21.1-summary/` 의 블록 정의·모델 데이터와 `1.21.1-atlas` 의 아틀라스

```bash
python nbt_test.py out.nbt
python big_test.py big.nbt
Xvfb :97 & DISPLAY=:97 node render_test.mjs <node_modules 폴더> <에셋 폴더> big.nbt big.png 45
```

## 알아 둘 것
- 아틀라스는 2의 거듭제곱 정사각형으로 채워야 한다(2048×1248 → 2048×2048).
- headless-gl에는 `canvas`가 없어서 가짜 `gl.canvas`를 붙인다.
- `builtin/entity` 부모 경고는 무시해도 된다. 상자 같은 블록 엔티티는 따로 처리해야 한다.
- 평평한 조명이라 배치와 팔레트 검토용이다. 분위기는 사용자 PC의 게임 화면으로 본다.
- 지금 클라우드에는 bbmodel 렌더 때문에 Node 24가 설치돼 있다. `gl` 바이너리가 Node 24에서 바로 되는지는 아직 확인하지 않았다.
