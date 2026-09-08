# 챕터 01 — (한 줄 요약을 여기 쓴다)
# 등장:
# 획득 단서: clue_photo
# 분기: 있음 — ch01_choice_drawer
#
# 이 파일은 템플릿이다. 구조만 유지하고 내용은 교체한다.

label chapter_01:

    call screen chapter_card(1, "장 제목")

    scene bg placeholder with dread

    me "여기서부터 본편."

    jump ch01_choice_drawer


label ch01_choice_drawer:

    menu:
        me "서랍이 반쯤 열려 있다."

        "서랍을 연다.":
            $ f_saw_photo = True
            $ add_clue("clue_photo")
            jump ch01_after_drawer

        "그냥 지나친다.":
            $ trust_jihye -= 1
            jump ch01_after_drawer


label ch01_after_drawer:

    if has_clue("clue_photo"):
        me "{clue}사진{/clue}을 주머니에 넣었다."
    else:
        me "뒤를 돌아보지 않았다."

    scene black with wipe_dark
    return
