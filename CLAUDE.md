# CLAUDE.md — 에이전트 작업 규칙

> Claude Code / Codex 는 작업 시작 전 이 파일을 항상 먼저 읽는다.

## 프로젝트

- 타입: 2D 비주얼노벨 (미스터리 / 호러)
- 엔진: Ren'Py 8.x
- 목표 분량: 플레이 3시간
- 목표 플랫폼: Steam (Windows / macOS / Linux)
- 언어: 한국어 우선, 영어 로컬라이징은 출시 후 고려
- 개발 인원: 1인
- 아트: AI 생성 후 수동 보정 (Steam AI 공개 대상)

## 절대 규칙

1. `game/gui.rpy`, `game/screens.rpy`, `game/options.rpy` 는 Ren'Py 런처가 생성한 파일이다.
   전체를 다시 쓰지 마라. 수정이 필요하면 어느 줄을 어떻게 바꿀지 **제안만** 하고 사용자가 승인하면 그 줄만 고친다.
2. 스타일 변경은 새 파일이 아니라 `game/gui.rpy` 의 `gui.*` 변수를 고쳐서 한다.
   추가 스타일은 `game/styles_horror.rpy` 안에서만 (init offset 100 구간).
3. 에셋(`game/images`, `game/audio`)은 생성하거나 지우지 마라. 파일명만 참조한다.
   없는 이미지를 참조하는 코드를 쓸 거면 주석으로 `# TODO: asset` 을 남긴다.
4. 커밋 없이 3개 넘는 파일을 동시에 고치지 마라.
5. 시나리오 텍스트를 **자동 생성해서 채우지 마라.** 초안 요청이 명시적으로 있을 때만 쓴다.

## 파일 구조와 역할

```
game/
  script.rpy            진입점. 챕터 호출만. 대사 넣지 말 것
  characters.rpy        Character() 정의 전용
  definitions.rpy       transform / transition / 오디오 채널 / 이미지 별칭
  flags.rpy             default 변수, 단서 DB, 엔딩 판정 함수
  horror.rpy            호러 연출 유틸 (흔들림, 점멸, 속삭임, 텍스트 태그)
  screens_custom.rpy    추가 스크린 (챕터 카드, 단서 수첩)
  styles_horror.rpy     스타일 오버라이드
  chapters/
    ch00_prologue.rpy   챕터별 파일 1개. 라벨명 = 파일명
```

## 네이밍 규칙

| 대상 | 규칙 | 예 |
|---|---|---|
| 챕터 라벨 | `chapter_NN` | `chapter_03` |
| 씬 라벨 | `chNN_스네이크` | `ch03_basement` |
| 분기 라벨 | `chNN_choice_이름` | `ch03_choice_door` |
| 엔딩 라벨 | `ending_이름` | `ending_ash` |
| 캐릭터 변수 | 소문자 이니셜 | `define j = Character(...)` |
| 플래그 | `f_스네이크` | `f_saw_photo` |
| 단서 ID | `clue_스네이크` | `clue_burnt_letter` |
| 배경 | `bg 장소_시간` | `bg hallway_night` |
| 스프라이트 | `이름 표정` | `jihye worried` |

## 챕터 파일 템플릿

모든 챕터 파일은 이 형태를 지킨다.

```renpy
# 챕터 N — 한 줄 요약
# 등장: 누구누구
# 획득 단서: clue_xxx
# 분기: 있음 / 없음

label chapter_NN:
    call screen chapter_card(NN, "장 제목")
    scene bg xxx with dread
    # ...
    return
```

## 커밋 규칙

- `feat(ch03): 지하실 씬 추가`
- `fix(ui): 단서 수첩 스크롤 안 되는 문제`
- `text(ch02): 대사 리라이팅`
- `asset: 지혜 표정 3종 교체`

챕터 하나 = 커밋 하나 이상. 텍스트 수정과 코드 수정은 커밋을 분리한다.

## 시나리오 톤 가이드

미스터리 / 호러. 다음을 지킨다.

- 설명하지 말고 보여준다. "무서웠다" 대신 그 장면의 소리와 온도를 쓴다.
- 화자는 자기가 아는 것보다 항상 조금 덜 안다.
- 단서는 회수 전에 최소 2회 먼저 노출된다.
- 점프 스케어는 챕터당 최대 1회. 남발하면 무뎌진다.
- 대사는 짧게. 한 대사창에 2문장 넘기지 않는다.

## 금지 문장 패턴 (LLM 티 나는 것들)

작성·검수 시 아래가 보이면 전부 고친다.

- "~라는 것을 깨달았다" / "~임을 알 수 있었다"
- "묘한", "형언할 수 없는", "말로 표현하기 어려운"
- "그 순간, 모든 것이 명확해졌다"
- 감정을 이름으로 부르기: "공포가 밀려왔다", "불안이 엄습했다"
- 대사 끝마다 붙는 "...", 문단마다 반복되는 삼단 구조
- 등장인물 전원이 같은 어투로 말하는 것

## 에이전트 분담

- Claude Code: 프로젝트 구조, `.rpy` 로직, 커스텀 UI, 리팩터링, 빌드
- Codex: 독립 함수, 짧은 유틸, 위 결과물 리뷰
- 같은 파일 동시 편집 금지

## 작업 전 확인

1. `git status` 가 깨끗한가
2. 고칠 파일이 위 "절대 규칙" 1~2번에 걸리는가
3. 이 작업으로 기존 세이브가 깨지는가 (`default` 변수 이름 변경 = 깨짐)
