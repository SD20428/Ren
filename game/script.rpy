################################################################################
# 진입점
#
# 이 파일에는 대사를 쓰지 않는다. 챕터 호출과 흐름 제어만.
################################################################################

label splashscreen:
    scene black
    with Pause(0.6)
    # TODO: asset — 제작사 로고를 넣을 거면 여기
    return


label start:
    # 세이브 호환을 위해 from 절을 붙인다. 지우지 말 것.
    call chapter_00 from _call_chapter_00
    call chapter_01 from _call_chapter_01
    call chapter_02 from _call_chapter_02
    call chapter_03 from _call_chapter_03
    call chapter_04 from _call_chapter_04
    call chapter_05 from _call_chapter_05
    call chapter_06 from _call_chapter_06
    call chapter_07 from _call_chapter_07

    jump ending_router


label ending_router:
    # 엔딩 판정은 flags.rpy 의 decide_ending() 이 담당한다.
    $ _e = decide_ending()

    if _e == "hidden":
        jump ending_hidden
    elif _e == "true":
        jump ending_true
    elif _e == "ash":
        jump ending_ash
    else:
        jump ending_default


label ending_default:
    scene black with wipe_dark
    centered "{i}아무것도 밝혀내지 못한 채, 아침이 왔다.{/i}"
    $ unlock_ending("default")
    return


label ending_ash:
    scene black with wipe_dark
    centered "{i}재만 남았다.{/i}"
    $ unlock_ending("ash")
    return


label ending_true:
    scene black with wipe_dark
    centered "{i}진실.{/i}"
    $ unlock_ending("true")
    return


# 히든 — 트루 조건 + 신뢰 최대 + 정신력 무손실 + 지하실 진입.
# 판정식은 flags.rpy 의 decide_ending() 에만 있다.
label ending_hidden:
    scene black with wipe_dark
    # TODO: text — 히든 엔딩 문구
    centered "{i}…{/i}"
    $ unlock_ending("hidden")
    return
