################################################################################
# 스타일 오버라이드
#
# init offset 을 올려서 screens.rpy / gui.rpy 보다 나중에 적용되게 한다.
# 이 구간 밖에서 스타일을 건드리지 말 것.
################################################################################

init offset = 100

# 화면 중앙 정렬 문구 (엔딩, 장면 전환)
style centered_text:
    color "#8a9490"
    size 40
    text_align 0.5
    xalign 0.5
    yalign 0.5
    layout "subtitle"
    line_spacing 14

# 목소리만 나오는 존재
style whisper_text:
    color "#7d5a5a"
    italic True
    size 30

# 챕터 카드
style card_num:
    color "#5c6360"
    size 24
    xalign 0.5

style card_title:
    color "#cfd6d3"
    size 54
    xalign 0.5
    line_spacing 10

# 단서 수첩
style clue_name:
    color "#a89a6d"
    size 30
    bold True

style clue_desc:
    color "#9aa3a0"
    size 24
    line_spacing 6

style clue_empty:
    color "#4a5254"
    size 26
    italic True

init offset = 0
