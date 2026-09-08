################################################################################
# 호러 연출 유틸
#
# 사용 예:
#   $ shake_screen()
#   show jihye worried at at_center, flicker
#   "{clue}탄 편지{/clue}를 주머니에 넣었다."
################################################################################

# --- 화면 흔들림 --------------------------------------------------------------
transform shake(n=6, mag=12):
    block:
        linear 0.02 xoffset mag yoffset -mag
        linear 0.02 xoffset -mag yoffset mag
        repeat n
    linear 0.03 xoffset 0 yoffset 0


# --- 형광등 점멸 --------------------------------------------------------------
transform flicker:
    block:
        alpha 1.0
        pause 0.9
        alpha 0.2
        pause 0.04
        alpha 0.95
        pause 0.06
        alpha 0.35
        pause 0.03
        alpha 1.0
        pause 1.7
        repeat


# --- 숨쉬기 (정지 스프라이트가 죽어보이지 않게) --------------------------------
transform breathe:
    subpixel True
    block:
        ease 2.8 yoffset 5
        ease 2.8 yoffset 0
        repeat


# --- 서서히 붉어짐 ------------------------------------------------------------
transform creeping_red(t=4.0):
    linear t matrixcolor TintMatrix("#c48b8b") * SaturationMatrix(0.7)


# --- 초점 흐려짐 (정신력 낮을 때) ---------------------------------------------
transform losing_it(t=2.5):
    linear t matrixcolor SaturationMatrix(0.25) * BrightnessMatrix(-0.15)


init python:

    def shake_screen(intensity=1):
        """
        가벼운 화면 충격. intensity 1~3.
        점프 스케어는 챕터당 1회까지만.
        """
        if intensity <= 1:
            renpy.with_statement(hpunch)
        else:
            for _ in range(intensity):
                renpy.with_statement(vpunch)


    def whisper(sfx=None):
        """대사 위에 겹치는 단발 사운드."""
        if sfx:
            renpy.sound.play(sfx, channel="whisper")


    def drain_sanity(n=1):
        """정신력 소모. 0 이 되면 ash 엔딩으로 잠긴다."""
        store.sanity = max(0, store.sanity - n)
        if store.sanity <= 2:
            renpy.notify("손이 떨린다.")


    # --- 커스텀 텍스트 태그 ---------------------------------------------------
    # {clue}...{/clue} — 단서로 강조. 색을 직접 쓰지 말고 이 태그를 쓴다.
    def _clue_tag(tag, argument, contents):
        result = [(renpy.TEXT_TAG, u"color=#8f2f2f"), (renpy.TEXT_TAG, u"b")]
        result.extend(contents)
        result.append((renpy.TEXT_TAG, u"/b"))
        result.append((renpy.TEXT_TAG, u"/color"))
        return result

    config.custom_text_tags["clue"] = _clue_tag
