# 챕터 00 — 프롤로그
# 등장: 나
# 획득 단서: 없음
# 분기: 없음
#
# 목적: 5분 안에 훅을 건다. 세계관 설명 금지. 상황만 던진다.
# 이 파일은 연출 유틸 사용법 예시를 겸한다. 대사는 전부 교체 대상.

label chapter_00:

    scene bg placeholder with dread
    # TODO: asset — scene bg hallway_night

    play ambient "audio/ambient_rain.ogg" fadein 2.0
    # TODO: asset

    me "복도 끝 형광등이 나갔다 켜졌다 한다."

    show expression "#1a2124" as light at at_center, flicker
    # 위는 임시. 실제로는 조명 레이어 이미지에 flicker 를 건다.

    me "3층에는 나 말고 아무도 없어야 한다."

    pause 0.8

    $ shake_screen(1)

    me "위에서 뭔가 끌리는 소리가 났다."

    ghost "……"

    $ drain_sanity(1)

    me "천장을 올려다봤다. 4층은 작년에 폐쇄됐다."

    hide light with snap

    scene black with wipe_dark
    centered "{i}그날 밤, 나는 4층으로 올라갔다.{/i}"

    stop ambient fadeout 2.0

    return
