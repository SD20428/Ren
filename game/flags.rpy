################################################################################
# 게임 상태 — 플래그 / 단서 / 엔딩 판정
#
# 주의: 여기 있는 default 변수의 "이름"을 바꾸면 기존 세이브가 깨진다.
#       추가는 안전. 이름 변경/삭제는 위험.
################################################################################

# --- 진행 플래그 --------------------------------------------------------------
default f_saw_photo    = False   # 서랍 속 사진을 봤는가
default f_opened_door  = False   # 지하실 문을 열었는가
default f_told_truth   = False   # 지혜에게 사실대로 말했는가

# --- 수치 -------------------------------------------------------------------
default trust_jihye = 0          # -3 ~ +3
default sanity      = 5          # 0 이 되면 강제 배드엔딩

# --- 단서 -------------------------------------------------------------------
default clues = set()
default unlocked_endings = set()


# --- 단서 DB -----------------------------------------------------------------
# 단서 수첩에 표시되는 내용. 이름과 설명만.
init python:

    clue_db = {
        "clue_burnt_letter": (
            "탄 편지",
            "가장자리가 그을렸다. 남은 글자는 세 개뿐이다.",
        ),
        "clue_photo": (
            "사진",
            "네 명이 찍혔는데, 한 명의 얼굴만 긁혀 있다.",
        ),
        "clue_key": (
            "작은 열쇠",
            "지하실 문에는 맞지 않는다.",
        ),
    }


    def add_clue(cid):
        """단서 획득. 중복 호출해도 안전하다."""
        if cid not in clue_db:
            raise Exception("정의되지 않은 단서 ID: %s" % cid)
        if cid not in clues:
            clues.add(cid)
            renpy.notify("단서를 얻었다 — %s" % clue_db[cid][0])


    def has_clue(cid):
        return cid in clues


    def clue_count():
        return len(clues)


    def unlock_ending(name):
        unlocked_endings.add(name)


    def decide_ending():
        """
        엔딩 판정. script.rpy 의 ending_router 에서만 호출한다.
        판정 순서가 곧 우선순위다. 위쪽이 먼저 걸린다.
        """
        if sanity <= 0:
            return "ash"

        if clue_count() >= 3 and f_told_truth and trust_jihye >= 2:
            return "true"

        if f_opened_door and not f_saw_photo:
            return "ash"

        return "default"
