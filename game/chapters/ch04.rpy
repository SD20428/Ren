# 챕터 04 — TODO: 한 줄 요약
# 등장: TODO
# 획득 단서: 없음 (clue_photo 재노출)
# 분기: 없음
#
# 역할(docs/OUTLINE.md): 반전 1. 지금까지 믿던 것 하나가 뒤집힌다
# 목표 분량: 25분

label chapter_04:
    $ begin_chapter(4)
    call screen chapter_card(4, "장 제목")

    scene bg placeholder with dread

    # TODO: text — 반전. OUTLINE 미스터리 규칙 2: 진상 관련 인물은 이미 등장해 있어야 한다.

    # 01 에서 얻은 사진을 다시 꺼낸다. 회수(06)는 아직 아니다.
    if has_clue("clue_photo"):
        pass  # TODO: text — 사진을 다시 본다. 처음과 다르게 읽히게
    else:
        pass  # TODO: text — 사진을 못 봤을 때의 대체 정보

    # 신뢰 변동 지점. 히든 엔딩은 trust_jihye 3 을 요구한다.
    # TODO: $ trust_jihye += 1

    scene black with wipe_dark
    return
