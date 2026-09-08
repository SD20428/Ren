################################################################################
# 캐릭터 정의 전용 파일
#
# 여기 외의 곳에서 Character() 를 만들지 않는다.
# 색은 이름표에 쓰인다. 호러 톤에 맞춰 채도를 낮게 유지할 것.
################################################################################

# 주인공 — 이름표 없이 나오는 독백/속마음
define nvl_narrator = Character(None, kind=nvl)

# 화면 중앙 정렬 (엔딩, 장면 전환 문구)
define centered = Character(None, what_style="centered_text", window_style="empty")

# 등장인물 --------------------------------------------------------------------
# TODO: 실제 이름으로 교체

define me = Character("나", color="#b8c0bd")
define j  = Character("지혜", color="#9fb4a8")
define s  = Character("선우", color="#a89a6d")
define x  = Character("???",  color="#6b6f70")

# 목소리만 나오는 존재 — 대사창 스타일을 따로 쓴다
define ghost = Character(
    "…",
    color="#7d5a5a",
    what_style="whisper_text",
)
