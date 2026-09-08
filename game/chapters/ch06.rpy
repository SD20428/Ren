# 챕터 06 — TODO: 한 줄 요약
# 등장: TODO
# 획득 단서: 회수 (clue_photo, clue_burnt_letter, clue_key)
# 분기: 없음
#
# 역할(docs/OUTLINE.md): 진실. 심어둔 복선 회수
# 목표 분량: 25분

label chapter_06:
    $ begin_chapter(6)
    call screen chapter_card(6, "장 제목")

    scene bg placeholder with dread

    # 회수 구간. 여기서 '새 정보'를 처음 꺼내면 사기다 (OUTLINE 미스터리 규칙 1).
    # 아래 세 갈래는 플레이어가 뭘 아는지에 따라 진실의 해상도를 달리 준다.

    if clue_count() >= 3:
        pass  # TODO: text — 전부 맞춰진 상태의 진실
    elif clue_count() >= 1:
        pass  # TODO: text — 반쯤 아는 상태
    else:
        pass  # TODO: text — 아무것도 모르는 상태

    # TODO: $ trust_jihye += 1

    scene black with wipe_dark
    return
