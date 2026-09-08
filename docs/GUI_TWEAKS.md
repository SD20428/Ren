# gui.rpy 수정값 — 미스터리/호러 팔레트

`game/gui.rpy` 를 열고 아래 변수를 찾아서 값만 바꾼다. **파일을 통째로 갈아엎지 않는다.**

## 색

버려진 건물 실내. 습기, 꺼진 형광등, 황변한 종이. 순수 검정과 네온 강조색은 쓰지 않는다.

| 이름 | 값 | 쓰임 |
|---|---|---|
| 배경 | `#0d1214` | 청록빛 도는 검정. 순검정보다 화면이 죽지 않는다 |
| 텍스트 | `#cfd6d3` | 형광등 아래 회색 |
| 이름표 | `#a89a6d` | 바랜 놋쇠 |
| 강조 / 단서 | `#8f2f2f` | 마른 피. 밝은 빨강 금지 |
| 비활성 | `#4a5254` | |
| 호버 | `#e8eeea` | |

```renpy
define gui.accent_color         = '#a89a6d'
define gui.idle_color           = '#6f7876'
define gui.idle_small_color     = '#535b59'
define gui.hover_color          = '#e8eeea'
define gui.selected_color       = '#cfd6d3'
define gui.insensitive_color    = '#4a525466'

define gui.text_color           = '#cfd6d3'
define gui.interface_text_color = '#b8c0bd'
```

## 폰트 — 안 바꾸면 한글이 네모로 나온다

`game/fonts/` 에 파일 넣고:

```renpy
define gui.text_font        = "fonts/NanumMyeongjo.ttf"      # 대사 — 명조가 톤에 맞다
define gui.name_text_font   = "fonts/Pretendard-Bold.ttf"    # 이름표
define gui.interface_text_font = "fonts/Pretendard-Regular.ttf"  # 메뉴/버튼

define gui.text_size        = 33
define gui.name_text_size   = 36
define gui.interface_text_size = 26
```

명조체는 산세리프보다 행간이 더 필요하다:

```renpy
define gui.dialogue_text_line_spacing = 8
```

## 대사창

기본 Ren'Py 대사창을 그대로 두면 "아, 렌파이" 소리가 바로 나온다. 여기가 인상의 90%다.

```renpy
define gui.textbox_height = 300
define gui.textbox_yalign = 1.0

# 불투명 판 대신 아래에서 위로 사라지는 그라데이션을 쓴다.
# game/gui/textbox.png 를 직접 교체하는 게 가장 효과가 크다.
# 1920x300, 아래는 #0d1214 불투명 → 위로 갈수록 투명한 세로 그라데이션.

define gui.dialogue_xpos = 340
define gui.dialogue_width = 1240
define gui.dialogue_ypos = 60

define gui.name_xpos = 340
define gui.name_ypos = 8
define gui.name_xalign = 0.0
```

## 텍스트 속도 기본값

호러는 느린 게 낫다. 조급하면 무섭지 않다.

`game/options.rpy` 에서:

```renpy
default preferences.text_cps = 40
default preferences.afm_time = 20
```

## 확인

수정 후 런처에서 실행 → 대사 한 줄 뜨는 화면 스크린샷 찍어서 본다.
글자가 네모(□)면 폰트 경로가 틀린 것이다.
