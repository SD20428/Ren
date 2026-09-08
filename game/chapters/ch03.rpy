# 챕터 03 — TODO: 한 줄 요약
# 등장: TODO
# 획득 단서: clue_burnt_letter, clue_key
# 분기: 있음 — ch03_choice_search
#
# 역할(docs/OUTLINE.md): 조사 / 단서 수집. 첫 분기
# 목표 분량: 30분

label chapter_03:
    $ begin_chapter(3)
    call screen chapter_card(3, "장 제목")

    scene bg placeholder with dread

    # TODO: text — 조사 도입. 02 에서 스친 두 물건을 플레이어가 다시 떠올리게 한다.

    jump ch03_choice_search


label ch03_choice_search:

    menu:
        # TODO: text — 선택 상황 설명 한 줄

        "선택 A — TODO":
            $ add_clue("clue_burnt_letter")
            $ trust_jihye += 1
            jump ch03_after_search

        "선택 B — TODO":
            $ add_clue("clue_key")
            jump ch03_after_search


label ch03_after_search:

    # 트루/히든은 단서 3개를 요구한다. 한 번에 다 주지 말고,
    # 놓친 쪽을 05 나 06 에서 회수할 경로를 반드시 열어둬라.
    # TODO: text

    scene black with wipe_dark
    return
