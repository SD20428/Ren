################################################################################
# 추가 스크린
#
# screens.rpy 를 고치지 않고 여기에 새 스크린만 정의한다.
################################################################################

## 챕터 카드 ###################################################################
# 사용: call screen chapter_card(1, "비 오는 날")

screen chapter_card(num, title):
    modal True
    zorder 100

    add "#000000"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22

        text "제 [num] 장" style "card_num"
        text title style "card_title"

    timer 3.4 action Return()
    key "dismiss" action Return()


## 단서 수첩 ###################################################################
# 사용: 게임 중 아무 때나 열 수 있게 하려면 아래 quick_menu 훅 참고

screen clue_notebook():
    modal True
    zorder 90

    add "#0d1214"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1100
        ysize 780
        background "#141a1c"
        padding (48, 44)

        vbox:
            spacing 26

            text "수첩" style "card_title"

            if len(clues) == 0:
                text "아직 적어둔 것이 없다." style "clue_empty"
            else:
                viewport:
                    ysize 560
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 30
                        for cid in sorted(clues):
                            vbox:
                                spacing 8
                                text clue_db[cid][0] style "clue_name"
                                text clue_db[cid][1] style "clue_desc"

    textbutton "닫기":
        xalign 0.5
        yalign 0.94
        action Hide("clue_notebook")

    key "game_menu" action Hide("clue_notebook")
    key "dismiss" action Hide("clue_notebook")


## 퀵메뉴에 수첩 버튼 추가 ######################################################
# screens.rpy 의 quick_menu 를 고치지 않고 얹는 방식.

# 단서가 하나도 없으면 아예 그리지 않는다. 회색 버튼이 계속 보이는 것보다 낫다.
# 챕터 카드와 엔딩 문구 위에는 뜨지 않는다 — 연출이 깨진다.
screen clue_button():
    zorder 50

    # 스플래시/메인메뉴에서는 default 변수가 아직 없다. getattr 로 막는다.
    if getattr(store, "clues", None) and not renpy.get_screen("chapter_card") and not getattr(store, "suppress_clue_button", False):
        textbutton "수첩":
            xalign 0.985
            yalign 0.02
            action Show("clue_notebook")


# 엔딩·연출 구간에서 버튼을 감출 때 쓴다.
#   $ suppress_clue_button = True
# 세이브에 남는 값이라 default 로 선언한다. 이름 바꾸면 세이브가 깨진다.
default suppress_clue_button = False

init python:
    # 게임 중 항상 표시. 필요 없으면 이 줄만 지우면 된다.
    config.overlay_screens.append("clue_button")
