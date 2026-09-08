# 챕터 07 — TODO: 한 줄 요약
# 등장: TODO
# 획득 단서: 없음
# 분기: 있음 — ch07_choice_truth (f_told_truth 설정 지점)
#
# 역할(docs/OUTLINE.md): 최종 선택 → 엔딩 분기
# 목표 분량: 20분

label chapter_07:
    $ begin_chapter(7)
    call screen chapter_card(7, "장 제목")

    scene bg placeholder with dread

    # OUTLINE 미스터리 규칙 5: 배드엔딩 직전에 되돌아갈 지점을 준다.
    # TODO: text — 마지막으로 물러날 수 있는 구간

    jump ch07_choice_truth


label ch07_choice_truth:

    # 규칙 4: 결과를 예상할 수 있게 쓴다. 여기서 뒤통수치지 말 것.
    menu:
        # TODO: text — 선택 상황 설명 한 줄

        "사실대로 말한다 — TODO":
            $ f_told_truth = True
            jump ch07_end

        "말하지 않는다 — TODO":
            $ trust_jihye -= 1
            jump ch07_end


label ch07_end:

    # TODO: text — 엔딩 직전 마무리. 판정은 script.rpy 의 ending_router 가 한다.

    scene black with wipe_dark
    return
