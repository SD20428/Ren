# 챕터 05 — TODO: 한 줄 요약
# 등장: TODO
# 획득 단서: 놓친 단서 회수 경로
# 분기: 없음 (f_opened_door 설정 지점)
#
# 역할(docs/OUTLINE.md): 추격·압박. 호러 밀도 최대
# 목표 분량: 30분

label chapter_05:
    $ begin_chapter(5)
    call screen chapter_card(5, "장 제목")

    scene bg placeholder with dread

    # OUTLINE 호러 규칙 3: 무서운 장면 앞에 조용한 구간을 먼저 둔다.
    # TODO: text — 정적

    # 이 챕터의 점프 스케어 1회.
    # if use_jump_scare():
    #     $ shake_screen(3)

    # 지하실 진입. ending_ash 판정(f_opened_door and not f_saw_photo)에 쓰인다.
    # TODO: $ f_opened_door = True

    # 03 에서 놓친 단서를 여기서 주워갈 수 있게 한다. 없으면 트루 도달이 막힌다.
    # TODO: if not has_clue("clue_key"): $ add_clue("clue_key")

    # 정신력 소모. 무조건 깎으면 히든 엔딩(sanity >= 4)이 도달 불가가 된다.
    # 플레이어가 피할 수 있는 선택·행동에 걸어라. 무조건 소모는 프롤로그 1회뿐이다.
    # TODO: $ drain_sanity(1)

    scene black with wipe_dark
    return
