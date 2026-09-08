# 챕터 02 — TODO: 한 줄 요약
# 등장: TODO
# 획득 단서: 없음 (clue_burnt_letter / clue_key 1차 노출만)
# 분기: 없음
#
# 역할(docs/OUTLINE.md): 첫 사건. 되돌아갈 수 없어진다
# 목표 분량: 25분

label chapter_02:
    $ begin_chapter(2)
    call screen chapter_card(2, "장 제목")

    scene bg placeholder with dread
    # TODO: asset — 사건이 벌어지는 장소

    # TODO: text — 첫 사건. 여기를 지나면 주인공이 돌아갈 수 없어야 한다.

    # 단서 1차 노출 — 여기서는 '보여주기만' 한다. add_clue 는 03 에서.
    # TODO: text — clue_burnt_letter 를 화면에 스치게 한다 (탄 자국 / 종이 냄새)
    # TODO: text — clue_key 를 화면에 스치게 한다 (금속 소리 / 열쇠고리)

    # 점프 스케어는 챕터당 1회. 쓸 거면 이 형태로.
    # if use_jump_scare():
    #     $ shake_screen(2)

    # 정신력 소모. 무조건 깎으면 히든 엔딩(sanity >= 4)이 도달 불가가 된다.
    # 플레이어가 피할 수 있는 선택·행동에 걸어라. 무조건 소모는 프롤로그 1회뿐이다.
    # TODO: $ drain_sanity(1)

    scene black with wipe_dark
    return
