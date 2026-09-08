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

    # 챕터 추가 시 여기에 한 줄씩 붙인다.
    # call chapter_02 from _call_chapter_02

    jump ending_router


label ending_router:
    # 엔딩 판정은 flags.rpy 의 decide_ending() 이 담당한다.
    $ _e = decide_ending()

    if _e == "ash":
        jump ending_ash
    elif _e == "true":
        jump ending_true
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
