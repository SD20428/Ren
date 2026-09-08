################################################################################
# 트랜스폼 / 트랜지션 / 오디오 채널 / 이미지 별칭
################################################################################

# --- 오디오 채널 --------------------------------------------------------------
# ambient : 계속 깔리는 환경음 (빗소리, 형광등 웅웅거림)
# whisper : 대사 위에 겹치는 단발 사운드
init python:
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)
    renpy.music.register_channel("whisper", mixer="sfx", loop=False)


# --- 트랜지션 -----------------------------------------------------------------
define dread     = Dissolve(1.6)                          # 느린 불안
define snap      = Dissolve(0.06)                         # 순간 전환
define blackout  = Fade(0.35, 0.5, 0.35, color="#000000") # 암전 후 복귀
define wipe_dark = Fade(0.2, 0.0, 1.4, color="#000000")   # 챕터 끝
define bloodout  = Fade(0.1, 0.3, 0.8, color="#2a0d0d")   # 붉은 암전


# --- 캐릭터 배치 --------------------------------------------------------------
transform at_left:
    xalign 0.22
    yalign 1.0

transform at_center:
    xalign 0.5
    yalign 1.0

transform at_right:
    xalign 0.78
    yalign 1.0

# 뒤로 물러난 인물 — 어둡고 살짝 작게
transform backgrounded:
    matrixcolor BrightnessMatrix(-0.22) * SaturationMatrix(0.55)
    zoom 0.96


# --- 등장 / 퇴장 --------------------------------------------------------------
transform slide_in_left:
    xoffset -80
    alpha 0.0
    parallel:
        ease 0.45 xoffset 0
    parallel:
        ease 0.35 alpha 1.0

transform fade_out_slow:
    ease 1.2 alpha 0.0


# --- 이미지 별칭 --------------------------------------------------------------
# TODO: asset — 실제 파일 넣은 뒤 주석 해제
# image bg hallway_night   = "images/bg/hallway_night.png"
# image bg classroom_dusk  = "images/bg/classroom_dusk.png"
# image jihye normal       = "images/sprite/jihye_normal.png"
# image jihye worried      = "images/sprite/jihye_worried.png"

# 에셋 없이 테스트할 때 쓰는 임시 색판
image bg placeholder = "#141a1c"
image bg blood       = "#2a0d0d"
